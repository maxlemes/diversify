# Ele buscará os ativos no banco e usará o yfinance para obter os preços.


import datetime as dt
import time

import pandas as pd
import yfinance as yf
from db_nexus.session import DatabaseSessionManager
from sqlalchemy.orm import Session

from diversify.database.models import Ativo
from diversify.database.repositories import AtivoRepository, PrecoHistoricoRepository


class QuoteService:
    """
    Serviço responsável por todas as operações relacionadas a cotações de ativos.
    """

    def __init__(self):
        # O construtor recebe e armazena as dependências necessárias.
        self.ativo_repo = AtivoRepository()
        self.preco_repo = PrecoHistoricoRepository()

    # Mapeamento de tickers B3 para os tickers do Yahoo Finance para os principais índices
    def _get_yahoo_finance_ticker(self, ticker: str) -> str:
        """
        Converte um ticker da B3 para o formato do Yahoo Finance,
        com tratamento especial para o IBOV.
        """
        # Adicionado .upper() para tornar a verificação insensível a maiúsculas/minúsculas
        # O ticker do IBOV no Yahoo Finance é ^BVSP
        if ticker != "IBOV":
            # Para todos os outros ativos (ações, FIIs, etc.), adiciona o sufixo .SA
            return f"{ticker}.SA"
        else:
            return "^BVSP"

    def update_historical_prices(self, db_manager: DatabaseSessionManager):
        """
        Serviço principal que orquestra todo o fluxo de atualização de cotações,
        usando transações curtas para cada ativo para máxima robustez.
        """
        print("\n--- INICIANDO ATUALIZAÇÃO DE COTAÇÕES HISTÓRICAS ---")
        ativo_repo = AtivoRepository()
        preco_repo = PrecoHistoricoRepository()

        # Etapa 1: Busca apenas os IDs dos ativos em uma sessão rápida.
        ativos_ids_para_atualizar = []
        with db_manager.get_session() as session:
            resultados = session.query(Ativo.id).all()
            ativos_ids_para_atualizar = [id_tuple[0] for id_tuple in resultados]

        print(
            f"Encontrados {len(ativos_ids_para_atualizar)} ativos para verificar/atualizar cotações."
        )

        # Etapa 2: Itera sobre a lista de IDs, com uma transação para cada ativo.
        for ativo_id in ativos_ids_para_atualizar:

            # Inicia uma nova sessão/transação para este ativo.
            with db_manager.get_session() as session:
                try:
                    ativo = ativo_repo.get_by_id(session, ativo_id)
                except Exception as e:
                    print(
                        f"Não foi possível buscar o ativo com ID {ativo_id}. Erro: {e}"
                    )
                    continue

                yf_ticker = self._get_yahoo_finance_ticker(ativo.ticker)
                print(f"\nProcessando: {ativo.ticker} ({yf_ticker})")

                latest_date_in_db = preco_repo.get_latest_date(session, ativo.id)

                historico = None
                if latest_date_in_db:
                    start_date = latest_date_in_db + dt.timedelta(days=1)
                    if start_date >= dt.date.today():
                        print("Dados já estão atualizados. Pulando.")
                        continue
                    # Busca a partir da última data
                    historico = yf.Ticker(yf_ticker).history(
                        start=start_date, end=dt.date.today(), auto_adjust=True
                    )
                else:
                    # Se não há dados, busca o período completo
                    historico = yf.Ticker(yf_ticker).history(
                        period="3y", auto_adjust=True
                    )

                if historico is not None and not historico.empty:
                    historico.dropna(subset=["Close"], inplace=True)

                    if not historico.empty:
                        dados_para_inserir = [
                            {
                                "ativo_id": ativo.id,
                                "data_pregao": data.date(),
                                "preco_fechamento": row[
                                    "Close"
                                ],  # 'Close' já é ajustado com auto_adjust=True
                            }
                            for data, row in historico.iterrows()
                        ]

                        if dados_para_inserir:
                            preco_repo.bulk_insert(session, dados_para_inserir)
                    else:
                        print("Nenhuma cotação *válida* encontrada no período.")
                else:
                    print("Nenhuma nova cotação encontrada no período.")

            # Pausa educada entre as chamadas de API para cada ativo
            time.sleep(1)
