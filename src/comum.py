"""Utilitarios partilhados: rotulos, caminhos, leitura das divisoes e metricas.

Uma unica definicao de cada coisa, para que `dados.py`, `al.py` e `avaliar.py`
nao possam discordar sobre a ordem das classes ou sobre o que e um "grupo".
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "data"
RUNS = RAIZ / "runs"
PAPEL = RAIZ / "paper"

# Ordem alfabetica: deterministica e independente da ordem em que o zip foi lido.
CLASSES = [
    "Background",
    "CorrosionStain",
    "Crack",
    "Efflorescence",
    "ExposedBars",
    "Spallation",
]
N_CLASSES = len(CLASSES)
SEP = "|"

# A raiz onde o zip foi extraido. Aceita as duas profundidades que o zip do
# CODEBRIM produz, em vez de obrigar a editar codigo quando muda o unzip.
BASES = ("data/raw", "data/raw/CODEBRIM_classification_dataset", "data/raw/classification_dataset")


def base_dados() -> Path:
    for b in BASES:
        p = RAIZ / b / "classification_dataset"
        if p.is_dir():
            return p
    for b in BASES:
        p = RAIZ / b
        if (p / "classification_dataset").is_dir():
            return p / "classification_dataset"
    raise FileNotFoundError(
        "Nao encontrei classification_dataset/. Extrai o zip para data/raw/ "
        "(python -m zipfile -e data/raw/CODEBRIM_classification_dataset.zip data/raw/)."
    )


def caminho_imagem(rel: str) -> Path:
    """`splits.csv` guarda o caminho a partir de data/raw/."""
    return RAIZ / "data" / "raw" / rel


def parse_label(s: str) -> np.ndarray:
    """'Crack|Spallation' -> vetor de 6 posicoes em CLASSES."""
    y = np.zeros(N_CLASSES, dtype=np.float32)
    if isinstance(s, str) and s.strip():
        for t in s.split(SEP):
            t = t.strip()
            if t:
                y[CLASSES.index(t)] = 1.0
    return y


def matriz_rotulos(df: pd.DataFrame) -> np.ndarray:
    return np.stack([parse_label(s) for s in df["label"]]) if len(df) else np.zeros((0, N_CLASSES), np.float32)


def carregar(csv: str | Path = "data/splits.csv") -> pd.DataFrame:
    csv = Path(csv)
    if not csv.is_absolute():
        csv = RAIZ / csv
    df = pd.read_csv(csv)
    for c in ("path", "label", "grupo", "split"):
        if c not in df.columns:
            raise ValueError(f"falta a coluna {c!r} em {csv}")
    df["grupo"] = df["grupo"].astype(str)
    return df


def macro_f1(y: np.ndarray, p: np.ndarray, limiar: np.ndarray | float = 0.5) -> float:
    """Macro-F1 multi-rotulo. Classe sem positivos nem previstos fica fora da media
    (comportamento declarado: nao se inventa F1=0 para uma classe ausente)."""
    from sklearn.metrics import f1_score

    yhat = (p >= np.asarray(limiar)).astype(int)
    presentes = (y.sum(0) > 0) | (yhat.sum(0) > 0)
    if not presentes.any():
        return float("nan")
    return float(f1_score(y[:, presentes], yhat[:, presentes], average="macro", zero_division=0))


def f1_por_classe(y: np.ndarray, p: np.ndarray, limiar) -> dict[str, float]:
    from sklearn.metrics import f1_score

    yhat = (p >= np.asarray(limiar)).astype(int)
    f = f1_score(y, yhat, average=None, zero_division=0, labels=list(range(N_CLASSES)))
    return {c: float(v) for c, v in zip(CLASSES, f)}


def hash_indices(idx) -> str:
    h = hashlib.sha256()
    for i in sorted(int(i) for i in idx):
        h.update(str(i).encode())
        h.update(b",")
    return h.hexdigest()[:16]


def garantir_dirs() -> None:
    for d in (RUNS, PAPEL / "tabelas", PAPEL / "figuras"):
        d.mkdir(parents=True, exist_ok=True)


def json_simples(obj):
    """numpy -> tipos JSON, para nao falhar nos dumps."""
    if isinstance(obj, dict):
        return {k: json_simples(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_simples(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        v = float(obj)
        return None if (v != v) else v
    if isinstance(obj, np.ndarray):
        return json_simples(obj.tolist())
    if isinstance(obj, float) and obj != obj:
        return None
    return obj


def escrever_json(obj, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(json_simples(obj), f, ensure_ascii=False, indent=2)


def csv_resultados() -> Path:
    """Esquema da PL08: data, commit, configuracao, metrica de validacao, tempo."""
    return PAPEL / "resultados.csv"


CABECALHO_RESULTADOS = [
    "data",
    "commit",
    "configuracao",
    "estrategia",
    "seed",
    "fracao_rotulos",
    "f1_val",
    "f1_teste",
    "n_rotulos",
    "tempo_s",
]


# Chave que identifica uma corrida. Repetir uma corrida com a mesma chave tem de
# SUBSTITUIR a linha anterior (senao o resultados.csv acumula duplicados e as
# medias do relatorio deixam de ter um sentido unico).
CHAVE_RESULTADO = ("configuracao", "estrategia", "seed")


def _trancar(caminho: Path, espera_max: float = 60.0) -> Path:
    """Fecho de escrita portatil, para as 6 corridas de `al.py` poderem escrever
    no mesmo CSV sem uma apagar a linha da outra."""
    lock = caminho.with_name(caminho.name + ".lock")
    t0 = time.time()
    while True:
        try:
            os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            return lock
        except FileExistsError:
            if time.time() - t0 > espera_max:
                # fecho de uma corrida interrompida: assume-se e segue-se
                try:
                    lock.unlink()
                except OSError:
                    pass
            else:
                time.sleep(0.02)


def registar_resultado(linha: dict, substituir: bool = False) -> None:
    """Acrescenta uma linha ao paper/resultados.csv, criando o cabecalho se preciso.

    Com `substituir=True`, as linhas com a mesma (configuracao, estrategia, seed)
    sao removidas primeiro: correr duas vezes nao duplica resultados.
    """
    f = csv_resultados()
    f.parent.mkdir(parents=True, exist_ok=True)
    lock = _trancar(f)
    try:
        if substituir and f.exists():
            antigo = pd.read_csv(f)
            repetido = pd.Series(True, index=antigo.index)
            for c in CHAVE_RESULTADO:
                if c in antigo.columns and c in linha:
                    repetido &= antigo[c].astype(str) == str(linha[c])
            if repetido.any():
                antigo[~repetido].to_csv(f, index=False)
        df = pd.DataFrame([linha])
        for c in CABECALHO_RESULTADOS:
            if c not in df.columns:
                df[c] = ""
        df = df[CABECALHO_RESULTADOS]
        df.to_csv(f, mode="a", header=not f.exists(), index=False)
    finally:
        try:
            lock.unlink()
        except OSError:
            pass


def commit_atual() -> str:
    import subprocess

    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=RAIZ, stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        return "sem-git"


def thread_count() -> int:
    return max(1, (os.cpu_count() or 4))
