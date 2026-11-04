"""Cabeca linear sobre caracteristicas congeladas — usada pelo teto (A2) e pelas rondas (A3).

Um unico treinador para as duas coisas: se o teto e as rondas usassem codigo diferente,
a curva do AL estaria a ser comparada com outro modelo.

Decisoes fixadas em PROTOCOLO.md §3:
  * `BCEWithLogitsLoss` (rotulos nao exclusivos) — nunca softmax.
  * AdamW, epocas 200, lr 0.01, weight_decay 1e-4, batch 64, semente propria.
  * dropout opcional (so a BALD precisa; sem ele a BALD degenera em entropia).
  * limiares por classe escolhidos na VALIDADE e congelados.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn


class Cabeca(nn.Module):
    def __init__(self, dim: int, n_classes: int, dropout: float = 0.0):
        super().__init__()
        self.drop = nn.Dropout(dropout)
        self.fc = nn.Linear(dim, n_classes)

    def forward(self, x):
        return self.fc(self.drop(x))


def treinar(
    F: np.ndarray,
    Y: np.ndarray,
    idx: np.ndarray,
    seed: int = 0,
    epocas: int = 200,
    lr: float = 0.01,
    wd: float = 1e-4,
    batch: int = 64,
    dropout: float = 0.0,
) -> Cabeca:
    torch.manual_seed(seed)
    g = torch.Generator().manual_seed(seed)
    X = torch.from_numpy(np.ascontiguousarray(F[idx]))
    T = torch.from_numpy(np.ascontiguousarray(Y[idx]))
    modelo = Cabeca(F.shape[1], Y.shape[1], dropout)
    opt = torch.optim.AdamW(modelo.parameters(), lr=lr, weight_decay=wd)
    perda = nn.BCEWithLogitsLoss()
    n = len(idx)
    bs = min(batch, n)
    for _ in range(epocas):
        ordem = torch.randperm(n, generator=g)
        for i in range(0, n, bs):
            b = ordem[i : i + bs]
            opt.zero_grad()
            perda(modelo(X[b]), T[b]).backward()
            opt.step()
    modelo.eval()
    return modelo


@torch.no_grad()
def probabilidades(modelo: Cabeca, F: np.ndarray, batch: int = 2048) -> np.ndarray:
    modelo.eval()
    saida = []
    for i in range(0, len(F), batch):
        saida.append(torch.sigmoid(modelo(torch.from_numpy(np.ascontiguousarray(F[i : i + batch])))))
    return torch.cat(saida).numpy()


@torch.no_grad()
def probabilidades_mc(modelo: Cabeca, F: np.ndarray, T: int = 10, batch: int = 2048) -> np.ndarray:
    """T passagens em modo treino (dropout ativo) -> (T, n, C)."""
    modelo.train()
    saida = []
    for _ in range(T):
        p = []
        for i in range(0, len(F), batch):
            p.append(torch.sigmoid(modelo(torch.from_numpy(np.ascontiguousarray(F[i : i + batch])))))
        saida.append(torch.cat(p).numpy())
    modelo.eval()
    return np.stack(saida)


def entropia_binaria(p: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    p = np.clip(p, eps, 1 - eps)
    return -(p * np.log(p) + (1 - p) * np.log(1 - p))


def incerteza_entropia(P: np.ndarray) -> np.ndarray:
    return entropia_binaria(P).mean(1)


def incerteza_margem(P: np.ndarray) -> np.ndarray:
    """Media de |p-0,5|; MENOR = mais incerto (o chamador ordena ascendente)."""
    return np.abs(P - 0.5).mean(1)


def incerteza_bald(Pmc: np.ndarray) -> np.ndarray:
    media = Pmc.mean(0)
    return entropia_binaria(media).mean(1) - entropia_binaria(Pmc).mean(2).mean(0)


def limiares_por_classe(Y: np.ndarray, P: np.ndarray, grelha: np.ndarray | None = None) -> np.ndarray:
    """Limiar que maximiza o F1 de cada classe na validade. Devolve vetor de 6."""
    from sklearn.metrics import f1_score

    if grelha is None:
        grelha = np.arange(0.05, 0.96, 0.05)
    lim = np.full(Y.shape[1], 0.5, dtype=np.float32)
    for c in range(Y.shape[1]):
        if Y[:, c].sum() == 0:
            continue
        melhor, melhor_t = -1.0, 0.5
        for t in grelha:
            f = f1_score(Y[:, c], (P[:, c] >= t).astype(int), zero_division=0)
            if f > melhor:
                melhor, melhor_t = f, float(t)
        lim[c] = melhor_t
    return lim


def temperatura(logits: np.ndarray, Y: np.ndarray) -> float:
    """Temperature scaling: um T>0 por minimizacao da BCE na validade (Guo et al. 2017)."""
    z = torch.from_numpy(np.ascontiguousarray(logits)).double()
    t = torch.from_numpy(np.ascontiguousarray(Y)).double()
    logT = torch.zeros(1, requires_grad=True, dtype=torch.double)
    opt = torch.optim.LBFGS([logT], lr=0.1, max_iter=60)
    perda = nn.BCEWithLogitsLoss()

    def fecho():
        opt.zero_grad()
        l = perda(z / torch.exp(logT), t)
        l.backward()
        return l

    opt.step(fecho)
    return float(torch.exp(logT).item())


def logits_de(modelo: Cabeca, F: np.ndarray) -> np.ndarray:
    with torch.no_grad():
        modelo.eval()
        return modelo(torch.from_numpy(np.ascontiguousarray(F))).numpy()
