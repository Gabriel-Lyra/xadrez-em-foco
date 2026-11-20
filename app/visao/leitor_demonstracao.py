"""Leitor de demonstração (ADR-011).

Devolve sempre a mesma posição de exemplo, sem olhar a imagem, para que a API e
a página possam ser usadas de ponta a ponta antes de o modelo existir. A
resposta da API informa ``"modo": "demonstracao"`` e um aviso explícito.
"""

from app.dominio.posicao import ROTULO_VAZIO, Posicao
from app.visao.classificacao import Classificacao
from app.visao.leitor_pecas import MODO_DEMONSTRACAO


class LeitorDemonstracao:
    # Mesma posição do protótipo de alta fidelidade (docs/prototipo).
    FEN_EXEMPLO = "r1bqk2r/pppnbppp/4pn2/3p2B1/2PP4/2N1P3/PP3PPP/R2QKBNR"

    modo = MODO_DEMONSTRACAO

    def ler(self, imagem) -> list[Classificacao]:
        matriz = Posicao.de_fen(self.FEN_EXEMPLO).para_matriz()
        return [
            Classificacao(ROTULO_VAZIO if peca is None else peca, None)
            for linha in matriz
            for peca in linha
        ]
