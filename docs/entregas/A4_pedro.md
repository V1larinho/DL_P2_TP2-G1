# A4 — Pedro Ribeiro (79354) · Responsável de Produto

> **O que fica em teu nome:** a fila de anotação, a app, a Tabela 2 (classes raras) e a regra de paragem.
> **Tempo:** ~40 min.
> **Bloqueado por:** A1, A2 e A5. És o último a commitar, e é de propósito.

## 0. O que a app faz (e a decisão que ela tomou por ti)

`src/app.py` mostra um recorte, seis caixas e um botão **gravar**. Por omissão **não mostra a
previsão do modelo** — mostra a incerteza:

```
37/40 — incerteza 0,412 (não é a previsão)
```

A previsão existe e é gravada numa coluna de **auditoria** (`previsto_oculto`), mas não chega aos
olhos do anotador. A razão não é estética: há evidência de que ver a sugestão do modelo desloca a
decisão humana mesmo quando a sugestão está errada. Numa app que se chama "assistente", esconder a
resposta é a única forma de o rótulo continuar a ser medição e não eco.

Detalhe que já podes usar como achado: na fila atual, **nenhuma** classe passa de 0,5 de probabilidade
— a coluna `previsto_oculto` está vazia em todas as linhas. Ou seja, com 5% dos rótulos a cabeça não
tem confiança suficiente para sugerir nada. Isso não é um bug; é o resultado a discutir no relatório.

## 1. Gerar a fila e abrir a app

```bash
git pull
python src/app.py --fila 40
```

**Tens de ver:**

```
fila: runs/fila_anotacao.csv  (40 recortes, estrategia=entropia, seed=0)
  previsto_oculto so serve para AUDITORIA — a app nao o mostra ao anotador.
  grupos distintos na fila: N (se < 40, ha quase-duplicados)
```

Se `grupos distintos` for menor que 40, tens a prova de que a aquisição por incerteza escolhe
recortes da mesma imagem — o problema que o A1 mediu (τ = 0,8677, 21,5% do pool redundante) e que o
`--dedup-grupo` do A3 resolve. Escreve o número: é teu, e é o argumento de produto do teu trabalho.

Depois, a interface (precisa de `gradio`, que está no `requirements.txt`):

```bash
pip install gradio
python src/app.py --servir
```

Abre `http://127.0.0.1:7860`. Marca duas ou três imagens e confirma que as anotações ficam em
`runs/anotacoes.csv` com `segundos` e `revelado=False`. **Esse tempo por recorte é o custo unitário
do produto** — sem ele não há "rótulos por ponte" nem conversa com cliente.

> `--revelar` existe para a **auditoria** (mostrar a sugestão e comparar). Em demonstração usa-o com
> cuidado: a partir do momento em que revelas, os rótulos deixam de servir para medir o modelo.

## 2. Commits

```bash
git add src/app.py
git commit -m "feat(A4): fila de anotacao por incerteza com previsao oculta e tempo por recorte"

git add runs/fila_anotacao.csv paper/tabelas/tabela2_diferencas.md \
        paper/tabelas/tabela2_por_classe.csv
git commit -m "chore(A4): fila gerada e tabela 2 — classes raras contra orcamento"

git add AI_LOG.md
git commit -m "docs(A4): registo de IA da aplicacao e da leitura da tabela 2"
```

`runs/anotacoes.csv` (as tuas anotações de teste) **não** vai para o git — é dado de sessão. Se
quiseres guardar a prova, deixa 3 linhas num bloco de código dentro do `PENDENTES.md` ou tira captura.

## 3. A tabela que ninguém mais pode escrever

`paper/tabelas/tabela2_diferencas.md` dá a diferença emparelhada por classe entre cada estratégia e a
aleatória (as células a **negrito** são as que têm IC da diferença a excluir o zero; a leitura
qualitativa, classe a classe, está na §4 do `RESULTADOS.md`). O que interessa ler:

| Classe | Situação | Leitura |
| --- | --- | --- |
| **CorrosionStain** | **crítica** (segurança estrutural) | Δ **+0,057** com o BALD, IC a excluir zero |
| **Efflorescence** | **mais rara** (833 no total, 27 positivos a 5%) | Δ +0,055, mas o IC inclui zero |
| ExposedBars | rara e crítica | Δ +0,020; é a classe que o protocolo do tema nomeia — lê o que os dados dizem, não o que esperavas |

O parágrafo que tens de escrever (e defender): *não é a raridade que impede o ganho, é o número de
positivos no orçamento.* Com 5% dos rótulos, a classe mais rara tem **27** exemplos — não há estratégia
que faça milagres com 27 exemplos. A H2 foi reformulada exatamente por isso, de "classes raras" para
"classe crítica vs classe rara".

## 4. Se te perguntarem

**"Se escondes a previsão, para que serve o modelo na app?"**
Para **ordenar** o que se anota. O valor não está em sugerir o rótulo, está em decidir onde o próximo
minuto de trabalho humano rende mais. É a diferença entre um assistente e um oráculo — e é a mesma
lógica do AL, vista do lado do utilizador.

**"Quando é que se para de anotar?"**
Aos **95% do teto**, medido com IC, e não "quando a curva parece plana". No nosso caso o teto é 0,8306,
portanto o alvo é ~0,789 — e a Tabela 1 diz que o BALD lá chega com **8,7% dos rótulos** (a aleatória
precisa de 13,1%). A regra para o cliente é a que ele entende: *"anotámos N recortes (≈ M voos) por
ponte até garantir 95% do que o modelo conseguiria com tudo rotulado"*.

**"O que fazes quando aparece um recorte que não é betão?"**
Nada de automático, e é uma lacuna declarada: a app não tem deteção de *out-of-distribution* a
funcionar. O que existe é o aviso fixo de que **não substitui inspeção** e a recomendação de recusar
anotações com confiança baixa em todas as classes. Escrever a limitação vale mais do que fingir uma
funcionalidade que não temos.

**"Porque é que a fila tem quase-duplicados?"**
Porque a incerteza não sabe nada sobre redundância: dois recortes da mesma imagem têm quase a mesma
probabilidade e entram os dois. É o argumento mais forte para o agrupamento do A3 (`--dedup-grupo`) e
para o botão de "refotografar esta zona" — num drone, o segundo recorte do mesmo defeito custa um voo.

## 5. O que continua teu

| Item | Quando | Nota |
| --- | --- | --- |
| `src/enviesamento.py`: composição do conjunto rotulado por ronda (**C2.4**) | 12/11 | gráfico de fração por classe × ronda |
| Assistente completo com **re-treino em segundos** e curva a atualizar (**C3.1**) | 26/11 | ciclo completo numa sessão de 5 min |
| Avisos de "não substitui inspeção" + sinalização **OOD** (**C3.2**) | 26/11 | visíveis no ecrã |
| Botão "refotografar esta zona" (eixo D4) | 03/12 | pode ficar desativado no protótipo, mas tem de existir |
| Demo do P2-D3 com recortes novos (**C3.6**) | 03/12 | corre de ponta a ponta |

## 6. Revisão cruzada (PL11)

Revês o **A5** (`src/avaliar.py`); ele revê a tua app. Pergunta-lhe três coisas concretas: o bootstrap
é por imagem ou por recorte; o `NaN` de alvo não atingido aparece na tabela; e onde é que o IC da
diferença emparelhada é calculado (não é o mesmo que comparar dois ICs).
