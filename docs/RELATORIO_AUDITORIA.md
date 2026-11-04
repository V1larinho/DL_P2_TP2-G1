# Relatório de Auditoria de Conformidade e Qualidade (Agente 4)
**Data da Auditoria:** 04/11/2026  
**Auditor:** Agente 4 (Auditor Chefe de Conformidade e Qualidade)  
**Repositório Auditado:** `DL_P2_TP2-G1` (Tema C: Active Learning 1 — CODEBRIM)  
**Marco de Referência:** Aula PL08 (05/11/2026) e planeamento do Seminário I (17/11/2026)

---

## 1. Veredicto Executivo

| Domínio de Auditoria | Classificação | Resumo |
|---|:---:|---|
| **Pipeline de Dados (`src/dados.py`)** | 🟢 **CONFORME** | Sem fugas (3 asserções), determinismo verificado, contagens exatas. |
| **Registo de Resultados (`paper/resultados.csv`)** | 🟢 **CONFORME** | 276 linhas íntegras com commit `9f897179`, 6 estratégias × 3 seeds. |
| **Respostas Escritas PL08 (`docs/RESPOSTAS_PL08.md`)** | 🟢 **CONFORME** | Respostas às 3 questões técnicas fechadas, precisas e em UTF-8. |
| **Plano do Seminário I (`docs/plano_seminario.md`)** | 🟢 **CONFORME** | Estrutura de 25 min nos 6 blocos regulamentares + perguntas antecipadas. |
| **Ficha-Resumo 1 p. (`docs/FICHA_RESUMO_SEMINARIO.md`)** | 🟢 **CONFORME** | Texto condensado pronto para entrega no Moodle (até 15/11). |
| **Feedback P2-D1 (`docs/FEEDBACK_P2D1.md`)** | 🟡 **A FAZER NA AULA** | Grelha estruturada pronta para preenchimento em aula com o docente. |
| **Acesso dos Docentes ao GitHub** | 🟡 **A FAZER NA AULA** | Convite aos docentes como colaboradores no repositório GitHub privado. |
| **Registo IA-4 (BADGE)** | 🟡 **A FAZER NA AULA** | Formalizar no `AI_LOG.md` o teste e sanidade do prompt IA-4. |
| **Baseline EfficientNet afinada (GPU)** | 🔴 **PENDENTE** | Script pronto em `src/baseline_efficientnet.py`; aguarda acesso a GPU. |
| **Seminário I (Ensaio e Apresentação)** | 🔴 **PENDENTE** | Ensaio na PL09 (11–12/11); apresentação oficial a 17/11. |

---

## 2. Auditoria Detalhada por Ponto de Controlo

### 2.1 Requisitos da Aula PL08 (05/11/2026)

#### A. Pipeline de Dados (`src/dados.py`) — Dono: A1 (Fausto)
- **Verificação de Fuga:** O método `verificar(df)` valida a disjunção estrita dos grupos (imagens de origem) entre as três partições:
  $$\text{train} \cap \text{test} = \emptyset, \quad \text{val} \cap \text{test} = \emptyset, \quad \text{train} \cap \text{val} = \emptyset$$
- **Execução Real (`python src/dados.py --verificar`):**
  - **Recortes:** 7 677 utilizáveis (6 438 treino / 611 validação / 628 teste); 0 excluídos com vetor a zero.
  - **Imagens de origem:** 1 249 treino / 138 validação / 135 teste (0 sobreposições).
  - **Multi-rótulo:** 1 640 recortes no treino (25,5%), 183 na validação, 167 no teste.
  - **Contagens por classe:** Fissura (2 208 tr / 149 val / 150 te), Fundo (2 185 / 150 / 150), Delaminação (1 608 / 140 / 150), Corrosão (1 263 / 146 / 150), Armadura Exposta (1 215 / 142 / 150), Eflorescência (543 / 141 / 149 — a mais escassa no treino).
- **Determinismo (`python src/dados.py --determinismo`):**
  - Executadas 2 extrações consecutivas do 1.º lote de treino com a mesma semente (`seed=42`).
  - Soma dos tensores e rótulos estritamente idêntica: `(806233.625, 25.0, (16, 6))`.
  - Augmentation ativada exclusivamente em `Recortes(treino=True)`; validação e teste determinísticos (Resize + CenterCrop).
- **Estado:** 🟢 **CONFORME / CONCLUÍDO**.

#### B. Registo de Experiências (`paper/resultados.csv`) — Dono: A1 / A5
- **Integridade da Tabela:**
  - Total de registos: **276 linhas**, todas com carimbo temporal (`2026-10-27`) e identificador de commit (`9f897179`).
  - 270 linhas correspondem às 6 estratégias de Active Learning (`aleatoria`, `bald`, `badge`, `coreset`, `entropia`, `margem`) ao longo de 3 sementes (0, 1, 2) e 15 pontos de amostragem (rondas 0 a 14, fração 0,05 a 0,40).
  - 6 linhas complementares devidamente etiquetadas: extração DINOv2 (475,1 s), sanidade k-NN (k=20, Macro-F1 0,7000 na validação), teto a 100% dos rótulos (Macro-F1 0,8296 a 0,8327 no teste) e baseline L-só (5%, Macro-F1 0,7665).
  - Todas as rondas de AL incluem `f1_val`, `f1_teste`, `ece`, `segundos`, `hash_rotulado` e o F1 individual para cada uma das 6 classes.
- **Estado:** 🟢 **CONFORME / CONCLUÍDO**.

#### C. Feedback do P2-D1 (`docs/FEEDBACK_P2D1.md`) — Dono: A1 (Fausto)
- O ficheiro foi desenhado com o template regulamentar: `# | Comentário do docente | Decisão do grupo | Responsável | Estado`.
- Regista a distribuição formal de papéis (A1 a A5).
- **Ação:** Deve ser levado aberto para a aula de 05/11 e preenchido em tempo real com as notas do docente sobre o P2-D1.
- **Estado:** 🟡 **A FAZER NA AULA DE AMANHÃ (05/11)**.

#### D. Plano do Seminário I (`docs/plano_seminario.md`) — Dono: A3 (Gonçalo)
- Estruturado em conformidade estrita com os 6 blocos da PL08 §2.4 (total de 25 min + 5 min discussão):
  1. Bloco 1 (3 min): Problema e motivação (A3).
  2. Bloco 2 (5 min): Dataset e métricas (A1 suporta).
  3. Bloco 3 (7 min): Método e representação congelada (A3 apresenta; A2/A5 prontos).
  4. Bloco 4 (4 min): Resultados e refutação/confirmação de hipóteses H1–H4 (A5 suporta).
  5. Bloco 5 (3 min): Aplicação Gradio e mitigação de ancoragem (A4 suporta).
  6. Bloco 6 (3 min): Conclusão e lições aprendidas (A3).
- Contém 5 questões difíceis preparadas para ensaio do grupo.
- Complementado pelo resumo de 1 página em `docs/FICHA_RESUMO_SEMINARIO.md`.
- **Estado:** 🟢 **CONFORME / CONCLUÍDO**.

#### E. Respostas Escritas da PL08 (`docs/RESPOSTAS_PL08.md`) — Dono: A5 / A2
- O ficheiro responde com rigor conceitual e clareza às 3 questões do §3 da PL08:
  - **Q1 (Augmentation):** Proibição de augmentation antes da partição para evitar fuga de dados e métricas inflacionadas; confinamento estrito ao treino.
  - **Q2 (Rastreabilidade):** Papel do hash de commit e da configuração para auditoria científica e garantia de reprodutibilidade exata.
  - **Q3 (Baseline Forte):** Rejeição de baselines débeis (ex: CNN treinada de raiz) que criam falsas impressões de avanço; adoção de amostragem aleatória com igual orçamento e teto a 100% dos rótulos.
- O ficheiro foi convertido para codificação padrão UTF-8 e o título foi corrigido.
- **Estado:** 🟢 **CONFORME / CONCLUÍDO**.

---

### 2.2 Auditoria às Diretrizes de IA (`AI_LOG.md`)

| Diretriz | Semana | Descrição e Objetivo | Estado | Notas do Auditor |
|---|:---:|---|:---:|---|
| **IA-1** | 6 | Pedir um README para o projeto CODEBRIM e documentar as alucinações da IA | 🟢 **CONCLUÍDO** | Registado em 05/11; erros da IA identificados (7 788 imagens, ResNet50, métrica mAP incompatível). |
| **IA-2** | 7 | Script de conversão de anotações COCO/máscaras e validação sobre 5 imagens | 🔴 **PENDENTE** | Opcional no Tema C (recortes), mas relevante para eventual módulo de segmentação (SegCODEBRIM). |
| **IA-3** | 8 | 5 perguntas difíceis sobre AL com modelos fundacionais congelados | 🟢 **CONCLUÍDO** | Registado em 05/11; respostas analisadas criticamente face a Guo 2017, Ash 2020 e Sener 2018. |
| **IA-4** | 8 | Implementação de BADGE multi-rótulo com IA e teste de sanidade ($K=\|pool\|$, t-SNE) | 🟡 **A FAZER (PL08)** | O algoritmo já está codificado em `src/al.py`. Falta formalizar a experiência do prompt e os testes no `AI_LOG.md`. |
| **IA-5** | 9 | Auditoria com IA a fugas de dados e comparações injustas no `PROTOCOLO.md` | 🔴 **PENDENTE (Sem. 9)** | Programado para 11–12/11/2026. |
| **IA-6** | 14 | Verificação de suporte factual entre texto e tabelas no relatório final | 🔴 **PENDENTE (Sem. 14)** | Programado para 16–17/12/2026. |

---

### 2.3 Auditoria ao Repositório Git

- **Branch e Sincronização:** `main` está perfeitamente sincronizado com `origin/main` (`https://github.com/V1larinho/DL_P2_TP2-G1.git`).
- **Histórico de Commits:** Respeita o padrão convencional (`feat:`, `chore(A3):`, `docs(A3):`).
- **Ação Obrigatória da UC:** Garantir que o repositório é privado e convidar os docentes como colaboradores antes do fecho da aula de 05/11 (PL06 §2.1 e PL08 §Fim da aula).

---

### 2.4 Matriz de Pendentes e Riscos (`PENDENTES.md`)

- **Checklist Atualizada:** Foram sincronizadas as caixas de verificação que já estavam implementadas no código mas mantinham estado desatualizado no documento (`P8.7`, `P8.8`, `P8.9`, `P8.10`, `P8.11`, `C2.14`, `V5`, `IA-1`, `IA-3`).
- **Pendência Técnica Crítica — Baseline EfficientNet (P8.6 / C2.3):**
  - O guião da PL08 prevê uma baseline afinada de CNN (EfficientNet-B0) a 100% dos dados.
  - O código de suporte está pronto em `src/baseline_efficientnet.py`.
  - A máquina local não dispõe de GPU CUDA (`torch.cuda.is_available() == False`). O fine-tuning completo exigiria dezenas de horas em CPU.
  - **Decisão Técnica de Auditoria:** Manter a cabeça linear sobre DINOv2 (Macro-F1 0,8306) como teto representacional exploratório. A corrida do `baseline_efficientnet.py` é classificada como pendente para execução em GPU (Google Colab ou laboratório).

---

## 3. Checklist Operacional para a Aula de 05/11/2026 (PL08)

1. [ ] **Verificação ao Vivo com o Docente:**
   - Executar no terminal diante do docente:
     ```bash
     python src/dados.py --verificar --determinismo
     ```
   - Demonstrar a disjunção total dos grupos (0 fugas) e a repetibilidade do 1.º lote.
2. [ ] **Entrega das Respostas Escritas:**
   - Ter disponível `docs/RESPOSTAS_PL08.md` para discussão ou submissão das 3 questões da PL08.
3. [ ] **Registo do Feedback P2-D1:**
   - Preencher a tabela em `docs/FEEDBACK_P2D1.md` com os comentários do docente e respetivas decisões/responsáveis.
4. [ ] **Convite aos Docentes no GitHub:**
   - Adicionar os utilizadores GitHub dos docentes como colaboradores do repositório privado.
5. [ ] **Ensaio do Seminário (Alinhamento Interno):**
   - Rever com os 5 membros a grelha de 6 blocos em `docs/plano_seminario.md` e a ficha de 1 página em `docs/FICHA_RESUMO_SEMINARIO.md`.

---
*Relatório emitido e assinado eletronicamente pelo Agente 4 (Auditor Chefe).*
