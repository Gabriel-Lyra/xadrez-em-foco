"""ClassificadorPecas: classifica as 64 casas em lote com o modelo ONNX (PB14, ADR-004)."""

import json
from pathlib import Path

import numpy as np

from app.visao.classificacao import ROTULOS, Classificacao


class ModeloIncompativel(Exception):
    """O arquivo do modelo não corresponde ao que a aplicação espera (erro de implantação)."""


class ClassificadorPecas:
    """Carrega o modelo uma vez e classifica as casas recortadas pelo ``SegmentadorCasas``.

    O arquivo ONNX já contém a conversão para ponto flutuante e o softmax
    (``treinamento/treinar.py``): a entrada é a própria saída do segmentador.
    """

    def __init__(self, arquivo_modelo: Path, arquivo_classes: Path | None = None, threads: int = 1):
        import onnxruntime

        arquivo_modelo = Path(arquivo_modelo)
        arquivo_classes = arquivo_classes or arquivo_modelo.with_name("classes.json")
        classes = tuple(json.loads(Path(arquivo_classes).read_text(encoding="utf-8")))
        if classes != ROTULOS:
            raise ModeloIncompativel(
                f"Classes do modelo {classes} diferentes das da aplicação {ROTULOS}."
            )

        opcoes = onnxruntime.SessionOptions()
        # Uma thread: a instância gratuita tem fração de CPU, e assim o uso de
        # memória e o tempo de resposta ficam previsíveis.
        opcoes.intra_op_num_threads = threads
        opcoes.inter_op_num_threads = 1
        self._sessao = onnxruntime.InferenceSession(
            str(arquivo_modelo), opcoes, providers=["CPUExecutionProvider"]
        )
        entrada = self._sessao.get_inputs()[0]
        if entrada.type != "tensor(uint8)" or list(entrada.shape[1:]) != [64, 64, 3]:
            raise ModeloIncompativel(
                f"Entrada do modelo {entrada.type} {entrada.shape}; esperado uint8 N×64×64×3."
            )
        self._nome_entrada = entrada.name

    def classificar(self, casas: np.ndarray) -> list[Classificacao]:
        """Recebe ``(N, 64, 64, 3)`` ``uint8`` BGR e devolve N classificações, na mesma ordem."""
        if casas.ndim != 4 or casas.shape[1:] != (64, 64, 3) or casas.dtype != np.uint8:
            raise ValueError(f"Casas em formato inesperado: {casas.shape} {casas.dtype}.")
        probabilidades = self._sessao.run(None, {self._nome_entrada: np.ascontiguousarray(casas)})[0]
        indices = probabilidades.argmax(axis=1)
        return [
            Classificacao(ROTULOS[i], float(probabilidades[n, i]))
            for n, i in enumerate(indices)
        ]
