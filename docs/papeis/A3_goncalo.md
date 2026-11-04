# A3 — Gonçalo Vilarinho (81970) · Investigador e **porta-voz**

> **Missão dupla:** és o dono do **método** (as estratégias de aquisição) e a **voz do grupo** no
> seminário. Numa sessão de perguntas, qualquer membro pode ser interpelado — mas o teu trabalho é
> não haver perguntas a que ninguém saiba responder.

## O que só tu decides

1. **A definição de margem multi-rótulo** (proposta em `PROTOCOLO.md` §3: média de `|p_c − 0,5|`) —
   sem isto uma das cinco estratégias não existe.
2. **O limiar `τ` do agrupamento de quase-duplicados** (com A1) — é o que impede a aquisição de
   escolher 20 vezes o mesmo defeito.
3. **A estrutura do seminário** e a divisão de quem responde ao quê.

## Próximas duas semanas

| Quando | Tarefa (ID) | Pronto quando |
| --- | --- | --- |
| 28/10 | Pitch de 5 min fechado nos 5 diapositivos e **ensaiado com cronómetro** (**P7.2**) | ≤ 4 min 30 s |
| 28/10 | Cobrir os 5 critérios a 20% da grelha (**P7.3**) | Checklist dos 5, um a um |
| 28/10 | Estimativa computacional com o A2 (**P7.8**) | Números do 210/84 justificados |
| 29/10 | **Falar com o orientador**: vídeo de drone e/ou dataset de fachadas; registar a resposta (**D5**, **C6.2**) | Resposta escrita no `README` |
| 29/10 | Fechar **H1–H4** com o grupo (**C1.12**) | Hipóteses aceites por todos |
| 29/10 | Fixar `L`, `K`, orçamento, regra de paragem (**C1.13**) | Números no `PROTOCOLO.md` |
| 05/11 | **Simulador** com a estratégia aleatória a correr **3 rondas** e registo por ronda (**C1.5**) | `resultados.csv` com 3 linhas × 3 seeds |
| 05/11 | Seminário planeado nos 6 blocos (**P8.8**) | Guião com tempos |
| 15/11 | **Ficha-resumo de 1 página** (prazo do Moodle: a PL08 diz 16/11, que é segunda — trata 15/11 como seguro, R19) (**P8.9**) | Submetida |
| 12/11 | Entropia/margem e **BALD** (dropout na cabeça, `T` passagens) (**C2.1**) | Ranking de BALD **difere** do da entropia |
| 12/11 | **CoreSet** e **BADGE** (**C2.7**) + pedido **IA-4** | `K=|pool|` seleciona tudo; mesmo seed ⇒ mesmo resultado |
| 12/11 | Corridas completas na validação: 5 estratégias × 3 seeds (**C2.8**, com A5) | 15 curvas |
| 12/11 | Ensaio do seminário na PL09 (**C2.10**) | Passa em 25 min |
| **17/11** | **Seminário I** — 25 min + 5 min (**C2.11**) | Apresentado |
| 12/11 | Agrupamento de quase-duplicados na aquisição, com `τ` e contagem de grupos colapsados por ronda (**D2**, `docs/DRONE.md`) | Log por ronda |

## Ângulo drone (o que te toca)

Duas coisas. **D5:** é contigo que o orientador fala sobre vídeo de drone e o dataset de fachadas —
leva a pergunta preparada e traz a resposta por escrito. **D2:** a aquisição por incerteza sobre
vídeo escolhe quase-duplicados; o agrupamento é teu, e é o detalhe que mostra que pensaste no cenário
real e não só no benchmark.

## Par de revisão e leituras

- **Revisão cruzada (PL11):** **A2 ↔ A3**. Revês a cabeça, os thresholds e as curvas de baseline dela;
  ela revê o teu simulador e as estratégias.
- **Leituras (as tuas duas vias):** Settles 2009 (survey) · Sener & Savarese 2018 (CoreSet) ·
  Ash et al. 2020 (BADGE) · Gal et al. 2017 (BALD) · Munjal et al. 2022 (reprodutibilidade).
  Fichas de 1 página em `paper/leituras/`.
- **Questões escritas:** Tema C Q1 (hiperparâmetros por estratégia) · Tema C Q2 (se a aleatória ganhar).

## Dependências

Bloqueado por: **A1** (`splits.csv`, embeddings) e **A2** (cabeça e teto para treinar em cada ronda).
Bloqueias: **A5** (sem listas adquiridas não há curvas) e o seminário de todo o grupo.
