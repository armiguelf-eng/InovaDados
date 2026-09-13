---
name: abrir-iniciativa
description: Abre a pasta de uma iniciativa nova no InovaDados a partir de um card do Laboratório de Inovação do Notion — cria iniciativas/<slug>/materials/, copia templates/card.md e templates/tasks.md para dentro e preenche os dois com o conteúdo do card. Use quando o usuário anexar o .md exportado de um card, colar o link de um card do Notion, ou disser "o card está preenchido", "abre a iniciativa", "cria a pasta do card", "começa o card novo", "novo card do lab".
---

# Abrir iniciativa a partir de um card do Notion

O card do Notion é a fonte. Esta skill só transcreve: cria a pasta, copia os dois
templates e preenche com o que já está no card. Nada é inventado, nada é
resumido com liberdade.

O par `materials/card.md` + `materials/tasks.md` é o insumo que a
`documentar-iniciativa` vai ler meses depois. Um campo errado aqui reaparece no
relatório final.

## Passo 1 — ler o que o usuário mandou

O usuário chega de duas formas:

- **anexou um `.md`** — é o export do card feito pelo Notion. Leia com `Read`.
  O nome do arquivo costuma trazer um hash colado no fim
  (`... de IA  3960805a57e9805ca130dec4fabb453d.md`): o hash **não** faz parte
  do título;
- **colou um link/URL** do card — vá direto para o Passo 2 com esse ID.

O export tem esta forma, e é dela que sai quase tudo:

```
# <Título do card>
Status: Finalizado<br>Área: Projetos<br>Núcleo: NDADOS<br>Ciclo: 26.2<br>
DOD básico: ...<br>DOD outlier: ...<br>Indicadores de sucesso: ...
## 🎯Objetivos
## 📝Tabela de hipóteses
## O que vamos fazer ⏯️
### Fase 1: <nome>
- [ ] ...
```

## Passo 2 — achar o card no Notion

O `.md` exportado é uma foto do passado. O Notion é o estado atual, e só ele tem
a URL que vai no frontmatter. Sempre confirme contra o Notion.

`ai_search` **não está disponível** neste workspace. Use `notion-search` com
palavras-chave curtas tiradas do título (duas ou três, sem artigo, sem emoji),
depois `notion-fetch` no resultado.

O database "Laboratório de Inovação" não aparece de forma confiável na busca por
nome. Se a busca por palavra-chave não achar o card:

- **0 resultados** — peça ao usuário a URL do card. Não siga sem ela.
- **2 ou mais candidatos** — liste título e ciclo de cada um e **pergunte qual**.
  Nunca escolha o mais recente por conta própria.

Nunca prossiga com `link (Notion)` vazio. É esse link que a `fechar-iniciativa`
usa no fim da sprint para anexar o PDF sem ter que buscar de novo — sem ele, o
fechamento vira uma busca às cegas.

## Passo 3 — derivar o slug do título

**O nome da pasta sai do nome do card no Notion**, não da preferência de ninguém.

Regra: minúsculas, sem acento, sem emoji, separado por hífen. Descarte prefixo
entre colchetes, preposição e artigo. Fique em 2 a 4 palavras.

| Título no Notion | Slug |
| --- | --- |
| Modelo de Precificação NDados | `pricing-ndados` |
| \[Reestruturação IA\] Diagnóstico + Discovery de IA Generativa | `discovery-ia-generativa` |

Se o título for curto o bastante para virar slug inteiro, crie direto e informe.
Se precisar cortar para caber em 4 palavras, **mostre o slug ao usuário e espere
o ok** — pasta de iniciativa é praticamente imutável depois de criada, e o slug
vira o campo `card` de todo documento da iniciativa.

Se `iniciativas/<slug>/` já existir, **pare e pergunte**. Duas iniciativas com o
mesmo slug é conflito de card, não detalhe de nomenclatura.

## Passo 4 — criar a pasta e copiar os templates

```bash
mkdir -p iniciativas/<slug>/materials
cp templates/card.md  iniciativas/<slug>/materials/card.md
cp templates/tasks.md iniciativas/<slug>/materials/tasks.md
```

Só `materials/`. `artefatos/` e `relatorio/` nascem quando o primeiro arquivo
deles existir — pasta vazia não entra no git, e criar as três agora só espalha
diretório fantasma.

Use `cp` de verdade, não reescreva o template de memória: se alguém mudou
`templates/card.md`, a iniciativa nova tem que nascer com a versão nova.

## Passo 5 — preencher o frontmatter

Os dois arquivos levam o mesmo frontmatter, só mudando `id` e `tipo`:

| Campo | De onde vem |
| --- | --- |
| `id` | o slug, em `card.md`; o slug + `-tasks`, em `tasks.md` |
| `tipo` | `card` e `tasks`, respectivamente — não mexa |
| `card` | o slug |
| `ciclo` | propriedade `Ciclo` do Notion, **literal** (`26.2` fica `26.2`) |
| `nucleo` | propriedade `Núcleo` |
| `status` | propriedade `Status` |
| `link (Notion)` | a URL do card resolvida no Passo 2 |

`id` é único no repositório todo e imutável depois de criado. Antes de gravar,
confira que ninguém usou:

```bash
grep -rn "^id: <slug>" iniciativas/
```

## Passo 6 — preencher o corpo do `card.md`

| Campo do template | Fonte no card do Notion |
| --- | --- |
| `# <Título do Card>` | título do card, sem o hash do export |
| Por quê | seção de objetivo estratégico — a que responde "por que essa iniciativa é importante" |
| Objetivo deste card | seção "Objetivos deste Card" |
| Métricas de Sucesso | propriedade `Indicadores de sucesso`, complementada pela seção de indicadores |
| DOD / Básico | propriedade `DOD básico` |
| DOD / Outlier | propriedade `DOD outlier` |

Regras de transcrição:

- **Condense, não reescreva.** O card do Notion é prolixo por natureza; o
  `card.md` é curto. Corte repetição e enrolação, preserve número, nome próprio
  e critério de aceite — é o que alguém vai conferir daqui a um ano.
- **Não copie o que o README manda ficar no Notion**: checklist, prioridade,
  nota, TE, responsáveis, datas. Governança muda toda semana e vive lá.
- **Não copie hipótese, feedback, conclusão nem material consultado.** Hipótese
  vira framework em `artefatos/discovery/`; conclusão vira
  `artefatos/resumoexecutivo.md` no fim da sprint. Nada disso é `card.md`.
- **Não copie dado proibido**: cliente identificável, credencial, valor nominal
  de proposta. Se o card do Notion tiver, deixe de fora e avise o usuário.
- Campo vazio no Notion vira campo vazio aqui. **Não invente objetivo nem
  métrica** para o arquivo parecer completo — placeholder não preenchido
  reaparece como `**[preencher: X]**` no relatório, e é assim que tem que ser.

## Passo 7 — preencher o `tasks.md`

Vem da seção "O que vamos fazer" do card. Cada `### Fase N: <nome>` vira um
`## Fase N — <nome>`; cada item vira um checkbox.

- Preserve o estado do checkbox como está no Notion: `- [x]` marcado continua
  marcado. Card recém-aberto normalmente é tudo `- [ ]`.
- Achate sub-item aninhado em uma linha só, ou perca o nível. Prefira achatar.
- Tire a data do nome da fase — data é governança e vive no Notion.
- Se o card não tiver fases, escreva as fases que ele descreve em prosa e
  **diga ao usuário que você as inferiu**.

## Passo 8 — conferir e avisar

Antes de entregar, releia os dois arquivos e garanta que não sobrou placeholder
do template (`<Título do Card>`, `<nome>`, `Task A`). Placeholder que vaza aqui
vaza no relatório.

Rode a `sincronizar-readme`: a árvore de `iniciativas/` no README mudou.

Aí avise o usuário — em poucas linhas — o que foi criado, qual slug, e **o que
ficou vazio por não existir no card**. Feche dizendo que ele pode commitar e dar
push.

## O que NÃO fazer

- **Não edite o card no Notion.** O fluxo é de mão única: Notion → repositório.
- **Não crie `artefatos/` com arquivo vazio** só para a pasta existir.
- **Não preencha `resumoexecutivo.md` nem `introducao.md`.** Pelo README, quem
  cria e preenche esses dois é o usuário, e eles são produto do fim da sprint.
- **Não reabra uma iniciativa existente por aqui.** Iniciativa fechada é
  imutável; card novo é pasta nova.
