# Xadrez em Foco

Aplicação web que converte a captura de tela (print) de um tabuleiro de xadrez digital em notação FEN e abre a posição para análise no Lichess.

Projeto Integrador II — Ciência da Computação — UniCEUB — 2º semestre de 2026.

## Identificação do repositório

| Campo | Informação |
| --- | --- |
| Instituição | CEUB |
| Organização no GitHub | CampusCEUB |
| Professor(a) responsável | Prof. Valdemir dos Santos Silva — DRT: [informar] |
| Equipe | Gabriel Lyra Galvão dos Santos (projeto individual) |
| Usuário parceiro (ACE) | Matheus Belfort de Moura Torres, enxadrista |
| IDProjeto | [informar o ID do Portfólio de Projetos de TI do CEUB] |

## Problema

Para analisar uma posição vista em um print de partida on-line, o jogador precisa montá-la peça por peça em uma ferramenta como o editor do Lichess. O processo é lento e sujeito a erros: uma única peça no lugar errado invalida a análise.

## Solução proposta

O usuário envia o print; o sistema localiza o tabuleiro com visão computacional, identifica a peça de cada uma das 64 casas com uma rede neural convolucional, gera o campo de posição do FEN e oferece um link direto para o tabuleiro de análise do Lichess.

- **Público:** enxadristas que jogam em plataformas digitais (chess.com, lichess.org).
- **Valor esperado:** posição pronta para análise em poucos segundos, sem digitação manual.
- **Escopo do MVP (23/11/2026):** entrada apenas por captura de tela; saída apenas do campo de posição das peças do FEN. Foto de tabuleiro físico, turno, roque e en passant estão fora do escopo (ver [ADR-001](docs/decisoes/ADR-001-entrada-apenas-captura-de-tela.md)).

## Tecnologias

Python 3.12, Flask 3 (MVC), OpenCV, CNN treinada em PyTorch e executada com ONNX Runtime, front-end em HTML/CSS/JavaScript, hospedagem no Render. Não há banco de dados. Detalhes em [docs/arquitetura.md](docs/arquitetura.md).

## Estado atual

| Sprint | Período | Situação |
| --- | --- | --- |
| Sprint 1 — Concepção | ago/2026 | Concluída: escopo e requisitos |
| Sprint 2 — Planejamento | ago–set/2026 | Concluída: Project Model e apresentação |
| Sprint 3 — Arquitetura | 21/09 – 05/10 | Em andamento: arquitetura, backlog, protótipo |
| Sprint 4 — Visão computacional | out – início de nov | Planejada |
| Sprint 5 — MVP | nov – 23/11 | Planejada |

Ainda não há código-fonte; o esqueleto da aplicação está previsto na Sprint 3 (item PB05 do backlog).

## Estrutura deste repositório

| Item | Link |
| --- | --- |
| Backlog | GitHub Project do repositório (itens PB01–PB25) e [Backlog do Produto](docs/Aula-08-PI_II-Backlog%20do%20Produto.docx) |
| Sprints | [sprints/README.md](sprints/README.md) |
| Entregas | [entregas/README.md](entregas/README.md) |
| Requisitos | [docs/requisitos.md](docs/requisitos.md) |
| Arquitetura | [docs/arquitetura.md](docs/arquitetura.md) |
| Decisões (ADRs) | [docs/decisoes/](docs/decisoes/README.md) |
| Diagramas | [docs/diagramas/](docs/diagramas/) |
| Protótipo | [docs/prototipo/](docs/prototipo/) |

## Documentos da disciplina

| Documento | Sprint |
| --- | --- |
| [Declaração do escopo (assinada)](docs/Aula-03-PI_II-Declaracao_do_escopo_do_projeto_assinado_assinado.pdf) | 1 |
| [Documento de Requisitos v1.1](docs/Aula-03-PI_II-DocumentoRequisitos.docx) | 1 (revisado na 3) |
| [MVP](docs/Aula-02-PI_II-%20MVP.pdf) | 1 |
| [Project Model](docs/Xadrez%20em%20Foco%20-%20Project%20Model.pptx) | 2 |
| [Apresentação de escopo e requisitos](docs/apresentacao_escopo_e_requisitos.pptx) | 2 |
| [Documento de Arquitetura de Software](docs/Aula-08-PI_II-Documento%20de%20Arquitetura%20de%20Software.docx) | 3 |
| [Backlog do Produto](docs/Aula-08-PI_II-Backlog%20do%20Produto.docx) | 3 |
