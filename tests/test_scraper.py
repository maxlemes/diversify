from diversify.scrapping.scraper import extrair_profile, extrair_indicador
from diversify.scrapping.database import (
    conectar,
    consultar_ativos,
    criar_tabela,
    salvar_indicadores,
)

# Criar tabelas no banco
criar_tabela()

# Capturar e salvar dados de alguns ativos
ativos = ['WEGE3', 'FESA4', 'LEVE3']

# for ativo in ativos:
#     extrair_profile(ativo)

# # Consultar ativos no banco
# print(consultar_ativos("ativos"))

# for ativo in ativos:
#     eps = extrair_indicador(ativo, 'EPS')
#     salvar_indicadores(eps)
#     roe = extrair_indicador(ativo, 'ROE')
#     salvar_indicadores(roe)

# print(consultar_ativos('valores_ativos'))

    
tabela = extrair_indicador2('FESA4', 'EPS')

print(tabela)

