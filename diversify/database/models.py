import datetime
import enum
from typing import List, Optional

# Importa a Base do seu projeto db_nexus. É o catálogo central!
from db_nexus.base import Base

# Importe o Enum do SQLAlchemy também
from sqlalchemy import (
    Date,
    Enum,
    Float,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


# ==============================================================================
# ENUMS
# ==============================================================================
# Colocamos o Enum aqui para ser usado pelo modelo da tabela.
# Usar Enums em vez de strings evita erros de digitação e torna o código mais claro.
class TipoAtivo(enum.Enum):
    ACAO = "Ação"
    FII = "Fundo Imobiliário"
    FIAGRO = "FiAgro"
    FIINFRA = "FI-Infra"
    RENDA_FIXA = "Renda Fixa"
    ETF_BR = "ETF Brasil"
    ETF_EXTERIOR = "ETF Exterior"
    BDR = "BDR"
    CRIPTOMOEDA = "Criptomoeda"
    INDICE = "Índice"


# --- TABELA COM A INFO DOS ATIVOS ---
class Ativo(Base):
    """
    Representa um ativo financeiro que pode estar em uma carteira.
    Ex: PETR4, Tesouro Selic 2029, IVVB11.
    """

    __tablename__ = "ativos"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[TipoAtivo] = mapped_column(Enum(TipoAtivo))

    # 🔁 Relacionamentos recíprocos
    precos_historicos: Mapped[list["PrecoHistorico"]] = relationship(
        back_populates="ativo", cascade="all, delete-orphan"
    )

    indicadores: Mapped[list["Indicador"]] = relationship(
        back_populates="ativo", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Ativo(ticker='{self.ticker}', nome='{self.nome}', tipo='{self.tipo.value}')"


# --- TABELA COM PREÇOS HISTÓRICOS ---
class PrecoHistorico(Base):
    __tablename__ = "precos_historicos"

    ativo_id: Mapped[int] = mapped_column(ForeignKey("ativos.id"))
    data_pregao: Mapped[datetime.date] = mapped_column(Date, index=True)
    preco_fechamento: Mapped[float] = mapped_column(Float)
    retorno: Mapped[float | None] = mapped_column(Float, nullable=True)

    # 🔁 Relacionamento de volta para Ativo
    ativo: Mapped["Ativo"] = relationship(back_populates="precos_historicos")

    __table_args__ = (
        PrimaryKeyConstraint("data_pregao", "ativo_id", name="pk_preco_historico"),
    )

    def __repr__(self) -> str:
        return f"PrecoHistorico(ativo_id={self.ativo_id}, data={self.data_pregao}, preco={self.preco_fechamento})"


# --- TABELA DE INDICADORES FUNDAMENTALISTAS E DE RISCO ---
class Indicador(Base):
    __tablename__ = "indicadores"

    ativo_id: Mapped[int] = mapped_column(
        ForeignKey("ativos.id"), index=True, nullable=False
    )
    data_referencia: Mapped[datetime.date] = mapped_column(
        Date, index=True, nullable=False
    )

    # --- Indicadores fundamentalistas ---
    p_vp: Mapped[float | None] = mapped_column(Float)
    p_l: Mapped[float | None] = mapped_column(Float)
    dy: Mapped[float | None] = mapped_column(Float)
    ev_ebitda: Mapped[float | None] = mapped_column(Float)
    margem_liquida: Mapped[float | None] = mapped_column(Float)
    roe: Mapped[float | None] = mapped_column(Float)
    roic: Mapped[float | None] = mapped_column(Float)
    divida_liquida_ebitda: Mapped[float | None] = mapped_column(Float)

    # --- Indicador de risco ---
    # O banco já tem a coluna `volatilidade`. Aqui mapeamos o atributo
    # `volatilidade_2a` para essa coluna para manter nomes claros no código
    # sem alterar o schema do SQLite.
    volatilidade_2a: Mapped[float | None] = mapped_column(
        "volatilidade", Float, doc="Volatilidade(últimos 2 anos)"
    )

    # 🔁 Relacionamento de volta para Ativo
    ativo: Mapped["Ativo"] = relationship(back_populates="indicadores")

    # Tornamos (ativo_id, data_referencia) a chave primária composta
    __table_args__ = (
        PrimaryKeyConstraint("ativo_id", "data_referencia", name="pk_indicador"),
    )

    def __repr__(self) -> str:
        return f"Indicador(ativo_id={self.ativo_id}, data={self.data_referencia}, vol_2a={self.volatilidade_2a})"
