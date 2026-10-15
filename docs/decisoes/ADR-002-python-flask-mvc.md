# ADR-002 — Python 3.12 + Flask organizado em MVC

## Status

Proposto (aprovação na apresentação da Sprint 3)

## Data

2026-09-26

## Contexto

O núcleo do problema é visão computacional e aprendizado de máquina. O modelo do Documento de Arquitetura da disciplina sugere Java e MVC como exemplo. O projeto é individual e precisa minimizar o número de tecnologias.

## Decisão

Usar **Python 3.12** em todo o projeto e **Flask 3** como framework web, organizado em MVC: templates Jinja2 e arquivos estáticos como View, rotas como Controller, pacotes `servicos`, `visao` e `dominio` como Model. Front-end em HTML, CSS e JavaScript sem framework.

## Alternativas consideradas

- **Java + Spring:** o ecossistema de visão computacional e ML está em Python; seriam duas linguagens e uma integração extra.
- **FastAPI + React:** dois projetos e dois deploys para uma única tela.
- **FastAPI com HTML simples:** também viável; o Flask foi preferido por ter templates integrados que mapeiam diretamente para a View do MVC. Decisão de margem estreita.
- **Streamlit:** mais rápido, mas oculta a arquitetura que a disciplina avalia.

## Consequências

- Uma única linguagem para aplicação e treino.
- MVC explícito na estrutura de pastas.
- Sem SPA: interações dinâmicas feitas com JavaScript simples.

## Links relacionados

- Documento de Arquitetura, Seções 3 e 5
- Issue PB05
