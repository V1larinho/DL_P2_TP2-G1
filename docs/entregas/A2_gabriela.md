# A2 — Gabriela Cardoso (79295) · Responsável da Baseline

> **O que fica em teu nome:** o teto, o L-só e os hiperparâmetros que ninguém volta a escolher.
> **Tempo:** ~40 min (a maior parte é o computador a treinar 6 cabeças lineares).
> **Bloqueada por:** A1 (divisões e embeddings commitados). **Bloqueias:** A3 e A5.

## 0. O ponto de partida

| Número | Valor | O que é |
| --- | --- | --- |
| Teto (100% = 6 438 rótulos) | **0,8306** — seeds 0,8296 / 1,8296 / 2,8327 | capacidade de referência |
| L-só (5% = 322 rótulos) | **0,7665** | o que se consegue com o orçamento inicial do AL |
| Hiperparâmetros | guardados em `runs/baseline/teto_s*.json` | congelados, na validação, com a estratégia **aleatória** |

**Nunca confundir três coisas** (é a pergunta 1 da §5):

1. **Baseline do projeto** (PL08) = EfficientNet afinada. É a comparação da disciplina — **em aberto**, ver §4.
2. **Teto** = cabeça linear sobre DINOv2 congelado a 100% dos rótulos. É o denominador dos
   "rótulos para 95%" do A5.
3. **Baseline do AL** = estratégia aleatória com o **mesmo orçamento**. É contra esta que o A3 compara.

## 1. Correr o teto e o L-só (depois de o A1 ter feito o push)

```bash
git pull
for s in 0 1 2; do python src/baseline.py --experiencia ambos --seed $s; done
```

Cada seed faz dois ajustes (teto e L-só), ~20 s cada. **Tens de ver**, no fim:

```bash
python - <<'EOF'
import pandas as pd
r = pd.read_csv("paper/resultados.csv")
print(r[r.estrategia.isin(["teto", "l_so"])].to_string(index=False))
EOF
```

- `teto` × 3 seeds, F1 de teste **0,8296 · 0,8296 · 0,8327** (média 0,8306)
- `l_so` × 3 seeds, F1 de teste **0,7665** (era só a seed 0; agora são três)
- coluna `commit` **preenchida** — se disser `sem-git`, o A1 ainda não fez o push do código

> Se algum valor mudar face aos de cima, **para**. Significa que algo deixou de ser determinístico
> (threads do torch, versão de biblioteca). É um achado, não um detalhe: avisa o grupo antes de commitar.

## 2. Commits

```bash
git add src/probe.py src/baseline.py runs/baseline/*.json
git commit -m "feat(A2): cabeca linear de referencia (teto) e baseline L-so"

git add paper/resultados.csv AI_LOG.md
git commit -m "chore(A2): registo das corridas do teto e do L-so com o commit de origem"
```

Dois commits de propósito: o primeiro é **código**, o segundo são **resultados que citam esse
código**. É exatamente o que a PL08 §P8.7 pede (configuração + métrica + commit) e é o que te
permite responder "de que versão do código saiu este número?" sem hesitar.

*Não entram no git:* `runs/baseline/limiares_*.npy` (pesos/binários, `*.npy` está ignorado). Os
limiares por classe estão **dentro** dos JSON — verifica que estão lá antes de commitar:

```bash
python -c "import json;print(json.load(open('runs/baseline/teto_s0.json'))['limiares'])"
```

## 3. O que congelaste (e porque não podes voltar atrás)

| Decisão | Valor | Onde foi escolhida |
| --- | --- | --- |
| Otimizador / lr | SGD 0,9 · lr 1e-3 · weight decay 0 | validação, estratégia **aleatória** |
| Épocas / batch | as de `runs/baseline/*.json` | idem |
| Limiar por classe | `limiares` no JSON | idem |

A regra que te protege: **os hiperparâmetros escolhem-se uma vez, na validação, com a estratégia
aleatória**. Se os escolheres com o BALD e depois comparares estratégias, estás a dar ao BALD uma
vantagem que a comparação não mede. Isso é o erro clássico do tema e o enunciado pergunta por ele
(Tema C, Q1).

## 4. O item que continua em aberto e é teu (P8.6)

**Baseline EfficientNet afinda a 100% dos rótulos** — não está feita. Sem GPU não cabe no tempo, e é
por isso que o teto que usamos é o da representação congelada. Tens duas saídas honestas:

**(a) Correr** (Colab T4, ~25 min):

```bash
pip install torchvision
python - <<'EOF'
# esqueleto: efficientnet_b0, 224 px, AdamW 1e-4, 10 epocas, batch 32
# registar no resultados.csv com configuracao="efficientnet_b0/finetune"
EOF
```

**(b) Declarar a lacuna** no `README` §9 e no relatório: *"a baseline EfficientNet do PL08 não foi
corrida por falta de GPU; o denominador usado é a cabeça linear sobre DINOv2, que é um teto mais
favorável e portanto **conservador** para as conclusões do AL"*.

Nenhuma das duas é má. O que é mau é a tabela do relatório dizer "baseline" e não se saber qual.
Escolhe, escreve, e resolve.

## 5. Se te perguntarem

**"Porque é que o teto é uma cabeça linear e não uma CNN afinada?"**
Porque o teto tem de ser **o melhor que se consegue com os rótulos todos, mantendo tudo o resto
igual** às curvas de AL. As curvas do A3 treinam cabeças lineares sobre as mesmas características
congeladas; se o teto fosse uma CNN afinada, a diferença entre teto e curva mediria *duas* coisas ao
mesmo tempo (arquitetura e quantidade de rótulos) e o "rótulos para 95%" perdia sentido.

**"0,77 com 5% dos rótulos e 0,83 com 100% — vale a pena o AL?"**
É a pergunta certa, e a resposta é a que os dados dão: o intervalo é estreito (0,06), por isso o
ganho de uma estratégia tem de ser medido **emparelhado com a aleatória no mesmo teste**, não contra
o teto. O A3 mede +0,022 de ALC para o BALD, com IC a excluir zero. Isso é pequeno — e é real.

**"Como é que sabes que não estás a fazer seleção de hiperparâmetros no teste?"**
Porque os hiperparâmetros e os limiares são escolhidos na validação, com a aleatória, e ficam num
JSON com data. O teste é tocado uma vez, no fim, pelo A5. Se alguém quiser mudar um limiar depois de
ver o teste, tem de escrever no `AI_LOG.md` que o fez.

## 6. Fora deste repositório (mas é teu, e conta para a nota das aulas)

| Entrega | Onde vai | Pronto quando |
| --- | --- | --- |
| Guia de segmentação PL06 (U-Net, poucas épocas) **P6.4** | `notebooks/` | treina e prevê |
| SAM com ponto e com caixa + tabela Dice/IoU **P6.5** | `notebooks/` | 3 linhas com tempo/imagem |
| Guia de deteção PL07 (`yolo11n` em `coco8`, 5 épocas) **P7.5** | `notebooks/` | `map50` **e** `map` impressos |
| Tabela conf × iou com FP visíveis **P7.6** | `notebooks/` | 4 linhas |
| Latência no hardware alvo: ViT-S/14 + cabeça linear **D3** | `docs/DRONE.md` §latência | ms/quadro e dispositivo escritos |

Se o Ultralytics entrar no repositório, **declara a AGPL-3.0** no `README` §8 — é a única licença
do projeto que contamina.

## 7. Revisão cruzada (PL11)

Revês o **A3** (`src/al.py`) e ele revê o teu `src/probe.py` e `src/baseline.py`. Olha para três
coisas concretas no código dele:

1. Os limiares por classe acompanham a cabeça de cada ronda (não ficam presos ao teto).
2. O `assert` que impede o teste de entrar no conjunto rotulado está lá.
3. O `K` é fixo em número absoluto (161), não em percentagem do que resta — senão as rondas finais
   adquirem cada vez menos.

Deixa um comentário com **uma** coisa que não percebeste. É isso que a grelha valoriza.
