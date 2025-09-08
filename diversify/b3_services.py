# ==============================================================================
# DIVERSIFY/DIVERSIFY/B3_SERVICES.PY
# ==============================================================================
#
# DESCRIÇÃO GERAL:
# Este módulo funciona como um serviço completo para o ciclo de vida dos dados de
# composição de índices da B3. Ele contém todas as funções necessárias para
# orquestrar o processo, desde a decisão de quando rodar, o download, a
# verificação dos arquivos, o processamento e extração dos dados, até a
# persistência dos resultados limpos e a manutenção dos arquivos baixados.
#
# FLUXO DE EXECUÇÃO PRINCIPAL:
# O ponto de entrada para a execução completa é a função `run_update_manager()`.
# Ela gerencia todo o fluxo, que inclui as seguintes etapas:
#
#   1. DECISÃO (`moment_index`):
#      - (Opcional) Verifica se a data atual está dentro da janela de
#        rebalanceamento da B3 para determinar se a atualização é necessária.
#
#   2. GERENCIAMENTO E DOWNLOAD (`run_update_manager` -> `refresh_indices`):
#      - Tenta obter todos os arquivos de índice para o dia. Possui lógica de
#        múltiplas tentativas para lidar com falhas de rede.
#      - A obtenção é inteligente: se o arquivo do dia já existe, ele é usado;
#        senão, é feito o download via Selenium.
#
#   3. PROCESSAMENTO E PERSISTÊNCIA (Lógica no script principal):
#      - Após `run_update_manager` retornar os caminhos dos arquivos, o script
#        principal chama as funções para processar os CSVs (`b3_composition`),
#        transformando-os em dados estruturados.
#      - Em seguida, os dados limpos são salvos em arquivos JSON para consumo
#        futuro (`save_composition_to_json`).
#
#   4. MANUTENÇÃO (`cleanup_old_index_files`):
#      - Após um ciclo bem-sucedido, a função de limpeza é chamada para deletar
#        os arquivos CSV de dias anteriores, mantendo a pasta de dados organizada.
#
# COMPONENTES PRINCIPAIS (Agrupados por Responsabilidade):
#
# - ORQUESTRAÇÃO:
#   - run_update_manager(): O controlador principal de todo o processo.
#
# - LÓGICA DE NEGÓCIO:
#   - moment_index(): Verifica se é o momento certo do mês para a atualização.
#
# - DOWNLOAD:
#   - refresh_indices(): Gerencia a instância do navegador e o loop de downloads.
#   - download_b3_file(): Executa a tarefa de baixar um único arquivo CSV.
#   - find_todays_file_for_index(): Utilitário que verifica se o arquivo do dia
#     já foi baixado.
#
# - PROCESSAMENTO:
#   - b3_composition(): O "parser" de baixo nível que usa Pandas para ler e
#     limpar o conteúdo do arquivo CSV bruto.
#   - get_composition_for_index(): (Se utilizada) Função de alto nível que
#     decide entre processar um arquivo ou usar dados de fallback.
#
# - PERSISTÊNCIA:
#   - save_composition_to_json(): Salva os dados processados em um arquivo JSON.
#
# - MANUTENÇÃO:
#   - cleanup_old_index_files(): Deleta arquivos CSV de dias anteriores.
#
# ==============================================================================

import json
import os
import time
from datetime import date, datetime
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class B3Service:
    """
    Contém a lógica de negócio de alto nível para lidar com dados da B3.
    """

    # A função principal agora gerencia a criação e destruição do navegador
    def refresh_indices(self) -> dict:
        """
        Cria uma única instância do navegador e a reutiliza para baixar todos
        os arquivos de índices, mantendo os arquivos antigos na pasta de destino.

        Retorna um dicionário com os nomes dos índices e os caminhos dos arquivos
        recém-baixados.
        """
        print("--- Iniciando atualização dos arquivos de composição dos índices ---")

        # --- 1. CONFIGURAÇÃO INICIAL ---
        download_dir = Path("data").resolve()
        os.makedirs(download_dir, exist_ok=True)

        try:
            config_path = Path(__file__).resolve().parent.parent / "b3_links.json"
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            indices = config["indices_b3"]
        except FileNotFoundError:
            print(
                f"❌ ERRO: Arquivo 'b3_links.json' não encontrado na raiz do projeto."
            )
            return {}

        # --- 2. INICIALIZAÇÃO DO NAVEGADOR (FEITA UMA ÚNICA VEZ) ---
        options = Options()
        options.add_argument("--headless")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", str(download_dir))
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

        service = Service(executable_path="./drivers/geckodriver")
        driver = webdriver.Firefox(service=service, options=options)

        downloaded_files = {}

        # --- 3. EXECUÇÃO DOS DOWNLOADS COM VERIFICAÇÃO ---
        try:
            for name, url in indices.items():

                # ** AQUI ESTÁ A NOVA LÓGICA **
                # Primeiro, verifica se o arquivo do dia já existe
                existing_file_path = self.find_todays_file_for_index(name, download_dir)

                if existing_file_path:
                    print(
                        f"\n✅ Arquivo para '{name}' já existe hoje. Pulando download."
                    )
                    # Adiciona o arquivo existente à nossa lista de resultados
                    downloaded_files[name] = existing_file_path
                    continue  # Pula para o próximo índice do loop

                # Se o arquivo não existe, prossegue com o download
                file_path = self.download_b3_file(driver, url, name, str(download_dir))

                if file_path:
                    downloaded_files[name] = file_path

                time.sleep(2)

        finally:
            # --- 4. ENCERRAMENTO DO NAVEGADOR ---
            if driver:
                driver.quit()
            print("\n--- Atualização concluída ---")

        return downloaded_files

    def moment_index(self) -> bool:
        """
        Verifica se a data atual está dentro da janela de rebalanceamento dos
        índices da B3 (período de prévias + início da nova carteira).
        Retorna True se for um bom momento para atualizar, False caso contrário.
        """
        hoje = date.today()
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

    def find_todays_file_for_index(
        self, index_name: str, download_dir: Path
    ) -> str | None:
        """
        Verifica se um arquivo para um determinado índice, com a data de hoje, já existe.

        O padrão do nome do arquivo esperado é: NOME_DO_INDICEDia_DD-MM-YY.csv

        :param index_name: O nome do índice (ex: "IFIX").
        :param download_dir: O diretório onde o arquivo seria salvo.
        :return: O caminho completo do arquivo se ele existir, senão, None.
        """
        # Formata a data de hoje como DD-MM-YY (ex: 01-09-25)
        today_str = datetime.now().strftime("%d-%m-%y")

        # Monta o nome do arquivo que estamos procurando
        expected_filename = f"{index_name}Dia_{today_str}.csv"

        # Monta o caminho completo do arquivo
        expected_filepath = download_dir / expected_filename

        # Verifica se o arquivo realmente existe nesse caminho
        if expected_filepath.exists():
            return str(expected_filepath)  # Retorna o caminho se encontrou

        return None  # Retorna None se não encontrou

    # A função de download agora recebe o 'driver' já criado como argumento
    def download_b3_file(
        self, driver: webdriver.Firefox, url: str, index_name: str, download_dir: str
    ) -> str | None:
        """
        Usa uma instância de driver existente para baixar o arquivo de composição de um índice.

        Esta versão aprimorada:
        - Espera o download ser concluído de forma inteligente.
        - Mantém o nome original do arquivo baixado.
        - Retorna o caminho completo do arquivo baixado em caso de sucesso, ou None em caso de falha.
        """
        try:
            print(f"\nIniciando download da composição do índice {index_name}...")

            # 1. Pega a lista de arquivos na pasta ANTES do download
            files_before = set(os.listdir(download_dir))

            driver.get(url)

            download_button_xpath = "//a[normalize-space()='Download']"
            print("Aguardando o botão de download ficar disponível...")

            download_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, download_button_xpath))
            )
            print("Botão de download encontrado. Clicando...")
            download_button.click()

            # 2. Lógica de espera inteligente (substituindo time.sleep)
            print("Aguardando o download ser concluído...")
            timeout = 30  # Tempo máximo de espera em segundos
            for i in range(timeout):
                # Pega a lista de arquivos DEPOIS do clique
                files_after = set(os.listdir(download_dir))
                new_files = files_after - files_before

                # Verifica se um novo arquivo .csv apareceu e não é um download parcial
                if new_files:
                    new_filename = new_files.pop()
                    if new_filename.endswith(".csv"):
                        # Espera um segundo extra para garantir que a escrita terminou
                        time.sleep(1)
                        file_path = os.path.join(download_dir, new_filename)
                        print(f"✅ Download concluído. Arquivo salvo como: {file_path}")
                        return file_path  # Retorna o caminho do novo arquivo

                time.sleep(1)  # Espera 1 segundo antes de verificar novamente

            # Se o loop terminar sem encontrar um arquivo, é um erro de timeout
            print("❌ Erro: O download não foi concluído dentro do tempo esperado.")
            return None

        except Exception as e:
            print(f"❌ Erro durante o download do {index_name}: {e}")
            return None

    def b3_composition(self, file_path: str, index_name: str) -> list[dict]:
        """
        Lê um arquivo CSV de composição de índice da B3, extraindo apenas as
        duas primeiras colunas (ticker e nome do ativo).

        Esta versão assume que a primeira coluna é sempre o ticker e a segunda
        é sempre o nome do ativo.
        """
        print(
            f"Processando arquivo de composição para {index_name} de '{file_path}'..."
        )

        try:
            # --- MUDANÇA PRINCIPAL AQUI ---
            # Usamos 'usecols' e 'names' para ler APENAS as colunas que nos interessam,
            # já nomeando-as corretamente no momento da leitura.
            df_composicao = pd.read_csv(
                file_path,
                sep=";",
                encoding="latin-1",
                skipfooter=2,
                engine="python",
                skiprows=2,  # Pula a primeira linha do arquivo (título geral)
                header=None,  # Informa que o arquivo não tem um cabeçalho que queremos usar
                usecols=[0, 1],  # Lê APENAS a primeira (0) e a segunda (1) colunas
                names=[
                    "ticker",
                    "nome",
                ],  # Dá a essas colunas os nomes 'ticker' e 'nome'
            )

            # Como já selecionamos as colunas, basta remover linhas que possam estar vazias.
            df_composicao.dropna(inplace=True)

            print(f"Processados {len(df_composicao)} ativos do arquivo {file_path}.")
            return df_composicao.to_dict("records")

        except FileNotFoundError:
            print(
                f"❌ ERRO CRÍTICO: O arquivo '{file_path}' não foi encontrado ao tentar processar."
            )
            return []
        except Exception as e:
            print(f"❌ Erro ao processar o arquivo {file_path}: {e}")
            return []

    # Adicione a importação do `datetime` se ainda não tiver no topo do arquivo
    from datetime import datetime

    # ... (todas as outras funções que criamos: find_todays_file_for_index,
    #      download_b3_file, b3_composition, refresh_indices) ...

    def cleanup_old_index_files(self, target_dir: Path, index_names: list[str]):
        """
        Limpa arquivos de índice antigos de um diretório, mantendo apenas os do dia atual.

        Para cada nome de índice, esta função procura por todos os arquivos que
        correspondem ao padrão (ex: "IFIXDia_*.csv") e deleta todos, exceto o que
        corresponde à data de hoje.

        :param target_dir: O diretório a ser limpo (ex: a pasta 'data').
        :param index_names: Uma lista com os nomes dos índices (ex: ["IBOV", "IFIX"]).
        """
        print(f"\n--- INICIANDO LIMPEZA DE ARQUIVOS ANTIGOS EM '{target_dir}' ---")

        # Pega a data de hoje no formato DD-MM-YY (ex: 02-09-25)
        today_str = datetime.now().strftime("%d-%m-%y")

        # Garante que o diretório alvo existe antes de continuar
        if not target_dir.exists():
            print(
                f"⚠️ Diretório '{target_dir}' não encontrado. Nenhuma limpeza a ser feita."
            )
            return

        # Repete o processo de limpeza para cada nome de índice
        for index_name in index_names:
            # Define o nome do arquivo que queremos MANTER para o índice atual
            file_to_keep = f"{index_name}Dia_{today_str}.csv"

            # Usa glob para encontrar TODOS os arquivos que correspondem ao padrão do índice
            # Ex: vai encontrar IFIXDia_01-09-25.csv, IFIXDia_02-09-25.csv, etc.
            files_found = target_dir.glob(f"{index_name}Dia_*.csv")

            for file_path in files_found:
                # Compara o nome do arquivo encontrado com o nome do arquivo que queremos manter
                if file_path.name != file_to_keep:
                    try:
                        os.remove(file_path)
                        print(f"🗑️ Deletado arquivo antigo: {file_path.name}")
                    except Exception as e:
                        print(f"❌ Erro ao tentar deletar {file_path.name}: {e}")

        print("--- LIMPEZA FINALIZADA ---")

    def run_update_manager(
        self, max_attempts: int = 3, retry_delay_minutes: int = 1
    ) -> dict:
        """
        Gerencia o processo completo de atualização dos arquivos de índices da B3.
        ... (o resto da docstring) ...
        """
        print("==========================================================")
        print(f"🚀 INICIANDO GERENCIADOR DE ATUALIZAÇÃO DE ÍNDICES B3")
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("==========================================================")

        try:
            config_path = Path(__file__).resolve().parent.parent / "b3_links.json"
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            target_indices = set(config["indices_b3"].keys())
        except FileNotFoundError:
            print(f"❌ ERRO FATAL: Arquivo 'b3_links.json' não encontrado. Abortando.")
            return {}  # Retorna um dicionário vazio em caso de erro inicial

        # Inicializa o dicionário ANTES do loop
        downloaded_files = {}

        # Loop de tentativas
        for attempt in range(1, max_attempts + 1):
            print(f"\n--- TENTATIVA {attempt} de {max_attempts} ---")

            # A cada tentativa, a variável `downloaded_files` é atualizada
            downloaded_files = self.refresh_indices()

            successful_indices = set(downloaded_files.keys())

            if target_indices.issubset(successful_indices):
                print(
                    "\n✅ SUCESSO! Todos os arquivos de índice para hoje foram obtidos."
                )
                if target_indices:
                    self.cleanup_old_index_files(Path("data"), list(target_indices))
                break
            else:
                missing_indices = target_indices - successful_indices
                print(
                    f"\n⚠️ AVISO: A tentativa {attempt} falhou em obter todos os arquivos."
                )
                print(f"Índices faltando: {', '.join(missing_indices)}")

                if attempt < max_attempts:
                    print(
                        f"Aguardando {retry_delay_minutes} minutos antes de tentar novamente..."
                    )
                    time.sleep(retry_delay_minutes * 60)
                else:
                    print("\n❌ ERRO FINAL: Número máximo de tentativas atingido.")

        print("\n==========================================================")
        print("🏁 GERENCIADOR DE ATUALIZAÇÃO FINALIZADO.")
        print("==========================================================")

        # <<< A CORREÇÃO ESTÁ AQUI! >>>
        # Retorna o resultado da última tentativa (bem-sucedida ou não).
        return downloaded_files

    def save_composition_to_json(
        self, index_name: str, composition_data: list[dict], output_dir: Path
    ):
        """
        Salva a lista de composição de um índice em um arquivo JSON.

        :param index_name: O nome do índice (ex: "IFIX"), usado para nomear o arquivo.
        :param composition_data: A lista de dicionários de ativos para salvar.
        :param output_dir: O diretório onde o arquivo JSON será salvo.
        """
        # Garante que o diretório de saída exista
        os.makedirs(output_dir, exist_ok=True)

        # Define o caminho completo do arquivo de saída
        file_path = output_dir / f"{index_name}_composition.json"

        print(f"Salvando composição do {index_name} em: {file_path}")

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # json.dump é usado para escrever o objeto Python no arquivo
                json.dump(
                    composition_data,
                    f,
                    ensure_ascii=False,  # Essencial para salvar caracteres como 'Ç' e 'Ã' corretamente
                    indent=4,  # Formata o JSON para ser legível, com 4 espaços de indentação
                )
            print(f"✅ Arquivo {file_path} salvo com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao salvar o arquivo JSON para {index_name}: {e}")

    def refresh_index(self):
        """
        Executa o processo de atualização dos dados de índices da B3.
        """
        if self.moment_index():
            # ETAPA 1: Gerenciar e garantir o download de todos os arquivos de índice.
            available_files_map = self.run_update_manager(
                max_attempts=3, retry_delay_minutes=1
            )

            # Verifica se a etapa de download teve algum sucesso antes de prosseguir
            if not available_files_map:
                print(
                    "\nNenhum arquivo foi encontrado ou baixado. Encerrando o processo."
                )
            else:
                print("\n--- INICIANDO ETAPA DE PROCESSAMENTO DOS ARQUIVOS ---")
                all_compositions = {}
                for index_name, file_path in available_files_map.items():
                    composition = self.b3_composition(file_path, index_name)
                    all_compositions[index_name] = composition

                print("\n--- PROCESSAMENTO CONCLUÍDO ---")

                # --- ETAPA 3: SALVAR OS RESULTADOS PROCESSADOS EM ARQUIVOS JSON ---
                print("\n--- INICIANDO ETAPA DE SALVAMENTO EM JSON ---")

                # Define um diretório para salvar os dados processados
                processed_data_dir = Path("processed_data")

                for index_name, composition_list in all_compositions.items():
                    if (
                        composition_list
                    ):  # Salva apenas se a lista de composição não estiver vazia
                        self.save_composition_to_json(
                            index_name, composition_list, processed_data_dir
                        )
                    else:
                        print(
                            f"⚠️ Nenhuma composição para salvar para o índice {index_name}."
                        )

                print("\n--- SALVAMENTO CONCLUÍDO ---")
        else:
            print(f"Atualização dos índices não é necessária.")
