# ADR-009 — Tratamento da orientação do tabuleiro (UC04)

## Status

Proposto (aprovação na apresentação da Sprint 3)

## Data

2026-09-26

## Contexto

Quando o jogador está de pretas, as plataformas exibem o tabuleiro invertido. Sem tratamento, o FEN gerado sairia espelhado. O Documento de Requisitos não previa esse caso.

## Decisão

Incluir o caso de uso **UC04 Inverter orientação**: o sistema detecta automaticamente qual cor está embaixo e o usuário pode corrigir com um botão, que alterna para o FEN correspondente sem nova requisição.

## Alternativas consideradas

- **Perguntar a orientação antes do envio:** um passo a mais para todos os usuários.
- **Ignorar:** metade dos prints de quem joga de pretas geraria FEN errado.

## Consequências

- Novo item no backlog (PB17).
- A heurística inicial usa a posição dos reis e dos peões, que é frágil em finais de partida. Alternativa a avaliar na Sprint 5: ler as coordenadas (a–h, 1–8) desenhadas na borda do tabuleiro pela maioria das plataformas.

## Links relacionados

- Documento de Arquitetura, Seção 4
- Issue PB17
