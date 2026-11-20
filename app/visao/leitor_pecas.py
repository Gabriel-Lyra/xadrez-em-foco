"""Contrato do leitor de peças: recebe o print decodificado e devolve as 64 casas classificadas.

O leitor definitivo combina ``DetectorTabuleiro``, ``SegmentadorCasas`` e
``ClassificadorPecas`` (PB11 a PB14). Até lá, a aplicação usa o
``LeitorDemonstracao`` (ADR-011). O ``ServicoReconhecimento`` depende só deste
contrato, então a troca não altera a API nem a página.
"""

from typing import Protocol

import numpy as np

from app.visao.classificacao import Classificacao

MODO_DEMONSTRACAO = "demonstracao"
MODO_MODELO = "modelo"


class TabuleiroNaoEncontrado(Exception):
    """O print não contém um tabuleiro 8×8 localizável (resposta 422)."""


class LeitorPecas(Protocol):
    modo: str

    def ler(self, imagem: np.ndarray) -> list[Classificacao]:
        """Recebe o print em BGR (8 bits) e devolve 64 classificações na ordem a8, b8, …, h1."""
        ...
