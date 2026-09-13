---
name: fechar-iniciativa
description: Fecha uma iniciativa do InovaDados no fim da sprint — confere o que há em materials/ e artefatos/, gera o relatório LaTeX pela skill documentar-iniciativa, compila o PDF e anexa esse PDF ao card correspondente no Laboratório de Inovação do Notion. Use quando o usuário disser "a sprint acabou", "o card fechou", "fecha a iniciativa", "sobe o relatório pro Notion", "anexa o PDF no card" ou avisar que terminou o ciclo de um card.
---

# Fechar iniciativa no fim da sprint

Quem decide que a sprint acabou é o usuário, não esta skill. Ela não adivinha
fechamento a partir de checkbox marcado — ela responde ao aviso.

O que ela faz: confere a pasta, gera o relatório, compila e **anexa o PDF ao card
do Notion**. Esse último passo sai do repositório e vai para fora — é o único
irreversível do fluxo, e a skill inteira existe para chegar nele com segurança.

## Passo 1 — identificar a iniciativa

O alvo é uma pasta `iniciativas/<slug>/` com `materials/card.md` dentro. Se o
usuário citar um nome que não casa com nenhuma pasta, **pergunte qual** — não
escolha a mais recente por conta própria.

Leia `materials/card.md` e guarde `ciclo`, `nucleo`, `status` e, sobretudo,
`link (Notion)`. É esse link que o Passo 5 usa.

## Passo 2 — conferir o que está na pasta

Este passo aponta problema; ele não corrige nada. Enquanto o
`scripts/verificar_card.py` não existir, faça à mão:

```bash
INI=iniciativas/<slug>
ls -R $INI
grep -c '^- \[ \]' $INI/materials/tasks.md          # task aberta
grep -rln '^# Rascunho' $INI/artefatos/benchmarks/  # rascunho não removido
grep -rLn '^origem:' $INI/artefatos/discovery/      # framework sem origem
wc -w $INI/artefatos/resumoexecutivo.md             # limite de 100 palavras
```

O que tem que estar de pé para o card contar como fechado:

- `artefatos/resumoexecutivo.md` existe e está preenchido, em até 100 palavras;
- `materials/tasks.md` sem checkbox aberto;
- nenhuma ata com seção `# Rascunho` sobrando;
- todo framework em `artefatos/discovery/` declara `origem` com os IDs das atas
  que o embasam;
- nenhum placeholder de template vazou (`<Título do Card>`, `Task A`, `<nome>`).

Se `link (Notion)` estiver vazio, resolva agora: busque o card com
`notion-search` (palavras-chave curtas — `ai_search` não está disponível neste
workspace), confirme com o usuário e **grave o link no frontmatter**. Sem ele o
Passo 5 não acontece.

**Falhou alguma coisa? Relate tudo de uma vez e pergunte se gera assim mesmo.**
Card não fechado gera relatório que documenta trabalho inacabado — e, pior aqui
do que na `documentar-iniciativa`, esse relatório vai parar no Notion.

## Passo 3 — gerar o relatório

Invoque a skill `documentar-iniciativa` e siga o que ela manda. Ela é o motor:
é dela o parser, o template LaTeX e a lista de avisos. **Não duplique a lógica
dela aqui, e não chame o gerador por fora para pular as conferências dela.**

Leia os avisos que o gerador imprime em stderr e repasse todos ao usuário.

## Passo 4 — compilar o PDF

```bash
cd iniciativas/<slug>/relatorio
lualatex -interaction=nonstopmode relatorio.tex >/dev/null
lualatex -interaction=nonstopmode relatorio.tex >/dev/null
```

Duas passagens: o sumário só resolve na segunda.

Confirme que o PDF existe e tem tamanho plausível antes de seguir:

```bash
ls -lh iniciativas/<slug>/relatorio/relatorio.pdf
```

Sem `lualatex` instalado, **pare aqui**. Entregue o `.tex`, diga que a compilação
não aconteceu e não tente anexar nada. Não finja que o PDF saiu.

## Passo 5 — anexar o PDF ao card do Notion

Este passo é o único com efeito fora do repositório, e **rodar duas vezes anexa
dois PDFs**. Antes de começar, diga ao usuário qual arquivo vai para qual card e
**espere o ok**.

### 5.1 Ver como o card guarda artefato

```
notion-fetch { id: "<link (Notion)>" }
```

Duas formas possíveis, e o card manda:

- **propriedade de arquivos** chamada `Artefatos` (ou nome parecido) — anexe
  como valor de propriedade;
- **seção no corpo** da página (`## Artefatos`, `## 📃 Documentação`) — anexe
  como bloco de conteúdo.

Se o card não tiver nem uma nem outra, **pergunte ao usuário onde colocar**. Não
crie propriedade nova num database de governança por conta própria.

### 5.2 Subir o arquivo

```
notion-create-file-upload { filename: "<slug>-relatorio.pdf" }
```

Devolve `id`, `upload_url` e `upload_headers`. Envie o arquivo com um único POST
multipart, repetindo todos os headers devolvidos:

```bash
curl -sS -X POST "<upload_url>" \
  -H "<cada header de upload_headers>" \
  -F "file=@iniciativas/<slug>/relatorio/relatorio.pdf"
```

Limite de 20 MiB nesse fluxo. Relatório com muita imagem pode estourar — se
estourar, avise o usuário em vez de tentar comprimir o PDF por conta própria.

### 5.3 Prender o arquivo no card

Propriedade de arquivos:

```
notion-update-page {
  page_id: "<id do card>",
  command: "update_properties",
  properties: { "Artefatos": [{ "type": "file_upload", "file_upload": { "id": "<id>" } }] }
}
```

Atenção: isso **substitui** o valor da propriedade. Se já houver arquivo lá,
inclua os existentes na lista ou pergunte ao usuário antes de sobrescrever.

Seção no corpo — use o `markdown_source` devolvido pelo upload:

```
notion-update-page {
  page_id: "<id do card>",
  command: "insert_content",
  content: "<markdown_source>",
  position: { "type": "end" }
}
```

Depois `notion-fetch` no card de novo e confirme que o anexo está lá. Só então
diga ao usuário que subiu.

## Passo 6 — fechar

Relate, em poucas linhas: o que foi conferido, o que o gerador reclamou, onde o
PDF ficou e em que campo do card ele foi parar. Diga o que você deixou de fora
por precisar de decisão dele.

O `.tex` é versionável e entra no commit; o PDF está no `.gitignore` e não entra.
Avise que ele pode commitar e dar push.

## O que NÃO fazer

- **Não comite o PDF.** O README proíbe binário compilado; a única exceção é a
  marca d'água.
- **Não edite o markdown da iniciativa para "melhorar" o relatório.** Iniciativa
  fechada é imutável: correção posterior é nota no card seguinte.
- **Não edite o `.tex` gerado.** Conteúdo se corrige no markdown; forma, em
  `templates/latex/relatorio.tex`.
- **Não mexa em status, checklist ou nota do card no Notion.** Esta skill anexa
  arquivo; quem move governança é o usuário.
- **Não reanexe "para garantir".** Se ficou dúvida se subiu, confira com
  `notion-fetch` — não suba de novo.
