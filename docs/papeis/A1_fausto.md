# A1 — Fausto Cananga (2025102675) · Engenheiro de Dados

> **Missão:** garantir que os dados, as divisões e o registo são irrepreensíveis. Se houver uma fuga
> de dados ou uma contagem errada no relatório, a responsabilidade para aqui.

## O que só tu decides

1. **Que versão do dataset entra** e se o md5 confere (já está decidido: `classification_dataset`;
   falta confirmares a integridade).
2. **A regra de estratificação de `L`** em multi-rótulo (com o A3) — é o que torna as 3 seeds
   comparáveis. Sem isto o protocolo não fecha.
3. **O formato canónico das divisões**: `data/splits.csv` (colunas `path,label,grupo,split`) e
   `splits.json` só com hashes e listas `L0`.
4. **O nome final do repositório** (grupo real, não `G1`).

## Próximas duas semanas

| Quando | Tarefa (ID) | Pronto quando |
| --- | --- | --- |
| 27/10 | Repositório privado no GitHub, docentes como colaboradores, nome correto (**P6.1**, **R8**) | Os docentes recebem o convite |
| ✅ 27/10 | Descarregar, confirmar `md5` e **contar** os recortes (**C1.1**, **C1.2**) | **Feito**: 7,9 GB, md5 conferido, 7 677 utilizáveis, 52 sem rótulo excluídos, 0 imagens em duas partições |
| 28/10 | Gerar `splits.json` com **hashes** e as listas `L0` por seed (**C1.7**) | Hash por seed no `splits.json` |
| 28/10 | **Inspeção visual** de 5 recortes por classe (**C1.2b**) | 25 imagens vistas, com nota no `README` |
| 28/10 | Exportar o P2-D1 para PDF e **submeter no Moodle** antes da aula (**P7.1**) | Confirmação de submissão |
| 28/10 | Extração **DINOv2 ViT-S/14** de todos os recortes → `runs/emb_vits14.npy` (**C1.3**) | Shape coerente com a contagem de recortes |
| 28/10 | Sanidade: **k-NN (k=20)** na validação acima do acaso, embeddings normalizados (**C1.4**) | Macro-F1 registado em `resultados.csv` |
| 29/10 | Registar o feedback do docente no `README` com decisão e responsável (**P7.4**, **P8.1**) | Tabela preenchida |
| 29/10 | Declarar a licença **AGPL-3.0** do Ultralytics se o guia de deteção entrar no repo (**P7.7**) | Linha no `README` §8 |
| 05/11 | `src/dados.py` + `verificar()`; `python src/dados.py --verificar` sem erro; determinismo do 1.º lote (**P8.2–P8.5**) | Duas execuções, mesmo lote |
| 05/11 | Esquema do `resultados.csv` (data, commit, config, métrica val, tempo) (**P8.7**) | Uma linha real da baseline |
| 12/11 | `PROTOCOLO.md` **fechado e versionado** antes de qualquer avaliação no teste (**C2.6**) | Commit com tag |
| 12/11 | Pedido obrigatório **IA-5** (fugas, métricas, comparações injustas) e decisão crítica a crítica | `AI_LOG.md` preenchido |
| 12/11 | **Medir a redundância do pool** e propor o limiar `τ` de quase-duplicados (**D1**, `docs/DRONE.md`) | Distribuição de similaridades + `τ` justificado |

## Ângulo drone (o que te toca)

O pool de um drone é **vídeo**: precisa de agrupamento de quase-duplicados antes de cada aquisição.
A tua parte é medir a redundância que já existe no CODEBRIM (recortes da mesma imagem são quase
duplicados por construção) e propor o `τ`. É a medição que permite ao A3 implementar a aquisição sem
que ela escolha 20 vezes o mesmo defeito.

## Par de revisão e leituras

- **Revisão cruzada (PL11):** o teu trabalho é revisto **pelo grupo na aplicação** (não tens par fixo).
  Tu não revês o código de ninguém — revês o **registo**: `resultados.csv` e `splits.json`.
- **Leituras:** Mundt et al. 2019 §3 e §4.1 (aquisição e divisão) · DLwP Cap. 6 (fluxo do projeto) ·
  Munjal et al. 2022 (reprodutibilidade — a tua bíblia).
- **Questões escritas:** PL06 Q3 (unidade de agrupamento) · PL08 Q2 (porque se regista commit e config).

## Dependências

Bloqueias: **A2** (precisa das divisões para o teto), **A3** (precisa do `splits.csv` para as rondas),
**A5** (precisa dos embeddings para as curvas). Bloqueado por: ninguém — és o primeiro da fila.
