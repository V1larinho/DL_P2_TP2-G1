# A5 — Marco Maceda (66694) · Avaliador

> **Missão:** transformar corridas em **números com intervalos de confiança** e impedir que o grupo
> escreva conclusões que os dados não sustentam. És o último filtro antes do relatório.

## O que só tu decides

1. **Como se faz o bootstrap**: **por imagem**, nunca por recorte (os recortes de uma imagem não são
   independentes — é o erro mais fácil de cometer e o mais difícil de detetar).
2. **Como se reporta um alvo não atingido**: `NaN` é um resultado e aparece na Tabela 1; nunca se
   escreve 0.
3. **A escolha da calibração** (temperature scaling ajustado só na validação).

## Próximas duas semanas

| Quando | Tarefa (ID) | Pronto quando |
| --- | --- | --- |
| 28/10 | Tabela Dice/IoU do guia de segmentação (**P6.5**, com A2) | 3 linhas preenchidas |
| 28/10 | Verificar **Dice = 2·IoU/(1+IoU)** (IoU 0,6 → Dice 0,75) (**P6.6**) | Conta escrita no relatório da aula |
| 28/10 | Respostas às Q1–Q3 da **PL06** (**P6.9**) | Por escrito |
| 28/10 | Tabela conf × iou do guia de deteção (**P7.6**, com A2) | 4 linhas |
| 28/10 | Respostas às Q1–Q3 da **PL07** (**P7.10**) | Por escrito |
| 05/11 | Respostas às Q1–Q3 da **PL08** (**P8.11**) | Por escrito |
| 12/11 | `src/avaliar.py`: curvas, **ALC**, **rótulos para 95%**, bootstrap **por imagem** (**C2.5**) | Testado com dados sintéticos |
| 12/11 | **ECE** por ronda (**C2.9**) | Curva de calibração sai do script |
| 03/12 | IC por bootstrap de imagens **e** por seed; top-10 comentado (**C3.7**, com A4) | Bandas de IC na figura |
| 10/12 | **ECE** ativo vs aleatório por ronda + temperature scaling (**C4.1**) | Tabela 3 |
| 10/12 | **Grad-CAM** nos recortes adquiridos (**C4.2**) | Figura 4 |
| 17/12 | **Corrida única no teste oficial** para todas as condições (**C4.3**) | Curvas finais |
| 17/12 | **Tabela 1** (ALC e rótulos para 95%, com IC), **Tabela 3**, **figura central** (**C4.5**, **C4.7**, **C4.8**) | Geradas por script |
| 17/12 | Métricas novas do drone: **rótulos por ponte** e **quadros por defeito crítico** (**D4**, `docs/DRONE.md`) | No `avaliar.py` |

## Ângulo drone (o que te toca)

O avaliador é quem decide **o que conta como sucesso**. Num cenário de drone, "economizar rótulos" não
chega: a métrica que o cliente entende é **quantos rótulos (e quantos voos) por ponte** até 95% do
teto. Acrescenta-a ao `avaliar.py` — é a linha que faz a ponte entre o trabalho académico e o produto.

## Par de revisão e leituras

- **Revisão cruzada (PL11):** **A5 ↔ A4**. Revês a app e o `enviesamento.py`; ele revê o teu
  `avaliar.py` e as figuras.
- **Leituras:** Protocolo §6 (o que se mede e como) · **Guo et al. 2017** (calibração — o ECE e o
  temperature scaling são teus) · DLwP Cap. 8 · Munjal et al. 2022 (porque é que 3 seeds não é
  capricho).
- **Questões escritas:** PL06 Q1 e Q2 · PL07 Q1 · **Tema C Q3** (Macro-F1 melhor, ECE pior — porquê e
  o que isso faz à app).

## Dependências

Bloqueado por: **A2** (teto), **A3** (listas adquiridas), **A4** (composição por ronda).
Bloqueias: **o relatório** — sem Tabelas 1 e 3 não há P2-D4 nem discussão com IC.
