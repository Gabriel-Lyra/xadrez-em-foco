# ADR-007 — Dataset sintético para treino e prints reais para teste

## Status

Proposto (aprovação na apresentação da Sprint 3)

## Data

2026-09-26

## Contexto

Treinar a CNN exige milhares de casas rotuladas. Rotular prints manualmente é inviável no prazo.

## Decisão

Gerar tabuleiros **sintéticos** a partir de posições aleatórias, com conjuntos de peças e temas de licença livre, já rotulados. Os **prints reais** do parceiro (200+) formam o conjunto de **teste**, com gabarito em CSV.

## Alternativas consideradas

- **Somente prints reais:** exigiria rotular milhares de imagens.

## Consequências

- Rótulos automáticos e volume ilimitado de dados.
- **Risco conhecido:** peças de plataformas com conjuntos proprietários (por exemplo, o padrão do chess.com) podem não estar no dataset sintético. Se a acurácia nos prints reais ficar abaixo da meta, parte dos prints reais deve entrar no treino, mantendo um conjunto de teste separado.

## Links relacionados

- Issues PB09, PB10, PB13, PB16
