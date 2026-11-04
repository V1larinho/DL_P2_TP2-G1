# DATASETS.md — que dados usar (e porquê)

Pergunta feita: *qual é o melhor dataset para o trabalho ficar sólido?*
Resposta curta: **o CODEBRIM é o melhor que existe para esta tarefa e é obrigatório pelo protocolo do
Tema C** — não se troca. O que falta ao trabalho não é um dataset maior, é **um segundo domínio** para
mostrar que o ganho do AL não é um artefacto de um único conjunto. Isso está na §5.

Verificado a 27/10/2026 contra o paper (arXiv 1904.08486), o registo Zenodo e as fontes citadas na §4.

---

## 1. Critérios (o que faz um dataset servir *este* trabalho)

| # | Critério | Porquê |
| --- | --- | --- |
| C1 | **Multi-rótulo** (defeitos sobrepostos no mesmo recorte) | É a premissa do tema; single-class não testa a entropia multi-rótulo |
| C2 | **≥5 classes com patologias críticas** | H2 precisa de classes raras e de classes graves |
| C3 | **Desbalanceado** | O AL só tem interesse se o orçamento for escasso |
| C4 | **Unidade de agrupamento identificável** (ponte / imagem) | Sem isso não há verificação de fuga nem IC honestos |
| C5 | **Licença utilizável em trabalho académico** e citável | Não comercial serve; "sem licença" não |
| C6 | **Barato de iterar com características congeladas** | 3 seeds × 14 rondas × 5 estratégias só é viável se cada ronda for segundos |
| C7 | **Documentação publicada** (contagens, splits, baseline) | Para o relatório ter números que se citam, não que se inventam |

## 2. Comparação

| Dataset | Tarefa | Escala | Classes | Licença | C1–C7 | Veredicto |
| --- | --- | --- | --- | --- | --- | --- |
| **CODEBRIM** (Mundt et al., CVPR 2019) | **classificação multi-rótulo de recortes** | 1 590 imagens de **30 pontes** · 5 354 caixas de defeito + 2 506 de fundo | **5** + fundo | Zenodo `10.5281/zenodo.2620293`, *Other (Non-Commercial)* | ✅ todos | **Base do projeto. É o único que cumpre C1+C2+C3+C4 em simultâneo** |
| **SegCODEBRIM** (Jaziri et al., WACV 2024) | segmentação semântica de fissuras | **420 máscaras** sobre imagens do CODEBRIM | 1 (fissura) | **MIT** | C4 ✅ · C1 ✗ | **Extensão sancionada** pelo protocolo: AL com incerteza **por píxel**, mesmo domínio, custo baixo |
| **dacl10k** (Flotzinger et al., WACV 2024) | segmentação semântica multi-label | **9 920 imagens** de inspeções reais | **19** (13 danos + 6 objetos) | a confirmar na release original (a versão empacotada no FiftyOne/HF está listada como CC-BY-4.0) | C2 ✅✅ · C1 parcial | **Melhor candidato a segundo domínio**, mas exige converter máscaras em rótulos de recorte — trabalho de engenharia, não de hoje |
| **GYU-DET** | deteção de defeitos em vigas | multi-defeito, recente | várias | a confirmar | C1 ✗ (deteção) | Não serve: o nosso tema é classificação; voltaríamos ao erro do mAP |
| **SDNET2018 / Özgenel / METU crack** | fissura vs não-fissura | 10⁴–10⁵ recortes | **1** | variável (MIT/CC) | C1 ✗ C2 ✗ | Só como *pré-treino* ou sanity check. Não tem multi-rótulo nem patologias críticas |
| **Crack-Seg / CrackForest / DeepCrack** | segmentação de fissuras | 10²–10³ | 1 | variável | C1 ✗ | Ruído para o nosso objetivo |
| **Base de AL em fachadas do orientador** (Tema AL 2: fissuras em fachadas históricas) | classificação/segmentação | — | — | do orientador | C1–C4 a confirmar | **A jogada de maior retorno**: segundo domínio já alinhado com o SOTA que o protocolo manda ler, e o grupo irmão usa o mesmo simulador |

## 3. Factos verificados do CODEBRIM (para o relatório citar)

Fonte: §3.2 e §4.1 do paper (arXiv 1904.08486) e o registo Zenodo.

- **1 590** imagens de alta resolução, **30 pontes** distintas, várias câmaras e condições
  meteorológicas; parte adquirida por **UAV** (projeto AEROBI, 687384).
- **5 354** caixas de defeito anotadas (com sobreposições) + **2 506** caixas de **fundo** geradas
  (não anotadas à mão) → no máximo **≈7 860 recortes** se houver um recorte por caixa. O número real
  vem do conteúdo do zip; até lá, **não escrever "5 354 recortes"** — são caixas.
- **Contagens por classe** (nº de caixas com essa classe; somam 8 304 porque uma caixa pode ter
  várias classes):

| Classe | Caixas | Leitura |
| --- | --- | --- |
| fissura (`crack`) | **2 507** | a mais frequente |
| delaminação / `spallation` | **1 898** | |
| mancha de corrosão | **1 559** | |
| armadura exposta | **1 507** | crítica para a segurança |
| **eflorescência** | **833** | **a mais rara** — e não é a que o protocolo nomeia |

- **Divisão oficial:** 150 exemplos de defeito **por classe** para validação e 150 para teste —
  ou seja, **o teste é balanceado por desenho**. Todas as caixas de uma imagem ficam na mesma
  partição (**agrupamento por imagem**, não por ponte — o paper explica que dividir por ponte
  tornaria as partições impossíveis de balancear).
- **Versões no Zenodo** (é preciso escolher uma; ver §6):

| Ficheiro | Tamanho | md5 | Usar? |
| --- | --- | --- | --- |
| `CODEBRIM_classification_dataset.zip` | **7,9 GB** | `c1612d9674e2e628e72e7f5817c40130` | ✅ **é esta** (recortes com rótulos e a divisão oficial) |
| `CODEBRIM_original_images.zip` | 8,3 GB | `27baf3a036d0b7d757ff4df47c08c449` | só se os nomes dos recortes não codificarem a imagem de origem |
| `CODEBRIM_cropped_dataset.zip` | 7,9 GB | `f72fb22dafa05f07995d0af852b6bd13` | não (sem divisão) |
| `CODEBRIM_classification_balanced_dataset.zip` | 12,2 GB | `562c563fc449a3b6e1ae10af2da9b37d` | ❌ **não** — replica imagens para balancear o treino; destruiria a composição de `L` e a curva de AL |
| `license.md` | 2,4 kB | `f87f35af2adf97c29d5f710f74587fb3` | ler antes de publicar |

- Código de referência (data loaders e baselines do paper): `github.com/ccc-frankfurt/meta-learning-CODEBRIM`.

### 3.1 O que se **mediu** no dataset (27/10/2026)

Continua a ser a fonte primária acima, mas com os números do próprio ficheiro: zip de **7,9 GB**
baixado, **md5 `c1612d9674e2e628e72e7f5817c40130`** conferido, contagem feita por
`scripts/contar_codebrim.py` (lê as etiquetas de `metadata/defects.xml` + `background.xml`).

| Classe | treino | validação | teste | **total** |
| --- | --- | --- | --- | --- |
| Background | 2 185 | 150 | 150 | 2 485 |
| Crack | 2 208 | 149 | 150 | 2 507 |
| Spallation | 1 608 | 140 | 150 | 1 898 |
| **Efflorescence** | **543** | 141 | 149 | **833** |
| ExposedBars | 1 215 | 142 | 150 | 1 507 |
| CorrosionStain | 1 263 | 146 | 150 | 1 559 |
| **recortes utilizáveis** | **6 438** | **611** | **628** | **7 677** |
| dos quais multi-rótulo (≥2 defeitos) | 1 640 | 183 | 167 | **1 990 (25,9%)** |

- **Imagens de origem: 1 522** com recortes utilizáveis (o zip declara 1 590).
- **52 recortes têm o vetor todo a zero** (nenhuma classe positiva, todos em `defects/`): estão nos
  ficheiros, mas **não** entram no `splits.csv` — um classificador supervisionado não os consegue
  usar. Ficam contados e reportados, não silenciados (`R25`).
- **29 combinações de rótulos** distintas; as três mais frequentes: `Spallation|ExposedBars|CorrosionStain`
  (789), `Spallation|ExposedBars` (434), só `Spallation` (307).
- **Fuga por imagem: 0** — nenhuma imagem de origem aparece em duas partições. A verificação que o
  protocolo pedia está feita (V1 parcial; falta a repetição por seed).
- As contagens por classe do paper (2 507 / 1 898 / 833 / 1 507 / 1 559) coincidem **exatamente** com
  as dos recortes: é ≈1 recorte por caixa. Os 5 354 do paper são caixas; os ficheiros são 5 192
  recortes de defeito utilizáveis + 2 485 de fundo = 7 677 (162 caixas sem recorte utilizável).
- **O treino é muito desbalanceado e o teste não**: eflorescência = **8,4%** do treino e ~23,5% do
  teste. Confirma R21 com números: qualquer afirmação sobre classes raras tem de dizer em que
  distribuição foi medida.
- Combina com o protocolo: com `L` = 5% do pool (324 recortes), sobram **~27 positivos** de
  eflorescência em `L` — a razão pela qual a regra de estratificação tem de garantir um mínimo por
  classe e os IC vão ser largos nessa classe.

## 4. O que isto obriga a corrigir no projeto

| # | Achado | Consequência |
| --- | --- | --- |
| D1 | **A classe mais rara é a eflorescência (833), não a armadura exposta nem a corrosão** (1 507 / 1 559) | **H2 tem de ser reescrita.** O protocolo chama "raras" a duas classes que são, na verdade, de frequência média. H2 passa a ter duas alças: **raridade** (eflorescência) e **criticidade** (armadura exposta, corrosão) — e o relatório ganha um parágrafo a justificar por que se separam |
| D2 | **O teste oficial é balanceado** (150 por classe) | Macro-F1 no teste **não reflete o prior de implantação**. Reportar Macro-F1 (comparável à literatura) **e** F1 por classe com IC; declarar explicitamente que o teste é balanceado por desenho. Sem isto, a afirmação "ajuda nas classes raras" fica ambígua |
| D3 | **Divisão por imagem, não por ponte** | Com 30 pontes, imagens da mesma ponte podem cair em partições diferentes: o teste **não** mede generalização para pontes novas. É limitação a escrever (e um bom slide de discussão) |
| D4 | **`5 354` são caixas; os recortes são outros** (≈7 860 no máximo) | Contar no dia 1 e corrigir todas as menções; a Tabela 2.1 fica com as duas unidades separadas |
| D5 | **A versão `balanced` do zip não serve para AL** | Se alguém a usar, `L` deixa de ser estratificado de forma honesta e a curva perde sentido |
| D6 | **150 exemplos por classe no teste** | Os IC nas classes raras serão largos: 150 amostras × ~5% de erro dão IC de ±3–4 pontos. É preciso dizê-lo antes que o avaliador o diga |

## 5. Recomendação (três níveis, por custo/retorno)

**Nível 1 — agora, para o P2-D1 (29/10).** Ficar com o **CODEBRIM `classification_dataset`** e
publicar no README as contagens reais da §3. Custo: um download de 7,9 GB e um script de contagem.
Retorno: fecha os 20% de "adequação dos dados" da grelha e destrava `splits.csv`/`L0`.

**Nível 2 — até ao P2-D3 (03/12).** Acrescentar **SegCODEBRIM** como a extensão que o próprio
protocolo autoriza (420 máscaras, **MIT**, mesmo domínio): a mesma estratégia de aquisição com
incerteza **por píxel** dá uma segunda curva (Dice vs imagens anotadas) sem custo de licença nem
trabalho de conversão de taxonomia. É o melhor retorno por hora de todo o projeto.

**Nível 3 — para o artigo (depois de 04/01).** Um **segundo domínio**, por ordem de preferência:
1. **o dataset de AL em fachadas do orientador** — já é o SOTA que o protocolo manda ler, o grupo
   irmão (AL 2) usa o mesmo simulador, e a comparação entre os dois grupos é material de artigo;
2. **dacl10k** (9 920 imagens, 19 classes) se for preciso escala e taxonomia mais rica — implica
   converter máscaras em rótulos multi-rótulo de recorte e confirmar a licença;
3. SDNET2018/Özgenel apenas como pré-treino ou sanity check.

**O que pedir ao orientador, numa frase:** *"o dataset de AL em fachadas que serve de SOTA ao tema,
para usarmos como segundo domínio com o mesmo simulador do grupo AL 2."* É a única peça que muda o
trabalho de "um dataset, um resultado" para "dois domínios, uma conclusão".

## 6. Passos de download (para o A1)

```bash
# 1) licença primeiro (2,4 kB): ler e registar no AI_LOG/README
curl -LO https://zenodo.org/records/2620293/files/license.md

# 2) o zip certo (7,9 GB) e verificação de integridade
curl -LO https://zenodo.org/records/2620293/files/CODEBRIM_classification_dataset.zip
md5sum CODEBRIM_classification_dataset.zip   # esperado: c1612d9674e2e628e72e7f5817c40130

# 3) ANTES de descarregar os 8,3 GB de imagens originais: ver se o nome do recorte
#    codifica a imagem de origem (ex.: <imgID>_<cropID>.jpg). Se sim, o agrupamento
#    por imagem verifica-se só com o zip de classificação.
unzip -l CODEBRIM_classification_dataset.zip | head -40
```

Depois: contar recortes por classe e partição, confirmar que nenhuma imagem cruza partições
(`splits.csv` com a coluna `grupo` = imagem), e só então extrair as características DINOv2.
