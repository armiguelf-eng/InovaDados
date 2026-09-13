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
│  ├─ abrir-iniciativa/        cria a pasta da iniciativa a partir de um card do Notion
│  ├─ fechar-iniciativa/       fecha a sprint: confere, gera o relatório e anexa o PDF ao card
│  ├─ documentar-iniciativa/   gera o relatório LaTeX de uma iniciativa fechada
│  └─ sincronizar-readme/      mantém este README fiel ao repositório
└─ iniciativas/
   └─ pricing-ndados/
```

Um card do Notion corresponde a uma pasta de iniciativa. Tudo que aquele card produziu fica dentro dela:

```
iniciativas/<iniciativa>/
├─ materials/          insumo: o que entrou no card
│  ├─ card.md
│  └─ tasks.md
├─ artefatos/          produto: o que o card gerou
│  ├─ resumoexecutivo.md
│  ├─ introducao.md
│  ├─ benchmarks/<primeiro-nome>-bench.md
│  └─ discovery/<FRAMEWORK>.md
└─ relatorio/          saída do gerador LaTeX
```

`materials/` guarda o que descreve o card e veio do Notion; `artefatos/` guarda o
que a iniciativa produziu e será lido daqui a um ano. `relatorio/` é saída
derivada e fica fora dos dois.

## Fronteira da iniciativa

Dentro da pasta: o que foi produzido naquele ciclo e não muda depois. Atas, análises, dados, resumo.

Teste: **se o próximo card vai editar o arquivo, ele não pertence a esta pasta** — abra uma iniciativa nova.

Iniciativa fechada é imutável. Correção posterior entra como nota na iniciativa seguinte, não como edição retroativa.

## Templates

| Template              | Contém                                                                                       | Não contém                            | Organização                                                                                                                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `card.md`             | Por quê, objetivo, métricas de sucesso, DOD (básico e outlier), link do card no Notion       | Checklist, prioridade, nota, TE       | Card preenchido no Notion. Agente cria novo arquivo e completa com o que está no Notion.                                                                                                                           |
| `tasks.md`            | Execução do card quebrada em fases, com checkboxes                                           | Conclusão ou aprendizado              | Tasks preenchidas no Notion. Agente cria novo arquivo e completa com o que está no Notion.                                                                                                                         |
| `benchmark.md`        | Ata: perguntas e respostas, depois síntese em objeções / surpresas / oportunidades / ameaças | Conclusão misturada ao registro bruto | Usuário cria arquivo, preenche com as perguntas. Duas opções nas respostas: ou usuário envia a transcrição da conversa e agente preenche as respostas, ou usuário preenche manualmente. Síntese feita pelo agente. |
| `resumoexecutivo.md`  | Síntese do card em até 100 palavras                                                          | Detalhe de execução                   | Usuário cria e preenche arquivo.                                                                                                                                                                                   |
| `frameworks/CSD.md`   | Matriz CSD: certezas, suposições, dúvidas                                                    | Dado bruto                            | Usuário cria e preenche arquivo.                                                                                                                                                                                   |
| `frameworks/SWOT.md`  | Análise SWOT: strengths, weaknesses, opportunities, threats                                  | Dado bruto                            | Usuário cria e preenche arquivo.                                                                                                                                                                                   |
| `introducao.md`       | Texto padrão da introdução do relatório, com marcadores preenchidos do `card.md`             | Conclusão do card                     | Usuário cria e preenche arquivo.                                                                                                                                                                                   |
| `latex/relatorio.tex` | Esqueleto do relatório: capa, marca d'água, sumário, ordem das seções                        | Conteúdo de iniciativa                | Agente capta os arquivos .md criados, transcreve usando o código. Cria PDF e salva na pasta destinada.                                                                                                             |

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
tipo: card | tasks | benchmark | resumo-executivo | introducao | csd | swot
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

- `card` é o slug da pasta da iniciativa e amarra qualquer documento ao seu ciclo de origem.
- `link (Notion)` é o caminho de volta para a governança — nunca duplique o conteúdo do card do Notion aqui.
- `link (Call)` aponta para a gravação no storage; a gravação em si não entra no repositório.
- Em framework, use `origem` com a lista de IDs que embasam a análise.

## Convenções

- Pasta de iniciativa: slug curto, ex. `pricing-ndados`. Uma pasta por card do Notion, com `materials/` e `artefatos/` dentro.
- Nomes de arquivo e pasta: minúsculas, sem acento, separados por hífen. Única exceção: o framework, que usa a sigla como o mercado a escreve (`CSD.md`, `SWOT.md`).
- Nome da ata: `<primeiro-nome-do-entrevistado>-bench.md`, ex. `rafael-bench.md`. Dois entrevistados de mesmo primeiro nome no mesmo card ganham sobrenome (`rafael-toledo-bench.md`).
- Nome do framework: o nome do próprio framework, ex. `CSD.md`, `SWOT.md`. Um por tipo por card.
- Prefixos de ID: `bm-` benchmark, `fw-` framework. O prefixo vive no campo `id`, não no nome do arquivo — os dois deixaram de coincidir de propósito, para que o arquivo seja legível na pasta e o ID continue estável. Documentos únicos da iniciativa (`card`, `tasks`, `resumoexecutivo`) usam o próprio nome da pasta.
- Referência entre documentos sempre por ID, nunca por caminho ou título. Renomear um arquivo nunca quebra uma referência.
- Uma pergunta por heading nas atas.

## Relatório da iniciativa

Iniciativa fechada vira um relatório LaTeX de estrutura fixa, gerado pela skill
`documentar-iniciativa`:

```bash
python3 .claude/skills/documentar-iniciativa/scripts/gerar_relatorio.py \
  iniciativas/<iniciativa>
```

| Página | Fonte |
| --- | --- |
| 1 — capa | nome da iniciativa + `Inovação <ciclo>` |
| 2 | sumário |
| 3 | `artefatos/resumoexecutivo.md` |
| 4 | `artefatos/introducao.md`, ou `templates/introducao.md` se a iniciativa não tiver a sua, preenchida a partir do `card.md` |
| 5+ | uma página por ata (`artefatos/benchmarks/<primeiro-nome>-bench.md`) |
| depois | uma página por framework (`artefatos/discovery/<FRAMEWORK>.md`) |

Marca d'água da Poli Júnior em todas as páginas, a partir de
`templates/logo-polijunior.png`.

A saída vai para `<iniciativa>/relatorio/` e **não é editada à mão**: correção de
conteúdo vai no markdown da iniciativa, correção de forma vai em
`templates/latex/relatorio.tex`. O `.tex` é o fonte versionável; o PDF é saída
derivada e está no `.gitignore`.

Compilar exige duas passagens, para o sumário resolver:

```bash
cd iniciativas/<iniciativa>/relatorio
pdflatex relatorio.tex && pdflatex relatorio.tex
```

## Não entra neste repositório

- Planilha viva ou colaborativa (fica no Drive, link no `card.md`)
- PDF, deck ou binário compilado (o fonte entra, a saída não) — única exceção: `templates/logo-polijunior.png`, a marca d'água do relatório
- Gravação e transcrição bruta (ficam no storage, link no frontmatter)
- Dado de cliente identificável, credencial, valor nominal de proposta

## Fluxo

Abrir card, pela skill `abrir-iniciativa`:

1. Criar `iniciativas/<iniciativa>/`, com `materials/` dentro. O slug sai do nome do card no Notion.
2. Copiar `templates/card.md` e `templates/tasks.md` para `materials/`, preencher o frontmatter.
3. Colar o link do card no Notion em `link (Notion)`.

Durante o card: cada call vira um `artefatos/benchmarks/<primeiro-nome>-bench.md`; cada framework derivado vira um `artefatos/discovery/<FRAMEWORK>.md` com `origem` apontando para os benchmarks.

Fechar card, pela skill `fechar-iniciativa`, quando o usuário avisar que a sprint acabou: `artefatos/resumoexecutivo.md` preenchido, `tasks.md` sem pendência aberta, seção `# Rascunho` das atas removida, relatório gerado e PDF anexado ao card no Notion.

Toda mudança entra por pull request, inclusive ata nova. Na descrição do PR: link do card no Notion e IDs afetados.

## Pendências

O que este README descreve e ainda não existe:

- [ ] Template de Learning Card (`aprendizados.md`), para fechar o ciclo de hipótese → observação → aprendizado
- [ ] Template de ADR, se o repositório passar a guardar registro de decisão
- [ ] Validador de frontmatter e gerador de índice, rodando no CI a cada PR
- [ ] `verificar_card.py`, validador de card fechado compartilhado por `fechar-iniciativa` e `documentar-iniciativa` (hoje a conferência é manual nas duas)

## Dono

<!-- nome do responsável pelos templates, com sucessor previsto na virada de time -->
