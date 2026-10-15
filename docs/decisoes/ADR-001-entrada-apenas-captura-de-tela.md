# ADR-001 — Entrada apenas por captura de tela no MVP

## Status

Aprovado

## Data

2026-08-20

## Contexto

O termo de anuência da ACE e o documento de MVP previam leitura a partir de **fotografias ou capturas de tela**. Fotos de tabuleiro físico trazem perspectiva, iluminação, sombras e oclusão, o que exige técnicas e volume de dados incompatíveis com um projeto individual até 23/11/2026.

## Decisão

O MVP aceita **somente capturas de tela de tabuleiros digitais**. A leitura de fotos de tabuleiro físico passa a ser evolução futura. A saída também fica restrita ao campo de posição das peças do FEN (sem turno, roque e en passant).

## Alternativas consideradas

- **Aceitar fotos e prints desde o início:** inviável no prazo; o esforço de dados e modelo seria várias vezes maior.
- **Aceitar apenas fotos:** é o caso mais difícil e o de menor uso para quem joga on-line.

## Consequências

- Escopo viável e mensurável; entrada padronizada (sem perspectiva) permite a abordagem do ADR-003.
- Diverge do texto do termo de anuência e das personas do documento de MVP, que citam tabuleiro físico; a diferença deve ser explicada ao parceiro e ao professor.
- Foto de tabuleiro físico permanece registrada como item pós-MVP (PB26).

## Links relacionados

- Declaração do escopo (Sprint 1), aprovada em 23/08/2026
- Documento de MVP (Aula 02)
- Termo de anuência da ACE
