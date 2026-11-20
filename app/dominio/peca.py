"""Peça de xadrez: cor e tipo."""

from dataclasses import dataclass
from enum import Enum


class Cor(Enum):
    BRANCA = "brancas"
    PRETA = "pretas"


class TipoPeca(Enum):
    """Tipo da peça. O valor é a letra usada no FEN (minúscula)."""

    REI = "k"
    DAMA = "q"
    TORRE = "r"
    BISPO = "b"
    CAVALO = "n"
    PEAO = "p"


@dataclass(frozen=True)
class Peca:
    cor: Cor
    tipo: TipoPeca

    def simbolo_fen(self) -> str:
        """Letra da peça no FEN: maiúscula para as brancas, minúscula para as pretas."""
        letra = self.tipo.value
        return letra.upper() if self.cor is Cor.BRANCA else letra

    @classmethod
    def de_simbolo(cls, simbolo: str) -> "Peca":
        """Cria a peça a partir da letra do FEN (por exemplo, ``"K"`` ou ``"p"``)."""
        if len(simbolo) != 1:
            raise ValueError(f"Símbolo de peça inválido: {simbolo!r}")
        try:
            tipo = TipoPeca(simbolo.lower())
        except ValueError:
            raise ValueError(f"Símbolo de peça inválido: {simbolo!r}") from None
        cor = Cor.BRANCA if simbolo.isupper() else Cor.PRETA
        return cls(cor, tipo)
