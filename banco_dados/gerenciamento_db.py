import logging
import traceback

# Configuração do logging para desenvolvimento
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GerenciadorBD:
    def __init__(self, conexao):
        """
        Construtor da classe GerenciadorBD.

        Este método é chamado quando uma instância da classe é criada.
        Ele inicializa a conexão com o banco de dados através da
        instância da classe ConexaoBD que é passada como parâmetro.

        Parâmetros:
            conexao (ConexaoBD): Uma instância da classe ConexaoBD para realizar as operações no banco de dados.
        """
        self.conexao = conexao

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
            self.conexao.executar_query(query)
            logging.debug(f"Tabela {nome_tabela} criada com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao criar tabela {nome_tabela}: {e}")
            logging.debug(traceback.format_exc())  # Captura o traceback do erro

    def tabelas_iniciais(self):
        """Cria as tabelas iniciais do banco de dados."""

        # Definindo a tabela 'perfil'
        nome_tabela = "perfil"
        colunas = {
            "nome": "TEXT",
            "ticker": "TEXT PRIMARY KEY",
            "setor": "TEXT",
            "subsetor": "TEXT",
            "descricao": "TEXT",
        }
        self.criar_tabela_dinamica(nome_tabela, colunas)

        # Exemplo de outra tabela
        nome_tabela = "produtos"
        colunas = {"id": "INTEGER PRIMARY KEY", "nome": "TEXT", "preco": "REAL"}
        self.criar_tabela_dinamica(nome_tabela, colunas)
