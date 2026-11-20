"""DetectorTabuleiro: localiza o tabuleiro 8×8 em um print de tela (PB11, ADR-003).

Em um print, o tabuleiro é um quadrado alinhado aos eixos da imagem, sem
perspectiva. Por isso não é necessário procurar cantos nem corrigir
perspectiva: basta achar, em cada eixo, nove linhas igualmente espaçadas
(as bordas das casas) e confirmar o padrão de casas claras e escuras.

1. Uma cópia reduzida da imagem, em tons de cinza, é usada para a análise.
2. Para cada coluna (e cada linha) da imagem, mede-se quanto o brilho muda
   entre pixels vizinhos. As divisas entre casas aparecem como picos.
3. Para cada tamanho de casa e posição inicial possíveis, a pontuação é a do
   pior dos 7 picos internos esperados. Um único pico forte (a borda de um
   painel, por exemplo) não basta.
4. Os melhores candidatos de cada eixo são combinados em quadrados e
   conferidos pelo padrão alternado de cores das 64 casas.
"""

from dataclasses import dataclass

import cv2
import numpy as np

from app.visao.leitor_pecas import TabuleiroNaoEncontrado

# Lado máximo da cópia usada na análise. Um tabuleiro de 400 px em um print
# 4K ainda fica com casas de 13 px, suficiente para achar as divisas.
LADO_ANALISE = 1024
CASA_MINIMA = 8  # px na cópia de análise
CANDIDATOS_POR_EIXO = 8
# Diferença máxima entre a largura e a altura das casas.
TOLERANCIA_QUADRADO = 0.04
# Fração mínima de casas cuja cor de fundo segue o padrão alternado. Abaixo de
# 1 porque destaques de lance, xeque e setas mudam a cor de algumas casas.
PADRAO_MINIMO = 0.8
# Diferença mínima de brilho (0 a 255) entre casas claras e escuras.
CONTRASTE_MINIMO = 12.0


@dataclass(frozen=True)
class Regiao:
    """Retângulo do tabuleiro em pixels da imagem original (``x1`` e ``y1`` exclusivos)."""

    x0: int
    y0: int
    x1: int
    y1: int

    @property
    def largura(self) -> int:
        return self.x1 - self.x0

    @property
    def altura(self) -> int:
        return self.y1 - self.y0


@dataclass(frozen=True)
class _Candidato:
    inicio: float
    lado: float
    pontuacao: float


def _perfil(gradiente: np.ndarray) -> np.ndarray:
    """Média do gradiente por coluna, com o máximo em uma janela de ±1 px.

    A janela tolera divisas que, depois da redução da imagem, caem entre dois pixels.
    """
    perfil = gradiente.mean(axis=0)
    janela = np.maximum(perfil, np.roll(perfil, 1))
    return np.maximum(janela, np.roll(perfil, -1))


def _candidatos(
    perfil: np.ndarray,
    comprimento: int,
    lados: np.ndarray | None = None,
    faixa_inicio: tuple[float, float] | None = None,
) -> list[_Candidato]:
    """Melhores combinações de início e lado de casa ao longo de um eixo.

    ``perfil[i]`` é a intensidade da divisa entre os pixels ``i`` e ``i + 1``;
    a divisa da casa que começa no pixel ``x`` fica em ``x - 1``. ``lados`` e
    ``faixa_inicio`` restringem a busca no refinamento.
    """
    candidatos = []
    referencia = float(np.median(perfil)) + 1e-6
    k = np.arange(1, 8)
    if lados is None:
        lados = np.arange(CASA_MINIMA, comprimento / 8 + 1, 0.25)
    for lado in lados:
        folga = 0.15 * lado  # o tabuleiro pode estar cortado um pouco na borda da imagem
        if faixa_inicio is None:
            inicios = np.arange(-folga, comprimento - 8 * lado + folga + 1)
        else:
            inicios = np.arange(faixa_inicio[0], faixa_inicio[1] + 0.5, 0.5)
        if len(inicios) == 0:
            continue
        posicoes = np.rint(inicios[:, None] + k * lado).astype(int) - 1
        validas = (posicoes >= 0).all(axis=1) & (posicoes < len(perfil)).all(axis=1)
        if not validas.any():
            continue
        inicios, posicoes = inicios[validas], posicoes[validas]
        # Pior das 7 divisas internas: todas precisam existir.
        pontuacoes = perfil[posicoes].min(axis=1) / referencia
        # Até 3 inícios por lado, em picos diferentes: inícios vizinhos de um
        # mesmo pico têm quase a mesma pontuação e esconderiam o tabuleiro certo.
        escolhidos_lado: list[float] = []
        for i in np.argsort(pontuacoes)[::-1]:
            if all(abs(inicios[i] - e) >= 0.5 * lado for e in escolhidos_lado):
                escolhidos_lado.append(float(inicios[i]))
                candidatos.append(_Candidato(float(inicios[i]), float(lado), float(pontuacoes[i])))
                if len(escolhidos_lado) == 3:
                    break

    candidatos.sort(key=lambda c: c.pontuacao, reverse=True)
    escolhidos: list[_Candidato] = []
    for candidato in candidatos:
        # Descarta candidatos quase iguais a um já escolhido.
        if any(
            abs(candidato.lado - e.lado) < 0.05 * e.lado
            and abs(candidato.inicio - e.inicio) < 0.5 * e.lado
            for e in escolhidos
        ):
            continue
        escolhidos.append(candidato)
        if len(escolhidos) == CANDIDATOS_POR_EIXO:
            break
    return escolhidos


def _fundo_das_casas(imagem: np.ndarray, x0: float, y0: float, lado_x: float, lado_y: float) -> np.ndarray:
    """Cor de fundo (BGR) de cada uma das 64 casas: mediana da faixa junto às bordas.

    As peças ficam no centro da casa; a faixa da borda mostra a cor da casa.
    """
    altura, largura = imagem.shape[:2]
    cores = np.zeros((8, 8, 3), np.float32)
    for linha in range(8):
        for coluna in range(8):
            xa = int(round(x0 + coluna * lado_x))
            ya = int(round(y0 + linha * lado_y))
            xb = int(round(x0 + (coluna + 1) * lado_x))
            yb = int(round(y0 + (linha + 1) * lado_y))
            margem_x = max(1, int(lado_x * 0.12))
            margem_y = max(1, int(lado_y * 0.12))
            xa, ya = max(xa + 1, 0), max(ya + 1, 0)
            xb, yb = min(xb - 1, largura), min(yb - 1, altura)
            if xb - xa < 3 or yb - ya < 3:
                return cores  # casa fora da imagem: o candidato será descartado
            casa = imagem[ya:yb, xa:xb]
            faixa = np.concatenate(
                [
                    casa[:margem_y].reshape(-1, 3),
                    casa[-margem_y:].reshape(-1, 3),
                    casa[:, :margem_x].reshape(-1, 3),
                    casa[:, -margem_x:].reshape(-1, 3),
                ]
            )
            cores[linha, coluna] = np.median(faixa, axis=0)
    return cores


def _padrao_alternado(cores: np.ndarray) -> tuple[float, float]:
    """Fração de casas que seguem o padrão claro/escuro e o contraste entre os dois grupos."""
    paridade = (np.add.outer(np.arange(8), np.arange(8)) % 2).astype(bool)
    grupo_a = np.median(cores[~paridade], axis=0)
    grupo_b = np.median(cores[paridade], axis=0)
    contraste = float(np.linalg.norm(grupo_a - grupo_b))
    distancia_a = np.linalg.norm(cores - grupo_a, axis=2)
    distancia_b = np.linalg.norm(cores - grupo_b, axis=2)
    no_grupo_certo = np.where(paridade, distancia_b < distancia_a, distancia_a < distancia_b)
    return float(no_grupo_certo.mean()), contraste


class DetectorTabuleiro:
    def localizar(self, imagem: np.ndarray) -> Regiao:
        """Região do tabuleiro na imagem BGR. Lança ``TabuleiroNaoEncontrado``."""
        altura, largura = imagem.shape[:2]
        escala = min(1.0, LADO_ANALISE / max(altura, largura))
        reduzida = imagem
        if escala < 1.0:
            reduzida = cv2.resize(
                imagem,
                (max(1, round(largura * escala)), max(1, round(altura * escala))),
                interpolation=cv2.INTER_AREA,
            )
        if min(reduzida.shape[:2]) < 8 * CASA_MINIMA:
            raise TabuleiroNaoEncontrado("Imagem pequena demais para conter um tabuleiro.")

        cinza = cv2.cvtColor(reduzida, cv2.COLOR_BGR2GRAY).astype(np.float32)
        perfil_x = _perfil(np.abs(np.diff(cinza, axis=1)))
        perfil_y = _perfil(np.abs(np.diff(cinza, axis=0)).T)
        candidatos_x = _candidatos(perfil_x, cinza.shape[1])
        candidatos_y = _candidatos(perfil_y, cinza.shape[0])

        melhor = None
        for cx in candidatos_x:
            for cy in candidatos_y:
                if abs(cx.lado - cy.lado) > TOLERANCIA_QUADRADO * max(cx.lado, cy.lado):
                    continue
                cores = _fundo_das_casas(reduzida, cx.inicio, cy.inicio, cx.lado, cy.lado)
                padrao, contraste = _padrao_alternado(cores)
                if padrao < PADRAO_MINIMO or contraste < CONTRASTE_MINIMO:
                    continue
                # O padrão decide; as divisas desempatam (por exemplo, entre o
                # tabuleiro certo e o deslocado uma casa para fora da borda).
                chave = (round(padrao, 2), min(cx.pontuacao, cy.pontuacao))
                if melhor is None or chave > melhor[0]:
                    melhor = (chave, cx, cy)

        if melhor is None:
            raise TabuleiroNaoEncontrado("Nenhuma grade 8×8 com casas alternadas foi encontrada.")

        _, cx, cy = melhor
        x0, lado_x = self._refinar(imagem, cx.inicio / escala, cx.lado / escala, eixo=1)
        y0, lado_y = self._refinar(imagem, cy.inicio / escala, cy.lado / escala, eixo=0)
        regiao = Regiao(
            x0=max(0, round(x0)),
            y0=max(0, round(y0)),
            x1=min(largura, round(x0 + 8 * lado_x)),
            y1=min(altura, round(y0 + 8 * lado_y)),
        )
        if min(regiao.largura, regiao.altura) < 64:
            raise TabuleiroNaoEncontrado("O tabuleiro encontrado é pequeno demais para ser lido.")
        return regiao

    def _refinar(self, imagem: np.ndarray, inicio: float, lado: float, eixo: int) -> tuple[float, float]:
        """Ajusta início e lado na resolução original, em uma faixa em volta da estimativa.

        Na cópia reduzida, um erro de 1 px vira vários pixels no print original;
        o recorte precisa ficar dentro da tolerância usada no treino (cerca de 1%).
        """
        comprimento = imagem.shape[eixo]
        a = max(0, int(inicio - lado))
        b = min(comprimento, int(inicio + 9 * lado) + 1)
        faixa = imagem[:, a:b] if eixo == 1 else imagem[a:b, :].transpose(1, 0, 2)
        # A outra dimensão não precisa de resolução total para medir as divisas.
        if faixa.shape[0] > LADO_ANALISE:
            passo = int(np.ceil(faixa.shape[0] / LADO_ANALISE))
            faixa = faixa[::passo]
        cinza = cv2.cvtColor(np.ascontiguousarray(faixa), cv2.COLOR_BGR2GRAY).astype(np.float32)
        perfil = _perfil(np.abs(np.diff(cinza, axis=1)))
        lados = np.arange(lado * 0.95, lado * 1.05, max(0.05, lado / 400))
        relativo = inicio - a
        refinados = _candidatos(
            perfil, cinza.shape[1], lados, (relativo - 0.45 * lado, relativo + 0.45 * lado)
        )
        if not refinados:
            return inicio, lado
        return a + refinados[0].inicio, refinados[0].lado

    def recortar(self, imagem: np.ndarray) -> np.ndarray:
        """Só a área do tabuleiro, pronta para o ``SegmentadorCasas``."""
        regiao = self.localizar(imagem)
        return imagem[regiao.y0 : regiao.y1, regiao.x0 : regiao.x1]
