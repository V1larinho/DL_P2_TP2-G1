#!/usr/bin/env python3
"""Contagem e verificação do CODEBRIM a partir do zip, sem extrair.

O zip publicado (`CODEBRIM_classification_dataset.zip`, 7,9 GB) tem esta forma, verificada:

    classification_dataset/<split>/<pasta>/image_<id>_crop_<n>.png
    classification_dataset/metadata/defects.xml      <- etiquetas multi-rótulo
    classification_dataset/metadata/background.xml   <- idem, para o fundo
    __MACOSX/...                                     <- lixo de resource forks, ignorado

Cada `<Defect name="...">` traz um vetor de 6 bits:
Background, Crack, Spallation, Efflorescence, ExposedBars, CorrosionStain.

Fases:

  `--listar`   descobre a estrutura real e imprime uma amostra. Corre SEMPRE primeiro.
  `--contar`   junta imagens + etiquetas, conta recortes por classe e partição, verifica que
               nenhuma **imagem de origem** aparece em duas partições e escreve `data/splits.csv`
               com as colunas da PL08: `path, label, grupo, split` (label = classes positivas
               separadas por `|`, porque o problema é multi-rótulo).

Exemplos:
    python scripts/contar_codebrim.py --listar
    python scripts/contar_codebrim.py --contar --splits data/splits.csv

Saída: tabela no stdout + JSON com as contagens. Código de saída 2 se houver fuga por grupo.
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

SPLITS = ("train", "training", "val", "valid", "validation", "test", "testing")
SPLIT_CANON = {
    "train": "train", "training": "train",
    "val": "val", "valid": "val", "validation": "val",
    "test": "test", "testing": "test",
}
IMG_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")
CLASSES = ("Background", "Crack", "Spallation", "Efflorescence", "ExposedBars", "CorrosionStain")
DEFECTS = CLASSES[1:]
FICHEIROS_ETIQUETAS = ("defects.xml", "background.xml")


def imagens(zf: zipfile.ZipFile) -> list[str]:
    """Caminhos de imagem úteis, sem lixo de sistema de ficheiros."""
    saida = []
    for n in zf.namelist():
        if n.endswith("/") or not n.lower().endswith(IMG_EXT):
            continue
        if "__MACOSX" in n or os.path.basename(n).startswith("._"):
            continue
        saida.append(n)
    return saida


def normalizar(nome: str) -> list[str]:
    return [p for p in nome.replace("\\", "/").split("/") if p][:-1]


def inferir_split(partes: list[str]) -> str | None:
    for p in partes:
        if p.lower() in SPLIT_CANON:
            return SPLIT_CANON[p.lower()]
    return None


def inferir_grupo(nome: str) -> str:
    """Imagem de origem: `image_0000058_crop_0000002.png` -> `0000058`."""
    base = os.path.basename(nome).rsplit(".", 1)[0]
    m = re.search(r"image[_-]?(\d+)", base, re.IGNORECASE)
    if m:
        return m.group(1)
    m = re.match(r"^([A-Za-z]*\d+)", base)
    if m:
        return m.group(1)
    m = re.search(r"(\d+)", base)
    return m.group(1) if m else base


def ler_etiquetas(zf: zipfile.ZipFile) -> dict[str, list[str]]:
    """Lê os XML de metadados e devolve {nome_do_ficheiro: [classes positivas]}."""
    etiquetas: dict[str, list[str]] = {}
    for alvo in FICHEIROS_ETIQUETAS:
        entradas = [n for n in zf.namelist() if n.endswith(alvo) and "__MACOSX" not in n]
        for entrada in entradas:
            with zf.open(entrada) as fh:
                raiz = ET.parse(fh).getroot()
            for d in raiz.findall("Defect"):
                nome = (d.get("name") or "").strip()
                if not nome:
                    continue
                positivas = [c for c in CLASSES if (d.findtext(c) or "0").strip() == "1"]
                etiquetas[nome] = positivas
    return etiquetas


def cmd_listar(zf: zipfile.ZipFile, limite: int) -> None:
    nomes = zf.namelist()
    imgs = imagens(zf)
    etq = ler_etiquetas(zf)
    print(f"entradas no zip : {len(nomes)}")
    print(f"imagens         : {len(imgs)}")
    print(f"etiquetas lidas : {len(etq)}")

    raizes = collections.Counter(n.replace("\\", "/").split("/")[0] for n in nomes if "/" in n)
    print("\nraízes (nível 1):")
    for r, c in raizes.most_common(10):
        print(f"  {c:>7}  {r}")

    print("profundidade de pastas das imagens:",
          dict(sorted(collections.Counter(len(normalizar(n)) for n in imgs).items())))

    tokens = collections.Counter()
    for n in imgs:
        for p in normalizar(n):
            if p.lower() in SPLIT_CANON:
                tokens[SPLIT_CANON[p.lower()]] += 1
    print("partições detetadas:", dict(tokens) or "NENHUMA (a divisão não está em pastas)")

    print(f"\namostra de {min(limite, len(imgs))} caminhos:")
    for n in imgs[:limite]:
        b = os.path.basename(n)
        print(f"  {n}   -> {etq.get(b, ['(sem etiqueta)'])}")


def cmd_contar(zf: zipfile.ZipFile, splits_path: str | None, json_path: str | None) -> int:
    etq = ler_etiquetas(zf)
    imgs = imagens(zf)

    # contagens multi-rótulo: por classe (positivos) e por partição
    por_split_classe: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    crops_por_split = collections.Counter()
    multi_por_split = collections.Counter()
    grupos: dict[str, set] = collections.defaultdict(set)
    linhas = []
    sem_split, sem_etiqueta, sem_positiva = [], [], []

    for n in imgs:
        partes = normalizar(n)
        split = inferir_split(partes)
        if split is None:
            sem_split.append(n)
            continue
        base = os.path.basename(n)
        positivas = etq.get(base)
        if positivas is None:
            sem_etiqueta.append(n)
            positivas = [partes[-1] if partes else "?"]
        elif not positivas:
            # o dataset tem recortes com o vetor todo a zero: não servem para treinar
            sem_positiva.append(n)
            continue
        grupo = inferir_grupo(n)

        crops_por_split[split] += 1
        n_def = len([c for c in positivas if c in DEFECTS])
        if n_def >= 2:
            multi_por_split[split] += 1
        for c in positivas:
            por_split_classe[split][c] += 1
        grupos[grupo].add(split)
        linhas.append({"path": n, "label": "|".join(positivas) or "?",
                       "grupo": grupo, "split": split})

    ordem = [s for s in ("train", "val", "test") if s in crops_por_split]
    print("\n=== recortes por classe positiva × partição (multi-rótulo: um recorte conta em"
          " todas as suas classes) ===")
    largura = max(len(c) for c in CLASSES)
    print("classe".ljust(largura), "".join(f"{s:>8}" for s in ordem), f"{'total':>9}")
    for c in CLASSES:
        vals = [por_split_classe[s].get(c, 0) for s in ordem]
        if any(vals):
            print(c.ljust(largura), "".join(f"{v:>8}" for v in vals), f"{sum(vals):>9}")
    print("-" * (largura + 9 * len(ordem) + 9))
    print("recortes".ljust(largura), "".join(f"{crops_por_split[s]:>8}" for s in ordem),
          f"{sum(crops_por_split.values()):>9}")
    print("multi-rótulo".ljust(largura),
          "".join(f"{multi_por_split[s]:>8}" for s in ordem),
          f"{sum(multi_por_split.values()):>9}")

    if sem_split:
        print(f"\n!! {len(sem_split)} imagens sem partição reconhecível (ex.: {sem_split[0]})")
    if sem_etiqueta:
        print(f"\n!! {len(sem_etiqueta)} recortes sem etiqueta nos XML "
              f"(ex.: {sem_etiqueta[0]}) — ficaram com a pasta como rótulo")
    if sem_positiva:
        print(f"\n!! {len(sem_positiva)} recortes com TODAS as classes a zero "
              f"(ex.: {sem_positiva[0]}) — EXCLUÍDOS do splits.csv: um classificador "
              f"supervisionado não os consegue usar")

    fugas = {g: s for g, s in grupos.items() if len(s) > 1}
    print("\n=== verificação de fuga por grupo (imagem de origem) ===")
    print(f"imagens de origem distintas : {len(grupos)}")
    print(f"grupos em fuga              : {len(fugas)}")
    for g, s in list(fugas.items())[:10]:
        print(f"  {g}: {sorted(s)}")

    resumo = {
        "zip": os.path.basename(zf.filename or "?"),
        "recortes": sum(crops_por_split.values()),
        "por_split": dict(crops_por_split),
        "classe_por_split": {s: dict(por_split_classe[s]) for s in ordem},
        "multirrotulo_por_split": dict(multi_por_split),
        "imagens_de_origem": len(grupos),
        "grupos_em_fuga": len(fugas),
        "exemplos_fuga": {g: sorted(s) for g, s in list(fugas.items())[:20]},
        "sem_split": len(sem_split),
        "sem_etiqueta": len(sem_etiqueta),
        "sem_classe_positiva": len(sem_positiva),
        "exemplos_sem_classe_positiva": sem_positiva[:20],
        "recortes_utilizaveis": sum(crops_por_split.values()),
    }
    if json_path:
        os.makedirs(os.path.dirname(json_path) or ".", exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(resumo, fh, ensure_ascii=False, indent=2)
        print(f"\ncontagens escritas em {json_path}")

    if splits_path:
        os.makedirs(os.path.dirname(splits_path) or ".", exist_ok=True)
        with open(splits_path, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["path", "label", "grupo", "split"])
            w.writeheader()
            w.writerows(sorted(linhas, key=lambda r: (r["split"], r["label"], r["path"])))
        print(f"splits escritos em {splits_path}  ({len(linhas)} linhas)")

    if fugas:
        print("\nFALHA: há imagens de origem em mais do que uma partição. Não avançar.")
        return 2
    if sem_split:
        print("\nFALHA: a divisão não foi reconhecida nos caminhos. Correr --listar e mapear.")
        return 2
    print("\nOK: nenhuma imagem de origem em duas partições.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Contagem e verificação do CODEBRIM a partir do zip.")
    ap.add_argument("--zip", default="data/raw/CODEBRIM_classification_dataset.zip")
    ap.add_argument("--listar", action="store_true", help="mostra a estrutura e não conta nada")
    ap.add_argument("--contar", action="store_true", help="conta recortes e verifica a fuga por imagem")
    ap.add_argument("--limite", type=int, default=15, help="caminhos a mostrar em --listar")
    ap.add_argument("--splits", default=None, help="escreve o splits.csv neste caminho")
    ap.add_argument("--json", dest="json_path", default="docs/contagens_codebrim.json")
    args = ap.parse_args()

    if not os.path.exists(args.zip):
        print(f"zip não encontrado: {args.zip}", file=sys.stderr)
        return 1
    if not (args.listar or args.contar):
        ap.print_help()
        return 1

    with zipfile.ZipFile(args.zip) as zf:
        if args.listar:
            cmd_listar(zf, args.limite)
        if args.contar:
            return cmd_contar(zf, args.splits, args.json_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
