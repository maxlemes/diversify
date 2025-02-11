
from selenium import webdriver

from scrapping.extrair_balanco import extrair_balanco

class Coletor:
    def __init__(self):
        """Inicializa o coletor com o driver do Firefox."""
        self.driver = webdriver.Firefox()

    def fechar(self):
        """Fecha o navegador."""
        self.driver.quit()

Coletor.extrair_balanco = extrair_balanco