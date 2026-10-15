# ADR-004 — ONNX Runtime para executar o modelo em produção

## Status

Proposto (aprovação na apresentação da Sprint 3)

## Data

2026-09-26

## Contexto

A instância gratuita de hospedagem tem 512 MB de RAM e menos de 1 CPU. O pacote do PyTorch ocupa centenas de MB.

## Decisão

Treinar a CNN em **PyTorch** no Google Colab e exportá-la para o formato **ONNX**. Em produção, o modelo é carregado uma vez na inicialização e executado com o **ONNX Runtime (CPU)**.

## Alternativas consideradas

- **PyTorch no servidor:** risco alto de estourar a memória da instância.
- **TensorFlow Lite:** viável, mas mudaria o framework de treino sem ganho relevante.

## Consequências

- Aplicação mais leve; meta de até 400 MB de memória (a validar em PB23).
- Um passo extra de exportação no pipeline de treino.
- O arquivo `.onnx` (até 10 MB) é versionado no repositório.

## Links relacionados

- Documento de Arquitetura, Seções 6 e 7
- Issues PB13, PB14, PB23
