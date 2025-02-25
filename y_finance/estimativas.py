import logging
import sqlite3

from database.consultas_bd import ConsultasBD
from database.gerenciamento_bd import GerenciadorBD

# from banco_dados.conexao_bd import ConexaoBD

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Estimar:
    def __init__(self, banco_dados):
        """
        Inicializa a classe Estimar com a conexão ao banco de dados.

        Parâmetro:
        - banco_dados: conexão com o banco de dados SQLite.
        """
        self.bd = banco_dados
        self.consulta = ConsultasBD(self.bd)
        self.gerenciador = GerenciadorBD(self.bd)

    def fetch_roe(self, profile_id):
        """
        Calcula o ROE (Return on Equity) de um ativo específico com base no ticker.

        Parâmetros:
            ticker (str): Código do ativo.

        Retorna:
            list: Lista de tuplas contendo (perfil_id, ano, roe).
        """
        try:
            # Agora buscar o ROE apenas para esse perfil_id
            query_roe = """
            SELECT 
                income_stmt.profile_id,
                income_stmt.year, 
                (income_stmt.net_income / balance_sheet.stockholders_equity) AS roe
            FROM income_stmt
            JOIN balance_sheet ON income_stms.profile_id = balance_sheet.profile_id AND income_stmt.year = balance_sheet.year
            WHERE income.profile_id = ? AND balance_sheet.stockholders_equity IS NOT NULL;
            """

            return self.consulta._executar_consulta(query_roe, (profile_id,))

        except Exception as e:
            logging.error(f"Erro ao calcular ROE para {ticker}: {e}")
            return []
