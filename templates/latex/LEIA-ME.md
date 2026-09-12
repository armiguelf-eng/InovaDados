# Template LaTeX do relatório de iniciativa

`relatorio.tex` é o esqueleto do relatório gerado pela skill
`documentar-iniciativa`. Editar aqui muda **todos** os relatórios; a cópia
gerada dentro da pasta do card é descartável e não deve ser editada à mão.

## Estrutura fixa

| Página | Conteúdo |
| --- | --- |
| 1 | Capa: nome da iniciativa centralizado + subtítulo (`Inovação <ciclo>`) |
| 2 | Sumário |
| 3 | Resumo executivo (`resumoexecutivo.md`) |
| 4 | Introdução (`templates/introducao.md`, preenchida a partir do `card.md`) |
| 5+ | Atas transcritas (`benchmarks/bm-*.md`), se existirem |
| depois | Frameworks de discovery (`discovery/fw-*.md`) |

A marca d'água da Poli Júnior é aplicada em todas as páginas, inclusive na capa.

## Marca d'água

O gerador procura, sob `templates/`, o arquivo `logo-polijunior.png`
(aceita também `.pdf` e `.jpg`). A busca é recursiva, então o arquivo funciona
tanto em `templates/` quanto em subpastas.

Requisitos: fundo transparente e lado maior de pelo menos 1000 px — a marca
ocupa 65% da largura da página e é aplicada com 6% de opacidade.

Este é o único binário que o repositório aceita. O PDF compilado é saída
derivada e não entra no versionamento.

## Ajustes comuns

- **Cor institucional:** `\definecolor{pjazul}` no preâmbulo.
- **Intensidade da marca:** `opacity=0.06` no bloco `\AddToShipoutPictureBG`.
- **Tamanho da marca:** `width=0.65\paperwidth` no mesmo bloco.
- **Subtítulo:** vem do campo `ciclo` do `card.md`; sobrescreva na chamada com
  `--subtitulo`.

## Compilação

O `.tex` precisa de duas passagens para o sumário resolver:

```bash
cd <pasta-do-card>/relatorio
pdflatex relatorio.tex && pdflatex relatorio.tex
```

Pacotes usados, todos presentes em uma TeX Live completa: `babel`, `geometry`,
`graphicx`, `eso-pic`, `tikz`, `fancyhdr`, `titlesec`, `enumitem`, `xcolor`,
`booktabs`, `microtype`, `hyperref`.
