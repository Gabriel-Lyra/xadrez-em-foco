# ADR-005 — Aplicação sem banco de dados

## Status

Proposto (aprovação na apresentação da Sprint 3)

## Data

2026-09-26

## Contexto

O modelo do Documento de Arquitetura pede modelagem de banco de dados. O escopo exclui histórico de partidas, e a hospedagem gratuita apaga o disco a cada reinício.

## Decisão

A aplicação é **sem estado**: a imagem fica apenas em memória durante a requisição e é descartada. Os modelos conceitual, lógico e físico descrevem as estruturas em memória, o contrato JSON da API e os artefatos em arquivo.

## Alternativas consideradas

- **SQLite:** o arquivo seria perdido a cada reinício da instância gratuita.
- **PostgreSQL gerenciado:** acrescenta um serviço e um ponto de falha sem requisito que o justifique.

## Consequências

- Nenhum dado pessoal armazenado, o que simplifica a LGPD.
- Sem métricas de uso em produção; a acurácia é medida pelo script de avaliação (PB16).
- Se um histórico for pedido no futuro, esta decisão deve ser substituída.

## Links relacionados

- Documento de Arquitetura, Seção 9
