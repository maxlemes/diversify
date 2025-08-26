# ==============================================================================
# DIVERSIFY/DIVERSIFY/MODELS.PY
# ==============================================================================
#
# DESCRIÇÃO:
# Este arquivo é o "coração" da estrutura de dados da aplicação. Ele define
# todas as tabelas do banco de dados usando o SQLAlchemy ORM (Object-Relational
# Mapper). Em vez de escrever SQL, definimos classes Python que o SQLAlchemy
# traduz para tabelas e colunas no banco de dados SQLite.
#
# COMPONENTES PRINCIPAIS:
#
# 1. Enums (TipoAtivo, TipoOperacao):
#    - Classes que definem um conjunto fixo de opções para campos como o tipo
#      de um ativo ou o tipo de uma operação (Compra/Venda). Usar Enums
#      aumenta a clareza do código e previne erros de digitação.
#
# 2. Modelos de Tabelas (Base Declarativa):
#    - Carteira: Representa uma carteira de investimentos.
#    - Ativo: Representa um ativo financeiro (ex: PETR4, MXRF11). Contém
#      informações estáticas sobre o ativo.
#    - Transacao: Registra uma operação de compra ou venda de um ativo em uma
#      determinada data e para uma carteira específica.
#    - DadoHistorico: Armazena as cotações diárias de fechamento para ativos
#      e índices, essencial para cálculos de performance e risco.
#
# 3. Função de Setup (db_start):
#    - Uma função centralizada que verifica a existência do arquivo de banco de
#      dados ('portfolio.db'). Se o arquivo não existir, ela cria o banco e
#      todas as tabelas definidas neste arquivo. Garante que a aplicação
#      sempre tenha uma estrutura de dados válida para trabalhar.
#
# RELACIONAMENTOS:
# - Uma Carteira pode ter várias Transacoes.
# - Um Ativo pode estar em várias Transacoes.
# - Cada Transacao pertence a exatamente uma Carteira e um Ativo.
#
# ==============================================================================

import datetime
import enum  # Usaremos enums para padronizar os tipos
import os
from typing import List, Optional

from sqlalchemy import (
    Date,
    Enum,
    Float,
    ForeignKey,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


# --- FUNÇÃO DE SETUP CENTRALIZADA ---
def db_start():
    """
    Verifica se o banco de dados existe. Se não existir, cria a estrutura
    inicial. Esta função agora é a única fonte da verdade para o setup.
    Retorna True se o banco já existia, False se foi criado agora.
    """
    DATA_DIR = "data"
    DB_FILE = f"{DATA_DIR}/portfolio.db"
    DB_URL = f"sqlite:///{DB_FILE}"

    if os.path.exists(DB_FILE):
        return True  # Banco já existe, pode continuar

    print(f"O banco de dados '{DB_FILE}' não foi encontrado.")
    print("Criando estrutura inicial do banco de dados...")

    os.makedirs(DATA_DIR, exist_ok=True)
    engine = create_engine(DB_URL)

    # Usa a 'Base' deste mesmo arquivo para criar as tabelas
    Base.metadata.create_all(engine)

    print("✅ Banco de dados criado com sucesso!")
    return False  # Banco foi criado agora


# --- Classes de Enumeração ---
# Usar Enums em vez de strings evita erros de digitação e torna o código mais claro.
class TipoAtivo(enum.Enum):
    ACAO = "Ação"
    FII = "Fundo Imobiliário"
    RENDA_FIXA = "Renda Fixa"
    ETF_BR = "ETF Brasil"
    ETF_EXTERIOR = "ETF Exterior"
    BDR = "BDR"
    CRIPTOMOEDA = "Criptomoeda"
    INDICE = "Índice"


class TipoOperacao(enum.Enum):
    COMPRA = "Compra"
    VENDA = "Venda"


# --- Modelos do Banco de Dados ---


class Carteira(Base):
    __tablename__ = "carteiras"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    transacoes: Mapped[List["Transacao"]] = relationship(back_populates="carteira")

    def __repr__(self) -> str:
        return f"Carteira(id={self.id}, nome='{self.nome}')"


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

    # Armazenará a volatilidade anualizada calculada.
    # É 'nullable=True' porque um ativo pode não ter dados históricos suficientes.
    volatilidade: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relacionamento: Um Ativo pode ter muitas Transações associadas a ele.
    # `cascade` significa que se um ativo for deletado, todas as suas transações também serão.
    transacoes: Mapped[List["Transacao"]] = relationship(
        back_populates="ativo", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Ativo(ticker='{self.ticker}', nome='{self.nome}', tipo='{self.tipo.value}')"


class Transacao(Base):
    """
    Representa uma operação de compra ou venda de um ativo.
    """

    __tablename__ = "transacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    # `ForeignKey` cria o link entre a Transacao e o Ativo. Uma transação DEVE pertencer a um ativo.
    ativo_id: Mapped[int] = mapped_column(ForeignKey("ativos.id"), nullable=False)
    data: Mapped[datetime.date] = mapped_column(Date)
    tipo_operacao: Mapped[TipoOperacao] = mapped_column(Enum(TipoOperacao))
    # Usamos Float para quantidade e preço para suportar ativos fracionários.
    quantidade: Mapped[float] = mapped_column(Float)
    preco_unitario: Mapped[float] = mapped_column(Float)

    # Relacionamento reverso: permite acessar o objeto Ativo a partir de uma Transacao. Ex: minha_transacao.ativo
    ativo: Mapped["Ativo"] = relationship(back_populates="transacoes")
    carteira_id: Mapped[int] = mapped_column(ForeignKey("carteiras.id"), nullable=False)
    carteira: Mapped["Carteira"] = relationship(back_populates="transacoes")

    def __repr__(self) -> str:
        return f"Transacao(ativo='{self.ativo.ticker}', data='{self.data}', tipo='{self.tipo_operacao.value}', qtd={self.quantidade})"


class DadoHistorico(Base):
    """
    Armazena os dados de cotação diária para ativos e índices (IBOV, XFIX11).
    Essencial para calcular volatilidade e performance.
    """

    __tablename__ = "dados_historicos"

    # Adicionamos uma restrição para garantir que não teremos duas entradas para o mesmo
    # ticker no mesmo dia. Isso mantém a integridade dos nossos dados.
    __table_args__ = (UniqueConstraint("ticker", "data", name="uix_ticker_data"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    # O ticker aqui pode ser de um ativo da nossa carteira (ex: "PETR4")
    # ou de um índice (ex: "IBOV"). Por isso não usamos ForeignKey.
    ticker: Mapped[str] = mapped_column(String(20), index=True)
    data: Mapped[datetime.date] = mapped_column(Date, index=True)
    preco_fechamento: Mapped[float] = mapped_column(Float)

    def __repr__(self) -> str:
        return f"DadoHistorico(ticker='{self.ticker}', data='{self.data}', preco='{self.preco_fechamento}')"
