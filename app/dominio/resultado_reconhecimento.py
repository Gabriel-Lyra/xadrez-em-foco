"""Resultado do reconhecimento, no formato da resposta de ``POST /api/reconhecer``."""

from dataclasses import dataclass

from app.dominio.peca import Cor


@dataclass(frozen=True)
class ResultadoReconhecimento:
    fen: str
    fen_invertido: str
    orientacao: Cor
    pecas: list[list[str | None]]
    confianca_media: float | None
    avisos: list[str]
    link_lichess: str
    link_lichess_invertido: str
    modo: str
    tempo_ms: int

    def para_dict(self) -> dict:
        """Corpo JSON da resposta (Tabela 9 do Documento de Arquitetura e ADR-011)."""
        return {
            "fen": self.fen,
            "fen_invertido": self.fen_invertido,
            "orientacao": self.orientacao.value,
            "pecas": self.pecas,
            "confianca_media": (
                None if self.confianca_media is None else round(self.confianca_media, 3)
            ),
            "avisos": self.avisos,
            "link_lichess": self.link_lichess,
            "link_lichess_invertido": self.link_lichess_invertido,
            "modo": self.modo,
            "tempo_ms": self.tempo_ms,
        }
