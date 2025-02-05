# Contém as funções que fazem o scraping dos dados.
# Usa o WebDriver (importado do webdriver.py).
# Abre a página do ativo desejado.
# Coleta os dados relevantes da página.

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .webdriver import iniciar_navegador
from .database import salvar_profile
from .urls import profile_yahoo, income_tradingview, stats_tradingview


def extrair_profile(ativo):
    """Acessa o site do Yahoo e retorna o perfil da empresa."""
    url = profile_yahoo(ativo)
    driver = iniciar_navegador()
    driver.get(url)

    try:
        nome_acao = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/main/section/section/section/article/section[1]/div[1]/div/div/section/h1',
        ).text
        descricao = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/main/section/section/section/article/section[3]/section[1]/p',
        ).text
        website = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/main/section/section/section/article/section[2]/section[2]/div/div/a[2]',
        ).text
        cotacao = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/main/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[1]/span',
        ).text

        if cotacao != '-':
            cotacao = float(
                re.sub('[\u202a\u202c,]', '', cotacao).replace(',', '.')
            )

        dados = {
            'ticker': ativo,
            'nome': limpar_nome_empresa(nome_acao),
            'descricao': descricao,
            'website': website,
            'cotacao': cotacao
        }

        salvar_profile(dados)
        print(f'Perfil de {ativo} salvos com sucesso!')

    except Exception as e:
        print(f'Erro ao extrair dados: {e}')
        dados = None

    driver.quit()
    return dados


def limpar_nome_empresa(nome):
    """Remove 'S.A.', 'S/A' e outras informações extras do nome da empresa."""
    nome = re.sub(
        r'\bS\.?A\b', '', nome, flags=re.IGNORECASE
    ).strip()  # Remove 'S.A.' ou 'SA'
    nome = re.split(r'[\(\.]', nome)[0].strip()  # Corta no primeiro '(' ou '.'
    return nome


def extrair_indicador(ativo, indicador):

    # Ajustando o XPATH dos dados a setem extraidos
    anos_eps = [
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[16]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[17]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[18]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[19]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[20]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[21]/div/div[1]',
    ]
    valores_eps = [
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[16]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[17]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[18]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[19]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[20]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[21]/div/div[1]',
    ]

    anos_roe = [
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[16]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[17]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[18]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[19]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[20]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[21]/div/div[1]',
    ]
    valores_roe = [
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[16]/div/div',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[17]/div/div',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[18]/div/div',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[19]/div/div',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[20]/div/div',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[21]/div/div',
    ]

    # Ajutadondo os dados para coletar o EPS
    if indicador == 'EPS':
        url = income_tradingview(ativo)  # Acesso a página de demonstracoes do TradingView
        anos_ind = anos_eps
        valores_ind = valores_eps
    
    # Ajutadondo os dados para coletar o ROE
    if indicador == 'ROE':
            url = stats_tradingview(ativo) # Acesso a página de estatísticas do TradingView
            anos_ind = anos_roe
            valores_ind = valores_roe

    # Inicia o navegador
    driver = iniciar_navegador()
    driver.get(url)
   
    # Espera explícita para garantir que o elemento esteja presente
    wait = WebDriverWait(driver, 10)  # Espera até 15 segundos

    dados = []

    try:
        elemento = wait.until(
            EC.presence_of_element_located((By.XPATH, valores_ind[0]))
        )
        try:
            for index in range(len(anos_ind)):
                ano = driver.find_element(By.XPATH, anos_ind[index]).text
                valor = driver.find_element(By.XPATH, valores_ind[index]).text

                if valor.startswith('\u202a'):
                    valor = float(
                        re.sub('[\u202a\u202c,]', '', valor).replace(',', '.')
                        )/100

                dado = {
                    'ticker': ativo,
                    'ano': ano,
                    'indicador': indicador,
                    'valor': valor
                }
                dados.append(dado)

            # salvar_ativo(dados)
            print(f'{indicador} de {ativo} coletados com sucesso!')

        except Exception as e:
            print(f'Erro ao extrair dados: {e}')
            dados = None

    except TimeoutException:
        print('O elemento não foi encontrado dentro do tempo limite.')

    driver.quit()
    return dados

def extrair_indicador2(ativo, indicador):

    # Ajustando o XPATH dos dados a setem extraidos
    anos_eps = [
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[16]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[17]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[18]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[19]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[20]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[21]/div/div[1]',
    ]
    valores_eps = [
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[16]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[17]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[18]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[19]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[20]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]/div[5]/div[21]/div/div[1]',
    ]

    anos_roe = [
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[16]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[17]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[18]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[19]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[20]/div/div[1]',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[1]/div[4]/div[21]/div/div[1]',
    ]
    valores_roe = [
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[16]/div/div',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[17]/div/div',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[18]/div/div',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[19]/div/div',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[20]/div/div',
        '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[21]/div/div',
    ]

    tabela_eps = '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]' 

    # Ajutadondo os dados para coletar o EPS
    if indicador == 'EPS':
        url = income_tradingview(ativo)  # Acesso a página de demonstracoes do TradingView
        anos_ind = anos_eps
        valores_ind = valores_eps
    
    # Ajutadondo os dados para coletar o ROE
    if indicador == 'ROE':
            url = stats_tradingview(ativo) # Acesso a página de estatísticas do TradingView
            anos_ind = anos_roe
            valores_ind = valores_roe

    # Inicia o navegador
    driver = iniciar_navegador()
    driver.get(url)
   
    # Espera explícita para garantir que o elemento esteja presente
    wait = WebDriverWait(driver, 10)  # Espera até 15 segundos

    dados = []

    try:
        # Localizar a tabela pelo XPath
        tabela = driver.find_element(By.XPATH, tabela_eps)

        # Capturar todas as linhas da tabela
        dados = tabela.find_elements

    except TimeoutException:
        print('O elemento não foi encontrado dentro do tempo limite.')

    driver.quit()
    return dados
