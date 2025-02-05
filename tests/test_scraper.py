import pandas as pd
import re

from diversify.scrapping.scraper import extrair_profile, extrair_indicador2, criar_dataframe
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

    
tabela = extrair_indicador2('WEGE3', 'EPS')

# print(tabela)

# tabela = [['', '', 'Moeda: BRL', '2004\nDez 2004\n2005\nDez 2005\n2006\nDez 2006\n2007\nDez 2007\n2008\nDez 2008\n2009\nDez 2009\n2010\nDez 2010\n2011\nDez 2011\n2012\nDez 2012\n2013\nDez 2013\n2014\nDez 2014\n2015\nDez 2015\n2016\nDez 2016\n2017\nDez 2017\n2018\nDez 2018\n2019\nDez 2019\n2020\nDez 2020\n2021\nDez 2021\n2022\nDez 2022\n2023\nDez 2023\nTTM', ''], ['', '', 'Receita Total', '', '\u202a\u202a1,28\u202fB\u202c\u202c\n−7,35%\n\u202a\u202a1,62\u202fB\u202c\u202c\n+26,76%\n\u202a\u202a2,39\u202fB\u202c\u202c\n+47,31%\n\u202a\u202a3,14\u202fB\u202c\u202c\n+31,37%\n\u202a\u202a2,44\u202fB\u202c\u202c\n−22,42%\n\u202a\u202a2,17\u202fB\u202c\u202c', ''], ['', '', 'Custo das mercadorias vendidas', '', '\u202a\u202a−1,06\u202fB\u202c\u202c\n\u202a\u202a−1,22\u202fB\u202c\u202c\n\u202a\u202a−1,39\u202fB\u202c\u202c\n\u202a\u202a−1,72\u202fB\u202c\u202c\n\u202a\u202a−1,90\u202fB\u202c\u202c\n\u202a\u202a−1,75\u202fB\u202c\u202c', ''], ['', '', 'Lucro Bruto', '', '\u202a\u202a216,50\u202fM\u202c\u202c\n−52,98%\n\u202a\u202a397,69\u202fM\u202c\u202c\n+83,69%\n\u202a\u202a997,93\u202fM\u202c\u202c\n+150,93%\n\u202a\u202a1,41\u202fB\u202c\u202c\n+41,79%\n\u202a\u202a533,93\u202fM\u202c\u202c\n−62,26%\n\u202a\u202a424,63\u202fM\u202c\u202c', ''], ['', '', 'Despesas operacionais (excl. CPV)', '', '\u202a\u202a−72,95\u202fM\u202c\u202c\n\u202a\u202a−160,07\u202fM\u202c\u202c\n\u202a\u202a−214,37\u202fM\u202c\u202c\n\u202a\u202a−283,51\u202fM\u202c\u202c\n\u202a\u202a−299,97\u202fM\u202c\u202c\n\u202a\u202a−233,37\u202fM\u202c\u202c', ''], ['', '', 'Resultado Operacional', '', '\u202a\u202a143,55\u202fM\u202c\u202c\n−48,61%\n\u202a\u202a237,61\u202fM\u202c\u202c\n+65,53%\n\u202a\u202a783,57\u202fM\u202c\u202c\n+229,77%\n\u202a\u202a1,13\u202fB\u202c\u202c\n+44,39%\n\u202a\u202a233,96\u202fM\u202c\u202c\n−79,32%\n\u202a\u202a131,99\u202fM\u202c\u202c', ''], ['', '', 'Receita não operacional, total', '', '\u202a\u202a111,83\u202fM\u202c\u202c\n\u202a\u202a−165,75\u202fM\u202c\u202c\n\u202a\u202a−81,91\u202fM\u202c\u202c\n\u202a\u202a112,95\u202fM\u202c\u202c\n\u202a\u202a185,68\u202fM\u202c\u202c\n\u202a\u202a100,93\u202fM\u202c\u202c', ''], ['', '', 'Receita antes de impostos', '', '\u202a\u202a255,38\u202fM\u202c\u202c\n−27,01%\n\u202a\u202a71,86\u202fM\u202c\u202c\n−71,86%\n\u202a\u202a701,66\u202fM\u202c\u202c\n+876,36%\n\u202a\u202a1,24\u202fB\u202c\u202c\n+77,35%\n\u202a\u202a419,64\u202fM\u202c\u202c\n−66,28%\n\u202a\u202a265,08\u202fM\u202c\u202c', ''], ['', '', 'Equity em resultados', '', '\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n—', ''], ['', '', 'Impostos', '', '\u202a\u202a−33,85\u202fM\u202c\u202c\n\u202a\u202a−1,85\u202fM\u202c\u202c\n\u202a\u202a−58,75\u202fM\u202c\u202c\n\u202a\u202a−181,89\u202fM\u202c\u202c\n\u202a\u202a−36,75\u202fM\u202c\u202c\n\u202a\u202a−8,57\u202fM\u202c\u202c', ''], ['', '', 'Participação de não-controladores/minoritários', '', '\u202a\u202a−357,00\u202fK\u202c\u202c\n\u202a\u202a−242,00\u202fK\u202c\u202c\n\u202a\u202a−29,00\u202fK\u202c\u202c\n\u202a\u202a−198,00\u202fK\u202c\u202c\n\u202a\u202a−236,00\u202fK\u202c\u202c\n—', ''], ['', '', 'Depois de impostos outras receitas/despesas', '', '\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n—', ''], ['', '', 'Lucro líquido antes das operações descontinuadas', '', '\u202a\u202a221,18\u202fM\u202c\u202c\n\u202a\u202a69,77\u202fM\u202c\u202c\n\u202a\u202a642,88\u202fM\u202c\u202c\n\u202a\u202a1,06\u202fB\u202c\u202c\n\u202a\u202a382,65\u202fM\u202c\u202c\n\u202a\u202a256,33\u202fM\u202c\u202c', ''], ['', '', 'Operações descontinuadas', '', '\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n—', ''], ['', '', 'Lucro Líquido', '', '\u202a\u202a221,18\u202fM\u202c\u202c\n−28,38%\n\u202a\u202a69,77\u202fM\u202c\u202c\n−68,45%\n\u202a\u202a642,88\u202fM\u202c\u202c\n+821,40%\n\u202a\u202a1,06\u202fB\u202c\u202c\n+65,24%\n\u202a\u202a382,65\u202fM\u202c\u202c\n−63,98%\n\u202a\u202a256,33\u202fM\u202c\u202c', ''], ['', '', 'Ajuste de diluição', '', '\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n—', ''], ['', '', 'Dividendos preferenciais', '', '\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n\u202a0,00\u202c\n—', ''], ['', '', 'Lucro líquido diluído disponível para acionistas ordinários', '', '\u202a\u202a221,18\u202fM\u202c\u202c\n\u202a\u202a69,77\u202fM\u202c\u202c\n\u202a\u202a642,88\u202fM\u202c\u202c\n\u202a\u202a1,06\u202fB\u202c\u202c\n\u202a\u202a382,65\u202fM\u202c\u202c\n—', ''], ['', '', 'Lucro básico por ação (EPS Básico)', '', '\u202a0,65\u202c\n−28,38%\n\u202a0,20\u202c\n−68,45%\n\u202a1,89\u202c\n+821,40%\n\u202a3,12\u202c\n+65,24%\n\u202a1,12\u202c\n−63,98%\n\u202a0,74\u202c', ''], ['', '', 'Lucro diluído por ação (EPS Diluído)', '', '\u202a0,65\u202c\n−28,37%\n\u202a0,20\u202c\n−68,45%\n\u202a1,89\u202c\n+821,32%\n\u202a3,12\u202c\n+65,24%\n\u202a1,12\u202c\n−63,98%\n—', ''], ['', '', 'Média de ações ordinárias em circulação', '', '\u202a\u202a340,39\u202fM\u202c\u202c\n\u202a\u202a340,39\u202fM\u202c\u202c\n\u202a\u202a340,39\u202fM\u202c\u202c\n\u202a\u202a340,39\u202fM\u202c\u202c\n\u202a\u202a340,39\u202fM\u202c\u202c\n—', ''], ['', '', 'Ações diluídas em circulação', '', '\u202a\u202a340,39\u202fM\u202c\u202c\n\u202a\u202a340,39\u202fM\u202c\u202c\n\u202a\u202a340,39\u202fM\u202c\u202c\n\u202a\u202a340,39\u202fM\u202c\u202c\n\u202a\u202a340,39\u202fM\u202c\u202c\n—', ''], ['', '', 'EBITDA', '', '\u202a\u202a329,62\u202fM\u202c\u202c\n−22,72%\n\u202a\u202a415,40\u202fM\u202c\u202c\n+26,03%\n\u202a\u202a940,70\u202fM\u202c\u202c\n+126,45%\n\u202a\u202a1,30\u202fB\u202c\u202c\n+38,68%\n\u202a\u202a449,98\u202fM\u202c\u202c\n−65,51%\n\u202a\u202a379,55\u202fM\u202c\u202c', ''], ['', '', 'EBIT', '', '\u202a\u202a143,55\u202fM\u202c\u202c\n−48,61%\n\u202a\u202a237,61\u202fM\u202c\u202c\n+65,53%\n\u202a\u202a783,57\u202fM\u202c\u202c\n+229,77%\n\u202a\u202a1,13\u202fB\u202c\u202c\n+44,39%\n\u202a\u202a233,96\u202fM\u202c\u202c\n−79,32%\n\u202a\u202a131,99\u202fM\u202c\u202c', ''], ['', '', 'Total de custos operacionais', '', '\u202a\u202a−1,14\u202fB\u202c\u202c\n\u202a\u202a−1,38\u202fB\u202c\u202c\n\u202a\u202a−1,61\u202fB\u202c\u202c\n\u202a\u202a−2,01\u202fB\u202c\u202c\n\u202a\u202a−2,20\u202fB\u202c\u202c\n\u202a\u202a−2,04\u202fB\u202c\u202c', '']]

df = criar_dataframe(tabela)

# Salvar como CSV
nome_csv = 'income_wege.csv'
df.to_csv(nome_csv, index=False)
print(f"DataFrame salvo em {nome_csv}")

print(df)

