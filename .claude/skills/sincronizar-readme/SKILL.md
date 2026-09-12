---
name: sincronizar-readme
description: Verifica se o README.md ainda descreve o repositório InovaDados de verdade e corrige o que divergiu — árvore de pastas, lista de templates, vocabulário de `tipo` no frontmatter, caminhos citados em comandos, regras do .gitignore e a seção Pendências. Use sempre que algo estrutural do repositório mudar (template criado, renomeado ou removido; iniciativa nova; campo de frontmatter alterado; skill ou script adicionado; .gitignore editado), quando o usuário pedir "atualiza o README", "sincroniza o README", "o README está desatualizado", ou antes de commitar uma mudança que toque templates/, iniciativas/, .claude/skills/ ou .gitignore.
---

# Sincronizar o README com o repositório

O README do InovaDados é contrato, não descrição aproximada: ele é lido por quem
entra no time e por agentes que criam arquivos a partir dele. Quando descreve uma
estrutura que não existe, o erro se propaga em cada pasta nova.

Esta skill compara o README com o repositório e corrige **o README**, não o
repositório — salvo quando o usuário pedir o contrário.

## Quando rodar

Depois de qualquer mudança em `templates/`, `iniciativas/`, `.claude/skills/`,
`.gitignore` ou nos scripts geradores. Mudança de conteúdo dentro de uma ata ou
de um framework **não** exige sincronização; mudança de estrutura, sim.

## Passo 1 — rodar o validador

```bash
python3 .claude/skills/sincronizar-readme/scripts/verificar_readme.py
```

Ele imprime as divergências encontradas e sai com código 1 se houver alguma.
O validador **não edita nada** — ele aponta. A correção é sua, com julgamento.

## Passo 2 — para cada divergência, decidir a direção

O validador diz *o quê* divergiu, não *quem está certo*. Duas direções possíveis:

- **README desatualizado** (caso comum): o repositório mudou de propósito e o
  README ficou para trás. Corrija o README.
- **Repositório fora do padrão**: alguém criou um arquivo que viola uma convenção
  que o README declara. Aí o README está certo — **relate ao usuário e pergunte**
  antes de mexer no arquivo. Nunca renomeie ou mova arquivo de iniciativa por
  conta própria: iniciativa fechada é imutável.

Na dúvida sobre qual dos dois é a verdade, pergunte. Não escolha em silêncio.

## Passo 3 — o que manter sincronizado

| No README | Fonte da verdade no repo |
| --- | --- |
| Árvore em `## Estrutura` | `templates/`, `.claude/skills/`, `iniciativas/` |
| Árvore da pasta de iniciativa | uma iniciativa real existente |
| Tabela de `## Templates` | um arquivo em `templates/` por linha, e vice-versa |
| Lista de valores de `tipo:` | os `tipo:` distintos em `templates/*.md` |
| Campos de `## Frontmatter` | o frontmatter dos templates |
| Caminhos nos blocos `bash` | os caminhos reais dos scripts |
| Exceções em `## Não entra neste repositório` | `.gitignore` |
| `## Pendências` | só o que de fato ainda não existe |

Regras que valem ao editar:

- A tabela de templates tem quatro colunas: Template, Contém, Não contém,
  Organização. Template novo entra com as quatro preenchidas — a coluna
  Organização diz quem preenche o arquivo, usuário ou agente.
- Item de `## Pendências` que passou a existir sai da lista. A seção descreve
  só o que o README promete e o repo ainda não entrega.
- Não invente convenção nova para fechar uma divergência. Se o repo faz algo que
  o README não cobre e não há regra óbvia, proponha a regra ao usuário.
- Preserve o tom do README: frases curtas, imperativo, sem adjetivo de venda.

## Passo 4 — confirmar

Rode o validador de novo. Ele deve sair limpo. Depois relate ao usuário, em
poucas linhas, o que mudou e por quê — e o que você deixou de fora por precisar
de decisão dele.
