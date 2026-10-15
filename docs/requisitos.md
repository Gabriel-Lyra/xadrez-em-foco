# Requisitos

Resumo do [Documento de Requisitos v1.1](Aula-03-PI_II-DocumentoRequisitos.docx) e da [Declaração do escopo](Aula-03-PI_II-Declaracao_do_escopo_do_projeto_assinado_assinado.pdf). Em caso de divergência, valem os documentos originais.

## Visão do produto

Aplicação web que recebe a captura de tela de um tabuleiro de xadrez digital e devolve o campo de posição das peças em notação FEN, com link para análise no Lichess. Este repositório cobre o MVP previsto para 23/11/2026.

## Público-alvo

- **Usuários finais:** enxadristas que jogam em plataformas digitais e querem analisar posições vistas em prints, sem conhecimento técnico.
- **Usuário parceiro (ACE):** Matheus Belfort de Moura Torres — fornece prints reais e valida as entregas.
- **Avaliação acadêmica:** Prof. Valdemir dos Santos Silva.

## Problema

Hoje o jogador precisa montar manualmente, peça por peça, a posição vista em um print para analisá-la em uma ferramenta como o Lichess. O processo é lento e uma peça errada invalida a análise.

## Objetivos

- **Objetivo principal:** gerar o campo de posição do FEN a partir de prints com acerto mínimo de 90% das peças em um conjunto de pelo menos 200 posições distintas, até 23/11/2026.
- **Metas por sprint:** ver [sprints/](../sprints/README.md) e o roadmap no Documento de Arquitetura.

## Requisitos funcionais

| ID | Descrição | Prioridade | Itens do backlog |
| --- | --- | --- | --- |
| RF01 | Permitir o upload de uma captura de tela contendo um tabuleiro de xadrez digital. | Essencial | PB07, PB22 |
| RF02 | Detectar automaticamente a região do tabuleiro na imagem enviada. | Essencial | PB11, PB12 |
| RF03 | Identificar o tipo de cada peça presente no tabuleiro. | Essencial | PB12, PB13, PB14 |
| RF04 | Gerar a notação FEN correspondente à posição das peças identificadas. | Essencial | PB15, PB17, PB18 |
| RF05 | Exibir ao usuário o FEN gerado, permitindo copiá-lo. | Essencial (era Importante — ADR-008) | PB19 |
| RF06 | Disponibilizar link que abra a posição em ferramenta de análise externa (Lichess). | Importante | PB20 |

## Requisitos não funcionais

| ID | Categoria | Descrição | Prioridade | Itens do backlog |
| --- | --- | --- | --- | --- |
| RNF01 | Usabilidade | Interface simples o suficiente para uso sem treinamento prévio. | Importante | PB03, PB08, PB21, PB24 |
| RNF02 | Desempenho | Processar a imagem e retornar o resultado em até 3 s com o servidor ativo. | Importante | PB14, PB23 |
| RNF03 | Portabilidade | Acessível via navegador (desktop e celular), sem instalação. | Essencial | PB08, PB23 |
| RNF04 | Custo | Apenas ferramentas gratuitas ou de licença educacional. | Essencial | PB23 |
| RNF05 | Acurácia | Acerto mínimo de 90% na identificação das peças em 200+ posições reais; acompanhar também o percentual de FEN exato. | Essencial | PB09, PB10, PB13, PB16, PB24 |

## Critérios de aceitação

Os critérios de aceitação de cada requisito estão detalhados nos itens do backlog (issues PB01–PB25). Os critérios gerais do MVP, definidos na Declaração do escopo, são:

- modelo de detecção com acerto mínimo de 90% das peças em pelo menos 200 posições de teste;
- FEN gerado idêntico à posição real, medido como percentual de FEN exato;
- sistema funcional de ponta a ponta, validado pelo usuário parceiro com pelo menos 20 prints reais de suas partidas.

## Fora do escopo

Foto de tabuleiro físico; turno, roque e en passant; motor de análise integrado; histórico de partidas ou PGN; aplicativo mobile nativo; temas de peças fora dos padrões mais comuns.

## Dependências

- Prints reais fornecidos pelo usuário parceiro (necessários na Sprint 4 para teste e na Sprint 5 para validação).
- Disponibilidade do parceiro para a sessão de validação.
- Camadas gratuitas do Render, do Google Colab e do GitHub.

## Riscos e rastreabilidade para issues

| Risco | Requisitos afetados | Itens | Mitigação |
| --- | --- | --- | --- |
| Parceiro sem disponibilidade para prints ou validação | RNF05 | PB10, PB24 | Pedir os prints no início da Sprint 4 |
| Acurácia abaixo da meta em temas não previstos | RF03, RNF05 | PB09, PB13, PB16 | Mais variedade no dataset; restringir o MVP aos temas testados |
| Detecção falhar em prints com setas ou destaques | RF02 | PB11, PB21 | Incluir esses casos no treino; mensagem orientando o recorte |
| Limites da hospedagem gratuita | RNF02 | PB14, PB23 | Modelo ONNX leve; acordar o servidor antes das demonstrações |
