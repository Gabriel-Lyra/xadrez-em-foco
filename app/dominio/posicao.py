"""Posição: disposição das peças nas 64 casas do tabuleiro."""

from collections.abc import Iterator, Sequence

from app.dominio.peca import Peca

COLUNAS = "abcdefgh"
ROTULO_VAZIO = "vazio"

Fileira = tuple[Peca | None, ...]


class Posicao:
    """Disposição das peças em uma grade 8×8.

    A grade é guardada na ordem de leitura do FEN: a primeira linha é a
    fileira 8 e a última é a fileira 1; em cada linha, a primeira casa é a
    coluna ``a``. É a mesma ordem em que o print é recortado (a8…h1) quando as
    brancas estão embaixo.
    """

    def __init__(self, casas: Sequence[Sequence[Peca | None]]):
        if len(casas) != 8 or any(len(linha) != 8 for linha in casas):
            raise ValueError("A posição precisa ter 8 fileiras de 8 casas.")
        self._casas: tuple[Fileira, ...] = tuple(tuple(linha) for linha in casas)

    @classmethod
    def vazia(cls) -> "Posicao":
        return cls([[None] * 8 for _ in range(8)])

    @classmethod
    def de_rotulos(cls, rotulos: Sequence[str | None]) -> "Posicao":
        """Monta a posição a partir de 64 rótulos na ordem a8, b8, …, h1.

        Cada rótulo é a letra da peça no FEN (``"K"``, ``"p"``…) ou
        ``"vazio"``/``None`` para casa vazia. É o formato devolvido pelo
        classificador de peças.
        """
        if len(rotulos) != 64:
            raise ValueError(f"São necessários 64 rótulos; recebidos {len(rotulos)}.")
        pecas = [
            None if rotulo in (None, ROTULO_VAZIO) else Peca.de_simbolo(rotulo)
            for rotulo in rotulos
        ]
        return cls([pecas[i : i + 8] for i in range(0, 64, 8)])

    @classmethod
    def de_fen(cls, campo_posicao: str) -> "Posicao":
        """Monta a posição a partir do campo de posição do FEN.

        Aceita só o primeiro campo (por exemplo,
        ``"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"``).
        """
        partes = campo_posicao.split("/")
        if len(partes) != 8:
            raise ValueError(f"O FEN precisa ter 8 fileiras: {campo_posicao!r}")
        casas = []
        for parte in partes:
            linha: list[Peca | None] = []
            for caractere in parte:
                if caractere in "12345678":
                    linha.extend([None] * int(caractere))
                else:
                    linha.append(Peca.de_simbolo(caractere))
            if len(linha) != 8:
                raise ValueError(f"Fileira com tamanho diferente de 8: {parte!r}")
            casas.append(linha)
        return cls(casas)

    def fileiras(self) -> tuple[Fileira, ...]:
        """As 8 fileiras, da 8 para a 1."""
        return self._casas

    def peca_em(self, coluna: str, fileira: int) -> Peca | None:
        """Peça na casa indicada, por exemplo ``peca_em("e", 1)``."""
        if len(coluna) != 1 or coluna not in COLUNAS or not 1 <= fileira <= 8:
            raise ValueError(f"Casa inválida: {coluna}{fileira}")
        return self._casas[8 - fileira][COLUNAS.index(coluna)]

    def casas_ocupadas(self) -> Iterator[tuple[str, Peca]]:
        """Percorre as casas com peça, devolvendo o nome da casa (``"e4"``) e a peça."""
        for indice_linha, linha in enumerate(self._casas):
            for indice_coluna, peca in enumerate(linha):
                if peca is not None:
                    yield f"{COLUNAS[indice_coluna]}{8 - indice_linha}", peca

    def invertida(self) -> "Posicao":
        """Posição com o tabuleiro girado 180°.

        Usada quando o print mostra as pretas embaixo: o recorte lido de cima
        para baixo começa em h1, e não em a8.
        """
        return Posicao([tuple(reversed(linha)) for linha in reversed(self._casas)])

    def para_matriz(self) -> list[list[str | None]]:
        """Grade 8×8 com a letra de cada peça ou ``None`` (campo ``pecas`` da API)."""
        return [
            [None if peca is None else peca.simbolo_fen() for peca in linha]
            for linha in self._casas
        ]

    def __eq__(self, outra: object) -> bool:
        return isinstance(outra, Posicao) and self._casas == outra._casas

    def __hash__(self) -> int:
        return hash(self._casas)

    def __repr__(self) -> str:
        from app.dominio.gerador_fen import GeradorFEN

        return f"Posicao({GeradorFEN().gerar(self)!r})"
