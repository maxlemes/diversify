# ==============================================================================
# SCRIPT DE INICIALIZAÇÃO DE DADOS DO MERCADO (inicializar_mercado.py)
# ==============================================================================
#
# DESCRIÇÃO:
# Este é um script de setup ("bootstrap") projetado para ser executado uma vez
# para popular um banco de dados vazio com o universo de ativos e seus dados
# históricos. Ele é o ponto de partida para que a aplicação tenha dados
# suficientes para realizar qualquer análise.
#
# PRÉ-REQUISITOS:
# Antes de executar este script, é necessário que os arquivos CSV de composição
# dos índices (IBOV.csv, IFIX.csv, etc.) já tenham sido baixados pela tarefa
# de download (`b3_index.py`) e estejam presentes na pasta `data/`.
#
# FLUXO DE TRABALHO:
# 1. Leitura dos Arquivos Locais:
#    - O script lê os arquivos CSV da pasta `data/` usando a função
#      `b3_composition` para extrair a lista de ativos de cada índice.
#
# 2. Inicialização do Banco de Dados:
#    - A função `db_start()` é chamada para garantir que o arquivo do banco de
#      dados e todas as suas tabelas existam.
#
# 3. Povoamento dos Ativos (`popular_ativos_iniciais`):
#    - Itera sobre as listas de ativos dos índices e, usando o `PortfolioService`,
#      garante que cada um deles seja criado na tabela `ativos` do banco de
#      dados, evitando duplicatas.
#
# 4. Coleta de Dados Históricos (`coletar_historico_completo`):
#    - Após ter a lista completa de ativos no banco, o script utiliza a
#      biblioteca `yfinance` para baixar um longo período de histórico de
#      cotações diárias para CADA UM dos ativos cadastrados.
#
# 5. Armazenamento em Massa:
#    - Todos os milhares de registros de cotações coletados são enviados de
#      uma só vez para o banco de dados através do método de inserção em massa
#      do `PortfolioService`, que é altamente eficiente.
#
# COMO USAR:
# Execute este script diretamente do terminal a partir da raiz do projeto:
# > python inicializar_mercado.py
#
# ==============================================================================

import datetime

import yfinance as yf
from db_nexus import DatabaseSessionManager

from diversify.b3_index import b3_composition, refresh_indices
from diversify.models import TipoAtivo, db_start

# Importa as funções necessárias dos outros módulos
from diversify.services import PortfolioService

# --- UNIVERSO DE ATIVOS ---
# Agora, o script define os caminhos dos arquivos locais que ele espera encontrar
IBRX_FILE_PATH = "data/IBRA.csv"
IFIX_FILE_PATH = "data/IFIX.csv"
SMLL_FILE_PATH = "data/SMLL.csv"
IDIV_FILE_PATH = "data/IDIV.csv"

# Processa os arquivos locais. Se eles não existirem, a função de processamento
# usará a lista de fallback.
IBOV_COMPOSITION = b3_composition(IBRX_FILE_PATH, "IBrX-100")
IFIX_COMPOSITION = b3_composition(IFIX_FILE_PATH, "IFIX")
SMLL_COMPOSITION = b3_composition(SMLL_FILE_PATH, "SMLL")
IDIV_COMPOSITION = b3_composition(IDIV_FILE_PATH, "IDIV")


def atualizar_indices() -> bool:
    """
    Verifica se a data atual está dentro da janela de rebalanceamento dos
    índices da B3 (período de prévias + início da nova carteira).
    Retorna True se for um bom momento para atualizar, False caso contrário.
    """
    hoje = datetime.date.today()
    mes_atual = hoje.month
    dia_atual = hoje.day

    # Meses em que a nova carteira entra em vigor (Janeiro, Maio, Setembro)
    meses_rebalanceamento = [1, 5, 9]
    # Meses em que as prévias são divulgadas (Dezembro, Abril, Agosto)
    meses_previa = [12, 4, 8]

    # Verifica se estamos nos primeiros 10 dias de um mês de rebalanceamento
    if mes_atual in meses_rebalanceamento and dia_atual <= 10:
        print(
            f"INFO: Data ({hoje}) está no início do período de rebalanceamento. Atualização recomendada."
        )
        return True

    # Verifica se estamos nos últimos 10 dias de um mês de prévias
    if mes_atual in meses_previa and dia_atual >= 20:
        print(
            f"INFO: Data ({hoje}) está no período de prévias do rebalanceamento. Atualização recomendada."
        )
        return True

    print(f"INFO: Data ({hoje}) fora da janela de rebalanceamento da B3.")
    return False


def popular_ativos_iniciais(service: PortfolioService):
    """
    Garante que todos os ativos do IBRX, IDIV, SMLL e IFIX existam na tabela 'ativos'.
    """
    print("Verificando e criando ativos do universo de mercado...")

    for ativo in IBOV_COMPOSITION:
        service.garantir_existencia_ativo(
            ativo["ticker"], ativo["nome"], TipoAtivo.ACAO
        )

    for ativo in IDIV_COMPOSITION:
        service.garantir_existencia_ativo(
            ativo["ticker"], ativo["nome"], TipoAtivo.ACAO
        )

    for ativo in SMLL_COMPOSITION:
        service.garantir_existencia_ativo(
            ativo["ticker"], ativo["nome"], TipoAtivo.ACAO
        )

    for ativo in IFIX_COMPOSITION:
        service.garantir_existencia_ativo(ativo["ticker"], ativo["nome"], TipoAtivo.FII)

    # Adiciona os próprios índices (ou ETF equivalentes) como ativos ---
    service.garantir_existencia_ativo("^BVSP", "Índice Bovespa", TipoAtivo.INDICE)
    service.garantir_existencia_ativo(
        "DIVO11", "Índice Ações de Dividendos", TipoAtivo.INDICE
    )
    service.garantir_existencia_ativo("SMAL11", "Índice Small Caps", TipoAtivo.INDICE)
    service.garantir_existencia_ativo(
        "XFIX11", "Índice de Fundos Imobiliários", TipoAtivo.INDICE
    )

    print("Ativos do universo de mercado garantidos no banco de dados.")


def coletar_historico_completo(service: PortfolioService):
    """
    Coleta 3 anos de histórico de cotações para TODOS os ativos no banco.
    """
    print("\nIniciando coleta de 3 anos de dados históricos...")

    data_final = datetime.date.today()
    data_inicial = data_final - datetime.timedelta(days=5 * 365)
    data_inicial_str = data_inicial.strftime("%Y-%m-%d")
    data_final_str = data_final.strftime("%Y-%m-%d")

    print(f"Buscando dados no intervalo de {data_inicial_str} a {data_final_str}.")

    tickers = service.get_all_asset_tickers()

    dados_para_importar = []

    for ticker in tickers:
        ticker_api = ticker
        if not ticker.endswith(".SA") and ticker != "^BVSP":
            ticker_api = f"{ticker}.SA"

        try:
            print(f"  - Coletando dados para {ticker_api}...")
            dados = yf.download(
                ticker_api, start=data_inicial_str, end=data_final_str, progress=False
            )

            if dados.empty:
                print(f"    ⚠️ Nenhum dado retornado para {ticker_api}.")
                continue

            for data_cotacao, linha in dados.iterrows():
                dados_para_importar.append(
                    {
                        "ticker": ticker,
                        "data": data_cotacao.strftime("%Y-%m-%d"),
                        "preco_fechamento": linha["Close"],
                    }
                )

        except Exception as e:
            print(f"    ❌ Erro ao coletar dados para {ticker_api}: {e}")

    if dados_para_importar:
        print(
            f"\nTotal de {len(dados_para_importar)} registros de cotações para salvar..."
        )
        service.importar_dados_historicos(dados_para_importar)
    else:
        print("\nNenhum dado novo para importar.")


if __name__ == "__main__":
    db_start()

    DB_URL = "sqlite:///data/portfolio.db"
    session_manager = DatabaseSessionManager(DB_URL)
    service = PortfolioService(session_manager)

    # LÓGICA CONDICIONAL AQUI
    if atualizar_indices():
        # 1. Baixa os arquivos de composição dos índices
        print("\n--- Etapa 0: Baixando arquivos de composição dos índices da B3 ---")
        refresh_indices()

        # 2. Popula a tabela de ativos com base nos arquivos baixados
        popular_ativos_iniciais(service)

        # 3. Coleta o histórico completo para os ativos (incluindo os novos)
        coletar_historico_completo(service)

        print("\n✅ Inicialização/Atualização completa do mercado concluída!")
    else:
        print(
            "\nPulando atualização dos índices e coleta de dados. Para forçar, execute a tarefa 'update_indices' diretamente."
        )

        # 1. Popula a tabela de ativos com base nos arquivos baixados
        popular_ativos_iniciais(service)

        # 2. Coleta o histórico completo para os ativos (incluindo os novos)
        coletar_historico_completo(service)

    print("\n✅ Inicialização do mercado concluída!")
