import pandas as pd
import yfinance as yf

from banco_dados.gerenciador import GerenciadorBanco
from banco_dados.operacoes import OperacoesBanco
from diversify.github_api import GitHubAPI
from scrapping.coletor import Coletor
from scrapping.dados_teste import DADOS_TESTE
from scrapping.raspador import Raspador
from scrapping.tratador import TratadorDeDados

github = GitHubAPI()

dados = github.obter_repositorio("maxlemes", "diversify")
print(dados)
print(github.verificar_limite())

if __name__ == "__main__":
    banco = GerenciadorBanco()
    operacoes = OperacoesBanco(banco)

    ativo = "LEVE3"
    tipo_dados = "stats"

    # dados = {tipo_dados:DADOS_TESTE[tipo_dados]}

    # if dados:
    #     # Criar o tratador de dados
    #     tratador = TratadorDeDados(ativo, dados)

    #     # Criar o DataFrame com os dados tratados
    #     df = tratador.criar_dataframe()
    #     # print(df.columns)

    # Criar o raspador para coletar dados
    # raspador = Raspador(ativo, tipo_dados, headless=True)

    # # # Coleta a tabela de dados
    # tabela = raspador.coletar_tabela()
    # print(tabela)

    # Criar o tratador de dados para processar a tabela
    # tratador = TratadorDeDados(ativo, tabela)

    # # Criar o DataFrame com os dados tratados
    # df = tratador.criar_dataframe()
    # print(df.columns)

    # operacoes.inserir_dataframe(tipo_dados, df)

    coletor = Coletor(ativo)
    # coletor.balanco(tipo_dados)

    # cotacao = coletor.cotacao()
    # print(cotacao)

    # coletor.coletar_resumo()
    # print(resumo)

    # coletor.precos()

    # tipo_dados = 'stats'
    # dados_financeiros = operacoes.consultar_financas(tipo_dados,  ativo)
    # colunas = operacoes.listar_colunas(tipo_dados)

    # dt = pd.DataFrame(dados_financeiros, columns=colunas).sort_values(by='id')
    # print(dt)

    # Conecta ao banco de dados
    # banco = GerenciadorBanco()
    # operacoes = OperacoesBanco(banco)

    # dados = DADOS_TESTE['resumo']

    # dados = [ativo] + dados

    # print(len(dados))

    # # Inserir dados no banco de dados
    # operacoes.inserir_resumo(*dados)

    # dados_financeiros = operacoes.consultar_resumo(ativo)
    # colunas = operacoes.listar_colunas('resumo')
    # print(dados_financeiros)

    # dt = pd.DataFrame([dados_financeiros])
    # print(dt)
    # print(dt.loc[dt['ativo']=='VALE3','estimativas'].values[0])

    # dados = DADOS_TESTE['precos']
    # # df = pd.DataFrame(dados[1:], columns=dados[0])
    # # df.insert(0, 'ativo', ativo)
    # # print(df)

    #     # Função para limpar e converter os dados
    # def limpar_dados(linha):
    #     # Remover vírgulas do volume e converter para inteiro
    #     if isinstance(linha[-1], str):  # Verifica se o valor do volume é uma string
    #         linha[-1] = int(linha[-1].replace(',', ''))  # Volume
    #     # Converter os valores de preço para float
    #     for i in range(2, 7):  # Os preços estão nas posições 2 a 6
    #         if isinstance(linha[i], str):  # Verifica se os preços são strings
    #             linha[i] = float(linha[i])
    #     return linha

    # dados = dados[1:]
    # dados = [linha for linha in dados if len(linha) > 3]

    #  # Limpando os dados
    # # dados = [limpar_dados(linha) for linha in dados]

    # # Adicionando o dado como a primeira entrada de cada lista interna
    # for linha in dados:
    #     linha.insert(0, ativo)
    #     linha[-1] = int(linha[-1].replace(',', ''))  # Volume
    # # print(dados)

    # banco = GerenciadorBanco()
    # operacoes = OperacoesBanco(banco)

    # operacoes.inserir_precos(dados)

    # Inserir dados no banco de dados
    # for _, linha in df.iterrows():
    #     operacoes.inserir_precos(
    #         ativo,
    #         data = linha[0],
    #         open = linha[1],
    #         high = linha[2],
    #         low = linha[3],
    #         close = linha[4],
    #         adj_close = linha[5],
    #         volume = linha[6]
    #     )

    # dados = operacoes.consultar_precos(ativo)

    # df = pd.DataFrame(dados)

    # # Supondo que 'df' seja o seu DataFrame
    # df['data'] = pd.to_datetime(df['data'], format='%b %d, %Y')  # Converte a coluna 'data' para datetime

    # # Ordena o DataFrame pela coluna 'data' da mais recente para a mais antiga
    # df_sorted = df.sort_values(by='data', ascending=False)

    # # Exibe o DataFrame ordenado
    # print(df_sorted)

# Definir o ativo (exemplo: PETR4.SA para Petrobras na B3)

# # Obter dados do ativo
# dados = yf.Ticker(ativo)

# # Cotação atual
# cotacao_atual = dados.history(period="1d")["Close"].iloc[-1]
# print(f"Cotação atual de {ativo}: R$ {cotacao_atual:.2f}")

# # Histórico dos últimos 5 dias
# historico = dados.history(period="5y")
# print(historico[["Open", "High", "Low", "Close", "Volume"]])


# # Histórico de dividendos
# dividendos = dados.dividends
# print(dividendos.tail(10))  # Últ

# balanco = dados.balance_sheet
# print(balanco)

# resultado = dados.financials
# print(resultado)

# fluxo_caixa = dados.cashflow
# print(fluxo_caixa)

# cotacao = coletor.cotacao()
# print(cotacao)

# info = dados.info
# print(f"Nome: {info['longName']}")
# print(f"Setor: {info['sector']}")
# print(f"Capitalização de Mercado: {info['marketCap']}")
# print(f"Margem de Lucro: {info['profitMargins']}")
# print(f"Capitalização de Mercado: {info['marketCap']}")
# print(f"P/L (Price/Earnings): {info['trailingPE']}")
# print(f"P/VPA (Price/Book): {info['priceToBook']}")
# print(f"Valor da Empresa: {info['enterpriseValue']}")
# print(f"Beta (Risco): {info['beta']}")
# print(f"Dividend Yield: {info['dividendYield'] * 100:.2f}%")
# print(f"Dividendos Anuais: {info['lastDividendValue']}")
# print(f"Data do Último Dividendo: {info['lastDividendDate']}")
# print(f"Payout Ratio: {info['payoutRatio']}")
# print(f"Margem de Lucro Líquido: {info['profitMargins'] * 100:.2f}%")
# print(f"Receita (Últimos 12 meses): {info['totalRevenue']}")
# print(f"Lucro Bruto: {info['grossProfits']}")
# print(f"EBITDA: {info['ebitda']}")
# # print(f"Número de Funcionários: {info['fullTimeEmployees']}")
# print(f"Site Oficial: {info['website']}")
# print(f"Descrição da Empresa: {info['longBusinessSummary']}")


# meus_ativos = ['BBAS3', 'EZTC3', 'FESA4', 'KLBN4', 'LEVE3','SIMH3', 'SLCE3', 'TUPY3']

# # baixar as cotacoes dos ultimos 5 anos
# for ativo in meus_ativos:
#     coletor = Coletor(ativo)
#     precos = coletor.precos_yahoo()
#     print(precos)

# # baixar os dados financeiros
# for ativo in meus_ativos:
#     coletor = Coletor(ativo)
#     for tipo in ['dre', 'bp', 'fc', 'stats', 'divs', 'ests',  'ests_r']:
#         balanco = coletor.balanco(tipo)

# coletor = Coletor('BBAS3')
# coletor.balanco('bp')


# import requests

# resposta = requests.get(url, headers=headers)
# resposta = requests.get("https://api.github.com/rate_limit", headers=headers)
# print(resposta.json())
