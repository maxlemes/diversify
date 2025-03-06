import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from etl_tradinview.fontes import FONTES


class Raspador:
    def __init__(self, url, xpath, headless=True):
        """Inicializa o navegador e define a URL e XPath do balanço a ser raspado."""

        self.url = url
        self.xpath = xpath
        self.headless = headless
        self.driver = self._iniciar_navegador()

    def _iniciar_navegador(self):
        """Configura e inicia o navegador Firefox."""
        options = Options()
        (
            options.add_argument("--headless") if self.headless else None
        )  # Rodar sem interface gráfica se for True
        service = Service(
            GeckoDriverManager().install()
        )  # Usa o WebDriverManager para gerenciar o GeckoDriver
        driver = webdriver.Firefox(service=service, options=options)
        return driver

    def acessar_site(self):
        """Acessa a URL especificada e aguarda o carregamento da página."""
        self.driver.get(self.url)
        time.sleep(5)  # Aguarda 5 segundos para o site carregar completamente

    def coletar_tabela(self):
        """Coleta tabela cujas linhas são do tipo /div."""

        try:
            # Acessa o site
            self.acessar_site()

            # Localiza a tabela
            tabela = self.driver.find_element(By.XPATH, self.xpath)

            # Localiza as linhas da tabela
            linhas = tabela.find_elements(By.XPATH, "./div")

            # Extrai as linhas da tabela
            lista_dados = [
                [celula.text for celula in linha.find_elements(By.XPATH, "./div")]
                for linha in linhas
            ]

            # retorna a lista com os dados
            return lista_dados

        except (TimeoutException, NoSuchElementException):
            print(f"Erro ao coletar Tabela.")
            return None

    def coletar_tabela_2(self):
        """Coleta tabela num elemento /table."""

        try:
            # Acessa o site
            self.acessar_site()

            # Localiza a tabela
            tabela = self.driver.find_element(By.XPATH, self.xpath)

            lista_dados = []

            # Extrair cabeçalhos
            cabecalho = [
                th.text for th in tabela.find_elements(By.XPATH, ".//thead/tr/th")
            ]
            lista_dados.append(cabecalho)

            # Localiza as linhas da tabela
            for tr in tabela.find_elements(By.XPATH, ".//tbody/tr"):
                linha = [td.text for td in tr.find_elements(By.XPATH, ".//td")]
                lista_dados.append(linha)

            # retorna a lista com os dados
            return lista_dados

        except (TimeoutException, NoSuchElementException):
            print(f"Erro ao coletar Tabela.")
            return None

    def coletar_elemento(self):
        """Coleta um balanço financeiro (DRE, Balanço Patrimonial, Fluxo de Caixa) site do TradingView."""

        try:
            # Acessa o site
            self.acessar_site()

            # Localiza e extrai o elemento
            elemento = self.driver.find_element(By.XPATH, self.xpath).text

            return elemento

        except (TimeoutException, NoSuchElementException):
            print(f"Erro ao coletar elemento.")
            return None

    def fechar_navegador(self):
        """Fecha o navegador."""
        self.driver.quit()
