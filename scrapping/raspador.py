from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import time
from scrapping.fontes import FONTES

class Raspador:
    def __init__(self, ativo, tipo_balanco, headless=True):
        """Inicializa o navegador e define a URL e XPath do balanço a ser raspado."""
        if tipo_balanco not in FONTES:
            raise ValueError(f"Tipo de balanço '{tipo_balanco}' inválido. Escolha entre: {list(FONTES.keys())}")

        self.ativo = ativo
        self.tipo_balanco = tipo_balanco
        self.url = FONTES[tipo_balanco]["url"].format(ativo)
        self.xpath = FONTES[tipo_balanco]["xpath"]
        self.headless = headless
        self.driver = self._iniciar_navegador()
    
    def _iniciar_navegador(self):
        """Configura e inicia o navegador Firefox."""
        options = Options()
        options.add_argument("--headless") if self.headless else None # Rodar sem interface gráfica se for True
        service = Service(GeckoDriverManager().install())  # Usa o WebDriverManager para gerenciar o GeckoDriver
        driver = webdriver.Firefox(service=service, options=options)
        return driver
    
    def acessar_site(self):
        """Acessa a URL especificada e aguarda o carregamento da página."""
        self.driver.get(self.url)
        time.sleep(5)  # Aguarda 5 segundos para o site carregar completamente

    def coletar_tabela(self):
        """Coleta um balanço financeiro (DRE, Balanço Patrimonial, Fluxo de Caixa) do TradingView."""

        try:
            # Acessa o site e aguarada 5s
            self.driver.get(self.url)
            time.sleep(5)  # Aguarda 5 segundos para o site carregar completamente

            # Localizar a tabela
            tabela = self.driver.find_element(By.XPATH, self.xpath)
            linhas = tabela.find_elements(By.XPATH, "./div")

            # Extrair os dados da tabela
            dados = [[celula.text for celula in linha.find_elements(By.XPATH, "./div")] for linha in linhas]
            return dados

        except (TimeoutException, NoSuchElementException):
            print(f"Erro ao coletar Tabela.")
            return None
        
    def fechar_navegador(self):
        """Fecha o navegador."""
        self.driver.quit()
