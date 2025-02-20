import logging
import traceback

import yfinance as yf

# Configuração do logging para desenvolvimento
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Coleta:
    def __init__(self, ativo):
        """Inicializa a classe de coleta dos dados."""
        self.ativo = ativo

    def cotacao(self):
        """Coleta a cotacao do ativo"""

        ativo = self.ativo + ".SA"

        try:
            # Obter dados do ativo
            dados = yf.Ticker(ativo)

            # Cotação atual
            cotacao = dados.history(period="1d", auto_adjust=False)["Adj Close"].iloc[
                -1
            ]

            return cotacao

        except Exception as e:
            # Captura qualquer exceção e registra o erro
            logging.error(f"Erro ao coletar cotação: {e}")
            logging.debug(traceback.format_exc())

    def cotacoes(self):
        """
        Obtém as cotações históricos de um ativo no Yahoo Finance
        - Busca dados do ativo adicionando ".SA" para a B3.
        - Filtra e renomeia colunas relevantes.
        - Converte datas e adiciona o código do ativo.
        - Insere os dados no banco de dados.
        - Registra erros em caso de falha.
        """

        ativo = self.ativo + ".SA"

        try:
            # Obter dados do ativo nos últimos 5 anos
            dados = yf.Ticker(ativo)
            df_dados = dados.history(period="5y", auto_adjust=False)

            # Selecionando e renomeando as colunas 'open', 'high', 'low', 'close', 'adj_close' e 'volume'
            df_dados = df_dados[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
            df_dados.columns = ["open", "high", "low", "close", "adj_close", "volume"]

            # Convertendo índice para coluna de data
            df_dados.insert(0, "data", df_dados.index.strftime("%Y-%m-%d"))

            return df_dados

        except KeyError as e:
            # Captura qualquer exceção e registra o erro
            logging.error(f"Erro ao coletar cotações: {e}")
            logging.debug(traceback.format_exc())
        return False
