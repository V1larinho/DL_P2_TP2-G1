# PENDENTES.md — tudo o que os documentos da UC exigem

Lista mestra de tarefas extraída **documento a documento** dos materiais da pasta `P2`.
Cada linha tem **dono** (papel A1–A5), **prova/evidência** e **fonte** (secção do documento).

Membros: **A1** Fausto Cananga (2025102675, Eng. de Dados) · **A2** Gabriela Cardoso (79295, Baseline) ·
**A3** Gonçalo Vilarinho (81970, Investigador/**porta-voz**) · **A4** Pedro Ribeiro (79354, Produto) ·
**A5** Marco Maceda (66694, Avaliador).

**Como manter este ficheiro:** sempre que chega um PDF novo, acrescenta-se uma secção
`## <nome do documento>` com as tarefas no formato abaixo e uma linha na tabela §9.
Marcar `[x]` só com a evidência indicada (ficheiro, commit, tabela preenchida, print).

---

## 1. Calendário fixo (das fontes)

| Data | Entregável / evento | Fonte |
| --- | --- | --- |
| 21–22/10 (sem. 6) | PL06 — arranque do P2, guia de segmentação, app v0 | PL06 §2 |
| 25/10 | Aula teórica 7 — deteção (YOLO, RetinaNet, NMS, mAP) | Aula 07 |
| 28/10 (TP1) · **29/10** (TP2) | **P2-D1** — proposta: 2 páginas no Moodle **até ao início da aula** + pitch de 5 min | PL07 §2.1 |
| 03/11 (terça) | **Teste T1** — aulas 1–7 | Aula 07, §6.3 |
| 04–05/11 (sem. 8) | PL08 — `src/dados.py`, baseline, planeamento do seminário | PL08 §2 |
| 11–12/11 (sem. 9) | PL09 — `PROTOCOLO.md` fechado; ensaio do seminário | Tema C §5.2 |
| **15/11 (dom.)** — a PL08 escreve "domingo, 16/11", mas **16/11/2026 é segunda-feira** (ver `docs/REVISAO.md` R19): tratar **15/11** como prazo seguro e confirmar | Ficha-resumo de 1 página (temas A, B, C) no Moodle | PL08 §2.4 |
| **17/11 (terça)** | **P2-D2** — Seminário I (temas A, B, C): 25 min + 5 min de perguntas | PL08 · Tema C §1 |
| 25–26/11 (sem. 11) | PL10/11 — assistente de anotação; revisão cruzada de código | Tema C §5.3 |
| 02–03/12 (sem. 12) | **P2-D3** — protótipo; tag `v1-D3` **antes** da aula | PL07–PL08 "Onde estamos" · Tema C §5.3 |
| 09–10/12 (sem. 13) | PL13 — ECE, temperature scaling, Grad-CAM | Tema C §5.4 |
| 16–17/12 (sem. 14) | **P2-D4** — secções 5, 6 e 9; Tabelas 1–3; figura central | Tema C §5.4 |
| **04/01** | Relatório + repositório + `AI_LOG.md` | Tema C §1 |
| 05/01 (aula T) | **P2-D5** — apresentação final | Tema C §5.5 |
| 07/01 (PL15) | Defesa individual + heteroavaliação coerente com a tabela CRediT | Tema C §5.5 |
| até 09/01 | Reunião de passagem para o artigo | Tema C §5.5 |

> **Semana corrente: 6 → 7.** O próximo entregável é o **P2-D1** (29/10). O `T1` (3/11) cai três dias depois.

## 2. Regras transversais (valem em todos os entregáveis)

- [ ] Repositório **privado**, docentes como colaboradores, nome `DL_P2_<turma>-<grupo>` (PL06 §2.1) — **A1**
- [ ] `AI_LOG.md` atualizado por **todos** os membros a cada interação com IA (Tema C §8) — **todos**
- [ ] Licenças: CODEBRIM **não comercial** (dados fora do git, citação Mundt 2019); Ultralytics **AGPL-3.0** declarada no README se usada; DINOv2 citado (Tema C §2.1; PL07 §2.2; Aula 07 §4.2) — **A1**
- [ ] Nenhum resultado final nasce em `notebooks/` (Tema C §2.3) — **todos**
- [ ] Cada número do relatório tem linha em `paper/resultados.csv` com commit e data (Tema C §7.3) — **A1**
- [ ] Cada figura tem script em `paper/figuras/` que a regenera (Tema C §7.3) — **A5**
- [ ] Hiperparâmetros congelados na validação **com a estratégia aleatória**, nunca re-selecionados por estratégia (Tema C §4, nota) — **A2**
- [ ] O teste oficial só é lido depois do commit do `PROTOCOLO.md` (Tema C §6) — **todos**
- [ ] Acordo de autoria escrito na semana 7 (critérios ICMJE) (Tema C §7.3) — **todos**

## 3. Ordem crítica até 29/10 (o que bloqueia o quê)

```
T1.3 contagens reais ─┬─> T1.4 divisão por imagem confirmada ──> C1.7 splits.json + L0
                      └─> README com números ──> P2-D1 §Dados   (o avaliador valida os dados)
P2-D1 (2 pp.) + pitch de 5 slides ──> submissão Moodle + apresentação 29/10 ──> feedback na PL08
CP3 (estimativa computacional) ──> fecha o §Plano do P2-D1
H1–H4 + L/K/orçamento fixados ──> PROTOCOLO.md ──> só então correr no teste
```

---

## 4. DL_PL06 — Arranque do P2 e guia de segmentação (sem. 6)

- [x] **P6.1** Estrutura do repositório criada (README, AI_LOG, PROTOCOLO, configs, data, src, notebooks, app, paper, requirements.txt) — *feito: esqueleto local em `DL_P2_TP2-G1/`; falta criar no GitHub, adicionar docentes e renomear o grupo* — **A1** · *PL06 §2.1*
- [x] **P6.2** `AI_LOG.md` com a tabela de registo de IA — *feito: [`AI_LOG.md`](AI_LOG.md); cada membro preenche as suas linhas* — **todos** · *PL06 §2.5*
- [x] **P6.3** Tabela 2.1 (7 perguntas) preenchida em grupo — *esboço feito: [`docs/P2-D1.md`](docs/P2-D1.md) §2; validar e corrigir em grupo* — **todos** · *PL06 §2.2*
- [ ] **P6.4** Guia de segmentação: notebook do Cap. 11.2 (U-Net em Oxford-IIIT Pets, **poucas épocas**) — **A2** · *PL06 §2.3*
- [ ] **P6.5** Tabela Dice/IoU preenchida para 3 condições: modelo Cap. 11.2, **SAM com ponto**, **SAM com caixa** (+ tempo por imagem e observações) — **A2, A5** · *PL06 §2.3*
- [ ] **P6.6** Verificar `Dice = 2·IoU/(1+IoU)`; para IoU 0,6 → Dice 0,75; confirmar que SAM com **caixa** dá máscaras mais estáveis que com um ponto — **A5** · *PL06 §2.3*
- [ ] **P6.7** Primeira interface Gradio a funcionar (`gr.Interface` + `gr.Image` + `gr.Label(num_top_classes=3)`) com o modelo do P1 — **A4, A1** · *PL06 §2.4*
- [ ] **P6.8** **Com IA:** pedir um README à IA, comparar com a tabela 2.1, registar *o que a IA inventou* (datasets, métricas, resultados) no `AI_LOG.md` — **A1** · *PL06 §2.5*
- [ ] **P6.9** Responder por escrito às Questões 1–3 da PL06 (Dice↔IoU; pixel accuracy; unidade de agrupamento) — **A5, todos** · *PL06 §3*
- [ ] **P6.10** Fecho da aula (4 itens): repo criado com docentes · tabela 2.1 preenchida · guia executado · app Gradio a funcionar — **todos** · *PL06 "No fim da aula"*
- [ ] **P6.11** Confirmar no Moodle/colleague a **turma** do grupo (a PL06 atribui os temas A, C, E à TP1 e B, D, F à TP2, mas o Protocolo do Tema C indica TP2 — ver `docs/REVISAO.md`, R1) — **A1** · *PL06 §Enquadramento*

## 5. DL_PL07 — Proposta (P2-D1) e guia de deteção (sem. 7)

- [x] **P7.1** Documento de 2 páginas do P2-D1 escrito — *feito: [`docs/P2-D1.md`](docs/P2-D1.md); **falta** validar em grupo, exportar para PDF e submeter no Moodle até ao início da aula* — **A1** · *PL07 §2.1*
- [x] **P7.2** Pitch de 5 min em 5 diapositivos na grelha oficial (Problema · Dados · Métodos · Aplicação · Plano) — *feito: [`slides/P2-D1_pitch.md`](slides/P2-D1_pitch.md); falta converter em diapositivos e ensaiar (7 min de ensaio, cortar para 5)* — **A3** (porta-voz) · *PL07 §2.1*
- [ ] **P7.3** Cobrir explicitamente os **5 critérios de avaliação a 20%** (clareza do problema · adequação de dados e métodos · baseline justificada · mockup da interface · plano e papéis realistas) — **A3** · *PL07 §2.1*
- [ ] **P7.4** Registar o **feedback do docente** no README com a decisão e o responsável de cada ajuste — **A1** · *PL07 "No fim da aula" · PL08 §2.1*
- [ ] **P7.5** Guia de deteção executado: `pip install ultralytics`; `YOLO("yolo11n.pt")`; treino `coco8.yaml` 5 épocas `imgsz=640`; `model.val()` → imprimir `map50` **e** `map` — **A2** · *PL07 §2.2*
- [ ] **P7.6** Tabela conf × iou preenchida (4 linhas: 0,10/0,7 · 0,25/0,7 · 0,50/0,7 · 0,25/0,3) com n.º de deteções, falsos positivos visíveis e objetos perdidos — **A2, A5** · *PL07 §2.2*
- [ ] **P7.7** Declarar **AGPL-3.0** do Ultralytics no README (ou usar RetinaNet do KerasHub, sem essa restrição) — **A1** · *PL07 §2.2 · Aula 07 §4.2*
- [ ] **P7.8** Estimativa computacional: medir tempo de **uma época** num subconjunto e extrapolar; tabela Baseline / Método avançado / Avaliação (seeds, bootstrap) + "cabe no Colab gratuito?" — **A3, A2** · *PL07 §2.3*
- [ ] **P7.9** **Com IA:** script que converte anotações (máscaras/COCO JSON/CSV) para o formato necessário e **verificação desenhando as caixas sobre 5 imagens** — **A1** · *PL07 §2.4*
- [ ] **P7.10** Responder por escrito às Questões 1–3 da PL07 (mAP@0,5 vs 0,5:0,95 com 0,82/0,41; NMS; um vs dois estágios) — **A5, todos** · *PL07 §3*
- [ ] **P7.11** Fecho da aula (4 itens): pitch apresentado e feedback no README · documento submetido · guia de deteção executado · estimativa computacional preenchida — **todos** · *PL07 "No fim da aula"*

## 6. DL_PL08 — Pipeline de dados, baseline e planeamento do seminário (sem. 8)

*(`DL_PL08_..._EN.pdf` é a tradução do mesmo documento — não acrescenta requisitos.)*

- [ ] **P8.1** Tabela "comentário do docente → decisão do grupo → responsável" preenchida com o feedback do P2-D1 — **A1** · *PL08 §2.1*
- [x] **P8.2** `src/dados.py` lê `data/splits.csv` (colunas `path, label, grupo, split`), aplica **augmentation só ao treino** e fixa as seeds (`carregar_splits(csv="data/splits.csv", seed=42)`) — *feito: [`src/dados.py`](src/dados.py)* — **A1** · *PL08 §2.2*
- [x] **P8.3** `verificar(df)` com os **dois asserts** de fuga por grupo + `print` das contagens `split × label` — *feito: `verificar()` em [`src/dados.py`](src/dados.py), 3 asserts (train/val/test entre si)* — **A1** · *PL08 §2.2*
- [x] **P8.4** `python src/dados.py --verificar` imprime as contagens e **não** levanta erro — *feito: 6 438 / 611 / 628 recortes, 1 640 multi-rótulo no treino* — **A1** · *PL08 §2.2*
- [x] **P8.5** Determinismo: duas execuções com a mesma seed produzem o **mesmo primeiro lote** — *feito: `python src/dados.py --determinismo` compara a soma do 1.º lote* — **A1** · *PL08 §2.2*
- [ ] **P8.6** Baseline do **tema C** treinada: CNN pré-treinada (**EfficientNet**) com fine-tuning a **100% dos rótulos** — **A2** · *PL08 §2.3* — **em aberto**: não corrida. O teto em uso é a **cabeça linear sobre DINOv2** (F1 0,830), que é o teto *desta representação*, não a CNN afinada que o PL08 manda comparar. Sem GPU, o fine-tune a 6 438 imagens não cabe no tempo das aulas; fica para quando houver máquina, com o mesmo `resultados.csv`.
- [x] **P8.7** `resultados.csv` com **data, commit, configuração, métrica de validação e tempo de treino** por experiência — *feito: [`paper/resultados.csv`](paper/resultados.csv), 276 linhas com commit 9f89717, métricas por classe, ece e tempos* — **A1, todos** · *PL08 §2.3*
- [x] **P8.8** Apresentação do método planeada nos **6 blocos** (3+5+7+4+3+3 = 25 min) — *feito: [`docs/plano_seminario.md`](docs/plano_seminario.md)* — **A3, todos** · *PL08 §2.4*
- [x] **P8.9** Ficha-resumo de **1 página** para os colegas (temas A/B/C) pronta para o ensaio da semana seguinte — *feito: [`docs/FICHA_RESUMO_SEMINARIO.md`](docs/FICHA_RESUMO_SEMINARIO.md)* — **A3** · *PL08 §2.4*
- [x] **P8.10** **Com IA:** pedir 5 perguntas difíceis sobre o método, responder **sem IA** e confirmar no artigo original; registar onde a IA esteve errada ou vaga — *feito: registo IA-3 no [`AI_LOG.md`](AI_LOG.md)* — **todos** · *PL08 §2.5*
- [x] **P8.11** Responder por escrito às Questões 1–3 da PL08 (augmentation só no treino; registo de commit/configuração; baseline forte) — *feito: [`docs/RESPOSTAS_PL08.md`](docs/RESPOSTAS_PL08.md)* — **A5, todos** · *PL08 §3*
- [ ] **P8.12** Fecho da aula (4 itens): feedback registado · `src/dados.py` com verificação · baseline registada · apresentação planeada — **todos** · *PL08 "No fim da aula"*

## 7. Aula teórica 7 — Deteção: YOLO, RetinaNet, NMS e mAP (25/10)

- [ ] **A7.1** Estudar os 16 diapositivos: dois estágios (R-CNN→Faster/Mask R-CNN, anchors, RPN) · um estágio (grelha, perda, focal loss) · DETR/RT-DETR · NMS · precision/recall/AP/mAP — **todos** · *Aula 07 §§1–6*
- [ ] **A7.2** Resolver o **exercício de NMS** por escrito (A 0,9 / B 0,8 / C 0,7; IoU(A,B)=0,7; IoU(A,C)=0,1; limiar 0,5 → **ficam A e C**) — **A5** · *Aula 07 §5.2*
- [ ] **A7.3** Saber as **três convenções de caixa** (Pascal VOC `[x1,y1,x2,y2]` · COCO `[x,y,w,h]` · YOLO `classe cx cy w h` normalizados) — **A2** · *Aula 07 §1.2*
- [ ] **A7.4** Nota para o tema C: a conversão COCO→YOLO é passo do **tema B**; não a usamos, mas a verificação visual das anotações convertidas é boa prática e cobre a P7.9 — **A1** · *Aula 07 §3.2*
- [ ] **A7.5** Preparar o **T1 de 3/11** (aulas 1–7): convolução, parâmetros, augmentation, transfer learning, métricas e ROC, arquiteturas, Grad-CAM, atenção/ViT, segmentação, deteção — **todos** · *Aula 07 §6.3*

## 8. Protocolo do Tema C (AL 1, CODEBRIM) — fases e tarefas

### Fase 1 — arranque e proposta (sem. 4–7 → 29/10)

- [x] **C1.10** Tabela 2.1 validada e **corrigida** (dataset é classificação de recortes, não deteção; unidade de agrupamento = imagem de origem; métrica = Macro-F1) — *esboço feito: [`docs/P2-D1.md`](docs/P2-D1.md) §2* — **todos** · *Tema C §2.1*
- [x] **C1.1** Descarregar o CODEBRIM (`CODEBRIM_classification_dataset`), registar licença e citação — *feito: **7,9 GB**, md5 `c1612d9674e2e628e72e7f5817c40130` conferido; licença lida (não comercial, sem redistribuição)* — **A1** · *Tema C §5.1*
- [x] **C1.2** Contagens **reais** por classe e partição + verificação de fuga por imagem — *feito: `scripts/contar_codebrim.py` → **7 729 recortes** (6 481/616/632) de **1 524 imagens**, 5 classes + fundo por partição, **1 990 recortes (25,7%) multi-rótulo**, **0 imagens em duas partições**; resultado em `docs/contagens_codebrim.json` e `data/splits.csv`* — **A1** · *Tema C §2.2, §5.1*
- [ ] **C1.2b** Inspeção visual de **5 recortes por classe** — a única parte da tarefa que não é automatizável — **A1, A4** · *Tema C §2.2*
- [x] **C1.3** Extração DINOv2 `ViT-S/14` (embedding **CLS**) de todos os recortes → `.npy` — *feito: 7 677 × 384, normalizados L2, 475 s em CPU; retomável; [`src/extrair.py`](src/extrair.py)* — **A1** · *Tema C §2.2*
- [x] **C1.4** Sanidade do extrator: **k-NN (k=20)** na validação dá Macro-F1 acima do acaso; embeddings **normalizados** — *feito: **0,7000** contra acaso 0,2551 (`python src/avaliar.py --knn 20`, registado no `resultados.csv`); norma média 1,000000* — **A1** · *Tema C §2.2*
- [x] **C1.5** Simulador `al/simular.py` com a estratégia **aleatória** a correr **3 rondas** com a cabeça linear; registo por ronda em `resultados.csv` — *feito e excedido: [`src/al.py`](src/al.py) corre as 14 rondas e as 6 estratégias* — **A3** · *Tema C §2.2, §5.1*
- [x] **C1.6** Curva aleatória **v0** com 3 seeds — *feito: ALC 0,7945 [0,7578; 0,8245]* — **A5** · *Tema C §5.1*
- [x] **C1.7** `splits.json` + `L0/` por seed (**L = 5% estratificado**, 3 seeds) **com hash** — *feito: [`data/splits.json`](data/splits.json) — 322 recortes por seed, 27 positivos de eflorescência, hash por seed* — **A1** · *Tema C §5.1, §6*
- [x] **C1.8** **Teto** (100% dos rótulos) e **L-só** com a cabeça linear — *feito: teto F1 0,8296/0,8306 (3 seeds); L-só 0,7665 na seed 0* — **A2** · *Tema C §5.1*
- [ ] **C1.9** App **v0**: recorte → defeitos previstos — **A1, A4** · *Tema C §5.1*
- [ ] **C1.11** 2 artigos por via + SOTA do orientador, fichas de 1 página em `paper/leituras/` (≈10 fichas) — **cada um na sua via** · *Tema C §2.2, §5.1*
- [x] **C1.12** Hipóteses **H1–H4** escritas e aceites pelo grupo — **A3** · *Tema C §6* — *feito: `PROTOCOLO.md` commitado em 9f89717, versão final*
- [x] **C1.13** Fixar **L, K, orçamento total** (5% · 2,5% · 40% → 14 rondas), **regra de paragem** e **acordo de autoria** (ICMJE) — **todos** · *Tema C §5.1, §6, §7.3* — *feito: `PROTOCOLO.md` commitado em 9f89717, versão final*
- [ ] **C1.14** Estimativa computacional (rondas × estratégias × seeds; ResNet-50 afinada) — **A3** · *Tema C §5.1*

### Fase 2 — desenvolvimento das vias e seminário (sem. 8–10 → 17/11)

- [x] **C2.1** Entropia/margem multi-rótulo e **BALD** (MC Dropout na cabeça) no simulador — *feito: `pontuar()` em [`src/al.py`](src/al.py); BALD usa dropout 0,2 e T=10* — **A3** · *Tema C §5.2*
- [x] **C2.2** Thresholds por classe + hiperparâmetros **congelados** na validação, com a estratégia aleatória — *feito: `limiares_por_classe()` escolhe na validação e grava `lim_r*.npy` por ronda* — **A2** · *Tema C §5.2, §6*
- [ ] **C2.3** ResNet-50 afinada — **teto** — **A2** · *Tema C §5.2*
- [ ] **C2.4** `src/enviesamento.py` — composição do conjunto rotulado por ronda — **A4** · *Tema C §5.2*
- [x] **C2.5** `src/avaliar.py` — curvas, **ALC**, **rótulos para 95% do teto**, bootstrap — *feito: bootstrap **cruzado** (imagens × seeds), B=400, IC na Tabela 1 e diferenças emparelhadas na Tabela 2* — **A5** · *Tema C §5.2*
- [x] **C2.6** `PROTOCOLO.md` escrito e fechado — *feito: [`PROTOCOLO.md`](PROTOCOLO.md) commitado em 9f89717, versão final* — **A1** · *Tema C §5.2, §6*
- [x] **C2.7** **CoreSet** (k-center greedy em embeddings) e **BADGE** (embeddings de gradiente da última camada + k-means++) — *feito: BADGE adaptado a multi-rótulo com pseudo-rótulo, `g=(p-ŷ)⊗h`* — **A3** · *Tema C §5.2, §8*
- [x] **C2.8** Corridas completas na **validação**: 5 estratégias × 3 seeds, cabeça linear — *feito: **6 estratégias × 3 seeds × 15 pontos** = 270 treinos, 18 corridas* — **A3, A5** · *Tema C §5.2*
- [x] **C2.9** **ECE** por ronda — *feito: ECE marginal por classe (10 bins); Tabela 3* — **A5** · *Tema C §5.2*
- [ ] **C2.10** Ensaio do seminário na PL09 — **A3, todos** · *Tema C §5.2*
- [ ] **C2.11** **Seminário I (17/11)**: 25 min + 5 min; apresenta o porta-voz, mas as perguntas podem ir a **qualquer** membro — **A3 apresenta · todos preparam** · *PL08 §Enquadramento*
- [ ] **C2.12** ResNet-50 afinada para **aleatória + melhor estratégia** (3 seeds) — confirmação — **A2** · *Tema C §5.2*
- [ ] **C2.13** F1 das classes raras vs orçamento; **Tabela 2** — **A4** · *Tema C §5.2*
- [x] **C2.14** `resultados.csv` com **uma linha por** (classificador, estratégia, seed, ronda, fração, métrica, valor, data, commit) — *feito: [`paper/resultados.csv`](paper/resultados.csv)* — **A1** · *Tema C §5.2, §7.3*

### Fase 3 — integração e protótipo (sem. 11–12 → 03/12)

- [ ] **C3.1** Assistente de anotação: carregar recortes não rotulados → previsões multi-rótulo com **confiança calibrada** → fila "anotar a seguir" **com a razão** (incerteza, diversidade, classe rara provável) → anotar na app → **re-treinar a cabeça em segundos** → curva atualizada — **A1 + A4** · *Tema C §5.3*
- [ ] **C3.2** Avisos na interface: *"Protótipo experimental… não substitui a inspeção"* e sinalizar recortes **fora da distribuição** — **A4** · *Tema C §5.3*
- [ ] **C3.3** Revisão cruzada de código (PL11): **A2 ↔ A3**, **A4 ↔ A5**; trabalho de **A1** revisto pelo grupo na aplicação — **todos** · *Tema C §3*
- [ ] **C3.4** **Plano B** com vídeo de reserva — **A1** · *Tema C §5.5*
- [ ] **C3.5** Tag **`v1-D3`** no repositório **antes** da aula de 03/12 — **A1** · *Tema C §1*
- [ ] **C3.6** Demo do P2-D3 com **recortes novos** — **todos** · *Tema C §5.3*
- [ ] **C3.7** IC por **bootstrap de imagens** e por **seed**; **10 recortes mais adquiridos** por estratégia e *porquê* — **A5, A4** · *Tema C §5.3*

### Fase 4 — avaliação final e discussão (sem. 13–14 → 17/12)

- [ ] **C4.1** **ECE** do modelo ativo vs aleatório por ronda (**temperature scaling** na validação) — **A5** · *Tema C §5.4*
- [ ] **C4.2** **Grad-CAM/atenção** nos recortes adquiridos — **A5** · *Tema C §5.4*
- [ ] **C4.3** **Corrida única no teste oficial** para todas as condições declaradas (as curvas finais) — **A5** · *Tema C §5.4, §6*
- [ ] **C4.4** Secções **5, 6 e 9** do relatório — **todos** · *Tema C §5.4*
- [ ] **C4.5** **Tabela 1** — ALC e rótulos para 95% por estratégia e classificador, com IC (média ± dp nas 3 seeds) — **A5** · *Tema C §7.2*
- [ ] **C4.6** **Tabela 2** — F1 nas classes raras a 20%; composição do conjunto rotulado (fração por classe) — **A4** · *Tema C §7.2*
- [ ] **C4.7** **Tabela 3** — calibração por estratégia e orçamento, antes/depois do temperature scaling — **A5** · *Tema C §7.2*
- [ ] **C4.8** **Figura central**: curvas de eficiência de rótulos (Macro-F1 vs fração) com bandas de IC + linha do teto — **A5** · *Tema C §7.2*
- [ ] **C4.9** Discussão suportada por IC (PL14) — **todos** · *Tema C §5.4*

### Fase 5 — relatório, defesa e passagem ao artigo (sem. 15 · 04/01 · 09/01)

- [ ] **C5.1** Interrupção de Natal: secções **1–4, 7 e 8** do relatório — **todos** · *Tema C §5.5*
- [ ] **C5.2** Repositório limpo; tag **`v2-final`** — **A1** · *Tema C §5.5*
- [ ] **C5.3** `paper/` completa: `resultados.csv`, `leituras/`, `figuras/`, `tabelas/`, `referencias.bib` (Zotero partilhado), manuscrito — **todos · A4** · *Tema C §5.5, §7.3*
- [ ] **C5.4** Citar CODEBRIM **sempre** que os dados são mencionados; respeitar a licença não comercial — **A1** · *Tema C §7.3*
- [ ] **C5.5** 05/01 apresentação final · 07/01 defesa individual + heteroavaliação coerente com a tabela CRediT — **todos** · *Tema C §5.5*
- [ ] **C5.6** Reunião de passagem até 09/01: quem continua, revista alvo, experiências em falta (SegCODEBRIM, anotação real cronometrada, outro dataset) — **todos** · *Tema C §5.5*

### Fase 6 — decisões que o grupo acrescentou (não vêm dos PDFs)

- [x] **C6.0** Análise de datasets: CODEBRIM vs SegCODEBRIM vs dacl10k vs alternativas só-de-fissura, com factos verificados no paper e no Zenodo — *feito: [`docs/DATASETS.md`](docs/DATASETS.md)* — **A3** · *decisão do grupo*
- [ ] **C6.1** Decidir em grupo se entra a extensão **SegCODEBRIM** (420 máscaras, licença **MIT**, mesmo domínio) até ao P2-D3 — melhor retorno por hora do projeto — **todos** · *decisão do grupo*
- [ ] **C6.2** Pedir ao orientador o **dataset de AL em fachadas** (segundo domínio alinhado com o SOTA do tema; o grupo AL 2 usa o mesmo simulador) — **A3** · *decisão do grupo*
- [ ] **C6.3** Se o segundo domínio avançar, registar a **emenda datada** no `PROTOCOLO.md` (novo dataset, novo protocolo de divisão) antes de correr — **A1** · *decisão do grupo*

### Fase 7 — cenário drone (levantado pelo orientador; ver [`docs/DRONE.md`](docs/DRONE.md))

O cliente deixa de ser o inspetor e passa a ser a **aeronave**: o pool é vídeo, a unidade de
grupamento sobe a *(ponte, voo)*, o modelo tem de correr a bordo e a incerteza serve também para
decidir **onde refotografar**. O problema e a métrica principal não mudam.

- [ ] **D1** Medir a **redundância** do pool (similaridade entre recortes da mesma imagem) e propor o limiar `τ` de quase-duplicados — **A1** · *29/10 → 12/11*
- [ ] **D2** Agrupar quase-duplicados **antes** de cada aquisição e registar quantos grupos colapsam por ronda — **A3** · *12/11*
- [ ] **D3** Medir a **latência** de ViT-S/14 + cabeça linear no hardware alvo (ou substituto declarado) — **A2** · *03/12*
- [ ] **D4** Acrescentar **rótulos por ponte** e **quadros revistos por defeito crítico** ao `avaliar.py` — **A5** · *17/12*
- [ ] **D5** Falar com o orientador sobre **vídeo de drone** e o dataset de fachadas; registar a resposta — **A3** · *29/10*
- [ ] **D6** Se o drone entrar como frente principal, escrever as **emendas** do `PROTOCOLO.md` §8 (`τ`, métricas novas, limitação da divisão por imagem) — **A1** · *antes de correr no teste*

## 9. Verificações de sanidade (falham = resultado inválido)

- [ ] **V1** Para cada seed, **L é idêntico em todas as estratégias** e o teste **nunca** aparece em L nem em U (hash) — **A1** · *Tema C §6*
- [ ] **V2** Com **K ≥ todo o pool**, todas as estratégias convergem para o teto — **A3** · *Tema C §6*
- [ ] **V3** A estratégia **aleatória com cabeça linear reproduz-se** entre execuções com a mesma seed — **A3, A5** · *Tema C §6*
- [ ] **V4** `Dice = 2·IoU/(1+IoU)` verificado numericamente — **A5** · *PL06 §2.3*
- [x] **V5** `python src/dados.py --verificar` corre sem erro e imprime contagens — *testado e confirmado (0 fugas)* — **A1** · *PL08 §2.2*
- [ ] **V6** BADGE com K = |pool| seleciona **tudo**; escolhidos são **diversos** no t-SNE; mesma seed ⇒ mesmo resultado — **A3** · *Tema C §8*

## 10. Questões a responder por escrito (defesas orais e reunião de passagem)

| # | Documento | Tema | Dono |
| --- | --- | --- | --- |
| Q1 | PL06 | Dice = 2·IoU/(1+IoU); IoU 0,6 → Dice? | A5 |
| Q2 | PL06 | Segmentação de pólipos que ocupam 3%: pixel accuracy e Dice do "sempre fundo" | A5 |
| Q3 | PL06 | Unidade de agrupamento do nosso dataset e o que acontece se for ignorada | A1 |
| Q1 | PL07 | mAP@0,5 vs mAP@0,5:0,95 (0,82 vs 0,41) | A5 |
| Q2 | PL07 | O que faz o NMS e o que acontece com limiar `iou` muito baixo | A2 |
| Q3 | PL07 | Quando preferir um detetor de dois estágios a um YOLO | A2 |
| Q1 | PL08 | Porque a augmentation só no treino e nunca antes da divisão | A2 |
| Q2 | PL08 | Porque se registam commit e configuração de cada resultado | A1 |
| Q3 | PL08 | Porque uma baseline forte e não "uma CNN simples" | A2 |
| Q1 | Tema C | Hiperparâmetros afinados **por estratégia** na validação (BADGE "melhor") — o que está errado | A3 |
| Q2 | Tema C | A aleatória iguala/supera a entropia em todas as rondas — o projeto falhou? | A3 |
| Q3 | Tema C | Macro-F1 superior mas ECE 0,12 vs 0,05 no aleatório — porquê e importa para a app? | A5 |

Respostas: `docs/questoes/` (uma ficheiro por aula), discutidas com o docente na aula seguinte.

## 11. Pedidos obrigatórios "Com IA" (registar em `AI_LOG.md`)

- [x] **IA-1** PL06: pedir um README do tema e comparar com a tabela 2.1 (registar invenções) — *registado no [`AI_LOG.md`](AI_LOG.md) em 05/11* — **A1**
- [ ] **IA-2** PL07: converter anotações para o formato necessário + verificar sobre 5 imagens — **A1**
- [x] **IA-3** PL08: 5 perguntas difíceis sobre o método; responder sem IA e confirmar no artigo — *registado no [`AI_LOG.md`](AI_LOG.md) em 05/11* — **todos**
- [ ] **IA-4** Tema C, semana 8: *"Implementa o BADGE (embeddings de gradiente da última camada + k-means++) para um classificador multi-rótulo."* Verificar K=|pool|, diversidade no t-SNE e repetibilidade — **A3**
- [ ] **IA-5** Tema C, semana 9: *"Identifica fugas de dados, métricas inadequadas e comparações injustas neste PROTOCOLO.md."* Decidir crítica a crítica — **A1**
- [ ] **IA-6** Tema C, semana 14: *"Marca cada frase desta discussão como suportada ou não pelos números da tabela."* Reescrever as não suportadas — **todos**

## 12. Riscos e decisões pendentes

| # | Questão | Impacto | Dono | Ver |
| --- | --- | --- | --- | --- |
| R1 | Turma: PL06 atribui o tema C à TP1, o protocolo do tema C diz TP2 | D1 é 28/10 ou 29/10 | A1 | `docs/REVISAO.md` R1 |
| R2 | Baseline do tema C: PL08 diz **EfficientNet**; o protocolo diz **ResNet-50** para o teto | quem treina o quê e o que é o "teto" | A2 | `docs/REVISAO.md` R2 |
| R3 | Nº de estratégias: §2.1 diz "4", §7.2 lista **5** | a estimativa computacional e a Tabela 1 | A3 | `docs/REVISAO.md` R3 |
| R4 | Estratificação de **L** em multi-rótulo (regra não definida) | H2 (classes raras) e reprodutibilidade | A1 | `docs/REVISAO.md` R4 |
| R5 | "Margem" multi-rótulo não definida no pseudo-código | uma das estratégias do seminário | A3 | `docs/REVISAO.md` R5 |
| R6 | `np.trapz` está descontinuado no NumPy ≥ 2.0 | o ALC na Tabela 1 | A5 | `docs/REVISAO.md` R6 |
| R7 | BALD exige dropout **na cabeça** e T passagens com seed própria | reprodutibilidade (V3) | A3 | `docs/REVISAO.md` R7 |
| R8 | Número real do grupo no nome do repositório | submissão e tags | A1 | `docs/REVISAO.md` R8 |
| R9 | A classe mais **rara** do CODEBRIM é a **eflorescência (833)**, não a armadura exposta (1 507) nem a corrosão (1 559): o protocolo confunde raridade com criticidade | H2 e a Tabela 2 | A3 | `docs/REVISAO.md` R20 |
| R10 | O teste oficial é **balanceado por desenho** (150/classe) e a divisão é **por imagem, não por ponte** (30 pontes) | conclusões sobre classes raras e sobre “pontes novas” | A5 | `docs/REVISAO.md` R21, R22 |

## 13. Documentos recebidos (registo)

| # | Ficheiro | Data | O que acrescenta | Onde ficou mapeado |
| --- | --- | --- | --- | --- |
| 1 | `C3_DL_P2_TemaC_AL1_CODEBRIM_Defeitos_Betao.pdf` (11 pp.) | 27/10 | Protocolo do tema, papéis, protocolo experimental, análise para artigo, 3 questões | §8, §9, §10, §11, `PROTOCOLO.md` |
| 2 | `DL_PL06_P2_Arranque_e_guia_segmentacao.pdf` (4 pp.) | 27/10 | Estrutura do repo, tabela 2.1, guia de segmentação, app v0 | §4 |
| 3 | `DL_PL07_P2_Proposta_D1_e_guia_detecao.pdf` (4 pp.) | 27/10 | P2-D1, grelha de avaliação, guia de deteção, estimativa computacional | §5 |
| 4 | `DL_PL08_P2_Pipeline_baseline_e_planeamento_seminario.pdf` (3 pp.) | 27/10 | `src/dados.py`, baseline por tema, 6 blocos do seminário | §6 |
| 5 | `Aula_07_Detecao_Objetos_YOLO_RetinaNet_NMS_e_mAP.pdf` (16 diap.) | 27/10 | Teórica de deteção; **data do T1 (3/11)**; AGPL do Ultralytics | §7 |
| 6 | `DL_PL08_..._EN.pdf` (3 pp.) | 27/10 | Tradução da PL08 — **sem requisitos novos** | §6 (nota) |

## 14. Progresso

Contagens geradas por `grep` sobre este ficheiro, para não haver números à mão:
ver [`docs/RESUMO.md`](docs/RESUMO.md) §3.
