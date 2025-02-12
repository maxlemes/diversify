# main.py
import pandas as pd

from scrapping.empresas import *
from database.banco_de_dados import BancoDeDados

# Conectando ao banco de dados
db = BancoDeDados('database/dados_empresas.db')




# Salvando o perfil das empresas no banco de dados
for empresa in Empresa.lista:
    db.salvar_perfil(empresa)

# Listando as empresas armazenadas no banco de dados
empresas = db.listar_perfis()

# Exibindo as empresas
for empresa in empresas:
    print(empresa)


# Listar as colunas de uma tabela 
nome_tabela = 'dre'
db.cursor.execute(f"PRAGMA table_info({nome_tabela})")
colunas = [row[1] for row in db.cursor.fetchall()]
print(f"Colunas da tabela {nome_tabela}:", colunas)




# Fechando a conexão com o banco de dados
db.fechar_conexao()