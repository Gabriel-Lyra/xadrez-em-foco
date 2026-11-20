"""Classificação de uma casa do tabuleiro."""

from dataclasses import dataclass

# Ordem das classes na saída do modelo (modelos/classes.json). O treino (PB13) e o
# ClassificadorPecas (PB14) usam esta mesma tupla; o classificador confere o arquivo.
ROTULOS = ("K", "Q", "R", "B", "N", "P", "k", "q", "r", "b", "n", "p", "vazio")


@dataclass(frozen=True)
class Classificacao:
    """Rótulo de uma casa (letra da peça no FEN ou ``"vazio"``) e a confiança do modelo.

    ``confianca`` é ``None`` quando o rótulo não veio do modelo (modo demonstração).
    """

    rotulo: str
    confianca: float | None
