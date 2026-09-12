---
id: 001-A-tasks
tipo: tasks
card: pricing-ndados
ciclo: 2026.1
nucleo: NDados
status: Finalizado
link (Notion):
---

# Fases
## Fase 1 — Levantamento da base histórica
- [x] Exportar do CRM as propostas fechadas e perdidas dos últimos quatro ciclos
- [x] Normalizar escopo por horas-equipe, não por entregável nominal
- [x] Classificar cada projeto em uma das quatro esferas de atuação do núcleo
- [x] Anonimizar cliente e valor nominal antes de subir qualquer recorte ao repo

## Fase 2 — Benchmark externo
- [x] Mapear seis núcleos de dados de EJs com maturidade comparável
- [x] Rodar as calls de benchmark (viraram `bm-001` e `bm-002`)
- [x] Consolidar objeções e surpresas nas sínteses das atas

## Fase 3 — Modelagem
- [x] Definir a fórmula base: complexidade × esforço × fator de risco
- [x] Calibrar os pesos das quatro esferas contra a base histórica
- [x] Fixar o piso de margem por esfera
- [x] Escrever o notebook de backtest

## Fase 4 — Validação
- [x] Backtest sobre as 38 propostas históricas
- [x] Comparar preço sugerido pelo modelo com o preço praticado na época
- [x] Aplicar o modelo em três propostas reais em aberto (DOD outlier)
- [x] Registrar os desvios acima de 15% e investigar cada um

## Fase 5 — Fechamento
- [x] Derivar a matriz CSD (`fw-001`) e a SWOT (`fw-002`) a partir das atas
- [x] Escrever o resumo executivo
- [x] Remover as seções `# Rascunho` das atas
- [x] Subir a especificação do modelo para a raiz da iniciativa
