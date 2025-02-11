
# database.py
import sqlite3

class BancoDeDados:
    def __init__(self, db_path):
        """Inicializa a conexão com o banco de dados."""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def criar_tabela(self, nome_tabela):
        """Cria a tabela 'nome_tabela' no banco de dados."""
        query = f'''
            CREATE TABLE IF NOT EXISTS {nome_tabela} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                ticker TEXT NOT NULL,
                setor TEXT,
                subsetor TEXT,
                descricao TEXT,
                pais TEXT
            )
        '''
        self.cursor.execute(query)
        self.conn.commit()
       

    def salvar_empresa(self, empresa):
        """Salva uma instância da empresa no banco de dados."""
        self.cursor.execute('''
        INSERT INTO empresas (nome, ticker, setor, subsetor, descricao, pais)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (empresa.nome, empresa.ticker, empresa.setor, empresa.subsetor, empresa.descricao, empresa.pais))
        self.conn.commit()

    def listar_empresas(self):
        """Recupera todas as empresas do banco de dados."""
        self.cursor.execute('SELECT * FROM empresas')
        return self.cursor.fetchall()

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()
