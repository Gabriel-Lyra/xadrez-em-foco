"""Aplicação web do Xadrez em Foco.

O ponto de entrada é a função ``create_app`` (padrão *application factory* do
Flask). O modelo ONNX é carregado uma única vez, aqui.
"""

from flask import Flask

from app.controller.pagina_controller import pagina_bp
from app.controller.reconhecimento_controller import api_bp
from app.infra.configuracao import Configuracao
from app.infra.requisicao import RequisicaoEmMemoria
from app.servicos.servico_reconhecimento import ServicoReconhecimento
from app.visao.leitor_demonstracao import LeitorDemonstracao
from app.visao.leitor_modelo import LeitorModelo
from app.visao.leitor_pecas import MODO_DEMONSTRACAO, MODO_MODELO


def criar_leitor(config):
    if config["LEITOR"] == MODO_MODELO:
        return LeitorModelo.do_arquivo(config["ARQUIVO_MODELO"])
    if config["LEITOR"] == MODO_DEMONSTRACAO:
        return LeitorDemonstracao()
    raise ValueError(f"LEITOR deve ser {MODO_MODELO!r} ou {MODO_DEMONSTRACAO!r}: {config['LEITOR']!r}")


def create_app(configuracao: type[Configuracao] = Configuracao) -> Flask:
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.config.from_object(configuracao)
    app.request_class = RequisicaoEmMemoria
    # Mantém os campos do JSON na ordem do contrato (Tabela 9).
    app.json.sort_keys = False

    app.extensions["servico_reconhecimento"] = ServicoReconhecimento(criar_leitor(app.config))

    app.register_blueprint(pagina_bp)
    app.register_blueprint(api_bp)

    return app
