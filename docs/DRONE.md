# DRONE.md — o projeto se o cliente for um drone

O orientador levantou a hipótese de o trabalho evoluir para **inspeção por drone em vez de
inspetores humanos**. Isto não é um detalhe de apresentação: muda o desenho dos dados, três
parâmetros do protocolo e a própria definição do que é "economizar anotação". Este documento fixa o
que fica igual, o que muda e o que temos de decidir antes do P2-D1.

> **Resumo em três linhas.** O problema mantém-se (que recorte anotar a seguir, e quando parar), mas
> o pool deixa de ser fotografias independentes e passa a ser **vídeo com redundância temporal**, a
> unidade de agrupamento passa a ser a **missão de voo**, e a incerteza ganha um segundo uso:
> **decidir onde o drone volta a fotografar de perto**.

## 1. O que fica igual

- Pergunta central e métrica: **Macro-F1 vs fração de rótulos**, ALC e "rótulos para 95% do teto".
- Estratégias de aquisição (aleatória, entropia/margem, BALD, CoreSet, BADGE) — são independentes do
  sensor.
- Extração DINOv2 congelada + cabeça linear: continua a ser o que torna 210 rondas viáveis.
- Baseline = aleatória com o mesmo orçamento.

## 2. O que muda (seis eixos)

| # | Eixo | Efeito concreto |
| --- | --- | --- |
| **D1** | **Redundância temporal.** Um vídeo a 30 fps dá dezenas de quadros quase idênticos do mesmo defeito. A aquisição por incerteza escolheria 20 quadros do mesmo local | Antes de adquirir, **agrupar o pool por quase-duplicado** (similaridade de cosseno dos embeddings acima de um limiar `τ`) e escolher no máximo um representante por grupo. `τ` é hiperparâmetro **congelado** e declarado — passa a constar do `PROTOCOLO.md` §3 |
| **D2** | **Unidade de agrupamento.** A divisão do CODEBRIM é **por imagem** (e o teste pode partilhar pontes com o treino — limitação R22) | Num cenário de drone, dividir por **(ponte, voo)**: nenhum voo em duas partições. No CODEBRIM só conseguimos o nível imagem; a limitação fica escrita, e nos dados novos impõe-se |
| **D3** | **Inferência a bordo (edge).** O drone não tem um servidor | O classificador tem de ser **medido no hardware alvo** (latência por quadro, watts). A combinação DINOv2 ViT-S/14 + cabeça linear é a mais plausível; se não cumprir, a saída é reduzir resolução ou destilar um aluno — **decisão só depois de medir**, nunca por intuição |
| **D4** | **Incerteza como percepção ativa.** Num drone, a incerteza não serve só para escolher rótulos: serve para escolher **onde voltar a olhar** | Segundo uso do mesmo sinal: a fila de anotação ordena o que anotar *e* a app sugere a zona a refotografar. É o argumento de artigo mais forte que este projeto pode ter |
| **D5** | **Domínio deslocado.** Luz, sombra do próprio drone, desfoque de movimento, sujidade na lente, distância de tiro variável | O assistente **tem** de sinalizar recortes fora da distribuição (o protocolo já o pede) — com drone isto deixa de ser higiene e passa a ser requisito funcional |
| **D6** | **O que se economiza muda de unidade.** Com pessoas, poupa-se tempo de engenheiro; com drone, poupa-se também **voo e bateria** | Acrescentar uma métrica secundária: **rótulos por ponte até 95% do teto** e **quadros revistos por defeito crítico encontrado**. É a métrica que um cliente de inspeção entende |

## 3. Porque isto reforça a escolha do CODEBRIM (e não a muda)

O paper descreve a aquisição assim: imagens de alta resolução, **parte adquirida por UAV** para
chegar a zonas inacessíveis, quatro câmaras, distâncias e ângulos variáveis, flash difuso para as
zonas escuras, e fissuras com largura a partir de **0,3 mm** — que é o que obriga a alta resolução.
Ou seja: **o CODEBRIM já foi construído no regime de aquisição de um drone**, incluindo as variações
de escala que esse regime impõe. Isso é um argumento a favor da escolha, não uma coincidência.

O que o CODEBRIM **não** tem: vídeo, metadados de voo, nem máscaras de defeito fino. Para esses três
faltam complementos, por esta ordem de custo:

1. **SegCODEBRIM** (420 máscaras de fissura, **MIT**, mesmas imagens) — dá o eixo "defeito fino" e
   permite mostrar a fila de anotação ao nível do píxel. Custo: um download pequeno.
2. **Dataset de AL em fachadas do orientador** — segundo domínio, alinhado com o SOTA que o tema
   manda ler, partilhado com o grupo AL 2. Custo: um pedido.
3. **dacl10k** (9 920 imagens, 19 classes) — inspeções reais, taxonomia mais rica; **não** é
   drone-específico e exige converter máscaras em rótulos de recorte. Custo: engenharia.
4. **Vídeo de drone anotado**: **não existe** um benchmark público fiável de vídeo de inspeção de
   pontes com rótulos multi-rótulo. Se o projeto for por aqui, os dados vêm de um parceiro — e isso
   é uma conversa com o orientador, não um download.

## 4. O que dizemos no P2-D1 (parágrafo pronto)

> O protótipo foi desenhado para o regime de aquisição de um drone, não para fotografias de estúdio:
> o CODEBRIM inclui imagens obtidas por UAV, com variação de escala e iluminação, e fissuras na ordem
> dos 0,3 mm. Num voo real, o pool deixa de ser um conjunto de imagens independentes e passa a ser
> vídeo com redundância temporal; por isso a nossa aquisição agrupa quase-duplicados antes de
> escolher, a unidade de agrupamento sobe de *imagem* para *(ponte, voo)*, e a incerteza ganha um
> segundo uso — dizer à aeronave onde voltar a fotografar de perto. É a mesma pergunta do protocolo
> ("quantos rótulos são mesmo precisos?"), com o custo medido em rótulos **e** em voo.

## 5. Emendas a registar no `PROTOCOLO.md` (secção 8) se o drone entrar

1. Agrupamento de quase-duplicados com limiar `τ` congelado, aplicado **antes** de cada ronda de
   aquisição, e o número de grupos colapsados registado por ronda.
2. Métricas secundárias novas: **rótulos por ponte** e **quadros revistos por defeito crítico**.
3. Limitação declarada: o CODEBRIM não permite dividir por voo; a divisão por imagem é a melhor
   aproximação disponível e o teste pode partilhar pontes com o treino (R22).
4. Requisito de edge: latência medida no hardware alvo, com o valor e o dispositivo escritos.

## 5.1 A medição de `τ` — feita (27/10)

`python src/redundancia.py` → `runs/redundancia.json`. 21 668 pares intra-imagem e 299 605
pares entre imagens, embeddings DINOv2 ViT-S/14 normalizados:

| Medida | Valor |
| --- | --- |
| Similaridade **intra-imagem** (mesma imagem de origem) | média **0,631** |
| Similaridade **entre imagens** | média 0,424 · p99 0,782 · p99,9 **0,868** |
| **τ** (p99,9 dos pares entre imagens) | **0,868** |
| Pool fundido por τ | 6 438 → **4 402 grupos** (−31,6%) |
| Candidatos a ≤ τ de um rótulo já escolhido (após L=5%) | **1 387 = 21,5% do pool** |

Três consequências para a aquisição:

1. **O filtro não é cosmético:** um quinto do pool é quase-duplicado do que já está anotado. Sem
   filtro, uma estratégia de incerteza gasta ~1/5 do orçamento a re-perguntar defeitos conhecidos —
   e a curva parece pior sem que o método tenha piorado.
2. **O intervalo é grande e seguro:** entre 0,424 (par entre imagens, mediana) e 0,631 (média
   intra-imagem) há margem larga; τ=0,868 é conservador de propósito (aceita ~0,1% de falsos
   agrupamentos entre pontes diferentes).
3. **Não existe τ universal:** a pesquisa do A1 não encontrou nenhum valor publicado para betão; os
   números que circulam (Hamming ≤10 em 64 bits no `imagededup`, cosseno 0,95 em CLIP) são convenções
   de biblioteca, não limiares validados. Este τ é **deste** dataset.

## 6. Tarefas (entram no `PENDENTES.md`)

| ID | Tarefa | Dono | Até |
| --- | --- | --- | --- |
| **D1** | ~~Medir a **redundância** do pool CODEBRIM e propor `τ`~~ — **feito**: τ=0,868, 21,5% do pool redundante após L, `src/redundancia.py` | A1 | ✅ 27/10 |
| **D2** | Implementar o agrupamento de quase-duplicados na aquisição e registar quantos grupos colapsam por ronda | A3 | 12/11 |
| **D3** | Medir latência de ViT-S/14 + cabeça linear **no hardware alvo** (ou num substituto declarado: CPU do portátil / GPU do Colab) | A2 | 03/12 |
| **D4** | Acrescentar as duas métricas novas (rótulos por ponte, quadros por defeito crítico) ao `avaliar.py` | A5 | 17/12 |
| **D5** | Falar com o orientador: vídeo de drone e/ou dataset de fachadas; registar resposta no `README` | A3 | 29/10 |
