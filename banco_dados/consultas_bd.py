import logging

from banco_dados.conexao_bd import ConexaoBD

# Configuração do logging para desenvolvimento
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ConsultaBD:
    def __init__(self, db_file):
        """
        Construtor da classe Consulta.

        Inicializa a classe com o arquivo do banco de dados e prepara
        para realizar consultas SELECT no banco de dados.

        Parâmetros:
            db_file (str): O caminho do arquivo do banco de dados SQLite.
        """

        self.db_file = db_file  # Caminho para o banco de dados
        self.conexao = ConexaoBD(
            self.db_file
        )  # Instancia a classe ConexaoBD para conectar ao banco

    def cotacoes(self, ticker):
        """
        Consulta os preços das ações com base no ticker fornecido.

        Parâmetro:
        - ticker: O ticker da ação para a qual as cotações serão consultadas.

        Retorna:
        - Uma lista de tuplas contendo o ticker, data e preço das ações.
        """
        try:
            # Consulta SQL para pegar os preços das ações pelo ticker
            consulta = """
            SELECT p.ticker, c.data, c.preco
            FROM perfil p
            JOIN cotacoes c ON p.id = c.perfil_id
            WHERE p.ticker = ?
            """

            # Executa a consulta
            cursor = self.banco_dados.cursor()
            cursor.execute(consulta, (ticker,))

            # Obter todos os resultados
            resultados = cursor.fetchall()

            if resultados:
                return resultados
            else:
                print(f"Nenhum dado encontrado para o ticker '{ticker}'.")
                return []

        except sqlite3.Error as e:
            print(f"Erro ao consultar os dados: {e}")
            return []

    def consultar(self, query, params=None):
        """
        Realiza uma consulta SELECT no banco de dados.

        Executa a query SQL do tipo SELECT e retorna os resultados.

        Parâmetros:
            query (str): A consulta SQL a ser executada.
            params (tuple ou list, opcional): Parâmetros a serem passados para a query.

        Retorna:
            list: Uma lista contendo as linhas retornadas pela consulta.
        """

        try:
            # Estabelece a conexão com o banco
            self.conexao.conectar()
            # Executa a query
            self.conexao.executar_query(query, params)
            # Recupera os resultados da consulta
            resultados = self.conexao.cursor.fetchall()
            logging.debug(f"Consulta realizada com sucesso: {query}")
            return resultados
        except Exception as e:
            logging.error(f"Erro ao consultar dados: {e}")
            raise  # Levanta a exceção para ser tratada no código que chamou o método
        finally:
            # Garante que a conexão será fechada após a operação
            self.conexao.desconectar()


# Exemplo de uso:
# consulta = Consulta('meu_banco.db')
# resultados = consulta.consultar('SELECT * FROM usuarios WHERE idade > 18')
# print(resultados)
