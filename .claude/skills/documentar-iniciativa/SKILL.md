---
name: documentar-iniciativa
description: Gera o relatório LaTeX de uma iniciativa do InovaDados a partir de um card fechado (materials/card.md, artefatos/resumoexecutivo.md, artefatos/benchmarks/<primeiro-nome>-bench.md, artefatos/discovery/<FRAMEWORK>.md), com marca d'água da Poli Júnior, capa, sumário, resumo executivo, introdução, atas transcritas e frameworks. Use quando o usuário pedir para "documentar a iniciativa", "gerar o relatório", "fechar em PDF", "exportar o card para LaTeX", "montar o documento final" ou apontar para uma pasta de card concluído.
---

# Documentar iniciativa em LaTeX

Transforma um card fechado do InovaDados num relatório LaTeX de estrutura fixa.
O `.tex` é o artefato versionável; o PDF é saída derivada e fica fora do git.

## Estrutura produzida

| Página | Fonte |
| --- | --- |
| 1 — capa | nome da iniciativa centralizado + `Inovação <ciclo>` |
| 2 — sumário | automático |
| 3 — resumo executivo | `artefatos/resumoexecutivo.md` |
| 4 — introdução | `artefatos/introducao.md`, ou `templates/introducao.md` se ausente; marcadores preenchidos do `card.md` |
| 5+ — atas | `artefatos/benchmarks/<primeiro-nome>-bench.md`, em ordem de ID (omitida se não houver) |
| depois — frameworks | `artefatos/discovery/<FRAMEWORK>.md`, em ordem de ID |

Marca d'água da Poli Júnior em todas as páginas, capa inclusive.

## Passo a passo

### 1. Identifique a pasta da iniciativa

O alvo é uma pasta `iniciativas/<iniciativa>/` que contenha `materials/card.md`. Uma pasta
de iniciativa corresponde a um card do Notion, e o relatório é por iniciativa.
Se o usuário citar um nome que não casa com nenhuma pasta, **pergunte qual** —
não escolha a mais recente por conta própria.

### 2. Verifique se o card está de fato fechado

Antes de gerar, confira com `cat`/`grep` — o gerador avisa, mas não corrige:

- `artefatos/resumoexecutivo.md` existe e está preenchido (limite de 100 palavras);
- nenhuma ata tem `# Rascunho` com conteúdo (o gerador o remove do PDF e avisa);
- `materials/tasks.md` sem checkbox aberto (`grep -c '\- \[ \]' materials/tasks.md`);
- todo framework em `artefatos/discovery/` declara `origem` com os IDs das atas que o embasam.

Se algo falhar, **relate ao usuário e pergunte** se gera assim mesmo. Um card
não fechado gera um relatório que documenta trabalho inacabado.

### 3. Gere

```bash
python3 .claude/skills/documentar-iniciativa/scripts/gerar_relatorio.py \
  iniciativas/<iniciativa>
```

Opções: `-o <dir>` (saída; padrão `<card>/relatorio`), `--titulo` (sobrescreve o
nome da iniciativa), `--subtitulo` (sobrescreve `Inovação <ciclo>`).

O script aborta se a marca d'água não for encontrada e imprime avisos em stderr.
**Leia os avisos e repasse todos ao usuário** — eles apontam problemas no card,
não no gerador.

### 4. Compile, se houver compilador

```bash
command -v lualatex >/dev/null && (cd <saida> && lualatex -interaction=nonstopmode relatorio.tex >/dev/null && lualatex -interaction=nonstopmode relatorio.tex >/dev/null)
```

Duas passagens: o sumário só resolve na segunda. Sem `lualatex` instalado,
entregue o `.tex` e diga ao usuário que a compilação não foi verificada — não
finja que o PDF saiu.

### 5. Confira antes de entregar

Leia o `.tex` gerado. Os erros que aparecem na prática:

- seção `% seção vazia` — o markdown de origem estava vazio;
- `**[preencher: X]**` na introdução — marcador sem valor no `materials/card.md`;
- placeholders do template (`<Título do Card>`, `<Resposta>`) que vazaram para
  o relatório porque ninguém preencheu o markdown.

Todos são problema do card, não do gerador. Aponte o arquivo de origem.

## O que NÃO fazer

- **Não edite o `.tex` gerado.** Ele é descartável e some na próxima geração.
  Correção de conteúdo vai no markdown do card; correção de forma vai em
  `templates/latex/relatorio.tex`.
- **Não edite o markdown do card para "melhorar" o relatório.** Card fechado é
  imutável neste repositório. Se o conteúdo está errado, isso é nota no card
  seguinte — avise o usuário em vez de reescrever.
- **Não comite o PDF.** O README proíbe binário compilado; só a marca d'água é
  exceção.

## Arquivos da skill

- `scripts/gerar_relatorio.py` — parser de markdown/frontmatter e montagem do `.tex`.
- `templates/latex/relatorio.tex` (no repo) — preâmbulo, capa, marca d'água, sumário.
- `templates/introducao.md` (no repo) — texto padrão da introdução, com marcadores
  `{{iniciativa}}`, `{{ciclo}}`, `{{nucleo}}`, `{{porque}}`, `{{objetivo}}`, `{{metricas}}`.

Para mudar o texto da introdução de **uma** iniciativa, copie `introducao.md`
para dentro da pasta do card e escreva à mão — o gerador prefere a cópia local.
