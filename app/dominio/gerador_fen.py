"""Geração do campo de posição do FEN (RF04)."""

from app.dominio.posicao import Posicao


class GeradorFEN:
    def gerar(self, posicao: Posicao) -> str:
        """Campo de posição do FEN, percorrendo as fileiras da 8 para a 1.

        Casas vazias consecutivas viram um número (``"8"``, ``"3"``…). Turno,
        roque e en passant estão fora do escopo do MVP.
        """
        return "/".join(self._gerar_fileira(fileira) for fileira in posicao.fileiras())

    @staticmethod
    def _gerar_fileira(fileira) -> str:
        resultado = []
        vazias = 0
        for peca in fileira:
            if peca is None:
                vazias += 1
                continue
            if vazias:
                resultado.append(str(vazias))
                vazias = 0
            resultado.append(peca.simbolo_fen())
        if vazias:
            resultado.append(str(vazias))
        return "".join(resultado)
