"""Detecção do lado de baixo do tabuleiro no print (PB17, UC04, ADR-009).

A leitura das casas sempre assume as brancas embaixo. Esta heurística olha
onde estão os peões e os reis nessa leitura:

- peões brancos ficam, em média, mais perto da borda de baixo que os pretos;
- o rei branco costuma ficar mais embaixo que o rei preto;
- numa mesma coluna, o peão branco costuma estar abaixo do peão preto.

A pontuação soma os três sinais. Positiva: brancas embaixo; negativa: pretas
embaixo. Perto de zero (finais com poucas peças, posições artificiais), a
detecção não é conclusiva e o resultado assume as brancas embaixo, com aviso.
"""

from dataclasses import dataclass
from statistics import fmean

from app.dominio.peca import Cor
from app.dominio.posicao import Posicao

# Medido com treinamento/avaliar_orientacao.py (1000 posições de partidas reais,
# nas duas orientações): com este limiar, a detecção é conclusiva em 98,6% das
# leituras e acerta 99,9% delas. Os pesos e o limiar foram escolhidos com outras
# partidas do mesmo arquivo.
LIMIAR = 1.0
PESO_REIS = 0.25
PESO_COLUNAS = 0.5


@dataclass(frozen=True)
class DeteccaoOrientacao:
    lado_de_baixo: Cor
    conclusiva: bool
    pontuacao: float


def _linhas(matriz, simbolo: str) -> list[tuple[int, int]]:
    """(linha, coluna) de cada peça com o símbolo dado; linha 0 é a borda de cima do print."""
    return [
        (linha, coluna)
        for linha, fileira in enumerate(matriz)
        for coluna, peca in enumerate(fileira)
        if peca == simbolo
    ]


def pontuar(posicao: Posicao) -> float:
    """Positiva quando a posição lida parece ter as brancas embaixo."""
    matriz = posicao.para_matriz()
    peoes_brancos = _linhas(matriz, "P")
    peoes_pretos = _linhas(matriz, "p")
    reis_brancos = _linhas(matriz, "K")
    reis_pretos = _linhas(matriz, "k")

    peoes = 0.0
    if peoes_brancos and peoes_pretos:
        peoes = fmean(l for l, _ in peoes_brancos) - fmean(l for l, _ in peoes_pretos)

    reis = 0.0
    if reis_brancos and reis_pretos:
        reis = fmean(l for l, _ in reis_brancos) - fmean(l for l, _ in reis_pretos)

    colunas = sum(
        1 if linha_branco > linha_preto else -1
        for linha_branco, coluna_branco in peoes_brancos
        for linha_preto, coluna_preto in peoes_pretos
        if coluna_branco == coluna_preto
    )

    return peoes + PESO_REIS * reis + PESO_COLUNAS * colunas


def detectar_orientacao(posicao: Posicao) -> DeteccaoOrientacao:
    """Lado de baixo do print, a partir da posição lida com as brancas embaixo."""
    pontuacao = pontuar(posicao)
    if pontuacao > LIMIAR:
        return DeteccaoOrientacao(Cor.BRANCA, True, pontuacao)
    if pontuacao < -LIMIAR:
        return DeteccaoOrientacao(Cor.PRETA, True, pontuacao)
    return DeteccaoOrientacao(Cor.BRANCA, False, pontuacao)
