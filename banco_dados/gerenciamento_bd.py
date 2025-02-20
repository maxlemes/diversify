import logging
import sqlite3
import traceback

from banco_dados.conexao_bd import ConexaoBD

# Configuração do logging para desenvolvimento
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GerenciadorBD:
    def __init__(self, banco_dados):
        """
        Construtor da classe GerenciadorBD.

        Este método é chamado quando uma instância da classe é criada.
        Ele inicializa a conexão com o banco de dados através da
        instância da classe ConexaoBD que é passada como parâmetro.

        Parâmetros:
            banco_dados (ConexaoBD): Uma instância da classe ConexaoBD para realizar as operações no banco de dados.
        """
        self.banco_dados = banco_dados

    def criar_tabela(self, nome_tabela, colunas):
        """
        Cria uma tabela dinâmica no banco de dados com base no nome e colunas fornecidos.

        Parâmetros:
            nome_tabela (str): O nome da tabela a ser criada.
            colunas (dict): Um dicionário onde as chaves são os nomes das colunas
                            e os valores são os tipos de dados das colunas (exemplo: 'INTEGER', 'TEXT').

        Exemplo de uso:
            nome_tabela = 'usuarios'
            colunas = {'id': 'INTEGER PRIMARY KEY', 'nome': 'TEXT', 'idade': 'INTEGER'}
        """
        try:
            # Monta a string de criação de tabela a partir das colunas fornecidas
            colunas_sql = ", ".join(
                [f"{coluna} {tipo}" for coluna, tipo in colunas.items()]
            )
            query = f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({colunas_sql});"

            # Executa a query para criar a tabela
            self.banco_dados.executar_query(query)
            logging.debug(f"Tabela {nome_tabela} criada com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao criar tabela {nome_tabela}: {e}")
            logging.debug(traceback.format_exc())  # Captura o traceback do erro

    def inserir_dados(self, tabela, dados):
        """
        Insere os dados de um dicionário em uma tabela do banco de dados SQLite.

        Parâmetros:
        - tabela: Nome da tabela onde os dados serão inseridos.
        - dados: Dicionário contendo os dados a serem inseridos.
        - banco: Nome do banco de dados SQLite (padrão: 'dados_empresas.db').
        """
        try:
            # Criar a consulta de inserção com placeholders
            colunas = ", ".join(dados[0].keys())  # Nomes das colunas
            valores = ", ".join(
                [f":{key}" for key in dados[0].keys()]
            )  # Placeholders correspondentes

            consulta = f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})"

            # Inserir os dados de uma vez (executemany)
            self.banco_dados.cursor.executemany(consulta, dados)

            # Commit para salvar as mudanças
            self.banco_dados.commit()
            print("Dados inseridos com sucesso!")

        except sqlite3.Error as e:
            print(f"Erro ao inserir dados: {e}")

    def tabelas_iniciais(self):
        """Cria as tabelas iniciais do banco de dados."""

        # Definindo a tabela 'perfil'
        nome_tabela = "perfil"
        colunas = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "nome": "TEXT",
            "ticker": "TEXT",
            "setor": "TEXT",
            "subsetor": "TEXT",
            "website": "TEXT",
            "descricao": "TEXT",
        }
        self.criar_tabela(nome_tabela, colunas)

        # Definindo a tabela 'cotacoes'
        nome_tabela = "cotacoes"
        colunas = {
            "perfil_id": "INTEGER",
            "data": "TEXT NOT NULL",
            "open": "REAL",
            "high": "REAL",
            "low": "REAL",
            "close": "REAL",
            "adj_close": "REAL",
            "volume": "INTEGER",
            "PRIMARY KEY": "(perfil_id, data)",
            "FOREIGN KEY": "(perfil_id) REFERENCES perfil(id) ON DELETE CASCADE",
        }
        self.criar_tabela(nome_tabela, colunas)


# Exemplo de uso roda se o arquivo for executado diretamente (python gerenciador.py).
if __name__ == "__main__":
    banco_dados = ConexaoBD("banco_dados/banco_de_dados.db")
    banco_dados.conectar()
    gerenciador = GerenciadorBD(
        banco_dados
    )  # Cria uma instância da classe e conecta ao banco
    gerenciador.tabelas_iniciais()  # Chama o método criar_tabelas() que cria as tabelas
    banco_dados.desconectar()  # Fecha a conexão corretamente
