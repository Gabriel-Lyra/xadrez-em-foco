"""Avisos de posição impossível (PB18).

Os avisos não bloqueiam o resultado: servem para o usuário conferir o
reconhecimento, já que uma peça classificada errada costuma gerar uma
posição impossível.
"""

from collections import Counter

from app.dominio.peca import Cor, Peca, TipoPeca
from app.dominio.posicao import Posicao

MAX_PEOES_POR_COR = 8

_NOMES = {
    Cor.BRANCA: ("branco", "brancos"),
    Cor.PRETA: ("preto", "pretos"),
}


class ValidadorPosicao:
    def validar(self, posicao: Posicao) -> list[str]:
        """Lista de avisos; vazia quando a posição é plausível."""
        contagem: Counter[Peca] = Counter()
        peoes_na_borda = []
        for casa, peca in posicao.casas_ocupadas():
            contagem[peca] += 1
            if peca.tipo is TipoPeca.PEAO and casa[1] in "18":
                peoes_na_borda.append(casa)

        avisos = []
        for cor in Cor:
            singular, plural = _NOMES[cor]
            reis = contagem[Peca(cor, TipoPeca.REI)]
            peoes = contagem[Peca(cor, TipoPeca.PEAO)]
            if reis == 0:
                avisos.append(f"Falta o rei {singular}.")
            elif reis > 1:
                avisos.append(f"Há {reis} reis {plural}.")
            if peoes > MAX_PEOES_POR_COR:
                avisos.append(f"Mais de 8 peões {plural} ({peoes}).")

        if peoes_na_borda:
            avisos.append(f"Peão na primeira ou na última fileira: {', '.join(peoes_na_borda)}.")
        return avisos
