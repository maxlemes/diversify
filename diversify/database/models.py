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


# ==============================================================================
# MODELOS DAS TABELAS (TABLE MODELS)
# ==============================================================================


# --- TABELA COM A INFO DOS ATIVOS ---
class Ativo(Base):
    """
    Representa um ativo financeiro que pode estar em uma carteira.
    Ex: PETR4, Tesouro Selic 2029, IVVB11.
    """

    __tablename__ = "ativos"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Ticker é o código único do ativo. Ex: "ITSA4", "MXRF11".
    # `unique=True` garante que não teremos dois ativos com o mesmo ticker.
    # `index=True` torna as buscas por ticker muito mais rápidas.
    ticker: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(100))
    # Usamos o Enum que criamos para garantir que o tipo seja sempre um dos valores válidos.
    tipo: Mapped[TipoAtivo] = mapped_column(Enum(TipoAtivo))

    def __repr__(self) -> str:
        return f"Ativo(ticker='{self.ticker}', nome='{self.nome}', tipo='{self.tipo.value}')"


# --- TABELA COM PREÇOS HITÓRICOS ---
class PrecoHistorico(Base):
    """
    Armazena os dados de cotação diária para ativos e índices (IBOV, XFIX11).
    Essencial para calcular volatilidade e performance.
    """

    # Define o nome da tabela no banco de dados.
    __tablename__ = "precos_historicos"

    # --- Definição das Colunas ---
    ativo_id: Mapped[int] = mapped_column(ForeignKey("ativos.id"))

    data_pregao: Mapped[datetime.date] = mapped_column(Date, index=True)
    preco_fechamento: Mapped[float] = mapped_column(Float)

    # Adicionamos um relacionamento para facilitar a navegação no código.
    # Ex: `preco.ativo.ticker`
    ativo: Mapped["Ativo"] = relationship()

    # --- Definição das Regras da Tabela --
    # é o lugar correto para chaves primárias compostas.
    __table_args__ = (
        PrimaryKeyConstraint("data_pregao", "ativo_id", name="pk_preco_historico"),
    )

    def __repr__(self) -> str:
        return f"PrecoHistorico(ativo_id='{self.ativo_id}', data='{self.data_pregao}', preco='{self.preco_fechamento}')"
