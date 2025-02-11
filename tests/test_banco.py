import sqlite3
import pandas as pd

from database.banco_de_dados import BancoDeDados


# Escolha o ativo e o balanço desejado
ativo = "VALE3"  # Código da empresa na B3
tipo_balanco = "dre"  # Pode ser: "DRE", "Balanço Patrimonial" ou "Fluxo de Caixa"

df = pd.read_csv('data/database_teste.csv')

# Criar uma instancia do BancoDeDados
db = BancoDeDados('data/dados_empresas.db')


# Salvar a tabela no Banco de Dados
db.salvar_tabela(ativo, tipo_balanco, df)

# Conectar ao banco de dados
conexao = sqlite3.connect("data/dados_empresas.db")
cursor = conexao.cursor()

resultados = db.consultar_dados(ativo="VALE3", entrada='EPS')
for linha in resultados:
    print(linha)
    

db.cursor.execute(f"PRAGMA table_info('{tipo_balanco}')")
print( {row[1] for row in db.cursor.fetchall()})

db.fechar_conexao()