"""LeitorModelo: lê as peças do print com o modelo treinado (PB22, ADR-003 e ADR-011).

Substitui o ``LeitorDemonstracao``: localiza o tabuleiro, recorta as 64 casas e
classifica todas em um único lote.
"""

from pathlib import Path

import numpy as np

from app.visao.classificacao import Classificacao
from app.visao.classificador_pecas import ClassificadorPecas
from app.visao.detector_tabuleiro import DetectorTabuleiro
from app.visao.leitor_pecas import MODO_MODELO
from app.visao.segmentador_casas import SegmentadorCasas


class LeitorModelo:
    modo = MODO_MODELO

    def __init__(
        self,
        classificador: ClassificadorPecas,
        detector: DetectorTabuleiro | None = None,
        segmentador: SegmentadorCasas | None = None,
    ):
        self._classificador = classificador
        self._detector = detector or DetectorTabuleiro()
        self._segmentador = segmentador or SegmentadorCasas()

    @classmethod
    def do_arquivo(cls, arquivo_modelo: Path) -> "LeitorModelo":
        """Carrega o modelo uma única vez, na criação da aplicação."""
        return cls(ClassificadorPecas(arquivo_modelo))

    def ler(self, imagem: np.ndarray) -> list[Classificacao]:
        """Lança ``TabuleiroNaoEncontrado`` se não houver um tabuleiro no print."""
        tabuleiro = self._detector.recortar(imagem)
        casas = self._segmentador.segmentar(tabuleiro)
        return self._classificador.classificar(casas)
