# ==============================================================================
# DIVERSIFY/DIVERSIFY/REPOSITORIES.PY
# ==============================================================================
#
# DESCRIÇÃO:
# Este arquivo implementa o "Repository Pattern" (Padrão de Repositório).
# A função de um repositório é atuar como uma camada de abstração entre a
# lógica de negócio da aplicação (que ficará nos 'services') e os modelos de
# dados (definidos em 'models.py').
#
# Em vez de espalhar queries do SQLAlchemy por todo o código, nós as
# centralizamos aqui. Cada classe de repositório é responsável por todas as
# operações de leitura e escrita de um modelo específico no banco de dados.
#
# ARQUITETURA:
#
# 1. BaseRepository:
#    - Cada repositório herda de uma classe genérica `BaseRepository`
#      (definida pela biblioteca 'db_nexus'), que já fornece os métodos básicos de
#      um CRUD (Create, Read, Update, Delete), como `get_by_id`, `list_all`,
#      `add`, e `delete`.
#
# 2. Repositórios Específicos:
#    - Cada classe neste arquivo estende o `BaseRepository` para o seu
#      modelo específico e adiciona métodos de busca mais complexos e
#      significativos para aquele contexto.
#
# VANTAGENS DESTA ABORDAGEM:
# - Centralização: Toda a lógica de acesso ao banco de dados fica em um só lugar.
# - Reutilização: Métodos de busca podem ser reutilizados em diferentes partes
#   da aplicação.
# - Manutenção: Se a forma de buscar um dado mudar, a alteração é feita em
#   apenas um lugar.
# - Testabilidade: Facilita a criação de testes, pois podemos "mockar"
#   (simular) o repositório em vez de interagir com o banco de dados real.
#
# COMPONENTES:
# - AtivoRepository: Gerencia as operações para o modelo 'Ativo'.
# - TransacaoRepository: Gerencia as operações para o modelo 'Transacao'.
# - DadoHistoricoRepository: Gerencia as operações para 'DadoHistorico'.
# - CarteiraRepository: Gerencia as operações para o modelo 'Carteira'.
#
# ==============================================================================

import datetime as dt
from datetime import datetime, timedelta
from typing import List, Tuple

from db_nexus import BaseRepository
from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import Ativo, Indicador, PrecoHistorico, TipoAtivo


# --- Classe para interagir com a tabela AtivoRepository ---
class AtivoRepository(BaseRepository[Ativo]):
    """
    Repositório para operações com o modelo Ativo.
    Herda todos os métodos genéricos (get_by_id, list_all, add, delete)
    de BaseRepository.
    """

    def __init__(self):
        # Passamos o modelo 'Ativo' para o construtor da classe pai.
        super().__init__(Ativo)

    # --- Métodos Específicos para Ativos ---

    def find_or_create(
        self, session: Session, ticker: str, nome: str, tipo: TipoAtivo
    ) -> Ativo:
        """
        Busca um ativo pelo ticker. Se não existir, cria um novo.
        Se existir, verifica se o nome ou tipo precisam ser atualizados.
        """
        instance = session.query(self.model).filter_by(ticker=ticker).first()
        if not instance:
            print(f"Ativo não encontrado, criando: {ticker}")
            instance = Ativo(ticker=ticker, nome=nome, tipo=tipo)
            session.add(instance)
        else:
            # Opcional: Atualiza os dados se eles mudaram
            if instance.nome != nome or instance.tipo != tipo:
                instance.nome = nome
                instance.tipo = tipo
                print(f"Ativo encontrado, atualizando dados: {ticker}")
        return instance

    def list_all_ids_and_tickers(self, session: Session) -> List[Tuple[int, str]]:
        """
        Busca e retorna uma lista de tuplas contendo o ID e o Ticker de todos os ativos.
        """
        print("Buscando ID e Ticker de todos os ativos...")
        # A query seleciona especificamente as colunas 'id' e 'ticker'
        resultados = (
            session.query(self.model.id, self.model.ticker)
            .order_by(self.model.ticker)
            .all()
        )
        # O resultado já vem no formato [ (1, 'ABCB4'), (2, 'BBDC4'), ... ]
        return resultados


# --- Classe para interagir com a tabela PrecoHistorico ---
class PrecoHistoricoRepository(BaseRepository[PrecoHistorico]):
    """
    Repositório para operações com o modelo DadoHistorico.
    """

    def __init__(self):
        super().__init__(PrecoHistorico)

    # --- Métodos Específicos para Precos Históricos ---
    def find_by_ticker_and_date_range(
        self, session: Session, ticker: str, start_date: str, end_date: str
    ) -> list[PrecoHistorico]:
        """
        Busca os dados históricos para um ticker dentro de um intervalo de datas.
        """
        return (
            session.query(self.model)
            .filter(self.model.ticker == ticker.upper())
            .filter(self.model.data.between(start_date, end_date))
            .order_by(self.model.data.asc())
            .all()
        )

    def get_latest_price(
        self, session: Session, ativo_id: int
    ) -> PrecoHistorico | None:
        """
        Busca o preço histórico mais recente de um ativo.
        """
        return (
            session.query(self.model)
            .filter(self.model.ativo_id == ativo_id)
            .order_by(self.model.data_pregao.desc())
            .first()
        )

    def get_latest_date(self, session: Session, ativo_id: int) -> dt.date | None:
        """
        Encontra a data mais recente para a qual já temos um preço para um ativo.
        Esta é a chave para fazer atualizações eficientes.
        """
        # Usa a função `func.max` do SQLAlchemy para executar um `SELECT MAX(data_pregao)`
        latest_date = (
            session.query(func.max(self.model.data_pregao))
            .filter(
                self.model.ativo_id == ativo_id
            )  # Filtra pelo ID do ativo específico
            .scalar()  # Retorna o resultado único (a data ou None)
        )
        return latest_date

    def get_prices_since(self, session: Session, ativo_id: int, anos: int = 2):
        """
        Retorna todos os preços do ativo nos últimos X anos.
        """
        data_limite = datetime.now().date() - timedelta(days=anos * 365)

        return (
            session.query(self.model)
            .filter(self.model.ativo_id == ativo_id)
            .filter(self.model.data_pregao >= data_limite)
            .order_by(self.model.data_pregao.asc())
            .all()
        )
    
    def get_all_prices_since(self, session: Session, start_date):
        """
        Retorna todos os preços do ativo nos últimos X anos.
        """

        return (
            session.query(self.model)
            .filter(self.model.data_pregao >= start_date)
            .order_by(self.model.data_pregao.asc())
            .all()
        )

    def bulk_insert(self, session: Session, precos: list[dict]):
        """Insere uma lista de preços de forma otimizada."""
        if not precos:
            return
        session.bulk_insert_mappings(self.model, precos)
        print(f"{len(precos)} novos registros de preços inseridos.")


class IndicatorRepository:
    def inserir_ou_atualizar(
        self,
        session: Session,
        ativo_id: int,
        data_ref: datetime.date,
        volatilidade_2a: float,
    ):
        """
        Insere ou atualiza o indicador de volatilidade sem dar commit.
        O commit é feito pelo service.
        """
        indicador = (
            session.query(Indicador)
            .filter_by(ativo_id=ativo_id, data_referencia=data_ref)
            .first()
        )

        if indicador:
            indicador.volatilidade_2a = volatilidade_2a
        else:
            indicador = Indicador(
                ativo_id=ativo_id,
                data_referencia=data_ref,
                volatilidade_2a=volatilidade_2a,
            )

            session.add(indicador)
