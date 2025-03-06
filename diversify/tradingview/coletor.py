import logging
import re
import traceback

import pandas as pd
import yfinance as yf
from etl_tradinview.raspador import Raspador
from etl_tradinview.tratador import TratadorDeDados


class Coletor:
    def __init__(self, ativo):
        """Inicializa a classe de coleta dos dados."""
        self.ativo = ativo

    def balanco(self, tipo_dados):
        """Coleta o balanço e armazena no banco de dados"""

        if tipo_dados not in FONTES:
            raise ValueError(
                f"Tipo de balanço '{tipo_dados}' inválido. Escolha entre: {list(FONTES.keys())}"
            )

        try:
            # definindo a url e o xpath do balanço
            url = FONTES[tipo_dados]["url"].format(self.ativo)
            xpath = FONTES[tipo_dados]["xpath"]

            # Criar o raspador para coletar dados
            raspador = Raspador(url, xpath)

            # Coleta a tabela de dados
            lista_dados = raspador.coletar_tabela()

            # transformando a lista num dicionario
            dados_dict = {tipo_dados: lista_dados}

            # Criar o tratador de dados para processar a tabela
            tratador = TratadorDeDados(self.ativo, dados_dict)

            # Criar o DataFrame com os dados tratados
            df = tratador.criar_dataframe()

            # Conecta ao banco de dados
            banco = GerenciadorBanco()
            operacoes = OperacoesBanco(banco)

            # Inserir dados no banco de dados
            operacoes.inserir_dataframe(tipo_dados, df)

            logging.info(
                f"Dados do balanço do ativo '{self.ativo}' inseridos com sucesso no banco de dados."
            )

        except Exception as e:
            # Captura qualquer exceção e registra o erro
            logging.error(
                f"Erro ao coletar ou inserir dados do balanço para o ativo {self.ativo}: {e}"
            )
            print(f"Erro ao processar o balanço do ativo {self.ativo}: {e}")

        finally:
            # Fechar o navegador, garantindo que isso sempre aconteça
            if "raspador" in locals():
                raspador.fechar_navegador()
                logging.info(f"Navegador fechado para o ativo {self.ativo}.")

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
            logging.error(f"Erro ao coletar a cotação do ativo {self.ativo}: {e}")
            print(f"Erro ao coletar a cotação do ativo {self.ativo}: {e}")

    def resumo(self):
        """Coleta um resumo financeiro site do TradingView."""

        try:
            dados = [self.ativo]

            try:
                cotacao = self.cotacao()
                dados.append(cotacao)

            except Exception as e:
                # Captura qualquer exceção e registra o erro
                logging.error(f"Erro ao coletar a cotação do ativo {self.ativo}: {e}")
                print(f"Erro ao coletar a cotação do ativo {self.ativo}: {e}")

            try:
                for item in ["dre", "stats", "divs", "ests", "rece"]:

                    # definindo a url e o xpath do balanço
                    url = FONTES[item]["url"].format(self.ativo)
                    xpath = FONTES[item]["xpath_r"]

                    # Criar o raspador para coletar dados
                    raspador = Raspador(url, xpath, headless=True)

                    # Coleta a cotacao do ativo
                    elemento = raspador.coletar_elemento()

                    # formatar texto unicode
                    elemento = re.sub(r"[\u202a\u202c\u202f]", "", elemento)

                    dados.append(elemento)
            except Exception as e:
                logging.info(f"Resumo do ativo '{self.ativo}' coletados com sucesso.")
                print(f"Resumo do ativo '{self.ativo}' coletados com sucesso.")

            try:
                # Conecta ao banco de dados
                banco = GerenciadorBanco()
                operacoes = OperacoesBanco(banco)

                # Inserir dados no banco de dados
                operacoes.inserir_resumo(*dados)
            except Exception as e:
                logging.info(
                    f"Resumo do ativo '{self.ativo}' inseridos com sucesso no banco de dados."
                )
                print(
                    f"Resumo do ativo '{self.ativo}' inseridos com sucesso no banco de dados."
                )

        except Exception as e:
            # Captura qualquer exceção e registra o erro
            logging.error(
                f"Erro ao coletar ou inserir o resumo do ativo {self.ativo}: {e}"
            )
            print(f"Erro ao coletar ou inserir o resumo do ativo {self.ativo}: {e}")

        finally:
            # Fechar o navegador, garantindo que isso sempre aconteça
            if "raspador" in locals():
                raspador.fechar_navegador()
                logging.info(f"Navegador fechado para o ativo {self.ativo}.")

    def precos(self):
        """Coleta o preço do ativo nos ultimos 5 anos (yahoo) e armazena no banco de dados"""

        try:
            # definindo a url e o xpath do balanço
            url = FONTES["precos"]["url"].format(self.ativo)
            xpath = FONTES["precos"]["xpath"]

            # Criar o raspador para coletar dados
            raspador = Raspador(url, xpath)

            # Coleta a tabela de dados
            lista_dados = raspador.coletar_tabela_2()

            # remove o cabeçalho
            lista_dados = lista_dados[1:]

            # seleciona apenas as linhas com 7 itens
            lista_dados = [linha for linha in lista_dados if len(linha) == 7]

            # Converte os valores para números e remove as vírgulas do último item
            for sublista in lista_dados:
                sublista.insert(0, self.ativo)
                for i in range(2, len(sublista) - 1):
                    if sublista[i]:
                        sublista[i] = float(
                            sublista[i]
                        )  # Converte os itens em números (float)

                # Remove '-' no último item
                if sublista[-1]:
                    sublista[-1] = str(sublista[-1]).replace("-", "")

                # Remove as vírgulas e converte o último item para um número inteiro
                if sublista[-1]:
                    sublista[-1] = int(
                        sublista[-1].replace(",", "")
                    )  # Remove vírgulas e converte para inteiro

            # abrindo o banco de dados
            banco = GerenciadorBanco()
            operacoes = OperacoesBanco(banco)

            # inserindo os preços no banco de dados
            operacoes.inserir_precos(lista_dados)

        except Exception as e:
            # Captura qualquer exceção e registra o erro
            logging.error(
                f"Erro ao coletar ou inserir os preços do ativo {self.ativo}: {e}"
            )
            print(f"Erro  ao coletar ou inserir os preços do ativo {self.ativo}: {e}")

        finally:
            # Fechar o navegador, garantindo que isso sempre aconteça
            if "raspador" in locals():
                raspador.fechar_navegador()
                logging.info(f"Navegador fechado para o ativo {self.ativo}.")

    def precos_yahoo(self):
        """
        Obtém preços históricos de um ativo no Yahoo Finance e insere no banco de dados.

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
            df_dados.columns = [
                "open",
                "high",
                "low",
                "close",
                "adj_close",
                "volume",
            ]

            # Convertendo índice para coluna de data
            df_dados.insert(0, "data", df_dados.index.strftime("%Y-%m-%d"))

            # inserindo a coluna com o ativo
            df_dados.insert(0, "ativo", self.ativo)

            # abrindo o banco de dados
            banco = GerenciadorBanco()
            operacoes = OperacoesBanco(banco)

            # inserindo os preços no banco de dados
            operacoes.inserir_precos(df_dados.values.tolist())

            banco.fechar_conexao()

            logging.info(f"Preços do ativo {self.ativo} inseridos com sucesso.")

            return True

        except KeyError as e:
            logging.error(
                f"Erro: Coluna ausente no Yahoo Finance para {self.ativo} - {e}"
            )
        except Exception as e:
            logging.error(
                f"Erro ao coletar ou inserir os preços do ativo {self.ativo}: {traceback.format_exc()}"
            )

        return False
