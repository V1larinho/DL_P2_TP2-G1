# Respostões às Questões 1–3 da PL08 (entregar por escrito no fim da aula de 05/11)

> Fonte: PL08 §3. Respostas curtas, diretas, sem IA.

---

## Questão 1 — Augmentation

**Porque é que a data augmentation se aplica só ao conjunto de treino e nunca antes da divisão?**

Porque a augmentation cria versões transformadas das mesmas imagens. Se for aplicada antes da divisão em treino/validação/teste, versões aumentadas de uma mesma imagem podem cair em partições diferentes → fuga de informação (data leakage). O modelo veria, indiretamente, exemplos do teste durante o treino, e as métricas de validação/teste ficariam otimistas. A augmentation faz parte do pipeline de treino: deve ser aplicada apenas aos dados de treino, depois da divisão fixa. No nosso `src/dados.py`, as transformações aleatórias (RandomResizedCrop, flip, jitter) estão só no `Recortes(treino=True)`; val e teste usam resize + center crop determinístico.

---

## Questão 2 — Registo de experiências

**Porque se regista o commit e a configuração de cada resultado?**

Para reprodutibilidade e rastreabilidade. O commit identifica a versão exata do código que produziu o número; a configuração (estratégia, seed, L, K, hiperparâmetros, dataset) identifica as condições do experimento. Sem isto, não é possível reproduzir um resultado nem saber qual versão do código gerou cada linha da tabela. É também a base para a coluna `commit` do `paper/resultados.csv`, exigida pela PL08 §2.3: cada linha tem data, commit, configuração, métrica de validação e tempo de treino.

---

## Questão 3 — Baseline forte

**Porque se pede uma baseline forte e não apenas "uma CNN simples"?**

Uma CNN simples treinada do zero daria um teto artificialmente baixo; qualquer método avançado pareceria bom só por comparação com algo fraco. A baseline forte (CNN pré-treinada com fine-tuning a 100% dos rótulos, ou no tema C a aleatória com o mesmo orçamento) estabelece o patamar realista a superar. Só assim a comparação é justa e o ganho do método avançado é significativo. No nosso protocolo, a comparação própria do AL é a **aleatória com o mesmo orçamento** (PROTOCOLO.md §4), e o teto é o treino com 100% dos rótulos na mesma representação (cabeça linear sobre DINOv2 congelado).
