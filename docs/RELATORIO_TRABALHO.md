# RELATORIO_TRABALHO.md — relatório do trabalho feito

> **Não confundir** com o relatório final da UC (formato de artigo, entrega até 04/01).
> Este é o relatório **de trabalho**: o que foi produzido, com que base, que decisões foram tomadas,
> o que foi verificado e o que falta. O mapa para o relatório final está no §8.

Data: 27/10/2026 · Tema C (AL 1) · Grupo 1 (renomear) · TP2

## 1. Objetivo e âmbito

O grupo tinha os materiais da UC na pasta `P2` e o **P2-D1 a 29/10** (documento de 2 páginas +
pitch de 5 min). O trabalho feito aqui foi:

1. ler **todos** os documentos da pasta e extrair deles **uma lista única de tarefas**;
2. montar o **esqueleto do repositório** que a PL06 exige, com os papéis atribuídos;
3. escrever a **proposta do P2-D1** e o **pitch**, prontos a validar e submeter;
4. escrever o **protocolo experimental** que tem de fechar na PL09;
5. fazer uma **passagem crítica** às fontes e aos textos produzidos.

Fora do âmbito (e por isso não feito): descarregar o dataset, escrever o simulador de AL e treinar
qualquer modelo. Isso depende de dados que não estão nesta máquina e das decisões da §5.

## 2. Fontes usadas

| # | Documento | Págs. | O que fixa para o nosso trabalho |
| --- | --- | --- | --- |
| 1 | `C3_DL_P2_TemaC_AL1_CODEBRIM_Defeitos_Betao.pdf` | 11 | Método, papéis A1–A5, protocolo experimental (§6), hipóteses, plano por fase, 3 pedidos "Com IA", 3 questões |
| 2 | `DL_PL06_P2_Arranque_e_guia_segmentacao.pdf` | 4 | Estrutura do repositório, tabela 2.1, guia de segmentação (Dice/IoU, SAM), app v0 |
| 3 | `DL_PL07_P2_Proposta_D1_e_guia_detecao.pdf` | 4 | Conteúdo e **grelha de avaliação** do P2-D1, guia de deteção, estimativa computacional |
| 4 | `DL_PL08_P2_Pipeline_baseline_e_planeamento_seminario.pdf` | 3 | `src/dados.py` + `splits.csv`, baseline por tema, 6 blocos do seminário |
| 5 | `Aula_07_Detecao_Objetos_YOLO_RetinaNet_NMS_e_mAP.pdf` | 16 | Teórica de deteção; **data do T1 (3/11)**; AGPL do Ultralytics |
| 6 | `DL_PL08_..._EN.pdf` | 3 | Tradução do n.º 4 — **sem requisitos novos** (verificado campo a campo) |

Total: **41 páginas**. Texto extraído com `pdftotext -layout` para `P2/.extracted/` (pasta de trabalho;
pode ser apagada — não é entregável).

## 3. Artefactos produzidos

| Ficheiro | Para que serve | Exigido por | Dono |
| --- | --- | --- | --- |
| [`README.md`](../README.md) | Problema, dados, licença NC, papéis, estrutura, como executar, estado | PL06 §2.1 · Tema C §2.3 | A1 |
| [`PENDENTES.md`](../PENDENTES.md) | **Lista mestra**: 121 tarefas, cada uma com dono, prova e secção de origem | pedido do grupo | A1 |
| [`docs/P2-D1.md`](P2-D1.md) | Proposta de 2 páginas: tabela 2.1 corrigida, hipóteses, protocolo, mockup, plano | PL07 §2.1 · Tema C §5.1 | A1 (texto) · A3 (pitch) |
| [`slides/P2-D1_pitch.md`](../slides/P2-D1_pitch.md) | Pitch de 5 min nos 5 diapositivos da grelha, com notas de tempo | PL07 §2.1 | A3 |
| [`PROTOCOLO.md`](../PROTOCOLO.md) | Protocolo experimental a fechar na PL09: hipóteses, desenho, definições, riscos | Tema C §6 | A1 |
| [`AI_LOG.md`](../AI_LOG.md) | Registo de IA com os 6 pedidos obrigatórios pré-registados | Tema C §8 · PL06 §2.5 | todos |
| [`docs/DATASETS.md`](DATASETS.md) | Análise de datasets: critérios, comparação com 4 alternativas, factos verificados do CODEBRIM, recomendação em 3 níveis | pedido do grupo | A3 |
| [`docs/DRONE.md`](DRONE.md) | O cenário de inspeção por drone: 6 eixos que mudam (redundância temporal, agrupamento por voo, edge, percepção ativa, OOD, custo em voos) + emendas ao protocolo | orientador | A3 |
| [`docs/papeis/`](papeis/) | Um plano de trabalho por membro (A1–A5): decisões que só ele toma, próximas duas semanas, par de revisão, leituras, dependências | pedido do grupo | — |
| [`scripts/contar_codebrim.py`](../scripts/contar_codebrim.py) | Contagem de recortes por classe/partição e verificação de fuga por imagem **direto do zip**, sem extrair; escreve `splits.csv` | PL08 §2.2 · Tema C §2.2 | A1 |
| [`docs/REVISAO.md`](REVISAO.md) | **25** achados + 4 falhas próprias, com evidência e correção | pedido do grupo | — |
| [`data/splits.csv`](../data/splits.csv) | **7 677 recortes** com `path,label,grupo,split` (label multi-rótulo, `grupo` = imagem de origem) — o contrato da PL08, gerado por script | PL08 §2.2 | A1 |
| [`configs/al_vits14_aleatoria_s0.yaml`](../configs/al_vits14_aleatoria_s0.yaml) | Exemplo do "um YAML por experiência" | Tema C §2.3 | A3 |
| [`requirements.txt`](../requirements.txt) | Dependências, com as alternativas sem AGPL comentadas | PL06 §2.1 | A1 |
| `.gitignore` | `data/` e artefactos pesados fora do git; `splits.csv` e JSON leves dentro | Tema C §2.3, §7.3 | A1 |

## 4. Decisões tomadas

| Decisão | Porquê |
| --- | --- |
| **Papéis A1–A5 atribuídos pelo cargo de cada um**: Eng. de Dados→A1, Baseline→A2, Investigador/porta-voz→A3, Produto→A4, Avaliador→A5 | É a leitura que respeita tanto o cargo declarado como as competências que o protocolo pede a cada papel. A4 fica com o **enviesamento + regra de paragem + fila da app**, que é o trabalho de produto |
| Aplicação partilhada por **A1 (interface) + A4 (produto)** | O protocolo dá a interface ao A1 e a aplicação ao A4; separámos por "quem constrói" vs "quem decide o comportamento" |
| Repositório em `P2/DL_P2_TP2-G1/` | Fica junto dos materiais, onde o grupo já trabalha. O nome `G1` é marcador — **renomear** (R8) |
| **Baseline ≠ teto**: baseline = aleatória com o mesmo orçamento; teto = 100% dos rótulos | Resolve a contradição EfficientNet (PL08) vs ResNet-50 (protocolo) sem apagar nenhum dos dois (R2) |
| **5 estratégias**, 3 seeds, 14 rondas = 210 corridas | O protocolo lista 5 e estima 4; a contagem certa é 5 (R3) |
| `splits.csv` **canónico** + `splits.json` só com hashes e `L0` | A PL08 define as colunas do CSV; o protocolo pede JSON. Um formato canónico, o outro é derivado (R10) |
| Tabelas e figuras **geradas por script**, nunca à mão | Regra explícita do protocolo para o trabalho ser publicável (§7.3) |
| Nada inventado sobre o dataset | As contagens por classe/partição ficam **por medir** e marcadas como tal (M2) |

## 5. Verificação feita

| Verificação | Como | Resultado |
| --- | --- | --- |
| Todos os documentos foram lidos | `pdftotext -layout`; contagem de quebras de página vs `pypdf` (11+4+4+3+16+3 = 41) | ✅ nada ficou por ler |
| Cobertura das fontes na lista de tarefas | `grep` das referências `*PL06/PL07/PL08/Tema C/Aula 07` | ✅ 95 linhas com fonte explícita |
| Tarefas contadas | `grep -c '^- \[ \]'` / `'^- \[x\]'` | **121** total · 10 feitas · 111 a fazer |
| Script de contagem | `zip` sintético com uma fuga propositada: `--listar` e `--contar` | ✅ contagens certas, fuga detetada, **exit 2** na fuga |
| Download do dataset | `curl` com retoma + `md5sum` | ✅ **7 911 716 093 bytes**, md5 `c1612d9674e2e628e72e7f5817c40130` = o publicado |
| Contagem real | `scripts/contar_codebrim.py --contar` sobre o zip | ✅ **7 677 utilizáveis** (6 438/611/628), **1 990 (25,9%)** multi-rótulo, **0** imagens em duas partições, **52** sem rótulo excluídos, exit 0 |
| Aritmética do protocolo | `(40% − 5%) / 2,5%` | ✅ 14 rondas |
| Coerência de datas | `date -d` sobre as 19 datas dos documentos | ✅ TP1 = quarta, TP2 = quinta, T1 e Seminário I a uma terça, P2-D3/D4/D5 coerentes — **uma exceção**: o "domingo, 16/11" da PL08 é segunda-feira (**R19**, corrigido) |
| Grelha de avaliação do P2-D1 | soma dos pesos | ✅ 5 × 20% = 100% |
| Links internos dos `.md` | script de verificação de caminhos relativos | ✅ 28 links, 0 quebrados |
| Números do dataset | confronto do protocolo com o **paper** (arXiv 1904.08486 §3.2/§4.1) e o **registo Zenodo** | ✅ 1 590 imagens / 30 pontes / 5 354 caixas / 2 506 de fundo / contagens por classe / 150 por classe em val e teste; corrigidos dois erros do protocolo (R20, R23) |

## 6. Lacunas (e porque não estão fechadas)

1. ~~Nº de recortes e verificação de fuga~~ — **feito** (`C1.1`, `C1.2`): dataset descarregado, md5 conferido, contagens medidas e `splits.csv` gerado. Falta a **inspeção visual** de 5 recortes por classe (`C1.2b`) e a **extração DINOv2 + k-NN** (`C1.3`, `C1.4`).
2. **Código** (`src/dados.py`, `src/extrair.py`, `src/al/simular.py`): não escrito, porque não há dados para o verificar. Escrever código que não corre é pior do que não o escrever.
3. **Pesquisa web:** a primeira tentativa **falhou por rede** (agentes de pesquisa). Foi refeita **diretamente** para os dados — paper do CODEBRIM, Zenodo, SegCODEBRIM, dacl10k — e está em `AI_LOG.md` §3 com os valores e as fontes. Continua por confirmar só o que é de biblioteca: identificadores de DINOv2 e o detalhe do CoreSet/BADGE.
4. **Exportação**: o `docs/P2-D1.md` ainda não está em PDF de 2 páginas nem o pitch em `.pptx`/`.pdf`. Fica como passo manual (Word/Google Docs/Marp).

## 7. Próximas 72 horas (27 → 29/10)

| Quando | O que | Quem |
| --- | --- | --- |
| **27/10 (hoje)** | Confirmar a turma (R1) e o número do grupo (R8); abrir o repositório privado no GitHub e adicionar os docentes | A1 |
| 27/10 | ✅ Descarregar o CODEBRIM, contar e verificar a fuga — **feito** | A1 |
| 27–28/10 | Extração **DINOv2** de todos os recortes + **k-NN (k=20)** de sanidade na validação | A1 |
| 28/10 | Inspeção visual de **5 recortes por classe** e visto no §Dados do P2-D1 | A1, A4 |
| 28/10 | Validar a proposta em grupo (30 min): hipóteses H1–H4, `L`/`K`/orçamento, regra de estratificação (R4) e definição de margem (R5) | todos |
| 28/10 | Fechar as 5 secções do pitch, **ensaiar com cronómetro** (alvo 4 min 30 s) | A3 |
| 28/10 | Guia de segmentação da PL06, se ainda não estiver feito (Dice/IoU + SAM) | A2, A5 |
| 28/10 | Exportar o P2-D1 para PDF e submeter no Moodle **antes do início da aula** | A1 |
| 29/10 | Pitch + registar o feedback do docente no README | A3, A1 |
| paralelo | Estudar para o **T1 de 3/11** (aulas 1–7) — não é adiável para depois do P2-D1 | todos |

## 8. Mapa para o relatório final da UC (entrega 04/01)

| Secção do artigo | Vem de |
| --- | --- |
| Resumo e Introdução | `README.md` §1 · `docs/P2-D1.md` §1 · pergunta central |
| Trabalhos relacionados | `paper/leituras/` (≈10 fichas) + SOTA do orientador (`C1.11`) |
| Dados | contagens por classe/partição + divisão por imagem + licença (`C1.2`) |
| Métodos | `PROTOCOLO.md` §3 + `src/al/` · figura do ciclo de AL |
| Protocolo experimental | `PROTOCOLO.md` (§2, §4, §6) tal como foi commitado na PL09 |
| Resultados | `paper/resultados.csv` → Tabelas 1–3 e Figuras 2–5, geradas por script |
| Discussão e limitações | `docs/REVISAO.md` (riscos) + secção 6 do relatório (P2-D4) |
| Ética e dados | licença NC, `AI_LOG.md`, acordo de autoria (ICMJE) |

---

**Nota de honestidade sobre o processo.** O pedido original era pôr cinco agentes a trabalhar em
paralelo (executar, revisar, resumir, listar, relatar). Nesta sessão só existe um agente de pesquisa
disponível (`researcher-web`) e o arranque falhou por rede, por isso os cinco papéis foram feitos
**sequencialmente por mim**, com o rasto de cada um em ficheiro (execução → `README`/`docs`/
`PROTOCOLO`; revisão → `docs/REVISAO.md`; lista → `PENDENTES.md`; resumo → `docs/RESUMO.md`;
relatório → este documento). O resultado é auditável: cada afirmação tem a secção de origem.
