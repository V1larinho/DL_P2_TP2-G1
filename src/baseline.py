"""Baseline e teto do projeto (PL08 §2.3) — dona: A2 (Gabriela).

Duas coisas distintas, que o relatorio nao pode confundir:

  * **Teto** = cabeca linear com **100% dos rotulos do pool**. E o maximo que a
    estrategia de aquisicao pode atingir nesta representacao; e o denominador do
    "95% do teto". Nao e o teto da literatura (a CNN afinada do PL08 serve de
    confirmacao e vai no resultados.csv com o nome certo).
  * **L-so** = a mesma cabeca com os 5% iniciais. E o chao da curva.

Ambos gravam em paper/resultados.csv com data, commit, configuracao, metrica de
validacao e tempo (o esquema que a PL08 pede). Os limiares sao escolhidos na
VALIDADE e gravados, para nao voltarem a ser escolhidos no teste.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as C  # noqa: E402
import probe  # noqa: E402
from dados import selecionar_L  # noqa: E402

HIPER = dict(epocas=200, lr=0.01, wd=1e-4, batch=64)


def carregar_caracteristicas(saida: Path | None = None):
    saida = saida or (C.RUNS / "emb_vits14.npy")
    idx_p = saida.with_suffix("").with_name(saida.stem + "_index.csv")
    F = np.load(saida).astype(np.float32)
    import pandas as pd

    df = pd.read_csv(idx_p)
    df["grupo"] = df["grupo"].astype(str)
    if len(df) != len(F):
        raise ValueError(f"indice ({len(df)}) e embeddings ({len(F)}) nao batem certo")
    Y = C.matriz_rotulos(df)
    return F, Y, df


def correr(nome: str, seed: int = 0, F=None, Y=None, df=None, fracao: float | None = None) -> dict:
    if F is None:
        F, Y, df = carregar_caracteristicas()
    tr = np.flatnonzero(df.split.values == "train")
    va = np.flatnonzero(df.split.values == "val")
    te = np.flatnonzero(df.split.values == "test")
    if fracao is not None:
        tr = tr[selecionar_L(Y[tr], fracao, seed)]

    t0 = time.time()
    m = probe.treinar(F, Y, tr, seed=seed, **HIPER, dropout=0.0)
    Pv = probe.probabilidades(m, F[va])
    lim = probe.limiares_por_classe(Y[va], Pv)
    Pt = probe.probabilidades(m, F[te])
    dt = time.time() - t0

    f1_val = C.macro_f1(Y[va], Pv, lim)
    f1_te = C.macro_f1(Y[te], Pt, lim)
    por_classe = C.f1_por_classe(Y[te], Pt, lim)
    tem = probe.temperatura(probe.logits_de(m, F[va]), Y[va])
    ece = ece_macro(Y[te], Pt)

    res = {
        "nome": nome,
        "seed": seed,
        "n_rotulos": int(len(tr)),
        "fracao_pool": float(len(tr) / len(np.flatnonzero(df.split.values == "train"))),
        "f1_val": round(f1_val, 4),
        "f1_teste": round(f1_te, 4),
        "f1_por_classe": {k: round(v, 4) for k, v in por_classe.items()},
        "ece_macro": round(ece, 4),
        "temperatura": round(tem, 3),
        "limiares": {c: round(float(t), 2) for c, t in zip(C.CLASSES, lim)},
        "segundos": round(dt, 1),
    }
    C.registar_resultado(
        {
            "data": time.strftime("%Y-%m-%d %H:%M"),
            "commit": C.commit_atual(),
            "configuracao": f"vits14+linear/{nome}",
            "estrategia": nome,
            "seed": seed,
            "fracao_rotulos": round(res["fracao_pool"], 4),
            "f1_val": round(f1_val, 4),
            "f1_teste": round(f1_te, 4),
            "n_rotulos": len(tr),
            "tempo_s": round(dt, 1),
        },
        substituir=True,
    )
    d = C.RUNS / "baseline"
    d.mkdir(parents=True, exist_ok=True)
    C.escrever_json(res, d / f"{nome}_s{seed}.json")
    np.save(d / f"limiares_{nome}_s{seed}.npy", lim)
    print(
        f"{nome:<10} seed={seed}  n={len(tr):>5}  F1 val={f1_val:.4f}  F1 teste={f1_te:.4f}  "
        f"ECE={ece:.3f}  T*={tem:.2f}  ({dt:.0f}s)"
    )
    print("  " + "  ".join(f"{k[:12]}={v:.3f}" for k, v in por_classe.items()))
    return res


def ece_macro(Y: np.ndarray, P: np.ndarray, n_bins: int = 10) -> float:
    """ECE marginal por classe, depois media (a definicao que o A5 fixou)."""
    bordas = np.linspace(0, 1, n_bins + 1)
    eces = []
    for c in range(Y.shape[1]):
        p, y = P[:, c], Y[:, c]
        e = 0.0
        for a, b in zip(bordas[:-1], bordas[1:]):
            m = (p >= a) & (p < b if b < 1 else p <= b)
            if m.sum():
                e += m.sum() / len(p) * abs(y[m].mean() - p[m].mean())
        eces.append(e)
    return float(np.mean(eces))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiencia", default="teto", choices=["teto", "l_so", "ambos"])
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    F, Y, df = carregar_caracteristicas()
    print(f"caracteristicas: {F.shape}  (treino={int((df.split == 'train').sum())}, val={int((df.split == 'val').sum())}, teste={int((df.split == 'test').sum())})")
    if a.experiencia in ("teto", "ambos"):
        correr("teto", a.seed, F, Y, df)
    if a.experiencia in ("l_so", "ambos"):
        correr("l_so", a.seed, F, Y, df, fracao=0.05)
