from diversify.scrapping.scraper import extrair_dados
from diversify.scrapping.database import conectar, consultar_ativos, criar_tabela

# Criar tabelas no banco
criar_tabela()

# Capturar e salvar dados de alguns ativos
ativos = ["WEGE3", "ITSA4", "VALE3"]

for ativo in ativos:
    extrair_dados(ativo)

# Consultar ativos no banco
print(consultar_ativos())

