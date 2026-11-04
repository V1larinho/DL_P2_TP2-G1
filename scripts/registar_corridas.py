#!/usr/bin/env python
"""Reconstroi as linhas de `paper/resultados.csv` a partir de `runs/al/*/seed*/`.

Porque existe: a primeira vaga de 18 corridas foi feita antes de o registo do
PL08 (P8.7) estar a funcionar — ficaram os `meta.json` e os `rondas.csv`, mas o
`resultados.csv` so tinha as linhas da baseline. Este script nao inventa nada:
le os numeros ja medidos e escreve a linha que `al.py` passaria a escrever.

Idempotente: usar `substituir=True` faz com que correr duas vezes deixe o mesmo
numero de linhas.

Uso:
    python scripts/registar_corridas.py            # reconstroi (13 linhas de AL)
    python scripts/registar_corridas.py --seco     # so mostra o que faria
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import pandas as pd  # noqa: E402

import comum as C  # noqa: E402


def linhas() -> list[dict]:
    out = []
    for meta_path in sorted((C.RUNS / "al").glob("*/seed*/meta.json")):
        meta = C.json_simples(__import__("json").loads(meta_path.read_text(encoding="utf-8")))
        final = meta["final"]
        rondas = pd.read_csv(meta_path.parent / "rondas.csv")
        # o meta.json nao guarda a hora; a data de modificacao do ficheiro e a
        # hora a que a corrida terminou — um valor real, nao inventado
        quando = time.strftime("%Y-%m-%d %H:%M", time.localtime(meta_path.stat().st_mtime))
        out.append(
            {
                "data": quando,
                "commit": C.commit_atual(),
                "configuracao": f"al/{meta['estrategia']}",
                "estrategia": meta["estrategia"],
                "seed": meta["seed"],
                "fracao_rotulos": round(float(final["fracao"]), 4),
                "f1_val": round(float(final["f1_val"]), 4),
                "f1_teste": round(float(final["f1_teste"]), 4),
                "n_rotulos": int(final["n_rotulos"]),
                "tempo_s": round(float(rondas.segundos.sum()), 1),
            }
        )
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="regista em resultados.csv as corridas de AL ja feitas")
    ap.add_argument("--seco", action="store_true", help="nao escreve, so mostra")
    a = ap.parse_args(argv)

    ls = linhas()
    if not ls:
        print("nenhuma corrida encontrada em runs/al/*/seed*/meta.json", file=sys.stderr)
        return 1

    print(f"{len(ls)} corridas em runs/al/")
    print(pd.DataFrame(ls)[["estrategia", "seed", "n_rotulos", "f1_val", "f1_teste"]].to_string(index=False))
    if a.seco:
        print("\n(--seco: nada escrito)")
        return 0

    for linha in ls:
        C.registar_resultado(linha, substituir=True)

    res = pd.read_csv(C.csv_resultados())
    print(f"\nregistadas: {len(res)} linhas em {C.csv_resultados().relative_to(RAIZ)}")
    print(res.groupby("configuracao").size().to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
