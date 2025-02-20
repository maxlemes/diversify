import logging
import traceback

import yfinance as yf

# Configuração do logging para desenvolvimento
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Empresa:
    def __init__(self, ativo):
        """Inicializa a classe de coleta dos dados."""
        self.ativo = ativo

    def cotacao(self):
        """Coleta a cotacao do ativo"""

        try:
            # Obter dados do ativo
            dados = yf.Ticker(self.ativo + ".SA")

            # Cotação atual
            historico = dados.history(period="1d", auto_adjust=False)

            if historico.empty:
                print("Nenhum dado retornado!")
                return False
            else:
                cotacao = historico["Adj Close"].iloc[0]
                print(f"Cotação: {cotacao}")
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

            return dados

        except Exception as e:
            logging.error(f"Erro ao coletar perfil: {e}")
            logging.debug(traceback.format_exc())
            return None  # Retorna None caso haja erro
