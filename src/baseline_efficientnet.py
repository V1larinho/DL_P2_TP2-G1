# src/baseline_efficientnet.py
# Esqueleto da baseline do tema C (PL08 §2.3): CNN pré-treinada (EfficientNet)
# com fine-tuning a 100% dos rótulos. Executar apenas quando houver GPU disponível.
# Regista cada experiência em paper/resultados.csv (data, commit, configuracao,
# metrica de validacao, tempo de treino).

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import models

from comum import registar_resultado  # ja existe no vosso src/

N_CLASSES = 6  # CODEBRIM: 5 defeitos + fundo (multi-rótulo)


def build_model(device: torch.device, lr: float = 1e-4, weight_decay: float = 1e-4):
    model = models.efficientnet_b0(weights="IMAGENET1K_V1")
    # Fine-tuning: descongelar tudo e trocar a cabeça de classificação.
    in_feats = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_feats, N_CLASSES)
    model = model.to(device)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    return model, criterion, optimizer


def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running = 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        running += loss.item() * x.size(0)
    return running / len(loader.dataset)


def evaluate(model, loader, device):
    model.eval()
    ys, ps = [], []
    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            logits = model(x)
            ys.append(y.cpu())
            ps.append(torch.sigmoid(logits).cpu())
    ys = np.vstack(ys)
    ps = np.vstack(ps)
    preds = (ps >= 0.5).astype(int)

    f1s = []
    for c in range(N_CLASSES):
        tp = int(((preds[:, c] == 1) & (ys[:, c] == 1)).sum())
        fp = int(((preds[:, c] == 1) & (ys[:, c] == 0)).sum())
        fn = int(((preds[:, c] == 0) & (ys[:, c] == 1)).sum())
        f1 = 2 * tp / max(1, 2 * tp + fp + fn)
        f1s.append(f1)
    return float(np.mean(f1s))


def run_baseline(train_ds, val_ds, epochs: int = 20, batch: int = 32,
                 lr: float = 1e-4, seed: int = 42, device: str | None = None,
                 experiencia: str = "efficientnet_b0_100pct"):
    torch.manual_seed(seed)
    np.random.seed(seed)
    device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model, criterion, optimizer = build_model(device, lr=lr)

    train_loader = DataLoader(train_ds, batch_size=batch, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch, shuffle=False)

    t0 = time.time()
    for ep in range(epochs):
        train_one_epoch(model, train_loader, criterion, optimizer, device)
    macro_f1 = evaluate(model, val_loader, device)
    tempo = time.time() - t0

    registar_resultado(
        experiencia=experiencia,
        classificador="efficientnet_b0",
        estrategia="baseline_100pct",
        seed=seed,
        fracao=1.0,
        metrica="macro_f1_val",
        valor=macro_f1,
        tempo=tempo,
    )
    print(f"[baseline] Macro-F1 val = {macro_f1:.4f} | tempo = {tempo:.1f}s")
    return macro_f1, tempo


if __name__ == "__main__":
    # Exemplo de uso (adaptar ao vosso loader de dados):
    # from dados import carregar_splits
    # train_ds, val_ds, _ = carregar_splits(csv="data/splits.csv", seed=42)
    # run_baseline(train_ds, val_ds)
    raise SystemExit("Este ficheiro e um esqueleto; importar e chamar run_baseline(...) com os datasets reais.")
