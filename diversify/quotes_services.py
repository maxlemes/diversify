# Ele buscará os ativos no banco e usará o yfinance para obter os preços.


import datetime as dt
import time

import numpy as np
import pandas as pd
import yfinance as yf
from db_nexus.session import DatabaseSessionManager
from sqlalchemy.orm import Session

from diversify.database.models import Ativo, PrecoHistorico
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
        # ativo_repo = AtivoRepository()
        # preco_repo = PrecoHistoricoRepository()

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
                    ativo = self.ativo_repo.get_by_id(session, ativo_id)
                except Exception as e:
                    print(
                        f"Não foi possível buscar o ativo com ID {ativo_id}. Erro: {e}"
                    )
                    continue

                yf_ticker = self._get_yahoo_finance_ticker(ativo.ticker)
                print(f"\nProcessando: {ativo.ticker} ({yf_ticker})")

                latest_date_in_db = self.preco_repo.get_latest_date(session, ativo.id)

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
                            self.preco_repo.bulk_insert(session, dados_para_inserir)
                    else:
                        print("Nenhuma cotação *válida* encontrada no período.")
                else:
                    print("Nenhuma nova cotação encontrada no período.")

            # Pausa educada entre as chamadas de API para cada ativo
            time.sleep(1)

    # ==========================================================
    # 2️⃣ ETAPA: Cálculo e armazenamento dos retornos logarítmicos
    # ==========================================================
    def calcular_retorno_log(self, db_manager: DatabaseSessionManager):
        """
        Calcula o retorno logarítmico para todos os ativos no banco de dados
        usando apenas a tabela de preços históricos. É mais eficiente.
        """
        with db_manager.get_session() as session:
            print("\n--- INICIANDO CÁLCULO DE RETORNOS LOGARÍTMICOS ---")

            # 1. Busca todos os dados históricos necessários de uma só vez.
            historico_completo = self.preco_repo.list_all(session, limit=1000000)

            if not historico_completo:
                print("⚠️ Nenhum dado histórico encontrado para calcular retornos.")
                return

            print(f"Processando {len(historico_completo)} registros históricos...")

            # 2. Converte os dados para um DataFrame do Pandas.
            df = pd.DataFrame([h.__dict__ for h in historico_completo])

            # 3. Calcula o retorno logarítmico agrupando por 'ativo_id'.
            #    Esta é a otimização principal:
            print("Calculando retornos com base no 'ativo_id'...")
            df["retorno"] = df.groupby("ativo_id")["preco_fechamento"].transform(
                lambda x: np.log(x / x.shift(1))
            )

            # 4. Prepara os dados para a atualização em massa.
            #    Filtra apenas as linhas que têm um retorno e pega as colunas 'id' e 'retorno_log'.
            dados_para_atualizar = df.dropna(subset=["retorno"])[
                ["ativo_id", "data_pregao", "retorno"]
            ].to_dict("records")

            if not dados_para_atualizar:
                print(
                    "Nenhum retorno pôde ser calculado (talvez só haja 1 dia de dados por ativo)."
                )
                return

            # 5. Executa a atualização em massa (bulk update).
            print(
                f"Atualizando {len(dados_para_atualizar)} registros no banco de dados..."
            )
            session.bulk_update_mappings(PrecoHistorico, dados_para_atualizar)

            print("✅ Retornos logarítmicos salvos com sucesso!")
