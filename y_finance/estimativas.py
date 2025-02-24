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

    def calcular_roe(self, ticker):
        """
        Calcula o ROE (Return on Equity) de um ativo específico com base no ticker.

        Parâmetros:
            ticker (str): Código do ativo.

        Retorna:
            list: Lista de tuplas contendo (perfil_id, ano, roe).
        """
        try:
            # Buscar o perfil_id correspondente ao ticker
            perfil_id = self.consulta.buscar_perfil_id(ticker)
            if perfil_id is None:
                return []

            # Agora buscar o ROE apenas para esse perfil_id
            query_roe = """
            SELECT 
                dre.perfil_id,
                dre.ano, 
                (dre.lucro_liquido / bp.patrimonio_liquido) AS roe
            FROM dre
            JOIN bp ON dre.perfil_id = bp.perfil_id AND dre.ano = bp.ano
            WHERE dre.perfil_id = ? AND bp.patrimonio_liquido IS NOT NULL;
            """

            dados = self.consulta._executar_consulta(query_roe, (perfil_id,))
            print(dados)

            # Inserir os dados
            tabela = "stats"
            colunas = ["perfil_id", "ano", "roe"]
            self.gerenciador.insert_stats(tabela, colunas, dados)

        except Exception as e:
            logging.error(f"Erro ao calcular ROE para {ticker}: {e}")
            return []
