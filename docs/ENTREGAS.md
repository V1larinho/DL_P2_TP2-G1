# ENTREGAS.md — quem entrega o quê, e em que ordem

Este ficheiro existe por uma razão prática: **cinco pessoas a fazer `git push` no mesmo
repositório** dão mau resultado sem uma ordem definida. Aqui está a ordem, a razão de ser da ordem,
e o que cada um tem de correr antes de commitar.

Cada pessoa tem o seu guia em [`entregas/`](entregas/):

| Quem | Papel | Guia | Fica em teu nome |
| --- | --- | --- | --- |
| Fausto Cananga (2025102675) | A1 · Engenheiro de Dados | [A1_fausto.md](entregas/A1_fausto.md) | Dados, divisões, embeddings, redundância |
| Gabriela Cardoso (79295) | A2 · Baseline | [A2_gabriela.md](entregas/A2_gabriela.md) | Teto, L-só, hiperparâmetros congelados |
| Gonçalo Vilarinho (81970) | A3 · Investigador | [A3_goncalo.md](entregas/A3_goncalo.md) | Protocolo, simulador de AL, proposta D1 |
| Pedro Ribeiro (79354) | A4 · Produto | [A4_pedro.md](entregas/A4_pedro.md) | Fila de anotação, app, Tabela 2 |
| Marco Maceda (66694) | A5 · Avaliador | [A5_marco.md](entregas/A5_marco.md) | Avaliação, IC, calibração, Tabelas 1 e 3 |

## 1. A ordem (não é negociável)

```
1  A1  infraestrutura + dados      ← bloqueia todos
2  A2  baseline e teto             ← bloqueia A5 e A3
3  A3  protocolo + simulador AL     ← bloqueia A5
4  A5  avaliação + tabelas          ← bloqueia A4 (Tabela 2 sai do avaliar.py)
5  A4  aplicação + Tabela 2
6  A3  fecho: README, RESUMO, relatório
```

**Porque é que a ordem importa.** Todos escrevem no mesmo `paper/resultados.csv`, e cada linha cita
o `commit` do código que a produziu. Se A3 correr o simulador antes de o código dele estar commitado,
a coluna diz `sem-git` — e a PL08 §P8.7 pede exatamente o contrário: *"uma linha por execução
significativa com configuração, métrica e commit"*. Com a ordem acima, cada linha aponta para código
que existe no repositório.

**Regra de ouro:** nunca dois a mexer no `resultados.csv` ao mesmo tempo. Se tiveres de correr algo
enquanto outro está a commitar, usa um branch e dá *rebase* depois — mas o CSV regenera-se, não se
resolve à mão.

## 2. Preparação comum (faz isto uma vez, todos)

```powershell
git clone https://github.com/<grupo>/<repositorio>.git
cd <repositorio>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Dados.** O CODEBRIM (7,9 GB, não comercial) **não** está no git — está no Drive do grupo ou no
[Zenodo 2620293](https://zenodo.org/records/2620293) (ficheiro `CODEBRIM_classification_dataset.zip`,
md5 `c1612d9674e2e628e72e7f5817c40130`). Descomprime para `data/raw/`:

```bash
md5sum CODEBRIM_classification_dataset.zip          # tem de dar c1612d9674e2e628e72e7f5817c40130
unzip -q CODEBRIM_classification_dataset.zip -d data/raw
```

> **Se o `unzip` falhar ou der "Bad magic number":** usa o `unzip` do Git Bash (não o `python -m
> zipfile`, que rebenta neste ficheiro — os deslocamentos do diretório central são de 32 bits e
> passam dos 4 GiB). No Windows, 7-Zip também serve.

Confirma que os dados estão sãos:

```bash
python src/dados.py --verificar
```

Tens de ver **7 677** recortes, `train` 6 438 · `val` 611 · `test` 628, 52 recortes sem classe
positiva excluídos e **0** grupos em fuga (nenhuma imagem em duas partições). Se os números não
baterem, para tudo e fala com o A1 — não é problema de código, é de dados.

**Características.** `runs/emb_vits14.npy` tem 11,8 MB e não vai para o git (`*.npy`). Ou pedes ao A1,
ou regeneras:

```bash
python src/extrair.py --modelo dinov2_vits14    # 7 677 × 384, ~475 s em CPU, retomável
```

## 3. Convenção das mensagens

`tipo(âmbito): o que muda, na voz imperativa` — em português, sem ponto final.

```
feat(A2): cabeca linear de referencia e baseline L-so
docs(A3): protocolo experimental com H1-H4 e regra de paragem
chore(A1): registo das corridas de AL em resultados.csv
fix(A4): fila nao repete recortes da mesma imagem
```

Tipos usados: `feat`, `fix`, `docs`, `chore`, `test`.

## 4. O que **nunca** se commita

| Fica fora | Porquê |
| --- | --- |
| `data/raw/**` | licença **não comercial**, não redistribuível |
| `*.npy`, `*.pt`, `*.pth` | 11,8 MB dos embeddings e pesos; vai para o Drive |
| `runs/**/*.log` | ruído, reproduzível |
| `.venv/`, `__pycache__/` | ambiente local |
| `.venv` e credenciais | óbvio |

O que **entra** de `runs/`: só os `.json` e `.csv` — são a prova das corridas. O `.gitignore` já está
testado para isto (verificado num repositório descartável: `splits.csv`, `meta.json` e `rondas.csv`
entram; `.npy` e logs ficam fora).

## 5. Antes de cada `git push`

```bash
git status                      # nada de ficheiros que nao conheces
git diff --stat                 # o que vais mesmo commitar
git ls-files | wc -l            # ~50 ficheiros, nunca milhares
du -sh .git                     # < 5 MB; se estiver grande, commitaste dados
git log --oneline -5            # mensagens legiveis, uma por unidade de trabalho
```

Se `du -sh .git` der dezenas de MB, commitaste `data/raw` ou um `.npy`. Corrige **antes** do push.

## 6. Registo de IA (obrigatório, e é individual)

Cada um acrescenta a **sua** linha ao [`AI_LOG.md`](../AI_LOG.md) no seu próprio commit. As colunas
são as do protocolo: data · membro · pedido · proposta da IA · funcionou? · o que estava errado ·
como verificou · ficheiro. A coluna *"como verificou"* é a que vale nota: `exit 0`, *shape*, contagem,
métrica — nunca "pareceu bem".

## 7. Revisão cruzada (PL11)

| Par | Revê | Perguntas que tem de saber responder |
| --- | --- | --- |
| **A2 ↔ A3** | A2 revê `src/al.py`; A3 revê `src/probe.py` e `src/baseline.py` | O `L` é fixo em percentagem do pool; porque não em número absoluto? |
| **A4 ↔ A5** | A4 revê `src/avaliar.py`; A5 revê `src/app.py` | O bootstrap é por imagem ou por recorte, e porque é que isso muda o IC? |
| **A1** | Revê o **registo** (não código): `resultados.csv` e `splits.json` | Todas as linhas têm commit? Os hashes de `L0` batem com os seeds? |

Quem revê deixa um comentário no commit (ou uma issue) com **uma** coisa que não percebeu. Não é
formalidade: é o que a grelha da PL11 valoriza.
