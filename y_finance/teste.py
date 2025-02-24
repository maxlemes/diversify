import yfinance as yf

from database.consultas_bd import ConsultasBD
from database.db_manager import ConexaoBD
from database.gerenciamento_bd import GerenciadorBD
from diversify.github_api import GitHubAPI
from y_finance.empresa import Empresa
from y_finance.estimativas import Estimar

github = GitHubAPI()

dados = github.obter_repositorio("maxlemes", "diversify")
# print(dados)
# print(github.verificar_limite())


# eliminar tabela
# with ConexaoBD() as bd:
#     bd.executar_query("DROP TABLE IF EXISTS cotacoes;")

# meus_ativos = ['BBAS3', 'EZTC3', 'FESA4', 'KLBN4', 'LEVE3','SIMH3', 'SLCE3', 'TUPY3']
meus_ativos = ["WEGE3", "LEVE3"]

for ativo in meus_ativos:
    # coleta de dados
    empresa = Empresa(ativo)
    # perfil = empresa.perfil()
    # dre = empresa.balanco('dre')
    # bp = empresa.balanco('bp')
    # fc = empresa.balanco('fc')
    # ttm_dre = empresa.ttm("dre")
    # ttm_fc = empresa.ttm("fc")
    divs = empresa.divs()
    # cotacoes = empresa.cotacoes()

    # inserir dados no banco
    with ConexaoBD() as bd:
        gerenciador = GerenciadorBD(bd)
        consulta = ConsultasBD(bd)
        # gerenciador.deletar_tabela('stats')
        gerenciador.tabelas_iniciais()
        # gerenciador.inserir_dados('perfil', perfil)
        # # gerenciador.inserir_dados('cotacoes', cotacoes)
        # gerenciador.inserir_dados('dre', dre)
        # gerenciador.inserir_dados('dre', ttm_dre)
        # gerenciador.inserir_dados('bp', bp)
        # gerenciador.inserir_dados('fc', fc)
        # gerenciador.inserir_dados('fc', ttm_fc)
        perfil_id = consulta.buscar_perfil_id(ativo)
        divs = [(perfil_id,) + dado for dado in divs]

        gerenciador.insert_stats("stats", ["perfil_id", "ano", "dividendos"], divs)

        print(divs)
        consulta = ConsultasBD(bd)
        perfil = consulta.buscar_perfil_id(ativo)
        print(perfil)

        estimar = Estimar(bd)
        estimar.calcular_roe(ativo)

# # consultar dados no banco
# with ConexaoBD() as bd:
# consultas = ConsultasBD(bd)
# perfil = consultas.buscar_perfil(nome="WEG")
# setores = consultas.consultar_tabelas('perfil', 'setor')
# tabelas = consultas.listar_tabelas()
# cotacoes = consultas.buscar_cotacoes('WEGE3')
# dre = consultas.buscar_dre('WEGE3')

# print("")
# print(perfil['subsetor'])
# print(setores)
# print(tabelas)
# print(cotacoes[0])
# print(dre)

# ativo = 'WEGE3'

# stock = yf.Ticker(ativo + ".SA")

# info = stock.earnings_estimate # estimativa EPS current (0y) e proximo ano (+1y) tem tambem trimestral
# info = stock.earnings_dates # eps estimativa vs reportado com datas
# info = stock.earnings_history['epsActual'].sum() # EPS TTM
# info = stock.financials
# print(info)
# print(f"Nome: {info['longName']}")= dados.info["currentPrice"]

# with ConexaoBD() as bd:
#     estimar = Estimar(bd)
#     print(estimar.calcular_roe('WEGE3'))
