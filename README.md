# InovaDados

## Objetivo

Guardar os artefatos produzidos pelas iniciativas de inovação da Poli Júnior: atas de benchmark, frameworks de discovery, resumos executivos e registro de decisões.

A governança fica no Notion (status, ciclo, DOD, prioridade, responsáveis, checklist, nota, TE). Não espelhe esses campos aqui.

| Conteúdo | Local |
| --- | --- |
| Muda de estado a cada semana | Notion |
| Controle de execução do ciclo | Notion |
| Evidência de campo ou conclusão derivada dela | Este repositório |
| Artefato que será lido em um ano | Este repositório |

## Estrutura

```
InovaDados/
├─ README.md
├─ templates/
│  ├─ card.md
│  ├─ benchmark.md
│  ├─ tasks.md
│  ├─ resumoexecutivo.md
│  ├─ introducao.md
│  ├─ logo-polijunior.png
│  ├─ frameworks/
│  │  ├─ CSD.md
│  │  └─ SWOT.md
│  └─ latex/
│     ├─ relatorio.tex
│     └─ LEIA-ME.md
├─ .claude/skills/
│  └─ documentar-iniciativa/   gera o relatório LaTeX de um card fechado
└─ iniciativas/
```

Um card do Notion corresponde a uma pasta. Tudo que aquele card produziu fica dentro dela:

```
iniciativas/<iniciativa>/
├─ cards/
│  └─ <ciclo>-<tipo-do-card>/
│     ├─ card.md
│     ├─ tasks.md
│     ├─ resumoexecutivo.md
│     ├─ benchmarks/bm-*.md
│     └─ discovery/fw-*.md
└─ (raiz da iniciativa: o que sobrevive ao card)
```

## Fronteira do card

Dentro da pasta do card: o que foi produzido naquele ciclo e não muda depois. Atas, análises, dados, resumo.

Na raiz da iniciativa: o que continua vivo e é revisado por cards seguintes. Especificação, decisões.

Teste: **se o próximo card vai editar o arquivo, ele não pertence a este card.**

Card fechado é imutável. Correção posterior entra como nota no card seguinte, não como edição retroativa.

## Templates

| Template | Contém | Não contém |
| --- | --- | --- |
| `card.md` | Por quê, objetivo, métricas de sucesso, DOD (básico e outlier), link do card no Notion | Checklist, prioridade, nota, TE |
| `tasks.md` | Execução do card quebrada em fases, com checkboxes | Conclusão ou aprendizado |
| `benchmark.md` | Ata: perguntas e respostas, depois síntese em objeções / surpresas / oportunidades / ameaças | Conclusão misturada ao registro bruto |
| `resumoexecutivo.md` | Síntese do card em até 100 palavras | Detalhe de execução |
| `frameworks/CSD.md` | Matriz CSD: certezas, suposições, dúvidas | Dado bruto |
| `frameworks/SWOT.md` | Análise SWOT: strengths, weaknesses, opportunities, threats | Dado bruto |
| `introducao.md` | Texto padrão da introdução do relatório, com marcadores preenchidos do `card.md` | Conclusão do card |
| `latex/relatorio.tex` | Esqueleto do relatório: capa, marca d'água, sumário, ordem das seções | Conteúdo de iniciativa |

Regras de conteúdo:

- A ata separa **registro** de **interpretação**: o que foi dito vai em `# Perguntas`, uma pergunta por heading; toda conclusão vai em `# Síntese`. O que ainda não está maduro fica em `# Rascunho` e some antes do card fechar.
- Todo framework declara em `origem` os IDs dos benchmarks que o embasam. Framework sem origem não é rastreável.
- `id` é único em todo o repositório e imutável após criação.
- `card` bate com o nome da pasta onde o arquivo está.
- Gráfico é saída derivada: dado versionado, script que gera, figura no card.

## Frontmatter

Obrigatório no topo de todo documento, em YAML, entre `---`.

Campos comuns a todos os templates:

```yaml
---
id:
tipo: card | tasks | benchmark | resumo-executivo | csd | swot
card:
ciclo:
nucleo:
status:
link (Notion):
---
```

O benchmark acrescenta:

```yaml
entrevistador:
entrevistado:
data:
link (Call):
```

- `card` amarra qualquer documento ao seu ciclo de origem.
- `link (Notion)` é o caminho de volta para a governança — nunca duplique o conteúdo do card do Notion aqui.
- `link (Call)` aponta para a gravação no storage; a gravação em si não entra no repositório.
- Em framework, use `origem` com a lista de IDs que embasam a análise.

## Convenções

- Pasta de card: `<ciclo>-<tipo-do-card>`, ex. `26-1-revisao-de-execucao`.
- Pasta de iniciativa: slug curto, ex. `pricing-ndados`.
- Nomes de arquivo e pasta: minúsculas, sem acento, separados por hífen.
- Prefixos de ID: `bm-` benchmark, `fw-` framework. Documentos únicos do card (`card`, `tasks`, `resumoexecutivo`) usam o próprio nome da pasta do card.
- Referência entre documentos sempre por ID, nunca por caminho ou título.
- Uma pergunta por heading nas atas.

## Relatório da iniciativa

Card fechado vira um relatório LaTeX de estrutura fixa, gerado pela skill
`documentar-iniciativa`:

```bash
python3 .claude/skills/documentar-iniciativa/scripts/gerar_relatorio.py \
  iniciativas/<iniciativa>/cards/<ciclo>-<tipo>
```

| Página | Fonte |
| --- | --- |
| 1 — capa | nome da iniciativa + `Inovação <ciclo>` |
| 2 | sumário |
| 3 | `resumoexecutivo.md` |
| 4 | `templates/introducao.md`, preenchida a partir do `card.md` |
| 5+ | uma página por ata (`benchmarks/bm-*.md`) |
| depois | uma página por framework (`discovery/fw-*.md`) |

Marca d'água da Poli Júnior em todas as páginas, a partir de
`templates/logo-polijunior.png`.

A saída vai para `<card>/relatorio/` e **não é editada à mão**: correção de
conteúdo vai no markdown do card, correção de forma vai em
`templates/latex/relatorio.tex`. O `.tex` é o fonte versionável; o PDF é saída
derivada e está no `.gitignore`.

Compilar exige duas passagens, para o sumário resolver:

```bash
cd iniciativas/<iniciativa>/cards/<ciclo>-<tipo>/relatorio
pdflatex relatorio.tex && pdflatex relatorio.tex
```

## Não entra neste repositório

- Planilha viva ou colaborativa (fica no Drive, link no `card.md`)
- PDF, deck ou binário compilado (o fonte entra, a saída não) — única exceção: `templates/logo-polijunior.png`, a marca d'água do relatório
- Gravação e transcrição bruta (ficam no storage, link no frontmatter)
- Dado de cliente identificável, credencial, valor nominal de proposta

## Fluxo

Abrir card:

1. Criar `iniciativas/<iniciativa>/cards/<ciclo>-<tipo>/`.
2. Copiar `templates/card.md` e `templates/tasks.md` para dentro, preencher o frontmatter.
3. Colar o link do card no Notion em `link (Notion)`.

Durante o card: cada call vira um `benchmarks/bm-*.md`; cada framework derivado vira um `discovery/fw-*.md` com `origem` apontando para os benchmarks.

Fechar card: `resumoexecutivo.md` preenchido, `tasks.md` sem pendência aberta, seção `# Rascunho` das atas removida, alteração na raiz da iniciativa mergeada.

Toda mudança entra por pull request, inclusive ata nova. Na descrição do PR: link do card no Notion e IDs afetados.

## Pendências

O que este README descreve e ainda não existe:

- [ ] Nenhuma iniciativa criada — `iniciativas/` ainda não existe
- [ ] Template de Learning Card (`aprendizados.md`), para fechar o ciclo de hipótese → observação → aprendizado
- [ ] Template de ADR, se o repositório passar a guardar registro de decisão
- [ ] `tasks.md` está sem os delimitadores `---` no frontmatter
- [ ] `resumoexecutivo.md` tem `tipo: resumo exeutivo` (typo) e os valores de `tipo` variam em acento e caixa entre templates
- [ ] Validador de frontmatter e gerador de índice, rodando no CI a cada PR

## Dono

<!-- nome do responsável pelos templates, com sucessor previsto na virada de time -->
