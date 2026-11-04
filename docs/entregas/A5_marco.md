# A5 — Marco Maceda (66694) · Avaliador

> **O que fica em teu nome:** a avaliação (ALC, IC, calibração), as Tabelas 1 e 3, a figura central,
> e o veredicto das hipóteses.
> **Tempo:** ~35 min.
> **Bloqueado por:** A2 e A3 (corridas com commit). **Bloqueias:** A4 (a Tabela 2 sai do teu script) e o relatório.

## 0. O que o teu script já produz

| Saída | Ficheiro |
| --- | --- |
| Tabela 1 — ALC, rótulos para 95% do teto, com IC | `paper/tabelas/tabela1.md` |
| Tabela 2 em bruto — diferenças por classe (H2) | `paper/tabelas/tabela2_por_classe.csv` |
| Tabela 3 — ECE por estratégia | `paper/tabelas/tabela3_calibracao.md` |
| Figura central | `paper/figuras/curva_al.png` |
| Resumo legível por máquina | `paper/tabelas/resumo_avaliacao.json` |

## 1. Correr a avaliação (depois do push do A3)

```bash
git pull
python src/avaliar.py --B 400
```

~1–2 min. **Tens de ver** os mesmos ALC do quadro do A3 (0,7945 aleatória … 0,8162 BALD) — se
alguma estratégia faltar, é porque o `meta.json` dessa corrida não existe ou não foi commitado.

Confirma três coisas antes de commitar:

```bash
python - <<'EOF'
import json
r = json.load(open("paper/tabelas/resumo_avaliacao.json", encoding="utf-8"))
print("B =", r["B"], "| seeds =", r["seeds"], "| teto =", r["teto"])
for t in r["tabela1"]:
    print(f'{t["estrategia"]:<9} ALC={t["ALC"]:.4f} [{t["ALC_lo"]:.4f}; {t["ALC_hi"]:.4f}]'
          f'  rot95={t["rot95"]:.3f}  atingido={t["rot95_atingido"]:.0%}')
EOF
```

*Tens de ver:* seis estratégias, `B = 400`, `teto = {'0': 0.8296, '1': 0.8296, '2': 0.8327}`, e o
`rot95_atingido` a 0,99 para o BALD e 0,91 para a aleatória (é o que a §3 explica: `NaN` só onde não
se atingiu, nunca 0).

1. Todas as linhas da Tabela 1 têm **IC** (não valores soltos).
2. Onde o alvo de 95% do teto não foi atingido, o campo é **`NaN`** e a nota diz "não atingido" —
   **nunca 0**. Um zero é uma mentira: sugere que se gastaram todos os rótulos e não se chegou lá.
3. A Tabela 2 mostra a diferença **emparelhada por classe** e marca a negrito as classes cujo IC
   exclui o zero (é o que sustenta a H2: corrosão Δ **+0,057**, IC a excluir zero; eflorescência
   Δ +0,055, IC a incluir zero — a leitura completa está na §4 do `RESULTADOS.md`).

## 2. Commits

```bash
git add src/avaliar.py
git commit -m "feat(A5): avaliacao com bootstrap por imagem, ALC, rotulos-para-95% e ECE"

git add paper/tabelas/tabela1.md paper/tabelas/tabela3_calibracao.md \
        paper/tabelas/resumo_avaliacao.json paper/figuras/curva_al.png
git commit -m "chore(A5): tabelas 1 e 3, figura central e resumo com intervalos de confianca"

git add docs/RESULTADOS.md docs/REVISAO.md AI_LOG.md
git commit -m "docs(A5): resultados com IC e veredicto das hipoteses H1-H4"
```

A **Tabela 2** (`tabela2_*.md`, `tabela2_por_classe.csv`) fica para o **A4** commitar: o script é teu,
a interpretação e a apresentação são dele — e é assim que os dois commits não colidem.

## 3. As três decisões que só tu podes defender

| Decisão | O que fizeste | Porque é que está certo |
| --- | --- | --- |
| **Bootstrap por imagem** | reamostra imagens de origem, não recortes | os recortes de uma imagem não são independentes; reamostrar recortes encolhe o IC artificialmente |
| **Bootstrap cruzado com seeds** | 2 dimensões (imagens × seeds) | as seeds e o conjunto de teste são cruzados, não aninhados; com 3 seeds o IC das seeds é **aproximado**, e isso está escrito no cabeçalho do ficheiro |
| **`NaN` para alvo não atingido** | aparece na Tabela 1 como resultado | "não atingiu 95% com este orçamento" é um resultado; escrever 0 transforma-o em "gastou tudo e não chegou" |

## 4. Se te perguntarem

**"Porque é que 400 réplicas de bootstrap e não 1000?"**
Porque o IC já estabiliza (as caudas mudam na terceira casa decimal) e cada réplica custa 6 estratégias
× 15 rondas de macro-F1 sobre ~600 recortes. 400 é o ponto em que o custo deixa de comprar precisão.
Se alguém quiser rigor, `--B 2000` corre em poucos minutos — o número está num argumento, não no código.

**"O ECE diz que os modelos ativos não estão pior calibrados. Isso não é suspeito?"**
É o oposto: é o resultado. A intuição diz que escolher os recortes mais incertos desequilibra a
calibração; os dados dizem que não (H4 não confirmada). O que **está** desequilibrado é o F1 das
classes raras — e isso é outro mecanismo (poucos positivos, não incerteza). Distinguir os dois é o
trabalho do avaliador.

**"O CoreSet perde. Isso não invalida a literatura?"**
Não. O CoreSet foi proposto em classificação de imagem única, com um pool onde a diversidade não
está garantida. Aqui o pool tem 30 pontes e 1 522 imagens, e 21,5% dele é quase-duplicado (medido pelo
A1). A conclusão honesta é: *"neste regime de redundância, a diversidade no espaço de características
não compra nada"* — não *"o CoreSet está errado"*.

## 5. O que continua teu

| Item | Quando | Nota |
| --- | --- | --- |
| **Temperature scaling** ajustado só na validação (**C4.1**) | 10/12 | Tabela 3 passa a ter duas colunas: antes/depois |
| **Grad-CAM** nos recortes adquiridos (**C4.2**) | 10/12 | Figura 4; olha para o que o modelo usa, não só para o F1 |
| **Corrida única no teste oficial** para todas as condições (**C4.3**) | 17/12 | o teste toca-se uma vez; combina com o A1 antes |
| Métricas de drone: **rótulos por ponte** e quadros por defeito crítico (**D4**) | 17/12 | é a linha que um cliente entende |
| Respostas PL06 Q1–Q2, PL07 Q1, Tema C Q3 | semanal | Q3 é teu: "Macro-F1 melhor, ECE pior — porquê e o que isso faz à app?" |

## 6. Revisão cruzada (PL11)

Revês o **A4** (`src/app.py`) e ele revê o teu `src/avaliar.py`. No código dele, verifica: a previsão
está **oculta** ao anotador (não é detalhe estético — é ancoragem, §3 do guia dele), a fila não repete
recortes da mesma imagem, e o tempo por recorte é registado.
