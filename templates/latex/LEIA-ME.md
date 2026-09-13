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

Requisitos: fundo transparente e lado maior de pelo menos 1000 px. A marca é
aplicada com 6% de opacidade e sua **tinta** ocupa 65% da largura da página,
centrada na página.

O gerador mede onde a tinta do arquivo começa e termina e emite um
`trim=...,clip` para o template. Sem esse recorte, a margem transparente do
arquivo entraria na conta: a marca encolheria e sairia do centro óptico. Isso
torna o resultado independente de quanto padding o arquivo do logo tem — trocar
o logo por um com proporção diferente não exige mexer no template.

A medição só funciona em PNG de 8 bits não entrelaçado. Para `.pdf` ou `.jpg` o
recorte é omitido e vale a tela inteira do arquivo.

Junto com as fontes em `fonts/`, é um dos binários que o repositório aceita.
O PDF compilado é saída derivada e não entra no versionamento.

## Formatação

Regras fixas do documento, todas no preâmbulo de `relatorio.tex`:

| Item | Valor |
| --- | --- |
| Fonte dos títulos | Host Grotesk |
| Fonte do texto corrido | Nunito Sans |
| Corpo | 11 pt |
| Entrelinha | 1,5 (`\onehalfspacing`) |
| Papel | A4 (210 × 297 mm), retrato |
| Margens superior/inferior | 2,5 cm |
| Margens esquerda/direita | 3 cm |
| Alinhamento | Justificado |
| Cabeçalho | Vazio |
| Rodapé | Iniciativa à esquerda, ciclo ao centro, número da página à direita |
| Cor dos títulos principais e do texto | Preto |
| Cor dos demais títulos | `#7239AF` (`pjroxo`) |

"Títulos principais" são a capa e as `\section` (resumo executivo, introdução,
cada ata, cada framework). "Demais títulos" são `\subsection` e abaixo, que vêm
dos headings internos do markdown.

## Fontes

Host Grotesk e Nunito Sans não existem no TeX Live e não podem ser assumidas
como instaladas na máquina, então os `.ttf` moram em `templates/latex/fonts/` e
o gerador os copia para `<pasta-do-card>/relatorio/assets/fontes/`. O template
os carrega por caminho relativo — o relatório compila em qualquer clone, sem
instalar nada no sistema.

Os dois arquivos são *variable fonts* (eixo `wght`), então cada peso é pedido
pelo eixo, não por um arquivo estático:

```latex
BoldFeatures = {RawFeature={axis={wght=700}}}
```

`BoldFont`/`ItalicFont` precisam nomear o arquivo mesmo quando é o mesmo da
versão normal. Sem isso, o fontspec não registra a forma e o `\textbf` cai
silenciosamente no peso regular, sem erro de compilação.

Ambas são licenciadas sob a OFL; o texto da licença está em
`fonts/OFL-HostGrotesk.txt` e `fonts/OFL-NunitoSans.txt` e precisa acompanhar
os arquivos.

## Ajustes comuns

- **Cor de destaque dos subtítulos:** `\definecolor{pjroxo}` no preâmbulo.
- **Intensidade da marca:** `opacity=0.06` no bloco `\AddToShipoutPictureBG`.
- **Tamanho da marca:** `width=0.65\paperwidth` no mesmo bloco.
- **Rodapé:** `\fancyfoot[L/C/R]` no preâmbulo. O cabeçalho é vazio de
  propósito (`\headrulewidth` = 0).
- **Subtítulo:** vem do campo `ciclo` do `card.md`; sobrescreva na chamada com
  `--subtitulo`.

## Compilação

O `.tex` precisa de duas passagens para o sumário resolver:

```bash
cd <pasta-do-card>/relatorio
lualatex relatorio.tex && lualatex relatorio.tex
```

Precisa ser `lualatex`, não `pdflatex`: as fontes da identidade são OpenType e
só o fontspec sob lualatex/xelatex as carrega.

Pacotes usados, todos presentes em uma TeX Live completa: `babel`, `geometry`,
`setspace`, `fontspec`, `graphicx`, `eso-pic`, `tikz`, `fancyhdr`, `titlesec`,
`enumitem`, `xcolor`, `booktabs`, `microtype`, `hyperref`.
