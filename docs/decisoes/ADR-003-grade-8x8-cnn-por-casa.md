# ADR-003 — Reconhecimento por grade 8×8 e CNN por casa

## Status

Proposto (aprovação na apresentação da Sprint 3)

## Data

2026-09-26

## Contexto

Prints têm tabuleiro plano, alinhado e sem perspectiva. É preciso identificar a peça (ou ausência) em cada uma das 64 casas.

## Decisão

Localizar o tabuleiro com OpenCV, normalizá-lo para 512×512 pixels, recortar 64 casas de 64×64 e classificá-las **em um único lote** com uma CNN leve de **13 classes** (6 peças brancas, 6 pretas, vazia).

## Alternativas consideradas

- **Detector de objetos (YOLO):** exige anotar caixas em milhares de imagens e é mais pesado; faz sentido para fotos com perspectiva (fora do escopo).
- **Comparação com imagens-modelo (template matching):** dispensa treino, mas falha quando o tema de peças muda.

## Consequências

- Rotulagem simples: cada casa recebe uma classe.
- Inferência rápida em CPU.
- O FEN só é correto se as 64 casas forem corretas: com erros independentes, 99% por casa resultaria em cerca de 53% de tabuleiros corretos. Para ~90% de FEN exato, a meta interna é **≥ 99,8% de acerto por casa** (PB13).

## Links relacionados

- Documento de Arquitetura, Seções 5.1 e 8.1
- Issues PB11, PB12, PB13, PB14
