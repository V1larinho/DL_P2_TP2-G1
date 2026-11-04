"""Extracao de caracteristicas DINOv2 (familia C) — dono: A1 (Fausto).

Pesos congelados, embedding **CLS normalizado L2**. Grava:
  runs/emb_vits14.npy     (n_recortes x 384) float32
  runs/emb_index.csv      path, label, grupo, split  (a MESMA ordem das linhas)
  runs/emb_meta.json      modelo, tamanho, hash do indice, data

Retomavel: se o checkpoint existir e o hash do indice bater certo, continua de onde parou.
Nunca inventa linhas: se faltar alguma, o npy nao e escrito.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as C  # noqa: E402
from dados import DESVIO, MEDIA, excluir_sem_rotulo  # noqa: E402

MODELOS = {
    "dinov2_vits14": "vit_small_patch14_dinov2.lvd142m",
    "dinov2_vitb14": "vit_base_patch14_dinov2.lvd142m",
}


def construir(modelo: str, tamanho: int):
    import timm
    import torch

    # dynamic_img_size: os pesos DINOv2 do timm assumem 518 px; queremos 224 (16x16 patches)
    net = timm.create_model(MODELOS[modelo], pretrained=True, num_classes=0, dynamic_img_size=True)
    net.eval()
    cfg = timm.data.resolve_data_config({}, model=net)
    cfg["input_size"] = (3, tamanho, tamanho)
    tf = timm.data.create_transform(**cfg, is_training=False)
    return net, tf


def extrair(
    modelo="dinov2_vits14",
    tamanho=224,
    batch=64,
    limite: int | None = None,
    saida: Path | None = None,
    threads: int | None = None,
) -> Path:
    import torch
    from PIL import Image

    torch.set_num_threads(threads or C.thread_count())
    C.garantir_dirs()

    df = C.carregar("data/splits.csv")
    df, vazios = excluir_sem_rotulo(df)
    if limite:
        df = df.groupby("split", group_keys=False).head(max(1, limite // 3)).reset_index(drop=True)
    saida = saida or (C.RUNS / f"emb_{modelo.split('_')[-1]}.npy")
    ckpt = saida.with_suffix(".ckpt.npy")
    meta_p = saida.with_suffix("").with_name(saida.stem + "_meta.json")

    hash_idx = C.hash_indices(range(len(df)))
    if ckpt.exists() and meta_p.exists():
        import json

        meta = json.loads(meta_p.read_text(encoding="utf-8"))
        if meta.get("hash_indice") == hash_idx and meta.get("modelo") == modelo:
            feito = int(meta.get("feito", 0))
            emb = np.load(ckpt)
            print(f"retomo de {feito}/{len(df)} ({ckpt.name})")
        else:
            feito, emb = 0, np.zeros((len(df), 1), np.float32)
    else:
        feito, emb = 0, np.zeros((len(df), 1), np.float32)

    if feito >= len(df):
        np.save(saida, emb)
        print(f"ja estava completo: {saida}")
        return saida

    net, tf = construir(modelo, tamanho)
    t0 = time.time()
    emb_full = np.zeros((len(df), net.num_features), dtype=np.float32)

    with torch.no_grad():
        i = feito
        while i < len(df):
            j = min(i + batch, len(df))
            xs = []
            for k in range(i, j):
                p = C.caminho_imagem(df.path.iloc[k])
                xs.append(tf(Image.open(p).convert("RGB")))
            x = torch.stack(xs)
            f = net(x)  # ViT com num_classes=0 -> token CLS
            f = f / f.norm(dim=1, keepdim=True).clamp_min(1e-12)
            emb_full[i:j] = f.numpy()
            i = j
            if (i // batch) % 10 == 0 or i >= len(df):
                vel = (i - feito) / max(1e-9, time.time() - t0)
                print(f"  {i}/{len(df)}  {vel:.1f} img/s  restam {(len(df) - i) / max(vel, 1e-9) / 60:.1f} min", flush=True)
            if (i // batch) % 20 == 0:
                np.save(ckpt, emb_full[:i])
                C.escrever_json(
                    {"modelo": modelo, "hash_indice": hash_idx, "feito": i, "n": len(df), "tamanho": tamanho}, meta_p
                )

    np.save(saida, emb_full)
    df.to_csv(saida.with_suffix("").with_name(saida.stem + "_index.csv"), index=False)
    C.escrever_json(
        {
            "modelo": modelo,
            "timm": MODELOS[modelo],
            "n": int(len(df)),
            "dim": int(emb_full.shape[1]),
            "normalizado_l2": True,
            "pooling": "cls",
            "tamanho": tamanho,
            "hash_indice": hash_idx,
            "excluidos_sem_rotulo": vazios,
            "segundos": round(time.time() - t0, 1),
        },
        meta_p,
    )
    if ckpt.exists():
        ckpt.unlink()
    print(f"\nescrito {saida}  shape={emb_full.shape}  em {time.time() - t0:.0f}s")
    return saida


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", default="dinov2_vits14", choices=list(MODELOS))
    ap.add_argument("--tamanho", type=int, default=224)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--limite", type=int, default=None, help="smoke test em poucos recortes")
    ap.add_argument("--threads", type=int, default=None)
    ap.add_argument("--saida", default=None, help="caminho do .npy (por omissao runs/emb_<modelo>.npy)")
    a = ap.parse_args()
    extrair(a.modelo, a.tamanho, a.batch, a.limite, Path(a.saida) if a.saida else None, threads=a.threads)
