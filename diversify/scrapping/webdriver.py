# Responsável por inicializar e configurar o Selenium com o Firefox.
# Configura o WebDriver do Firefox (usando webdriver_manager).
# Define opções como modo headless (sem abrir janela).
# Retorna uma instância do navegador pronta para uso.

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


def iniciar_navegador():
    """Inicia e retorna uma instância do navegador Firefox."""
    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # Executa o navegador sem abrir janela
    driver = webdriver.Firefox(service=service, options=options)
    return driver
