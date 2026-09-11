# Inovação

## Objetivo

Guardar os artefatos produzidos pelas iniciativas de inovação da Poli Júnior: atas de benchmark, frameworks de discovery, especificação de modelos, skills e registro de decisões.

A governança fica no Notion (status, ciclo, DOD, prioridade, responsáveis, checklist, nota, TE). Não espelhe esses campos aqui.

| Conteúdo | Local |
| --- | --- |
| Muda de estado a cada semana | Notion |
| Controle de execução do ciclo | Notion |
| Evidência de campo ou conclusão derivada dela | Este repositório |
| Artefato que será lido em um ano | Este repositório |

Exceção única: o Learning Card é copiado para `aprendizados.md` no fechamento do card.

## Estrutura

Um card do Notion corresponde a uma pasta em `cards/`. Tudo que aquele card produziu fica dentro dela.

```
inovacao/
├─ README.md
├─ .github/workflows/valida.yml
├─ _templates/
│  ├─ card.md
│  ├─ benchmark.md
│  ├─ framework.md
│  ├─ adr.md
│  ├─ skill.md
│  └─ construcao.md
├─ _scripts/
│  ├─ comum.py                     leitura de frontmatter compartilhada
│  ├─ novo_card.py                 cria a pasta de um card novo
│  ├─ valida_frontmatter.py        checagem estrutural, roda no CI
│  └─ gera_indice.py               reescreve as tabelas de índice
└─ iniciativas/
```

Pasta por iniciativa e por card.

## Fronteira do card

Dentro da pasta do card: o que foi produzido naquele ciclo e não muda depois. Atas, análises, dados, aprendizados.

Na raiz da iniciativa: o que continua vivo e é revisado por cards seguintes. Especificação, skill, decisões.

Teste: **se o próximo card vai editar o arquivo, ele não pertence a este card.**

Card fechado é imutável. Correção posterior entra como nota no card seguinte, não como edição retroativa.

## Iniciativas

<!-- INDICE:INICIO -->
<!-- INDICE:FIM -->

Gerado por `_scripts/gera_indice.py`. Não edite à mão.

## Tipos de documento

| Arquivo | Contém | Não contém |
| --- | --- | --- |
| `cards/*/card.md` | Objetivo, Test Card, DOD, link do card no Notion | Checklist, prioridade, nota, TE |
| `cards/*/aprendizados.md` | Learning Card: hipótese, observação, aprendizado, próximo passo | Planejamento do card seguinte |
| `cards/*/benchmarks/bm-*.md` | O que foi dito, em pares pergunta/resposta | Conclusão fora da seção de interpretação |
| `cards/*/discovery/fw-*.md` | Framework derivado: CSD, SWOT, análise | Dado bruto ou imagem sem script de origem |
| `cards/*/dados/` | Dados versionáveis e scripts de extração | Dado de cliente identificável |
| `modelo/especificacao.md` | A lógica do modelo, versão vigente | Instrução de execução |
| `modelo/decisoes/adr-*.md` | Uma decisão: contexto, alternativas, escolha, consequência | Mais de uma decisão por arquivo |
| `modelo/skill/SKILL.md` | O que o agente executa | Justificativa de design |
| `modelo/skill/CONSTRUCAO.md` | Por que ficou assim, o que foi descartado, calibração | Instrução de execução |

Regras verificadas pelo validador:

- Toda ata tem exatamente duas seções de conteúdo, nesta ordem: `## Registro bruto` e `## Interpretação`.
- Todo framework declara `origem` com os IDs dos benchmarks que o embasam. Framework sem `origem` derruba o PR.
- Todo ID citado em `origem`, `relacionados`, `substitui` ou `substituida_por` precisa existir no repositório.
- `id` é único em todo o repositório.
- `card` bate com o nome da pasta onde o arquivo está.

Gráfico é saída derivada: dado em `dados/`, script que gera, figura em `discovery/figuras/`.

## Frontmatter

Obrigatório no topo de todo documento, em YAML.

```yaml
---
id: bm-2026-05-22-arnold
tipo: card | aprendizados | benchmark | framework | adr | construcao
data: 2026-05-22
iniciativa: pricing-ndados
card: 26-1-revisao-de-execucao
ciclo: 26.1
nucleo: NDADOS
eixo: precificacao
fonte: Arnold
interlocutor: nome — cargo
modalidade: call | desk research | cliente oculto | documento
status: realizado | sintetizado
estado: rascunho | em validacao | vigente | depreciado
origem: campo | inferido
validado_por: nome
relacionados: [fw-matriz-csd]
---
```

- `id` é imutável após criação.
- `card` amarra qualquer documento ao seu ciclo de origem.
- `origem` em benchmark é `campo` ou `inferido`; em framework e ADR é a lista de IDs que embasam.
- `origem: inferido` marca conteúdo derivado por modelo, não observado.
- `status: realizado` sem par `sintetizado` após 7 dias vira aviso no validador.
- `SKILL.md` é a exceção: usa `name` e `description`, no formato de skill do Claude.

## Convenções

- Pasta de card: `<ciclo>-<tipo-do-card>`, ex. `26-1-revisao-de-execucao`.
- Pasta de iniciativa: slug curto, ex. `pricing-ndados`.
- Nomes de arquivo e pasta: minúsculas, sem acento, separados por hífen.
- Prefixos de ID: `bm-` benchmark, `fw-` framework, `adr-` decisão.
- Referência entre documentos sempre por ID, nunca por caminho ou título.
- Uma pergunta por heading nas atas.

## Não entra neste repositório

- Planilha viva ou colaborativa (fica no Drive, link no `card.md`)
- PDF, deck ou binário compilado (o fonte entra, a saída não)
- Gravação e transcrição bruta (ficam no storage, link no frontmatter)
- Dado de cliente identificável, credencial, valor nominal de proposta

## Fluxo

Abrir card:

```bash
python _scripts/novo_card.py pricing-ndados 26.3 \
  --tipo revisao-de-execucao --nucleo NDADOS \
  --ci "nome" --notion "https://notion.so/..."
```

Antes de abrir o PR:

```bash
pip install pyyaml
python _scripts/valida_frontmatter.py
python _scripts/gera_indice.py
```

Toda mudança entra por pull request, inclusive ata nova. Na descrição do PR: link do card no Notion e IDs afetados.

Fechar card: `aprendizados.md` preenchido, todo benchmark em `status: sintetizado`, alteração no `modelo/` mergeada, `status: fechado` no `card.md`.

O CI roda o validador e `gera_indice.py --check` em todo PR.

## Dono

<!-- nome do responsável pelos templates e pelo validador, com sucessor previsto na virada de time -->
