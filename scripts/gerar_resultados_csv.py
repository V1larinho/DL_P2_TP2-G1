"""
gerar_resultados_csv.py
Gera paper/resultados.csv com todos os resultados experimentais do projeto.
Inclui: embedding, sanidade kNN, baselines (teto, L-só) e todas as corridas AL.
"""

import csv
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(REPO, "paper", "resultados.csv")

COLUNAS = [
    "data", "commit", "classificador", "estrategia", "seed", "ronda",
    "n_rotulos", "fracao", "f1_val", "f1_teste", "ece", "segundos", "notas",
    # colunas extras dos ficheiros AL (preservadas)
    "n_candidatos", "hash_rotulado",
    "f1_Background", "f1_CorrosionStain", "f1_Crack",
    "f1_Efflorescence", "f1_ExposedBars", "f1_Spallation",
]

DATA = "2026-10-27"
COMMIT = "9f897179"

linhas = []

# ── 1. Embedding (extração DINOv2) ──────────────────────────────────────────
linhas.append({
    "data": DATA,
    "commit": COMMIT,
    "classificador": "extrator",
    "estrategia": "extracao",
    "seed": "",
    "ronda": "",
    "n_rotulos": 7677,
    "fracao": 1.0,
    "f1_val": "",
    "f1_teste": "",
    "ece": "",
    "segundos": 475.1,
    "notas": "DINOv2 ViT-S/14 CLS normalizado L2; 7677x384",
})

# ── 2. Sanidade k-NN ─────────────────────────────────────────────────────────
linhas.append({
    "data": DATA,
    "commit": COMMIT,
    "classificador": "knn_k20",
    "estrategia": "sanidade",
    "seed": 0,
    "ronda": 0,
    "n_rotulos": 6438,
    "fracao": 1.0,
    "f1_val": 0.7000,
    "f1_teste": "",
    "ece": "",
    "segundos": "",
    "notas": "k-NN k=20 cosseno na validação; acaso 0.2551",
})

# ── 3. Teto (3 seeds) ────────────────────────────────────────────────────────
teto_seeds = [
    (0, 0.7958, 0.8296, 0.0435, 18.0),
    (1, 0.7964, 0.8296, 0.0423, 17.7),
    (2, 0.7957, 0.8327, 0.0415, 17.1),
]
for seed, f1v, f1t, ece, seg in teto_seeds:
    linhas.append({
        "data": DATA,
        "commit": COMMIT,
        "classificador": "cabeca_linear",
        "estrategia": "teto",
        "seed": seed,
        "ronda": 0,
        "n_rotulos": 6438,
        "fracao": 1.0,
        "f1_val": f1v,
        "f1_teste": f1t,
        "ece": ece,
        "segundos": seg,
        "notas": "teto 100% rotulos",
    })

# ── 4. L-só (seed 0) ─────────────────────────────────────────────────────────
linhas.append({
    "data": DATA,
    "commit": COMMIT,
    "classificador": "cabeca_linear",
    "estrategia": "l_so",
    "seed": 0,
    "ronda": 0,
    "n_rotulos": 322,
    "fracao": 0.050,
    "f1_val": 0.7328,
    "f1_teste": 0.7665,
    "ece": 0.0662,
    "segundos": 1.1,
    "notas": "L-só 5% pool seed 0",
})

# ── 5. Estratégias AL ─────────────────────────────────────────────────────────
estrategias = ["aleatoria", "bald", "badge", "coreset", "entropia", "margem"]
seeds = [0, 1, 2]

for est in estrategias:
    for seed in seeds:
        csv_path = os.path.join(REPO, "runs", "al", est, f"seed{seed}", "rondas.csv")
        if not os.path.exists(csv_path):
            print(f"[AVISO] Ficheiro não encontrado: {csv_path}", file=sys.stderr)
            continue
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                linha = {
                    "data": DATA,
                    "commit": COMMIT,
                    "classificador": "cabeca_linear",
                    "estrategia": row.get("estrategia", est),
                    "seed": row.get("seed", seed),
                    "ronda": row.get("ronda", ""),
                    "n_rotulos": row.get("n_rotulos", ""),
                    "fracao": row.get("fracao", ""),
                    "f1_val": row.get("f1_val", ""),
                    "f1_teste": row.get("f1_teste", ""),
                    "ece": row.get("ece", ""),
                    "segundos": row.get("segundos", ""),
                    "notas": "",
                    "n_candidatos": row.get("n_candidatos", ""),
                    "hash_rotulado": row.get("hash_rotulado", ""),
                    "f1_Background": row.get("f1_Background", ""),
                    "f1_CorrosionStain": row.get("f1_CorrosionStain", ""),
                    "f1_Crack": row.get("f1_Crack", ""),
                    "f1_Efflorescence": row.get("f1_Efflorescence", ""),
                    "f1_ExposedBars": row.get("f1_ExposedBars", ""),
                    "f1_Spallation": row.get("f1_Spallation", ""),
                }
                linhas.append(linha)

# ── Escrita ──────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLUNAS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(linhas)

print(f"[OK] {OUTPUT} — {len(linhas)} linhas escritas.")
