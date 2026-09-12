---
id: bm-001
tipo: benchmark
card: pricing-ndados
ciclo: 2026.1
nucleo: NDados
status: Finalizado
link (Notion):
entrevistador: Helena Braga
entrevistado: Rafael Toledo — Núcleo de Dados, EJ Sigma (fictícia)
data: 2026-03-04
link (Call):
---

# Perguntas

## Como vocês chegam ao preço de um projeto de dados hoje?

Partimos de uma estimativa de horas por perfil — analista, engenheiro, gerente — e
multiplicamos por uma taxa interna. A taxa é revisada uma vez por ano, no planejamento.
Em cima disso entra um ajuste que o gerente comercial faz “no olho”, que ele chama de
fator de dor: o quanto o cliente parece sofrer com o problema.

## Esse ajuste no olho é registrado em algum lugar?

Não. É a maior fragilidade do processo. Quando o gerente sai, o critério sai com ele.
Já aconteceu de dois projetos quase idênticos saírem com 40% de diferença de preço em
semestres seguidos, e ninguém conseguiu reconstruir por quê.

## Vocês diferenciam o preço por tipo de projeto?

Diferenciamos por duração, não por natureza. Na prática, um dashboard e um modelo
preditivo de mesma duração saem pelo mesmo preço, o que é claramente errado — o
preditivo consome muito mais sênior e tem risco de não convergir.

## O que vocês já tentaram e não funcionou?

Tentamos precificação por valor gerado, pedindo ao cliente a estimativa de ganho.
Não funcionou: o cliente não tem esse número, e quando tem não compartilha. Voltamos
para custo mais margem em dois meses.

## Como vocês tratam projeto de escopo aberto?

Mal. Fechamos preço fixo e absorvemos o estouro. Foi a maior fonte de prejuízo do
último ciclo.

# Síntese

## Objeções

- Precificação por valor gerado foi testada e abandonada: depende de um número que o
  cliente não tem ou não compartilha.
- Resistência interna a “engessar” o julgamento comercial em fórmula.

## Surpresas

- A taxa interna é revisada só uma vez por ano, mesmo com o custo do time mudando a
  cada virada de time.
- Duração é o único eixo de diferenciação; natureza do projeto não entra.

## Oportunidades

- O fator de dor é tácito e não registrado — transformá-lo em parâmetro explícito
  resolve o problema de sucessão que eles descreveram.
- Separar preço por natureza do projeto é ganho imediato e barato.

## Ameaças

- Escopo aberto com preço fixo é a fonte de prejuízo deles; qualquer modelo nosso que
  ignore isso repete o erro.
- Modelo percebido como camisa de força é abandonado pelo comercial em poucos meses.
