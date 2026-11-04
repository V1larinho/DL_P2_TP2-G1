#!/usr/bin/env python
"""Sanidade do extrator (C1.4, dono: A1) — k-NN sobre as caracteristicas congeladas.

Para que serve: antes de discutir estrategias de aquisicao, e preciso provar que a
representacao separa alguma coisa. Um k-NN sem treino, sobre os mesmos embeddings,
da o chao da representacao. Se estivesse ao nivel do acaso, todas as curvas de AL
do grupo mediriam ruido.

O "acaso" e medido, nao assumido: os rotulos de validacao sao baralhados e o mesmo
k-NN e reavaliado.

Uso:
    python scripts/sanidade_knn.py            # k=20 (o do protocolo)
    python scripts/sanidade_knn.py --k 5      # variante, se quiseres ver a sensibilidade
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import numpy as np  # noqa: E402

import comum as C  # noqa: E402
from baseline import carregar_caracteristicas  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="k-NN de sanidade do extrator (train -> val)")
    ap.add_argument("--k", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0, help="seed do baralhamento que mede o acaso")
    a = ap.parse_args(argv)

    from sklearn.neighbors import KNeighborsClassifier

    F, Y, df = carregar_caracteristicas()
    Fn = F / (np.linalg.norm(F, axis=1, keepdims=True) + 1e-12)
    tr = (df.split == "train").values
    va = (df.split == "val").values

    t0 = time.time()
    m = KNeighborsClassifier(n_neighbors=a.k, metric="cosine", n_jobs=-1)
    m.fit(Fn[tr], Y[tr])
    pred = np.asarray(m.predict(Fn[va])).reshape(int(va.sum()), -1)
    f1 = C.macro_f1(Y[va], pred, 0.5)
    dt = time.time() - t0

    rng = np.random.default_rng(a.seed)
    acaso = C.macro_f1(Y[va], Y[va][rng.permutation(int(va.sum()))], 0.5)

    print(f"k-NN k={a.k} sobre vits14: macro-F1(val)={f1:.4f}  acaso={acaso:.4f}  ({dt:.1f}s)")
    print(f"  treino={int(tr.sum())} recortes, validacao={int(va.sum())} recortes")

    C.registar_resultado(
        {
            "data": time.strftime("%Y-%m-%d %H:%M"),
            "commit": C.commit_atual(),
            "configuracao": f"knn{a.k}/vits14",
            "estrategia": "knn",
            "seed": a.seed,
            "fracao_rotulos": 1.0,
            "f1_val": round(float(f1), 4),
            "f1_teste": float("nan"),  # o k-NN e uma sanidade, nao uma condicao do estudo
            "n_rotulos": int(tr.sum()),
            "tempo_s": round(dt, 1),
        },
        substituir=True,
    )
    print(f"  registado em {C.csv_resultados().relative_to(C.RAIZ)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
