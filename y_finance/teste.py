import yfinance as yf
from consultas import Consultar

from banco_dados.conexao_bd import ConexaoBD
from banco_dados.gerenciamento_bd import GerenciadorBD
from diversify.github_api import GitHubAPI
from y_finance.empresa import Empresa

github = GitHubAPI()

dados = github.obter_repositorio("maxlemes", "diversify")
# print(dados)
# print(github.verificar_limite())

ativo = "WEGE3"

empresa = Empresa(ativo)

# df = coleta.cotacoes()
# print(df)

# print(f"Nome: {info['longName']}")

# dados = yf.Ticker(ativo + ".SA")
# print(dados)

# print(list(info.keys()))

# cotacao = dados.info['currentPrice']
# print(f"A cotação de {ativo} é: {cotacao}")

# print(dados.earnings_dates)

perfil = empresa.perfil()

# print(perfil)


df = empresa.cotacoes()
print(df)


conexao = ConexaoBD("banco_dados/banco_de_dados.db")
conexao.conectar()
banco = GerenciadorBD(conexao)  # Cria uma instância da classe e conecta ao banco
banco.inserir_dados(
    "cotacoes", df
)  # Chama o método criar_tabelas() que cria as tabelas
conexao.desconectar()  # Fecha a conexão corretamente
