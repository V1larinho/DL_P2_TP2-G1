# RESUMO.md — o que ficou feito

**Em três linhas.** Os 6 documentos da pasta `P2` (41 páginas) estão transformados numa lista de 121
tarefas com dono e secção de origem; o repositório tem os documentos, os cinco planos de trabalho e o
**código a correr** — dados verificados, embeddings DINOv2, teto, 18 corridas de aprendizagem ativa e
avaliação com intervalos de confiança. O que falta está listado, com nome e não como "em breve".

## 1. O que existe agora

```
P2/DL_P2_TP2-G1/
├── README.md                     ← problema, dados medidos, licença NC, papéis, resultados, estado
├── PENDENTES.md                  ← 121 tarefas (27 feitas · 94 a fazer), com dono e fonte
├── PROTOCOLO.md                  ← protocolo experimental (por fechar e versionar na PL09)
├── AI_LOG.md                     ← registo de IA + os 6 pedidos obrigatórios e as fontes confirmadas
├── requirements.txt · configs/al_vits14_aleatoria_s0.yaml
├── src/
│   ├── comum.py                  ← rótulos, caminhos, métricas, registo em resultados.csv
│   ├── dados.py                  ← PL08 §2.2: splits, verificar(), determinismo, L estratificado
│   ├── extrair.py                ← DINOv2 ViT-S/14, CLS normalizado, retomável
│   ├── probe.py                  ← cabeça linear, BCE, limiares por classe, temperatura
│   ├── baseline.py               ← teto (100%) e L-só (5%)
│   ├── al.py                     ← 6 estratégias × rondas (aleatória, entropia, margem, BALD, CoreSet, BADGE)
│   ├── avaliar.py                ← ALC, rótulos-para-95%, bootstrap por imagem × seed, ECE
│   ├── redundancia.py            ← quase-duplicados: τ medido (eixo drone)
│   └── app.py                    ← assistente de anotação (Gradio), previsão oculta
├── docs/P2-D1.md                 ← a proposta de 2 páginas (+ tabela 2.1, hipóteses, mockup)
├── docs/DATASETS.md              ← CODEBRIM vs alternativas + recomendação em 3 níveis
├── docs/DRONE.md                 ← cenário de drone: o que muda, τ medido, emendas
├── docs/RESULTADOS.md            ← **os números reais, por pessoa, e o que não está feito**
├── docs/papeis/A1…A5.md          ← um plano de trabalho por membro (tarefas, prazos, dependências)
├── docs/contagens_codebrim.json  ← contagens medidas do dataset
├── docs/REVISAO.md               ← 25 achados + 4 falhas próprias, com correção
├── scripts/contar_codebrim.py    ← contagem + verificação de fuga por imagem, direto do zip
├── data/splits.csv               ← 7 677 recortes, rótulo multi-rótulo, grupo = imagem
├── data/splits.json              ← hashes e listas L0 por seed
├── paper/resultados.csv          ← registo por experiência (data, config, F1 val, tempo)
├── paper/tabelas/                ← Tabelas 1, 2 (por classe e diferenças), 3 (calibração)
├── paper/figuras/curva_al.png    ← a figura central, com banda ± dp por seed
├── runs/                         ← embeddings, 18 corridas, redundância (não versionado)
├── slides/P2-D1_pitch.md         ← 5 diapositivos + notas de tempo
└── configs/ · paper/leituras/    ← um YAML por corrida · fichas de leitura (por preencher)
```

## 2. Papéis (A1–A5 do protocolo, pelo cargo de cada um)

| Papel | Membro | Cargo | Entrega que lidera |
| --- | --- | --- | --- |
| **A1** Dados, protocolo e integração | Fausto Cananga (2025102675) | Engenheiro de Dados | D1 · D3 (interface) · D5 |
| **A2** Classificadores e teto | Gabriela Cardoso (79295) | Responsável da Baseline | D3 (comparação) · D4 (Tabela 1) |
| **A3** Estratégias de aquisição (**porta-voz**) | Gonçalo Vilarinho (81970) | Investigador | D2 · D3 (método avançado) |
| **A4** Classes raras e enviesamento | Pedro Ribeiro (79354) | Responsável de Produto | D3 (aplicação) · D4 (Tabela 2) |
| **A5** Avaliação, calibração e XAI | Marco Maceda (66694) | Avaliador | D4 (§5) · D5 |

## 3. Números (medidos, não estimados)

| Métrica | Valor |
| --- | --- |
| Documentos lidos | 6 (41 páginas) |
| Tarefas na lista mestra | **121** — 27 feitas, **94 por fazer** |
| Recortes utilizáveis (medidos) | **7 677** de 1 522 imagens de origem · 52 sem rótulo excluídos · 0 em fuga |
| Embeddings extraídos | 7 677 × 384 (DINOv2 ViT-S/14), 475 s em CPU |
| Sanidade do extrator | k-NN (k=20) **0,7000** na validação (acaso 0,2551) |
| Teto / L-só (Macro-F1 teste) | **0,8306** / 0,7665 |
| Treinos corridos | **270** (6 estratégias × 3 seeds × 15 pontos) em 18 corridas |
| Ganho do AL (BALD vs aleatória) | **+0,0218 de ALC** [+0,0109; +0,0321], emparelhado |
| Redundância do pool (drone) | τ = **0,868** · **21,5%** do pool quase-duplicado após L |
| Achados da revisão | **25** (7 de severidade alta) + 4 falhas próprias, todas registadas |

## 4. As 5 coisas mais urgentes

1. **Fechar e versionar o `PROTOCOLO.md`** antes de voltar a ler o teste. As curvas já corridas são
   **exploratórias** precisamente por isto (`RESULTADOS.md` §7).
2. **Inicializar o repositório git** e convidar os docentes (P6.1) — sem isso a coluna `commit` do
   `resultados.csv` fica vazia e nada é rastreável.
3. **Submeter o P2-D1** no Moodle antes da aula (28/10 ou 29/10, conforme a turma) e ensaiar o pitch.
4. **Decidir sobre o baseline EfficientNet** do PL08 (P8.6): ou há máquina com GPU, ou o relatório
   declara que o teto é o da representação congelada e porquê.
5. **Estudar para o T1 de 3/11** (aulas 1–7) — a data só aparece no deck da Aula 07.

## 5. Como usar

- **Antes de uma corrida:** `docs/RESULTADOS.md` §7 diz o que ainda não é válido.
- **Plano de trabalho:** `PENDENTES.md`, filtrar por dono, marcar `[x]` só com prova.
- **Antes de cada aula:** a secção da PL correspondente (§4, §5, §6) e o bloco "No fim da aula".
- **Antes de correr no teste:** `PROTOCOLO.md` §6 (fugas, métricas, comparações injustas).
