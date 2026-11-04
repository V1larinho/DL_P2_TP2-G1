# Plano do Seminário I — 17/11/2026 (25 min + 5 min perguntas)

> Fonte: PL08 §2.4. Porta-voz: A3 (Gonçalo Vilarinho). As perguntas podem ir a qualquer membro.

## Estrutura (6 blocos, PL08 §2.4)

### Bloco 1 — Problema e motivação (3 min) · A3

- Utilizador: equipa de inspeção de infraestruturas
- Decisão: que recortes anotar a seguir; quando parar
- Porque importa: rotular é caro; patologias críticas são raras (corrosão, armadura exposta)
- Pergunta central: com que fração dos rótulos uma estratégia ativa atinge 95% do teto, face à aleatória?
- **Dizer em voz alta:** "Não é sobre fazer ML melhor — é sobre gastar o orçamento de anotação onde rende mais."

### Bloco 2 — Dataset e métricas (5 min) · A1 suporta

- CODEBRIM: 7 677 recortes de 1 522 imagens, 5 classes + fundo, multi-rótulo (25,9%)
- Contagens por classe: fissura 2 507 · delaminação 1 898 · corrosão 1 559 · armadura exposta 1 507 · eflorescência 833 (a mais rara)
- Divisão por imagem (não por recorte): 0 imagens em duas partições
- Métrica: Macro-F1 multi-rótulo no teste; resumos: ALC e rótulos para 95% do teto com IC 95%
- **Mostrar:** contagens por classe no README; a distinção raridade ≠ criticidade

### Bloco 3 — Método (7 min) · A3 apresenta; A2, A5 prontos a responder

- Extrator: DINOv2 ViT-S/14 congelado, embedding CLS normalizado (384-d)
- Cabeça: linear, BCE por classe, sigmoid por classe independente
- Ciclo AL: pool → estratégia de aquisição → K recortes → oráculo revela rótulos → re-treinar cabeça
- Estratégias: aleatória (baseline) · entropia/margem · BALD (MC Dropout T=10) · CoreSet (k-center greedy) · BADGE (gradiente + k-means++)
- Protocolo: L=5%, K=2,5%, 14 rondas, 3 seeds, hiperparâmetros congelados na aleatória
- **Mostrar:** a figura `paper/figuras/curva_al.png`

### Bloco 4 — Resultados (4 min) · A5 suporta

- Teto: Macro-F1 0,8306 · L-só: 0,7665 · k-NN sanidade: 0,7000 (acaso 0,2551)
- Tabela 1: BALD ALC 0,8162 [0,7801; 0,8474] · H1 confirmada (4 estratégias batem aleatória com IC que exclui zero)
- H2 parcial: corrosão +0,057 (IC exclui 0); eflorescência +0,055 (IC inclui 0 — só 27 positivos em L)
- H3 refutada: CoreSet não bate aleatória (diversidade pura falha com embeddings fortes)
- H4 não confirmada: calibração similar entre estratégias ativas e aleatória
- **Dizer:** os IC sobrepõem-se todos na Tabela 1 — só a diferença emparelhada (Tabela 2) isola o efeito

### Bloco 5 — Aplicação (3 min) · A4 suporta

- Gradio: fila "anotar a seguir" com razão por recorte (incerteza/diversidade/classe rara provável)
- Previsão oculta por omissão (evitar ancoragem — Rosbach et al. 2026, 7% de reversão)
- Re-treino da cabeça em segundos; curva atualizada em tempo real
- Aviso: "Protótipo experimental; não substitui a inspeção"
- **Dizer:** o que nos distingue de um classificador vulgar é a fila com razão + re-treino em loop

### Bloco 6 — Conclusão e próximos passos (3 min) · A3

- O AL funciona neste regime, mas o efeito é modesto (+0,013 a +0,022 ALC)
- Vale a pena quando: classes raras são críticas; orçamento é muito limitado (<10%)
- Próximos passos: EfficientNet afinada (confirmação); campanha de anotação real; SegCODEBRIM
- **Fechar com:** "Se a aleatória ganhar, o resultado é esse — com análise do porquê. Já acontece na literatura."

---

## Notas de ensaio

- Cronometrar e cortar até 23 min (sobra margem para perguntas antecipadas)
- Ensaio na PL09 (semana 9, 11–12/11)
- Perguntas prováveis: diferença emparelhada vs IC na Tabela 1; porque L estratificado; porque CoreSet falhou; BADGE multi-rótulo vs single-label original

---

## Questões preparadas (qualquer membro deve saber responder)

1. Porque é que a comparação justa para AL é a aleatória com o mesmo orçamento, e não "uma CNN simples"?
2. O bootstrap é por recorte ou por imagem, e por quê?
3. Se o BALD ganha apenas +0,022 de ALC, isso justifica a complexidade adicional?
4. Porque é que o CoreSet (diversidade pura) falha com embeddings de DINOv2?
5. Como é que a ECE multi-rótulo é calculada aqui (marginal por classe)?
