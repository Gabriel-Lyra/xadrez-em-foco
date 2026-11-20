"""SegmentadorCasas: recorta o tabuleiro já localizado em 64 casas (PB12)."""

import cv2
import numpy as np

LADO_TABULEIRO = 512
LADO_CASA = LADO_TABULEIRO // 8

# Abaixo disto cada casa teria menos de 8 px e nenhuma peça seria legível.
LADO_MINIMO = 64


class SegmentadorCasas:
    """Normaliza o tabuleiro para 512×512 e o divide em 64 casas de 64×64 (ADR-003).

    O gerador do dataset de treino (PB09) usa esta mesma classe, para que o
    modelo seja treinado com casas recortadas exatamente como em produção.
    """

    def segmentar(self, tabuleiro: np.ndarray) -> np.ndarray:
        """Recebe só a área do tabuleiro (BGR, ``uint8``) e devolve as 64 casas.

        A saída tem formato ``(64, 64, 64, 3)``: 64 casas de 64×64 na ordem de
        leitura da imagem, linha a linha, de cima para baixo. Com as brancas
        embaixo, essa ordem é a8, b8, …, h1, a mesma de ``Posicao.de_rotulos``.
        """
        if tabuleiro.ndim != 3 or tabuleiro.shape[2] != 3 or tabuleiro.dtype != np.uint8:
            raise ValueError("O tabuleiro precisa ser uma imagem BGR de 8 bits (altura, largura, 3).")
        altura, largura = tabuleiro.shape[:2]
        if min(altura, largura) < LADO_MINIMO:
            raise ValueError(
                f"Tabuleiro de {largura}×{altura} px; o mínimo é {LADO_MINIMO}×{LADO_MINIMO}."
            )

        if (altura, largura) != (LADO_TABULEIRO, LADO_TABULEIRO):
            # INTER_AREA evita serrilhado ao reduzir; INTER_CUBIC preserva as bordas ao ampliar.
            reduzindo = min(altura, largura) > LADO_TABULEIRO
            tabuleiro = cv2.resize(
                tabuleiro,
                (LADO_TABULEIRO, LADO_TABULEIRO),
                interpolation=cv2.INTER_AREA if reduzindo else cv2.INTER_CUBIC,
            )

        # (8, 64, 8, 64, 3) -> (8, 8, 64, 64, 3) -> (64, 64, 64, 3)
        casas = tabuleiro.reshape(8, LADO_CASA, 8, LADO_CASA, 3).swapaxes(1, 2)
        return np.ascontiguousarray(casas.reshape(64, LADO_CASA, LADO_CASA, 3))
