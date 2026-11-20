"""Configuração da aplicação."""

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


class Configuracao:
    """Configuração padrão, usada em desenvolvimento e produção."""

    TAMANHO_MAX_MB = 10
    # O Flask recusa com 413 qualquer requisição maior que este limite (RF01).
    MAX_CONTENT_LENGTH = TAMANHO_MAX_MB * 1024 * 1024
    # Limite de pixels conferido antes de decodificar. Cobre prints de telas 6K
    # (6016×3384) e mantém a imagem decodificada abaixo de 75 MB.
    MAX_PIXELS = 25_000_000
    TESTING = False

    # "modelo" (padrão) ou "demonstracao" (ADR-011). Sem o arquivo do modelo, a
    # aplicação não inicia: nunca cai para a demonstração sem avisar.
    LEITOR = os.environ.get("LEITOR", "modelo")
    ARQUIVO_MODELO = RAIZ / "modelos" / "modelo_pecas.onnx"


class ConfiguracaoTeste(Configuracao):
    """Configuração usada pelo pytest.

    Usa o leitor de demonstração: os testes de contrato da API enviam imagens
    sem tabuleiro e não dependem do modelo. Os testes com o modelo usam
    ``ConfiguracaoTesteModelo``.
    """

    TESTING = True
    LEITOR = "demonstracao"


class ConfiguracaoTesteModelo(ConfiguracaoTeste):
    LEITOR = "modelo"
