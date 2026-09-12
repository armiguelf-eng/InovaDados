---
id: fw-001
tipo: csd
card: pricing-ndados
ciclo: 2026.1
nucleo: NDados
status: Finalizado
link (Notion):
origem: bm-001, bm-002
---

# Matriz CSD

## Certezas

- Precificação baseada em julgamento não registrado não sobrevive à troca de gerente.
  Os dois entrevistados relataram o mesmo problema de sucessão (`bm-001`, `bm-002`).
- Duração isolada não explica preço: projetos de mesma duração e naturezas diferentes
  consomem perfis de senioridade muito distintos (`bm-001`).
- Um modelo de três fatores com nota de 1 a 5 é operável por um comercial sem
  treinamento longo — está em produção há três anos na Delta (`bm-002`).
- Escopo aberto com preço fixo gera prejuízo recorrente (`bm-001`).
- O piso de margem precisa ser definido antes da fórmula, não depois (`bm-002`).

## Suposições

- A base histórica do NDados tem volume suficiente para calibrar os pesos das quatro
  esferas. A checar no backtest — desconfiamos que engenharia de dados tenha poucos casos.
- Nosso comercial aceitará operar por notas se o modelo rodar em paralelo por um ciclo,
  como funcionou na Delta. Nada garante que a cultura seja transferível.
- A dispersão de preço que observamos internamente vem da mesma causa relatada no
  benchmark, e não de diferenças reais de escopo mal registradas no CRM.
- Separar quem dá a nota de risco de quem dá as outras duas é suficiente para evitar a
  manipulação no nosso contexto, com um time menor que o da Delta.

## Dúvidas

- Como precificar projeto de descoberta, em que nenhum dos dois entrevistados tem
  resposta e ambos relatam prejuízo?
- Qual a periodicidade certa de revisão dos pesos para um núcleo que troca de time
  duas vezes por ano, contra o ciclo anual da Delta?
- O fator de risco deve multiplicar o preço ou definir um percentual de contingência
  separado, visível na proposta?
- Quem é o dono do modelo depois que este card fecha?
