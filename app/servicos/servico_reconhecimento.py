"""ServicoReconhecimento: orquestra o pipeline do print até o resultado."""

from statistics import fmean
from time import perf_counter

from app.dominio.gerador_fen import GeradorFEN
from app.dominio.gerador_link_lichess import GeradorLinkLichess
from app.dominio.orientacao import detectar_orientacao
from app.dominio.peca import Cor
from app.dominio.posicao import COLUNAS, Posicao
from app.dominio.resultado_reconhecimento import ResultadoReconhecimento
from app.dominio.validador_posicao import ValidadorPosicao
from app.servicos.validador_imagem import ValidadorImagem
from app.visao.leitor_pecas import MODO_DEMONSTRACAO, LeitorPecas

AVISO_DEMONSTRACAO = (
    "Modo demonstração: a posição exibida é um exemplo fixo, e não a do seu print."
)

# Casas com confiança abaixo deste valor são listadas em um aviso. Com o modelo
# de 16/11/2026, em peças nunca vistas no treino, o limiar de 0,7 aponta 134 dos
# 137 erros e marca, em média, 0,6 casa correta por tabuleiro (modelos/README.md).
LIMIAR_CONFIANCA = 0.7
MAX_CASAS_NO_AVISO = 6


AVISO_ORIENTACAO_INCERTA = (
    "Não foi possível identificar o lado de baixo do tabuleiro; o resultado assume "
    "as brancas embaixo. Confira e troque se for preciso."
)


def nome_casa(indice: int, lado_de_baixo: Cor) -> str:
    """Nome da casa na posição ``indice`` do print (0 = canto superior esquerdo)."""
    linha, coluna = divmod(indice, 8)
    if lado_de_baixo is Cor.PRETA:
        return f"{COLUNAS[7 - coluna]}{linha + 1}"
    return f"{COLUNAS[coluna]}{8 - linha}"


def aviso_leitura_incerta(
    confiancas: list[float | None], lado_de_baixo: Cor = Cor.BRANCA
) -> str | None:
    """Aviso com as casas de leitura incerta, nomeadas conforme o lado de baixo."""
    incertas = [
        nome_casa(i, lado_de_baixo)
        for i, confianca in enumerate(confiancas)
        if confianca is not None and confianca < LIMIAR_CONFIANCA
    ]
    if not incertas:
        return None
    lista = ", ".join(incertas[:MAX_CASAS_NO_AVISO])
    if len(incertas) > MAX_CASAS_NO_AVISO:
        lista += f" e mais {len(incertas) - MAX_CASAS_NO_AVISO}"
    return f"Leitura incerta em {lista} (com as {lado_de_baixo.value} embaixo): confira essas casas."


class ServicoReconhecimento:
    def __init__(
        self,
        leitor: LeitorPecas,
        validador_imagem: ValidadorImagem | None = None,
    ):
        self._leitor = leitor
        self._validador_imagem = validador_imagem or ValidadorImagem()
        self._gerador_fen = GeradorFEN()
        self._validador_posicao = ValidadorPosicao()
        self._gerador_link = GeradorLinkLichess()

    @property
    def modo(self) -> str:
        return self._leitor.modo

    def reconhecer(self, imagem: bytes) -> ResultadoReconhecimento:
        """Valida e decodifica a imagem, lê as 64 casas e monta o resultado.

        Lança ``ImagemInvalida`` (400), ``ImagemGrandeDemais`` (413) ou
        ``TabuleiroNaoEncontrado`` (422).
        """
        inicio = perf_counter()
        pixels = self._validador_imagem.carregar(imagem)

        classificacoes = self._leitor.ler(pixels)
        if len(classificacoes) != 64:
            raise ValueError(f"O leitor devolveu {len(classificacoes)} casas; esperado 64.")
        posicao = Posicao.de_rotulos([c.rotulo for c in classificacoes])
        invertida = posicao.invertida()

        # A leitura assume as brancas embaixo; a detecção diz qual dos dois FEN
        # vale, e o usuário pode corrigir na tela (ADR-009).
        deteccao = detectar_orientacao(posicao)
        orientacao = deteccao.lado_de_baixo
        fen = self._gerador_fen.gerar(posicao)
        fen_invertido = self._gerador_fen.gerar(invertida)

        confiancas = [c.confianca for c in classificacoes]
        avisos = []
        if self._leitor.modo == MODO_DEMONSTRACAO:
            avisos.append(AVISO_DEMONSTRACAO)
        incerteza = aviso_leitura_incerta(confiancas, orientacao)
        if incerteza:
            avisos.append(incerteza)
        if not deteccao.conclusiva:
            avisos.append(AVISO_ORIENTACAO_INCERTA)
        avisos.extend(self._validador_posicao.validar(posicao))

        confianca_media = None if None in confiancas else fmean(confiancas)

        return ResultadoReconhecimento(
            fen=fen,
            fen_invertido=fen_invertido,
            orientacao=orientacao,
            pecas=posicao.para_matriz(),
            confianca_media=confianca_media,
            avisos=avisos,
            link_lichess=self._gerador_link.gerar(fen),
            link_lichess_invertido=self._gerador_link.gerar(fen_invertido),
            modo=self._leitor.modo,
            tempo_ms=round((perf_counter() - inicio) * 1000),
        )
