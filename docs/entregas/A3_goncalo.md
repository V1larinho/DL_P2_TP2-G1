# A3 — Gonçalo Vilarinho (81970) · Investigador e **porta-voz**

> **O que fica em teu nome:** o protocolo, o simulador de aquisição, a proposta P2-D1, o pitch.
> **Tempo:** ~50 min, dos quais ~4 min são as 18 corridas em paralelo.
> **Bloqueado por:** A1 e A2. **Bloqueias:** A5 e o seminário.

## 0. O que já está medido

| Estratégia | ALC | Δ ALC vs aleatória | IC 95% da diferença |
| --- | --- | --- | --- |
| **BALD** | **0,8162** | **+0,0218** | [+0,0109; +0,0321] |
| entropia | 0,8113 | +0,0168 | [+0,0067; +0,0269] |
| margem | 0,8107 | +0,0162 | [+0,0064; +0,0267] |
| BADGE | 0,8072 | +0,0128 | [+0,0024; +0,0248] |
| CoreSet | 0,8002 | +0,0057 | [−0,0084; +0,0183] |
| aleatória | 0,7945 | — | — |

Desenho: `L` = 5% do pool (322 rótulos), `K` = 2,5% (161), 14 rondas → **2 576 rótulos** por corrida,
**270 ajustes** de cabeça linear nas 18 corridas.

## 1. Ordem dos trabalhos (importa)

```bash
git pull
```

1. **Fecha o `PROTOCOLO.md` §3** (definições) e §2 (desenho) — é o que a §C1.13 pede.
2. **Só depois** olhes para as tabelas do A5. Já olhaste, e isso está registado: as curvas atuais são
   **exploratórias**. Escreve isso no protocolo, em vez de deixar a ambiguidade.
3. Re-corre as 18 corridas **depois de commitares o código** — assim a coluna `commit` do
   `resultados.csv` aponta para código que existe (§P8.7).

## 2. Re-correr o simulador (com o código já commitado)

```bash
for e in aleatoria entropia margem bald coreset badge; do
  AL_THREADS=3 python src/al.py --estrategias $e &
done
wait
```

Sete segundos por ronda × 14 rondas × 6 estratégias em paralelo ≈ **3–4 min** de relógio (usa 3
threads por processo para não haver 6 processos a disputar os mesmos núcleos).

**Tens de ver**, no fim:

```bash
find runs/al -name meta.json | wc -l        # 18
python -c "
import pandas as pd; r=pd.read_csv('paper/resultados.csv'); a=r[r.configuracao.str.startswith('al/')]
print(len(a), 'linhas'); print(a.groupby('estrategia').commit.first().to_string())"
```

- 18 `meta.json` e 18 `rondas.csv`
- 18 linhas em `resultados.csv`, **todas com commit preenchido** (o `substituir=True` troca as linhas
  antigas `sem-git` em vez de acrescentar duplicados)
- F1 final por estratégia igual ao do quadro da §0. Se **um** valor mudar, para e investiga: o
  determinismo é parte do que estás a vender.

## 3. Commits

```bash
# 1) a proposta e o material que se apresenta
git add docs/P2-D1.md slides/P2-D1_pitch.md docs/DATASETS.md docs/DRONE.md
git commit -m "docs(A3): proposta P2-D1, pitch de cinco diapositivos e comparacao de datasets"

# 2) o protocolo — o documento que tranca o desenho
git add PROTOCOLO.md
git commit -m "docs(A3): protocolo experimental com H1-H4, L, K e regra de paragem"

# 3) o método
git add src/al.py configs/
git commit -m "feat(A3): simulador de aquisicao com seis estrategias e agrupamento de quase-duplicados"

# 4) as corridas (depois do commit 3, para a coluna commit apontar para ele)
git add runs/al/ paper/resultados.csv AI_LOG.md
git commit -m "chore(A3): dezoito corridas de AL (seis estrategias x tres seeds) registadas"
```

O commit 4 leva **só** `.json` e `.csv` de `runs/al/` — os `.npy` (previsões por ronda, 15 ficheiros
por corrida) ficam fora por `.gitignore`, e vão para o Drive do grupo. Se o `git status` te mostrar
`runs/al/*/seed*/P_r00.npy`, é sinal de que o `.gitignore` foi mexido — fala com o A1.

## 4. O detalhe que distingue o teu trabalho (eixo drone, D2)

`src/al.py` tem uma bandeira `--dedup-grupo` que **não foi usada** nas 18 corridas: com ela, a
aquisição nunca escolhe dois recortes da mesma imagem de origem. É a regra que um drone exige — num
vídeo, 30 quadros/s do mesmo defeito são redundância por construção, e o A1 mediu que **21,5% do
pool já é quase-duplicado** (τ = 0,8677).

Se quiseres o resultado que ninguém mais vai ter:

```bash
AL_THREADS=3 python src/al.py --estrategias bald --seeds 0 1 2 --dedup-grupo --saida runs/al_dedup
```

Comparar a ALC com e sem a regra responde a uma pergunta que o enunciado faz e que o benchmark não
responde: **quanto é que a diversidade vale quando a redundância é real?** Se não correres, diz no
`docs/DRONE.md` que a regra está implementada e não avaliada — as duas coisas são aceitáveis, o
silêncio não é.

## 5. Se te perguntarem

**"Porque é que o BALD ganha e o CoreSet perde?"**
O BALD paga a incerteza **epistémica** (desacordo entre passagens de dropout) — escolhe o recorte
onde o modelo ainda não tem opinião formada. O CoreSet escolhe diversidade **no espaço de
características**, e aqui isso é um mau proxy: a diversidade já está garantida pela composição do
dataset (30 pontes, 1 522 imagens), e o `k`-center gasta orçamento em recortes que são outliers
visuais, não em recortes informativos. É a única estratégia cujo IC inclui o zero — e dizê-lo é mais
forte do que forçar um ranking.

**"Como defines margem em multi-rótulo?"**
Média de `|p_c − 0,5|` sobre as classes: quanto mais perto de 0,5 em média, mais indeciso o modelo.
A alternativa (menor margem entre a classe mais e menos provável) não tem sentido num problema em que
um recorte pode ter três defeitos ao mesmo tempo. Está em `PROTOCOLO.md` §3 porque uma definição
inventada à pressa é a forma mais fácil de perder credibilidade na defesa.

**"Os intervalos sobrepõem-se. Como é que concluis que o BALD é melhor?"**
Não concluo por sobreposição de ICs — isso é o erro que o enunciado avisa para não fazer. Concluo
pela **diferença emparelhada** por réplica (mesmas imagens, mesmas seeds reamostradas): a média das
diferenças é +0,0218 e o IC dessa diferença é [+0,0109; +0,0321], que exclui zero. Comparar dois ICs
que se sobrepõem não prova ausência de efeito, e nós não usamos esse argumento em lado nenhum.

**"Três seeds não é pouco?"**
É. Com 3 seeds o IC das seeds é aproximado, e o `src/avaliar.py` diz isso no cabeçalho em vez de o
esconder: o bootstrap é cruzado (imagens × seeds) e as seeds são tratadas como amostra pequena. Mais
seeds alargariam o IC e não mudariam a conclusão qualitativa — mas se alguém pedir, o custo é ~4 min
por seed adicional.

## 6. Revisão cruzada (PL11)

Revês o `src/probe.py` e o `src/baseline.py` do **A2**; ela revê o teu `src/al.py`. Três coisas para
verificares no código dela: os limiares são calculados **na validação** (não no teste), o `weight_decay`
é o que está no JSON, e o teto usa 100% dos rótulos de `train` (6 438, não 6 433).

## 7. O que continua teu

| Item | Quando | Nota |
| --- | --- | --- |
| Pitch ensaiado com cronómetro ≤ 4 min 30 s (**P7.2**) | 28/10 | cronómetro à frente, sem desculpa |
| Falar com o orientador sobre vídeo de drone / dataset de fachadas (**D5**, **C6.2**) | 29/10 | leva a pergunta escrita; a resposta vai para o `README` |
| Ficha-resumo de 1 página no Moodle (**P8.9**) | **15/11** | a PL08 diz 16/11, que é segunda — 15/11 é o seguro |
| Seminário I: 25 min + 5 min (**C2.11**) | **17/11** | ensaio na PL09 |
