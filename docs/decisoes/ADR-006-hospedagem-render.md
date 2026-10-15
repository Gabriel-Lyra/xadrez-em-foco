# ADR-006 — Hospedagem na camada gratuita do Render

## Status

Proposto (aprovação na apresentação da Sprint 3)

## Data

2026-09-26

## Contexto

O sistema precisa de um endereço público sem custo (RNF03, RNF04), com deploy simples para um desenvolvedor.

## Decisão

Publicar no **Render (Free Web Service)**, com deploy automático a cada push na `main`, servidor Gunicorn com 1 processo e 2 threads.

## Alternativas consideradas

- **Hugging Face Spaces:** a opção com Docker passou a exigir plano pago.
- **Servidor próprio ou VPS:** custo e manutenção.

## Consequências

- 512 MB de RAM e menos de 1 CPU: exige o ADR-004.
- Hiberna após 15 min sem tráfego e leva cerca de 1 min para voltar: acessar o serviço antes das demonstrações.
- A aplicação não depende de recursos específicos do Render; migrar exige apenas nova configuração de deploy.

## Links relacionados

- Documento de Arquitetura, Seção 6
- https://render.com/docs/free
- Issue PB23
