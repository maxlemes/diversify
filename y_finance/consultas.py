import sqlite3


class Consultar:
    def __init__(self, banco_dados):
        """
        Inicializa a classe Consultar com a conexão ao banco de dados.

        Parâmetro:
        - banco_dados: conexão com o banco de dados SQLite.
        """
        self.banco_dados = banco_dados

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
