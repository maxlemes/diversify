
# database.py
import sqlite3

from database.consultar_dados import consultar_dados
from database.salvar_perfil import salvar_perfil
from database.salvar_tabela import salvar_tabela # type: ignore
from database.criar_tabelas import criar_tabelas 

class BancoDeDados:
    def __init__(self, db_path):
        """Inicializa a conexão com o banco de dados."""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def listar_perfis(self):
        """Recupera todas os ativos do banco de dados."""
        self.cursor.execute('SELECT * FROM perfil')
        return self.cursor.fetchall()
    
    
    def listar_tabela(self):
        """Recupera todas as empresas do banco de dados."""
        self.cursor.execute('SELECT * FROM perfil')
        return self.cursor.fetchall()

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()

# Adicionando funções ao método da classe BancoDeDados
BancoDeDados.criar_tabelas = criar_tabelas
BancoDeDados.salvar_perfil = salvar_perfil
BancoDeDados.salvar_tabela = salvar_tabela
BancoDeDados.consultar_dados = consultar_dados