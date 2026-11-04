# Ficha-resumo de 1 página — Seminário I (Tema C)

> Fonte: PL08 §2.4. Entregar no Moodle até 15/11 (prazo seguro; a PL08 diz "domingo 16/11" mas 16/11/2026 é segunda-feira — ver REVISAO.md R19). Traga pronta para o ensaio da semana seguinte.

---

## ACTIVE LEARNING PARA DEFEITOS EM PONTES DE BETÃO (CODEBRIM) — TEMA C / AL 1

**Problema.** Anotar recortes de fissura, delaminação, corrosão, armadura exposta e eflorescência é lento, caro e desequilibrado (as patologias críticas são raras; a eflorescência é 8,4% do treino). O Active Learning gasta o orçamento de anotação onde rende mais. Pergunta central: com que fração dos rótulos uma estratégia ativa atinge 95% do desempenho do treino completo, face à amostragem aleatória — e isso vale sobretudo nas classes raras?

**Dados.** CODEBRIM (Mundt et al., CVPR 2019; Zenodo 10.5281/zenodo.2620293): 7 677 recortes utilizáveis de 1 522 imagens de origem; treino 6 438 / validação 611 / teste 628; divisão por imagem (0 imagens em duas partições); 25,9% dos recortes são multi-rótulo (29 combinações). Licença não comercial; não redistribuir. Métrica principal: Macro-F1 multi-rótulo no teste.

**Método.** Extrator DINOv2 ViT-S/14 congelado (embedding CLS normalizado) + cabeça linear com BCE por classe. Estratégias de aquisição: aleatória (baseline do AL), entropia/margem multi-rótulo, BALD (MC Dropout na cabeça), CoreSet (k-center greedy em embeddings), BADGE (embeddings de gradiente + k-means++). L = 5% do pool (estratificado), K = 2,5% por ronda, orçamento total 40% → 14 rondas, 3 seeds. Re-treino da cabeça de raiz em cada ronda. Hiperparâmetros congelados na validação com a estratégia aleatória.

**Ideia central (figura).** Ciclo: pool não rotulado → estratégia de aquisição escolhe K recortes → anotar → treinar cabeça → adquirir novamente. A incerteza e a diversidade orientam onde anotar a seguir.

**Resultados (exploratórios, 27/10/2026, CPU).** Teto (100% rótulos): Macro-F1 0,8306. L-só (5%): 0,7665. Quatro estratégias batem a aleatória com IC 95% que exclui zero: BALD (+0,0218 de ALC), entropia (+0,0168), margem (+0,0162), BADGE (+0,0128). CoreSet não bate (+0,0057, IC inclui zero). A classe crítica (corrosão) ganha de forma significativa (+0,057 de F1 com BALD); a mais rara (eflorescência) ganha +0,055 mas com IC largo (apenas ~27 positivos em L). Modelos ativos não ficam pior calibrados (ECE melhora com mais rótulos, igual ao aleatório).

**Aplicação.** Assistente de anotação em Gradio: fila "anotar a seguir" ordenada por incerteza/diversidade, com a razão de cada escolha; previsão oculta por omissão (evitar ancoragem); re-treino da cabeça em segundos; curva de validação atualizada. Aviso: protótipo experimental, não substitui a inspeção.

**Custo.** Extração de embeddings uma vez (~8 min CPU). Cada corrida de AL ~2,5 min por estratégia em CPU (20 núcleos). Cabeça linear cabe no Colab gratuito; fine-tune de CNN total não cabe (ficaria para confirmação com máquina com GPU).

**Equipa (5 membros):** A1 dados, A2 baseline, A3 investigador/porta-voz, A4 produto, A5 avaliação. Todos programam, todos escrevem, todos sabem explicar qualquer parte na defesa (07/01/2027).

**Calendário até P2-D5:** P2-D1 (proposta, 29/10) → Seminário I (17/11) → P2-D3 protótipo (03/12) → P2-D4 avaliação final (17/12) → Relatório + repositório (04/01) → Defesa individual (07/01).
