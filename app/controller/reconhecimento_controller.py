"""ReconhecimentoController: API ``POST /api/reconhecer``."""

import logging

from flask import Blueprint, current_app, jsonify, request
from werkzeug.exceptions import HTTPException, RequestEntityTooLarge

from app.servicos.validador_imagem import ImagemGrandeDemais, ImagemInvalida
from app.visao.leitor_pecas import TabuleiroNaoEncontrado

api_bp = Blueprint("api", __name__, url_prefix="/api")
logger = logging.getLogger(__name__)

# Mensagens da Tabela 4 do Documento de Arquitetura.
MENSAGENS = {
    400: "Envie uma imagem PNG, JPG ou WEBP.",
    413: "A imagem excede o limite de 10 MB ou de 25 megapixels.",
    422: "Não encontramos um tabuleiro; recorte o print e tente de novo.",
    500: "Não foi possível processar agora; tente novamente.",
}


def resposta_erro(codigo: int):
    return jsonify({"erro": codigo, "mensagem": MENSAGENS[codigo]}), codigo


@api_bp.post("/reconhecer")
def reconhecer():
    arquivo = request.files.get("imagem")
    if arquivo is None:
        return resposta_erro(400)

    servico = current_app.extensions["servico_reconhecimento"]
    try:
        resultado = servico.reconhecer(arquivo.read())
    except ImagemInvalida:
        return resposta_erro(400)
    except ImagemGrandeDemais:
        return resposta_erro(413)
    except TabuleiroNaoEncontrado:
        return resposta_erro(422)
    return jsonify(resultado.para_dict())


@api_bp.errorhandler(RequestEntityTooLarge)
def arquivo_grande_demais(_erro):
    return resposta_erro(413)


@api_bp.errorhandler(Exception)
def erro_inesperado(erro):
    if isinstance(erro, HTTPException):
        return erro
    # Registra o erro sem a imagem: só o tipo e a pilha de chamadas.
    logger.exception("Erro inesperado em /api/reconhecer")
    return resposta_erro(500)
