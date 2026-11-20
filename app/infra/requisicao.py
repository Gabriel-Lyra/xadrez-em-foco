"""Requisição que mantém os arquivos enviados só em memória."""

import io

from flask import Request


class RequisicaoEmMemoria(Request):
    """Por padrão, o Werkzeug grava em arquivo temporário uploads acima de 500 KB.

    Como a imagem não pode ir para o disco (Documento de Arquitetura, privacidade),
    todo upload é recebido em memória. O tamanho já é limitado a 10 MB por
    ``MAX_CONTENT_LENGTH``.
    """

    def _get_file_stream(
        self, total_content_length, content_type, filename=None, content_length=None
    ):
        return io.BytesIO()
