import logging
import traceback

import pandas as pd
import yfinance as yf

from banco_dados.conexao_bd import ConexaoBD
from banco_dados.consultas_bd import ConsultasBD
from y_finance.info import BALANCOS

# Configuração do logging para desenvolvimento
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Empresa:
    def __init__(self, ativo):
        """Inicializa a classe de coleta dos dados."""
        self.ativo = ativo
        self.bd = ConexaoBD()
        self.consulta = ConsultasBD(self.bd)

    def cotacao(self):
        """Coleta a cotacao do ativo"""

        try:
            # Obter dados do ativo
            dados = yf.Ticker(self.ativo + ".SA")

            # Cotação atual
            preco = dados.info["currentPrice"]
            if preco:
                cotacao = preco
                return cotacao
            else:
                print("Nenhum dado retornado!")
                return False

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
        try:
            # Obter dados do ativo nos últimos 5 anos
            dados = yf.Ticker(self.ativo + ".SA")
            df_dados = dados.history(period="5y", auto_adjust=False)

            # Selecionando e renomeando as colunas 'open', 'high', 'low', 'close', 'adj_close' e 'volume'
            df_dados = df_dados[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
            df_dados.columns = ["open", "high", "low", "close", "adj_close", "volume"]

            # Remove o fuso horário e converte o índice para coluna de data
            df_dados.index = df_dados.index.tz_localize(None)
            df_dados.insert(0, "data", df_dados.index.strftime("%Y-%m-%d"))
            dict_dados = df_dados.to_dict(orient="records")
            dict_dados.insert(0, {"ticker": self.ativo})

            return dict_dados

        except KeyError as e:
            # Captura qualquer exceção e registra o erro
            logging.error(f"Erro ao coletar cotações: {e}")
            logging.debug(traceback.format_exc())
        return False

    def perfil(self):
        """
        Obtém informações básicas sobre a empresa a partir do Yahoo Finance.

        Retorna um dicionário contendo:
        - 'nome' (str): Nome completo da empresa.
        - 'ticker' (str): Código do ativo informado pelo usuário.
        - 'setor' (str): Setor econômico em que a empresa atua.
        - 'subsetor' (str): Subsetor específico dentro do setor econômico.
        - 'website' (str): Endereço do site oficial da empresa.
        - 'descricao' (str): Breve descrição das atividades da empresa.

        Caso ocorra um erro ao obter as informações, retorna None e registra o erro no log.

        Exemplo de uso:
            empresa = Empresa("PETR4")
            dados = empresa.perfil()
            print(dados)
        """
        try:
            ticker = yf.Ticker(self.ativo + ".SA")
            info = ticker.info

            # Verifica se as chaves existem antes de acessá-las
            dados = {
                "nome": info.get("longName", "N/A"),
                "ticker": self.ativo,
                "setor": info.get("sector", "N/A"),
                "subsetor": info.get("industry", "N/A"),
                "website": info.get("website", "N/A"),
                "descricao": info.get("longBusinessSummary", "N/A"),
            }

            return [dados]

        except Exception as e:
            logging.error(f"Erro ao coletar perfil: {e}")
            logging.debug(traceback.format_exc())
            return None  # Retorna None caso haja erro

    def balanco(self, tipo, periodo=None):
        """
        Obtém informações básicas sobre a empresa a partir do Yahoo Finance.

        Retorna um dicionário contendo o balanco desejado

        Caso ocorra um erro ao obter as informações, retorna None e registra o erro no log.

        Exemplo de uso:
            empresa = Empresa("PETR4")
            dados = empresa.balanco('dre')
            print(dados)
        """
        try:
            # definindo o dicionário dre
            balanco = BALANCOS[tipo]
            # conectando com o yfinance
            stock = yf.Ticker(self.ativo + ".SA")

            # selecionando o tipo do balanco
            if tipo == "dre":
                df_dados = (
                    stock.income_stmt if not periodo else stock.quarterly_income_stmt
                )
            elif tipo == "bp":
                df_dados = (
                    stock.balance_sheet
                    if not periodo
                    else stock.quarterly_balance_sheet
                )
            elif tipo == "fc":
                df_dados = stock.cashflow if not periodo else stock.quarterly_cashflow

            # filtrando os dados de interesse
            df_dados = df_dados[df_dados.index.isin(balanco.keys())]
            # Converte os nomes das colunas para datas e extrai apenas o ano
            if not periodo:
                df_dados.columns = pd.to_datetime(df_dados.columns).year
            # Renomeando o índice
            df_dados = df_dados.rename(index=balanco)
            # transformando em um dicionário
            dict_dados = [
                {"ano": ano, **df_dados[ano].to_dict()} for ano in df_dados.columns
            ]

            # inserindo o ticker
            dict_dados.insert(0, {"ticker": self.ativo})

            return dict_dados

        except Exception as e:
            logging.error(f"Erro ao coletar perfil: {e}")
            logging.debug(traceback.format_exc())
            return None  # Retorna None caso haja erro

    def divs(self):
        """
        Obtém informações sobre os dividendos pagos a partir do Yahoo Finance.

        Retorna um dicionário contendo os dividendos anuais pagos

        Caso ocorra um erro ao obter as informações, retorna None e registra o erro no log.

        Exemplo de uso:
            empresa = Empresa("PETR4")
            dados = empresa.divs()
            print(dados)
        """
        try:
            # definindo o dicionário dre
            # balanco = BALANCOS['fc']
            # conectando com o yfinance
            stock = yf.Ticker(self.ativo + ".SA")
            # baixando o bp
            serie_dados = stock.dividends
            serie_dados = serie_dados.groupby(serie_dados.index.year).sum()
            # Transformando a série em lista de tuplas
            dados = [(index, value) for index, value in serie_dados.items()]

            print(dados)

            # Criando a lista de dicionários
            dict_dados = [
                {"ano": ano, "dividendos": valor} for ano, valor in serie_dados.items()
            ]
            # inserindo o ticker
            dict_dados.insert(0, {"ticker": self.ativo})

            return dados

        except Exception as e:
            logging.error(f"Erro ao coletar perfil: {e}")
            logging.debug(traceback.format_exc())
            return None  # Retorna None caso haja erro

    def ttm(self, tipo):
        """
        Baixa os balancos trimestrais e calcula o ttm

        Retorna um dicionário contendo o ttm do balanco desejado

        Caso ocorra um erro ao obter as informações, retorna None e registra o erro no log.

        Exemplo de uso:
            empresa = Empresa("PETR4")
            dados = empresa.ttm('dre')
            print(dados)
        """
        try:
            # conectando com o yfinance
            stock = yf.Ticker(self.ativo + ".SA")

            # baixa o balanco trimestral
            dict_dados = self.balanco(tipo, "trimestral")
            # remove o primeiro dicionarios
            dict_dados = dict_dados[1:]
            # converte para DataFrame
            df_dados = pd.DataFrame(dict_dados).T
            # calcula a soma
            df_dados["ttm"] = df_dados.iloc[1:, :4].sum(axis=1)
            df_dados[df_dados.index == "ano"] = "ttm"
            # eliminando a 1a linha e ficando só com a coluna da soma
            df_dados = df_dados.iloc[:, -1]
            # corrigindo o eps
            if "eps" in df_dados.index:
                df_dados["eps"] = stock.earnings_history["epsActual"].sum()

            # Criando a lista de dicionários
            dict_dados = [df_dados.to_dict()]
            # inserindo o ticker
            dict_dados.insert(0, {"ticker": self.ativo})

            return dict_dados

        except Exception as e:
            logging.error(f"Erro ao coletar perfil: {e}")
            logging.debug(traceback.format_exc())
            return None  # Retorna None caso haja erro
