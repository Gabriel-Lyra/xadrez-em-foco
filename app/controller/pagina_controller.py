"""PaginaController: entrega a página única da aplicação e a verificação de saúde."""

from flask import Blueprint, current_app, jsonify, render_template

pagina_bp = Blueprint("pagina", __name__)


@pagina_bp.get("/")
def index():
    return render_template("index.html")


@pagina_bp.get("/saude")
def saude():
    """Usada pela hospedagem para saber se a aplicação subiu (o modelo é carregado na criação)."""
    servico = current_app.extensions["servico_reconhecimento"]
    return jsonify({"status": "ok", "modo": servico.modo})
