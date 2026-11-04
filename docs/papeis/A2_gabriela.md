# A2 — Gabriela Cardoso (79295) · Responsável da Baseline

> **Missão:** garantir que existe um **teto honesto** e uma **baseline forte**. Se o teto estiver mal
> treinado, todas as curvas de AL do grupo passam a medir nada.

## O que só tu decides

1. **O que é o teto**: cabeça linear sobre DINOv2 a 100% dos rótulos (o principal) e ResNet-50 afinada
   (a confirmação). Não confundir com a *baseline do projeto* (EfficientNet, PL08) nem com a
   *baseline do AL* (aleatória com o mesmo orçamento) — ver `REVISAO.md` R2.
2. **Os hiperparâmetros congelados**: épocas, `lr`, `weight_decay`, batch, dropout da cabeça. São
   escolhidos **uma vez**, na validação, **com a estratégia aleatória**, e nunca re-selecionados.
3. **Os thresholds por classe** — também na validação, também congelados.

## Próximas duas semanas

| Quando | Tarefa (ID) | Pronto quando |
| --- | --- | --- |
| 28/10 | Guia de segmentação da PL06: notebook Cap. 11.2 (U-Net, poucas épocas) (**P6.4**) | Treino corre e prevê |
| 28/10 | SAM com **ponto** e com **caixa**; tabela Dice/IoU + tempo/imagem (**P6.5**, com A5) | Tabela preenchida, 3 linhas |
| 28/10 | Guia de deteção da PL07: `yolo11n` em `coco8` 5 épocas; imprimir `map50` **e** `map` (**P7.5**) | Valores registados |
| 28/10 | Tabela conf × iou (4 linhas) com deteções, FP visíveis e objetos perdidos (**P7.6**, com A5) | Tabela preenchida |
| 28/10 | Estimativa computacional por fase (**P7.8**, com A3) | Cabe no Colab: sim/não justificado |
| 05/11 | **Baseline do tema C**: CNN pré-treinada (EfficientNet), fine-tuning a 100% dos rótulos (**P8.6**) | Linha no `resultados.csv` com tempo |
| 05/11 | **Teto + L-só** com cabeça linear (**C1.8**) | Macro-F1 do teto com IC de bootstrap |
| 12/11 | Thresholds por classe e hiperparâmetros **congelados** na validação, com a aleatória (**C2.2**) | `runs/thresholds.json` versionado |
| 12/11 | **ResNet-50 afinada** como teto de confirmação (**C2.3**) | Tempo/época medido antes de arrancar |
| 17/11 | ResNet-50 para **aleatória + melhor estratégia** (3 seeds) (**C2.12**) | 6 curvas registadas |
| 03/12 | **Latência no hardware alvo**: ViT-S/14 + cabeça linear (**D3**, `docs/DRONE.md`) | ms/quadro e dispositivo escritos |

## Ângulo drone (o que te toca)

O drone não tem servidor: alguém tem de dizer **se o modelo cabe a bordo**. Medes a latência do par
ViT-S/14 + cabeça linear no hardware disponível (ou num substituto declarado). Se não cumprir, a
decisão de reduzir resolução ou destilar um aluno é tomada **com números na mão**, e é tua.

## Par de revisão e leituras

- **Revisão cruzada (PL11):** revês o código do **A3** (estratégias) e ele revê o teu. O teu trabalho
  a rever por ele: cabeça, thresholds, curvas de baseline.
- **Leituras:** DLwP Cap. 11 (U-Net, SAM) e Cap. 12 (YOLO/RetinaNet) · Oquab et al. 2023 (DINOv2) ·
  **Guo et al. 2017** (calibração — vais precisar para o temperature scaling do A5).
- **Questões escritas:** PL07 Q2 (NMS com `iou` baixo) · PL07 Q3 (um vs dois estágios) ·
  PL08 Q1 (augmentation só no treino) · PL08 Q3 (baseline forte).

## Dependências

Bloqueado por: **A1** (`splits.csv` e embeddings). Bloqueias: **A5** (sem teto não há "rótulos para
95%") e **A3** (as curvas comparam-se contra o teu teto).
