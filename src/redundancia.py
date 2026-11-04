"""Redundancia do pool e limiar de quase-duplicados — dono: A1 (Fausto), eixo drone D1.

Porque isto e necessario: um pool de drone e **video**. Se a aquisicao escolher 20
quadros do mesmo defeito, gasta orcamento a repetir a mesma informacao. Antes de
inventar um limiar, mede-se a redundancia que ja existe no CODEBRIM — onde todos os
recortes de uma mesma imagem sao quase-duplicados **por construcao** (mesma ponte,
mesmo instante, deslocamento de milimetros). Essa e a distribuicao de referencia.

Metodo:
  * similaridade de cosseno entre embeddings DINOv2 (ja normalizados L2);
  * pares **intra-imagem** (mesma imagem de origem) = quase-duplicados conhecidos;
  * pares **inter-imagem** = o que "parecido mas diferente" e neste dataset;
  * `tau` = percentil 99,9 da distribuicao inter-imagem: o valor em que se aceita
    ~0,1% de falsos agrupamentos. Nao e um numero universal (a pesquisa do A1 nao
    encontrou nenhum para betao); e o numero **deste** dataset, medido.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as C  # noqa: E402
from baseline import carregar_caracteristicas  # noqa: E402


def medir(seed: int = 0, n_pares: int = 300000) -> dict:
    F, Y, df = carregar_caracteristicas()
    g = df.grupo.values
    pool = np.flatnonzero(df.split.values == "train")
    rng = np.random.default_rng(seed)

    # --- pares intra-imagem ------------------------------------------------------
    intra = []
    for grp, idx in pd.Series(pool).groupby(g[pool]):
        idx = idx.values
        if len(idx) < 2:
            continue
        S = F[idx] @ F[idx].T
        iu = np.triu_indices(len(idx), k=1)
        intra.append(S[iu])
    intra = np.concatenate(intra) if intra else np.array([])

    # --- pares inter-imagem (amostra) --------------------------------------------
    a = rng.choice(pool, n_pares)
    b = rng.choice(pool, n_pares)
    m = g[a] != g[b]
    inter = np.einsum("ij,ij->i", F[a[m]], F[b[m]])

    tau = float(np.percentile(inter, 99.9))

    # --- efeito do limiar ---------------------------------------------------------
    # quantas imagens "colapsariam" no pool se agrupassemos por tau
    grupos_por_tau = _agrupar(F[pool], tau)
    # apos L=5%, quantos candidatos do pool sao quase-duplicados de um rotulado
    from dados import selecionar_L

    lab = pool[selecionar_L(Y[pool], 0.05, seed)]
    S = F[lab] @ F[pool].T
    redundantes = (S.max(0) >= tau).sum()

    res = {
        "pares_intra": int(len(intra)),
        "pares_inter": int(m.sum()),
        "sim_intra_media": round(float(intra.mean()), 4) if len(intra) else None,
        "sim_intra_p5": round(float(np.percentile(intra, 5)), 4) if len(intra) else None,
        "sim_inter_media": round(float(inter.mean()), 4),
        "sim_inter_p99": round(float(np.percentile(inter, 99)), 4),
        "sim_inter_p999": round(tau, 4),
        "tau_proposto": round(tau, 4),
        "imagens_de_origem_no_pool": int(pd.Series(g[pool]).nunique()),
        "grupos_por_tau": int(len(np.unique(grupos_por_tau))),
        "recortes_do_pool_quase_dup_de_um_rotulado": int(redundantes),
        "fracao_pool_redundante_apos_L": round(float(redundantes / len(pool)), 4),
    }
    return res


def _agrupar(F: np.ndarray, tau: float) -> np.ndarray:
    """Agrupamento guloso por similaridade: cada ponto junta-se ao primeiro grupo
    cujo representante tenha cosseno >= tau; senao cria grupo novo.

    Os representantes vivem num array **pre-alocado**: converter a lista em matriz a
    cada ponto custaria O(n^2 * dim) de copia e tornava isto inviavel.
    """
    n, dim = F.shape
    reps = np.empty((n, dim), dtype=F.dtype)
    m = 0
    etiqueta = np.zeros(n, dtype=int)
    for i in range(n):
        if m:
            s = reps[:m] @ F[i]
            j = int(np.argmax(s))
            if s[j] >= tau:
                etiqueta[i] = j
                continue
        reps[m] = F[i]
        etiqueta[i] = m
        m += 1
    return etiqueta


if __name__ == "__main__":
    r = medir()
    C.escrever_json(r, C.RUNS / "redundancia.json")
    print("Redundancia do pool (treino oficial) — embeddings DINOv2 ViT-S/14\n")
    for k, v in r.items():
        print(f"  {k:<45} {v}")
    print(
        "\nLeitura: a similaridade intra-imagem (quase-duplicados reais) esta muito acima da\n"
        "inter-imagem. Um tau no percentil 99,9 dos pares inter-imagem separa os dois mundos\n"
        "sem juntar pontes diferentes. E o numero que a aquisicao passa a usar para nao\n"
        "readquirir o mesmo defeito — o que num video de drone e o caso normal, nao a excecao."
    )
