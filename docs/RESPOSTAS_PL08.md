# Respostas Ã s QuestÃµes 1â€“3 da PL08 (entregar por escrito no fim da aula de 05/11)

> Fonte: PL08 Â§3. Respostas curtas, diretas, sem IA.

---

## QuestÃ£o 1 â€” Augmentation

**Porque Ã© que a data augmentation se aplica sÃ³ ao conjunto de treino e nunca antes da divisÃ£o?**

Porque a augmentation cria versÃµes transformadas das mesmas imagens. Se for aplicada antes da divisÃ£o em treino/validaÃ§Ã£o/teste, versÃµes aumentadas de uma mesma imagem podem cair em partiÃ§Ãµes diferentes â†’ fuga de informaÃ§Ã£o (data leakage). O modelo veria, indiretamente, exemplos do teste durante o treino, e as mÃ©tricas de validaÃ§Ã£o/teste ficariam otimistas. A augmentation faz parte do pipeline de treino: deve ser aplicada apenas aos dados de treino, depois da divisÃ£o fixa. No nosso `src/dados.py`, as transformaÃ§Ãµes aleatÃ³rias (RandomResizedCrop, flip, jitter) estÃ£o sÃ³ no `Recortes(treino=True)`; val e teste usam resize + center crop determinÃ­stico.

---

## QuestÃ£o 2 â€” Registo de experiÃªncias

**Porque se regista o commit e a configuraÃ§Ã£o de cada resultado?**

Para reprodutibilidade e rastreabilidade. O commit identifica a versÃ£o exata do cÃ³digo que produziu o nÃºmero; a configuraÃ§Ã£o (estratÃ©gia, seed, L, K, hiperparÃ¢metros, dataset) identifica as condiÃ§Ãµes do experimento. Sem isto, nÃ£o Ã© possÃ­vel reproduzir um resultado nem saber qual versÃ£o do cÃ³digo gerou cada linha da tabela. Ã‰ tambÃ©m a base para a coluna `commit` do `paper/resultados.csv`, exigida pela PL08 Â§2.3: cada linha tem data, commit, configuraÃ§Ã£o, mÃ©trica de validaÃ§Ã£o e tempo de treino.

---

## QuestÃ£o 3 â€” Baseline forte

**Porque se pede uma baseline forte e nÃ£o apenas "uma CNN simples"?**

Uma CNN simples treinada do zero daria um teto artificialmente baixo; qualquer mÃ©todo avanÃ§ado pareceria bom sÃ³ por comparaÃ§Ã£o com algo fraco. A baseline forte (CNN prÃ©-treinada com fine-tuning a 100% dos rÃ³tulos, ou no tema C a aleatÃ³ria com o mesmo orÃ§amento) estabelece o patamar realista a superar. SÃ³ assim a comparaÃ§Ã£o Ã© justa e o ganho do mÃ©todo avanÃ§ado Ã© significativo. No nosso protocolo, a comparaÃ§Ã£o prÃ³pria do AL Ã© a **aleatÃ³ria com o mesmo orÃ§amento** (PROTOCOLO.md Â§4), e o teto Ã© o treino com 100% dos rÃ³tulos na mesma representaÃ§Ã£o (cabeÃ§a linear sobre DINOv2 congelado).
