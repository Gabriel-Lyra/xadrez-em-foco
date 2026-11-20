"""Validação e decodificação do arquivo enviado (RF01)."""

import struct

import cv2
import numpy as np

from app.infra.configuracao import Configuracao


class ImagemInvalida(Exception):
    """Arquivo ausente, vazio, corrompido ou em formato não suportado (resposta 400)."""


class ImagemGrandeDemais(Exception):
    """Arquivo acima de 10 MB ou imagem acima do limite de pixels (resposta 413)."""


def ler_dimensoes(dados: bytes, formato: str) -> tuple[int, int] | None:
    """Largura e altura lidas do cabeçalho, sem decodificar os pixels.

    Devolve ``None`` se o cabeçalho estiver incompleto.
    """
    try:
        if formato == "png":
            if dados[12:16] != b"IHDR":
                return None
            return struct.unpack(">II", dados[16:24])
        if formato == "jpg":
            posicao = 2
            while posicao + 9 <= len(dados):
                if dados[posicao] != 0xFF:
                    return None
                marcador = dados[posicao + 1]
                if marcador == 0xFF:  # preenchimento
                    posicao += 1
                    continue
                if marcador in (0xD8, 0x01) or 0xD0 <= marcador <= 0xD7:  # marcadores sem tamanho
                    posicao += 2
                    continue
                tamanho = struct.unpack(">H", dados[posicao + 2 : posicao + 4])[0]
                # SOF0 a SOF15, exceto DHT (C4), JPG (C8) e DAC (CC): trazem as dimensões.
                if 0xC0 <= marcador <= 0xCF and marcador not in (0xC4, 0xC8, 0xCC):
                    altura, largura = struct.unpack(">HH", dados[posicao + 5 : posicao + 9])
                    return largura, altura
                posicao += 2 + tamanho
            return None
        if formato == "webp":
            bloco = dados[12:16]
            if bloco == b"VP8 ":
                largura, altura = struct.unpack("<HH", dados[26:30])
                return largura & 0x3FFF, altura & 0x3FFF
            if bloco == b"VP8L":
                bits = struct.unpack("<I", dados[21:25])[0]
                return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
            if bloco == b"VP8X":
                largura = int.from_bytes(dados[24:27], "little") + 1
                altura = int.from_bytes(dados[27:30], "little") + 1
                return largura, altura
            return None
    except struct.error:
        return None
    return None


class ValidadorImagem:
    """Confere o formato pelos primeiros bytes do arquivo e as dimensões pelo cabeçalho.

    A extensão do nome e o tipo informado pelo navegador não são usados, porque
    qualquer arquivo pode ser renomeado para ``.png``. As dimensões são
    conferidas antes de decodificar: um PNG de 10 MB pode ter centenas de
    megapixels e ocupar gigabytes de memória ao ser aberto.
    """

    def __init__(
        self,
        tamanho_max_bytes: int = Configuracao.MAX_CONTENT_LENGTH,
        max_pixels: int = Configuracao.MAX_PIXELS,
    ):
        self._tamanho_max_bytes = tamanho_max_bytes
        self._max_pixels = max_pixels

    def validar(self, dados: bytes) -> str:
        """Formato do arquivo: ``"png"``, ``"jpg"`` ou ``"webp"``."""
        if not dados:
            raise ImagemInvalida("Arquivo vazio.")
        if len(dados) > self._tamanho_max_bytes:
            raise ImagemGrandeDemais("Arquivo acima do limite.")
        if dados.startswith(b"\x89PNG\r\n\x1a\n"):
            formato = "png"
        elif dados.startswith(b"\xff\xd8\xff"):
            formato = "jpg"
        elif dados[:4] == b"RIFF" and dados[8:12] == b"WEBP":
            formato = "webp"
        else:
            raise ImagemInvalida("Formato não suportado.")

        dimensoes = ler_dimensoes(dados, formato)
        if dimensoes is None or min(dimensoes) == 0:
            raise ImagemInvalida("Cabeçalho da imagem ilegível.")
        largura, altura = dimensoes
        if largura * altura > self._max_pixels:
            raise ImagemGrandeDemais(f"Imagem de {largura}×{altura} px acima do limite.")
        return formato

    def carregar(self, dados: bytes) -> np.ndarray:
        """Valida e decodifica a imagem em uma matriz BGR de 8 bits."""
        self.validar(dados)
        imagem = cv2.imdecode(np.frombuffer(dados, np.uint8), cv2.IMREAD_COLOR)
        if imagem is None:
            raise ImagemInvalida("Não foi possível decodificar a imagem.")
        return imagem
