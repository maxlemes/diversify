import sqlite3

from scrapping.coletor import Coletor
from scrapping.tratador_de_dados import TratadorDeDados
from database.banco_de_dados import BancoDeDados


# Criar uma instância do Coletor
coletor = Coletor()

# Escolha o ativo e o balanço desejado
ativo = "VALE3"  # Código da empresa na B3
tipo_balanco = "dre"  # Pode ser: "DRE", "Balanço Patrimonial" ou "Fluxo de Caixa"

# Coletar os dados
dados = coletor.extrair_balanco(ativo, tipo_balanco)

# Se os dados foram coletados com sucesso
if dados:
    # Criar o tratador de dados
    tratador = TratadorDeDados(dados)
    
    # Criar o DataFrame com os dados tratados
    df_tratado = tratador.criar_dataframe()
    
    # Exibir os dados tratados
    if df_tratado is not None:
        print(df_tratado)
        print(df_tratado.columns)
    else:
        print("Erro ao tratar os dados.")
 
# Fechar o coletor (importante para evitar processos abertos)
coletor.fechar()

df_tratado.to_csv('data/database_teste.csv', index=False)

# Criar uma instancia do BancoDeDados
db = BancoDeDados('database/dados_empresas.db')


# Salvar a tabela no Banco de Dados
db.salvar_tabela(ativo, tipo_balanco, df_tratado)


db.fechar_conexao()