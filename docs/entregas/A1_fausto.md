# A1 — Fausto Cananga (2025102675) · Engenheiro de Dados

> **O que fica em teu nome:** o repositório, as divisões, os embeddings, a medição de redundância.
> **Tempo:** ~90 min de trabalho teu, dos quais ~15 min são o computador a correr.
> **Bloqueias:** A2, A3 e A5. Ninguém commita antes de ti.
>
> Lê cada passo antes de o correres. Numa sessão de perguntas és **tu** que respondes por estes
> números — e a §5 tem as três perguntas que te vão fazer.

## 0. O que já está feito (não refazer)

| Artefacto | Valor medido | Onde |
| --- | --- | --- |
| Recortes utilizáveis | **7 677** (de 1 522 imagens de origem, 30 pontes) | `data/splits.csv` |
| Partições | `train` 6 438 · `val` 611 · `test` 628 | `data/splits.json` |
| Sem classe positiva | **52** excluídos (vetor de rótulos todo a zero) | `docs/contagens_codebrim.json` |
| Fugaz entre partições | **0** grupos em fuga | idem |
| Embeddings | 7 677 × 384, `dinov2_vits14`, 475 s em CPU | `runs/emb_vits14.npy` |
| Sanidade (k-NN k=20) | **0,7000** vs acaso **0,2551** | `paper/resultados.csv` |
| Redundância | **τ = 0,8677** · 21,5% do pool quase-duplicado | `runs/redundancia.json` |

O teu trabalho é **pôr isto num repositório com história** e provar que reproduz. Não é reescrever.

## 1. Criar o repositório — P6.1, R8 (20 min)

1. No GitHub: **New repository** → **Private** → nome real do grupo (não `G1`), por exemplo
   `dl-p2-tema-c-betuminoso`. **Sem** README, sem `.gitignore`, sem licença (já os temos).
2. **Settings → Collaborators** → convida os docentes da UC (os dois endereços do enunciado).
   *Pronto quando:* os convites estão enviados — tira captura de ecrã, é a prova do P6.1.
3. Liga a pasta local:

```powershell
cd "P2/DL_P2_TP2-G1"
git init -b main
git remote add origin https://github.com/<a-tua-conta>/<o-repositorio>.git
```

**Antes do primeiro `git add`, prova que o `.gitignore` faz o que promete** (é o passo que evita
commitar 16 GB):

```bash
git add -A
git status --short | wc -l                       # ~45 ficheiros, nao milhares
git status --short | grep -E "data/raw|\.npy$"    # TEM de dar vazio
```

Se o segundo comando imprimir alguma linha, **pára** e fala comigo: os dados do CODEBRIM não são
redistribuíveis (licença não comercial) e não podem entrar no GitHub.

> Nota técnica que te vai ser útil: o `.gitignore` deste repositório teve de ser corrigido. Os
> comentários em fim de linha **não existem** em `.gitignore` (tudo o que vem depois do padrão faz
> parte do padrão) e `runs/**` sozinho impedia a reinclusão de JSON/CSV aninhados. Agora
> `splits.csv`, `splits.json`, `meta.json` e `rondas.csv` entram; `.npy` e logs ficam fora. Está
> verificado num repositório descartável — podes repetir a prova quando quiseres.

## 2. Commit 1 — a estrutura

```bash
git add .gitignore requirements.txt README.md PENDENTES.md AI_LOG.md \
        docs/papeis/ docs/ENTREGAS.md docs/entregas/
git commit -m "chore: estrutura do repositorio e protecao dos dados nao versionaveis"
git push -u origin main
```

*Inclui:* o `.gitignore` corrigido, o `requirements.txt`, o README, a lista mestra, o registo de IA,
os planos por membro e os guias de entrega. É a base a partir da qual os outros quatro vão trabalhar.

## 3. Commit 2 — divisões e verificação de fugas

Corre de novo os dois comandos (agora o código vai ficar versionado, e é isso que a linha do
`resultados.csv` vai citar):

```bash
python src/dados.py --verificar --gerar-json      # ~13 s
python src/dados.py --determinismo                # ~26 s
```

**Tens de ver:**

```
recortes utilizaveis: 7677   excluidos (vetor todo a zero): 0
particao recortes  imagens  multi  vazio
train        6438     1249   1640      0
val           611      138    183      0
test          628      135    167      0
```

- `7 677` recortes · `train` 6 438 / `val` 611 / `test` 628 · `0` grupos em fuga (nenhuma imagem
  em duas partições)
- **Cuidado com a leitura do "excluídos: 0"**: os **52** recortes sem classe positiva já saíram na
  *geração* do CSV — este comando verifica o ficheiro que já os não tem (confirmado: nenhum dos 52
  caminhos aparece no `splits.csv`). O número e a lista dos caminhos estão em
  `docs/contagens_codebrim.json` (`sem_classe_positiva: 52`). Para reproduzir a exclusão, corre o
  `scripts/contar_codebrim.py` contra o **zip**, não contra o CSV.
- no `--determinismo`: o mesmo primeiro lote para a mesma seed, byte a byte

```bash
git add src/comum.py src/dados.py scripts/contar_codebrim.py \
        data/splits.csv data/splits.json docs/contagens_codebrim.json
git commit -m "feat(A1): divisoes canonicas, verificacao de fugas e L0 com hash"
```

*Porquê `splits.csv` no git e os recortes fora:* a divisão é **metadado** (reproduzível a partir do
zip) e a licença proíbe redistribuir as imagens. Sem o CSV versionado, as três seeds do A3 deixariam
de ser comparáveis.

## 4. Commit 3 — características, sanidade e redundância

```bash
python src/extrair.py --modelo dinov2_vits14    # 475 s; se interromper, retoma
python scripts/sanidade_knn.py                  # k-NN 0,7000 vs acaso 0,2551
python src/redundancia.py                       # tau = 0,8677 (~60 s)
```

*O k-NN é a tua rede de segurança:* se o extrator não separasse nada, todas as curvas do A3 mediriam
ruído e o grupo discutiria o nada. O "acaso" é medido, não assumido — os rótulos de validação são
baralhados e o mesmo k-NN é reavaliado.

```bash
git add src/extrair.py src/redundancia.py scripts/sanidade_knn.py scripts/registar_corridas.py \
        runs/emb_vits14_index.csv runs/emb_vits14_meta.json runs/redundancia.json \
        paper/resultados.csv
git commit -m "feat(A1): caracteristicas DINOv2, sanidade k-NN e redundancia do pool"
```

As linhas de `resultados.csv` vêm com `commit = sem-git` — foram medidas antes de existir
repositório. **Não as apagues à mão:** cada pessoa substitui as suas quando voltar a correr
(`src/comum.py` faz `substituir=True`, portanto repetir não duplica). Diz isso no commit, é mais
honesto do que fingir que os números nasceram versionados.

## 5. Se te perguntarem

**"Porque é que agrupas por imagem e não por ponte?"**
Porque os recortes da mesma imagem partilham iluminação, ângulo e sujidade — se um recorte dessa
imagem for para treino e outro para teste, o modelo reconhece a **fotografia**, não o defeito. O
campo `grupo` do `splits.csv` é a imagem de origem, e a verificação conta grupos em duas partições:
dá **0**. A divisão oficial do CODEBRIM (150 exemplos por classe em validação e em teste) também é
por imagem, não por ponte — não inventámos a regra, seguimo-la.

**"Como sabes que 21,5% do pool é redundante?"**
Porque medi. Calculo a similaridade cosseno entre todos os pares de recortes do pool e entre os
pares que são da mesma imagem: intra-imagem média **0,631**, entre imagens **0,424**. O τ proposto é
o percentil 99,9 dos pares entre imagens diferentes (**0,8677**) — ou seja, acima desse valor só
0,1% dos pares entre imagens distintas aparecem. Aplicando τ, o pool fica com **4 402 grupos** e
**1 387 recortes (21,5%)** são quase-duplicados de um recorte já rotulado. Num drone isto é pior,
porque 30 quadros/s do mesmo defeito são redundância por construção.

**"Porque é que 52 recortes foram excluídos?"**
Porque o vetor de rótulos deles é todo a zero: a pasta diz `defects` mas as etiquetas XML não têm
nenhuma das cinco classes. Se ficassem, seriam 52 falsos "background" e o macro-F1 da classe
`Background` subiria artificialmente. Excluir é uma decisão registada, não uma limpeza silenciosa.

## 6. Registo e revisão

Acrescenta a tua linha ao [`AI_LOG.md`](../../AI_LOG.md) **neste commit**, com a coluna *"como
verificou"* preenchida a sério (ex.: `0 grupos em fuga · 7 677 linhas no splits.csv · exit 0`).

Na PL11 és tu que revês o **registo** (não o código): confirma que todas as linhas do
`resultados.csv` têm commit preenchido e que os hashes de `L0` no `splits.json` batem com os seeds
0/1/2. Se encontrares uma linha sem commit, é bug de quem a escreveu, não teu — abre uma issue.

## 7. O que continua teu e ainda não está feito

| Item | Quando | Nota |
| --- | --- | --- |
| Inspeção visual de 5 recortes por classe (**C1.2b**) | antes da PL09 | 25 imagens vistas, com uma nota no `README`; é o que separa "contei" de "vi" |
| Exportar o P2-D1 para PDF e submeter no Moodle (**P7.1**) | 28/10 | o `.md` está pronto em `docs/P2-D1.md` |
| `PROTOCOLO.md` fechado e **com tag** antes de olhar para o teste (**C2.6**) | 12/11 | `git tag protocolo-v1`; é o que separa resultado confirmatório de exploratório |
| Pedido obrigatório **IA-5** (fugas, métricas inadequadas, comparações injustas) | 12/11 | três decisões críticas, escritas, no `AI_LOG.md` |
