import logging
import sqlite3
import traceback

# Configuração do logging para desenvolvimento
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ConexaoBD:
    def __init__(self, db_file):
        """
        Construtor da classe ConexaoBD.

        Este método é chamado automaticamente quando uma instância
        da classe é criada. Ele inicializa a conexão com o banco de
        dados e prepara o ambiente para realizar operações no banco.

        Parâmetros:
            db_file (str): O caminho do arquivo do banco de dados SQLite.
        """
        self.db_file = db_file  # Armazena o caminho para o banco de dados
        self.conn = None  # Inicializa a conexão como None
        self.cursor = None  # Inicializa o cursor como None
        logging.debug(f"Conexão iniciada com o banco de dados: {self.db_file}")

    def conectar(self):
        """Estabelece a conexão com o banco de dados SQLite."""
        try:
            self.conn = sqlite3.connect(self.db_file)  # Conecta ao banco de dados
            self.cursor = self.conn.cursor()  # Cria um cursor para executar as queries
            logging.debug(f"Conectado ao banco de dados {self.db_file}")
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            logging.debug(traceback.format_exc())
            raise  # Levanta a exceção para ser tratada no código que chamou o método

    def desconectar(self):
        """Fecha a conexão com o banco de dados."""
        try:
            if self.conn:
                self.conn.close()  # Fecha a conexão
                logging.debug("Conexão fechada com sucesso.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao fechar a conexão: {e}")
            logging.debug(traceback.format_exc())
            raise  # Levanta a exceção caso algum erro ocorra

    def executar_query(self, query, params=None):
        """
        Executa uma query SQL no banco de dados.

        Este método executa uma query no banco de dados. Pode ser
        utilizada para qualquer tipo de operação (SELECT, INSERT, etc).

        Parâmetros:
            query (str): A consulta SQL a ser executada.
            params (tuple ou list, opcional): Parâmetros a serem passados para a query.
        """
        try:
            if params:
                self.cursor.execute(query, params)  # Executa a query com os parâmetros
            else:
                self.cursor.execute(query)  # Executa a query sem parâmetros

            logging.debug(
                f"Query {query} executada com sucesso, com parâmetros: {params}"
            )

            # Retorna o número de linhas afetadas pelas operações.
            return self.cursor.rowcount

        except sqlite3.Error as e:
            logging.error(f"Erro ao executar a query: {e}")
            logging.debug(
                traceback.format_exc()
            )  # Captura o traceback completo do erro
            raise  # Levanta a exceção para ser tratada no código que chamou o método

    def commit(self):
        """Salva as alterações feitas no banco de dados."""
        try:
            self.conn.commit()  # Salva as alterações
            logging.debug("Alterações salvas no banco de dados.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao salvar alterações no banco de dados: {e}")
            logging.debug(traceback.format_exc())
            raise  # Levanta a exceção para ser tratada no código que chamou o método
