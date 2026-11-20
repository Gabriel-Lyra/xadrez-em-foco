"""Link para o tabuleiro de análise do Lichess (RF06)."""


class GeradorLinkLichess:
    URL_BASE = "https://lichess.org/analysis/standard/"
    # Turno, roque, en passant e contadores não são lidos do print (fora do
    # escopo); o Lichess exige os campos, então vão com os valores padrão.
    CAMPOS_PADRAO = "w - - 0 1"

    def gerar(self, campo_posicao: str) -> str:
        """URL de análise para o campo de posição do FEN.

        Os espaços do FEN completo viram ``_``, formato aceito pelo Lichess na URL.
        """
        if not campo_posicao or " " in campo_posicao:
            raise ValueError("Informe apenas o campo de posição do FEN, sem espaços.")
        fen_completo = f"{campo_posicao} {self.CAMPOS_PADRAO}"
        return self.URL_BASE + fen_completo.replace(" ", "_")
