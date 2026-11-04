# A4 — Pedro Ribeiro (79354) · Responsável de Produto

> **Missão:** transformar o método numa **coisa que se usa** — a fila de anotação — e provar o que ela
> faz ao conjunto rotulado. És também quem defende a decisão mais difícil do projeto: **quando parar
> de anotar**.

## O que só tu decides

1. **O comportamento da fila**: que razões aparecem em cada linha (incerteza, diversidade, classe rara
   provável), por que ordem, e o que a app faz quando não há razão clara.
2. **A regra de paragem** — quantos rótulos bastam, com que critério (95% do teto com IC, ou
   estabilização da curva), e como isso se comunica a um cliente não técnico.
3. **Os avisos da interface** e a sinalização de recortes fora da distribuição.

## Próximas duas semanas

| Quando | Tarefa (ID) | Pronto quando |
| --- | --- | --- |
| 28/10 | Primeira app Gradio a funcionar (recorte → 3 classes) (**P6.7**) | `launch()` sem erro |
| 05/11 | **App v0**: recorte → defeitos previstos multi-rótulo (**C1.9**, com A1) | Prevê nos recortes de teste |
| 12/11 | `src/enviesamento.py`: composição do conjunto rotulado por ronda (**C2.4**) | Gráfico de fração por classe × ronda |
| 12/11 | F1 das classes raras vs orçamento; **Tabela 2** em bruto (**C2.13**) | Tabela gerada por script |
| 26/11 | **Assistente de anotação completo**: fila com razão, anotar na app, **re-treino da cabeça em segundos**, curva atualizada (**C3.1**) | Ciclo completo numa sessão de 5 min |
| 26/11 | Avisos: *"não substitui a inspeção"* + sinalização **OOD** (**C3.2**) | Visíveis no ecrã |
| 03/12 | Demo do P2-D3 com **recortes novos** (**C3.6**) | Demo corre de ponta a ponta |
| 03/12 | 10 recortes mais adquiridos por estratégia, e **porquê** (**C3.7**, com A5) | Lista comentada |
| 17/12 | **Tabela 2** final: F1 nas classes raras a 20% + composição do conjunto rotulado (**C4.6**) | Gerada por script, nunca à mão |
| 04/01 | Secção de *paper/* sobre a aplicação e o enviesamento (**C5.3**) | Escrita e revista |

## Ângulo drone (o que te toca)

Num drone o produto ganha uma segunda função: a fila não serve só para anotar, serve para dizer
**onde voltar a fotografar** (`docs/DRONE.md`, eixo D4). Desenha a interface com um botão de
"refotografar esta zona" — mesmo que fique desativado no protótipo, mostra que o produto foi pensado
para o cenário real. E acrescenta a métrica que um cliente entende: **rótulos (e voos) por ponte até
95% do teto**.

## Par de revisão e leituras

- **Revisão cruzada (PL11):** **A4 ↔ A5**. Revês `avaliar.py` e as figuras dele; ele revê a app e o
  `enviesamento.py`.
- **Leituras:** Protocolo do Tema C §5.3 (o que a app tem de ter) · Gradio docs · Guo et al. 2017
  (calibração — a app promete "confiança calibrada", tens de saber o que isso é).

## Dependências

Bloqueado por: **A1** (dados e app) e **A2** (cabeça treinada). Bloqueias: **A5** (a Tabela 2 é tua;
a figura de enviesamento é dele) e a demo do P2-D3.
