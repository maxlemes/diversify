# ==============================================================================
# DIVERSIFY/DIVERSIFY/B3_INDEX.PY
# ==============================================================================
#
# DESCRIÇÃO:
# Este módulo é responsável por duas tarefas cruciais relacionadas aos dados
# de composição de índices da B3:
#
#   1. DOWNLOAD AUTOMATIZADO:
#      - Utiliza o Selenium para simular a navegação em um navegador, acessar as
#        páginas dos índices (IBOV, IFIX, etc.) e baixar as planilhas CSV
#        com a composição de cada um.
#
#   2. PROCESSAMENTO E PARSING DOS ARQUIVOS:
#      - Utiliza a biblioteca Pandas para ler os arquivos CSV baixados, que
#        possuem uma formatação específica da B3, e extrair as informações
#        relevantes (ticker e nome do ativo).
#
# FLUXO DE TRABALHO:
#   - A função `refresh_indices()` é o ponto de entrada principal para o download.
#   - Ela cria e gerencia uma única instância do navegador para ser mais eficiente,
#     evitando o erro de limite de API do GitHub e acelerando o processo.
#   - Para cada índice, a função `download_b3_file()` é chamada para realizar
#     a navegação e o clique que inicia o download.
#   - Após os arquivos serem baixados na pasta 'data/', a função
#     `b3_composition()` pode ser chamada por outros módulos (como os serviços)
#     para ler um desses arquivos e retornar uma lista estruturada de ativos.
#
# COMPONENTES PRINCIPAIS:
#
# - refresh_indices():
#     Orquestrador principal. Prepara o navegador, gerencia o loop de
#     downloads e fecha o navegador no final.
#
# - download_b3_file():
#     O "trabalhador" que opera o navegador para baixar um único arquivo de um
#     índice específico.
#
# - b3_composition():
#     O "processador de dados". Recebe o caminho de um arquivo CSV e usa o
#     Pandas para limpá-lo e extrair os dados necessários.
#
# - get_latest_file():
#     Função utilitária para encontrar o arquivo mais recente em uma pasta,
#     essencial para identificar o arquivo que acabou de ser baixado.
#
# ==============================================================================

import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_latest_file(path: str) -> str | None:
    """Encontra o arquivo modificado mais recentemente em um diretório."""
    files = [os.path.join(path, f) for f in os.listdir(path)]
    if not files:
        return None
    return max(files, key=os.path.getmtime)


# A função de download agora recebe o 'driver' já criado como argumento
def download_b3_file(
    driver: webdriver.Firefox, url: str, index_name: str, download_dir: str
) -> bool:
    """
    Usa uma instância de driver existente para navegar, clicar e baixar o arquivo.
    Retorna True em caso de sucesso, False em caso de falha.
    """
    try:
        print(f"\nIniciando download da composição do índice {index_name}...")
        driver.get(url)

        download_button_xpath = "//a[normalize-space()='Download']"
        print("Aguardando o botão de download ficar disponível...")

        download_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, download_button_xpath))
        )
        print("Botão de download encontrado. Clicando...")

        download_button.click()

        print("Aguardando o download ser concluído...")
        time.sleep(10)

        latest_file = get_latest_file(download_dir)
        if latest_file and latest_file.endswith(".csv"):
            file_path = os.path.join(download_dir, f"{index_name}.csv")
            # Apaga o arquivo de destino se ele já existir, para evitar erro na renomeação
            if os.path.exists(file_path):
                os.remove(file_path)
            os.rename(latest_file, file_path)
            print(f"✅ Arquivo salvo e renomeado para: {file_path}")
            return True
        else:
            print("❌ Erro: Nenhum arquivo CSV foi encontrado na pasta de downloads.")
            return False

    except Exception as e:
        print(f"❌ Erro durante o download do {index_name}: {e}")
        print(f"Screenshot de depuração salvo como 'debug_{index_name}.png'")
        return False


# A função principal agora gerencia a criação e destruição do navegador
def refresh_indices():
    """
    Cria uma única instância do navegador e a reutiliza para baixar todos os arquivos.
    """
    print("--- Iniciando atualização dos arquivos de composição dos índices ---")

    download_dir = os.path.abspath("data")
    os.makedirs(download_dir, exist_ok=True)

    options = Options()
    options.add_argument("--headless")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.download.useDownloadDir", True)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # INSTALA O DRIVER E CRIA O NAVEGADOR UMA ÚNICA VEZ
    # service = Service(GeckoDriverManager().install())
    service = Service(executable_path="./drivers/geckodriver")

    driver = webdriver.Firefox(service=service, options=options)

    try:
        indices = {
            "IBOV": "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br",
            "IFIX": "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IFIX?language=pt-br",
            "IDIV": "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IDIV?language=pt-br",
            "SMLL": "https://sistemaswebb3-listados.b3.com.br/indexPage/day/SMLL?language=pt-br",
            "IBRA": "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBRA?language=pt-br",  # IBrX-100
        }

        # Limpa arquivos .csv antigos antes de começar
        for f in os.listdir(download_dir):
            if f.endswith(".csv"):
                os.remove(os.path.join(download_dir, f))
        print("Arquivos CSV antigos da pasta 'data' foram removidos.")

        # REUTILIZA A MESMA JANELA DO NAVEGADOR PARA TODOS OS DOWNLOADS
        for name, url in indices.items():
            download_b3_file(driver, url, name, download_dir)
            time.sleep(2)

    finally:
        # FECHA O NAVEGADOR APENAS NO FINAL DE TODO O PROCESSO
        if driver:
            driver.quit()
        print("\n--- Atualização concluída ---")


def b3_composition(file_path: str, index_name: str):
    """
    Lê um arquivo CSV de composição de índice da B3 que já foi baixado,
    usando a segunda linha como cabeçalho e ignorando as outras.
    Retorna uma lista de dicionários com 'ticker' e 'nome'.
    """
    print(f"Processando arquivo de composição para {index_name} de '{file_path}'...")

    if not file_path or not os.path.exists(file_path):
        print(f"⚠️ Arquivo '{file_path}' não encontrado. Usando lista de fallback.")
        if index_name == "IBrX-100":
            return [
                {"ticker": "PETR4", "nome": "PETROBRAS PN"},
                {"ticker": "VALE3", "nome": "VALE ON"},
            ]
        if index_name == "IFIX":
            return [
                {"ticker": "MXRF11", "nome": "MAXI RENDA FII"},
                {"ticker": "HGLG11", "nome": "CSHG LOGISTICA FII"},
            ]
        return []

    try:
        # --- CORREÇÃO PRINCIPAL AQUI ---
        # Adicionado 'index_col=False' para garantir que nenhuma coluna
        # seja usada como índice do DataFrame.
        df_index = pd.read_csv(
            file_path,
            sep=";",
            encoding="latin-1",
            skipfooter=2,
            engine="python",
            skiprows=1,  # Pula apenas a primeira linha do arquivo
            index_col=False,  # Impede o pandas de adivinhar um índice
        )
        print(df_index)
        # Renomeia as colunas de forma robusta, procurando por variações
        rename_map = {}
        for col in df_index.columns:
            col_upper = col.upper()
            if "CÓD" in col_upper:
                rename_map[col] = "ticker"
            elif "AÇÃO" in col_upper or "NOME" in col_upper:
                rename_map[col] = "nome"

        df_index.rename(columns=rename_map, inplace=True)

        # Validação para garantir que as colunas foram encontradas
        if "ticker" not in df_index.columns or "nome" not in df_index.columns:
            raise ValueError(
                "Não foi possível encontrar as colunas de ticker e nome no arquivo CSV."
            )

        # Seleciona apenas as colunas que nos interessam e remove linhas vazias
        df_composicao = df_index[["ticker", "nome"]].dropna()

        print(f"Processados {len(df_composicao)} ativos do arquivo {file_path}.")
        return df_composicao.to_dict("records")

    except Exception as e:
        print(f"❌ Erro ao processar o arquivo {file_path}: {e}")
        return []  # Retorna lista vazia em caso de erro de processamento


if __name__ == "__main__":
    refresh_indices()
