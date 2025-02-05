# Contém as funções que fazem o scraping dos dados.
# Usa o WebDriver (importado do webdriver.py).
# Abre a página do ativo desejado.
# Coleta os dados relevantes da página.

import re
import time
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

def extrair_indicador(ativo, indicador):

    # link para as tabelas
    tabela_income = '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]' 
    tabela_stats = '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]'
    
    # Ajutadondo os dados para coletar o EPS
    if indicador == 'EPS':
        url = income_tradingview(ativo)  # Acesso a página de demonstracoes do TradingView
        tabela = tabela_income

    
    # Ajutadondo os dados para coletar o ROE
    if indicador == 'ROE':
            url = stats_tradingview(ativo) # Acesso a página de estatísticas do TradingView
            tabela = tabela_stats

    # Inicia o navegador
    driver = iniciar_navegador()
    driver.get(url)

    # esperar 10 segundos para a página carregar
    time.sleep(10)

    try:
        # Localizar a tabela pelo XPath
        tabela = driver.find_element(By.XPATH, tabela)

        # Coletar todas as linhas da tabela
        linhas = tabela.find_elements(By.XPATH, "./div")

        # Extrair os dados
        dados = []
        for linha in linhas:
            celulas = linha.find_elements(By.XPATH, "./div")  # Ou "th" para cabeçalhos
            dados.append([celula.text for celula in celulas])


    except TimeoutException:
        print('O elemento não foi encontrado dentro do tempo limite.')

    driver.quit()
    return dados


def processar_cabecalho(linha):
    """
    Processa uma linha extraída de uma tabela:
    - Remove os dois primeiros elementos.
    - Divide o segundo item por '\n' e substitui no lugar original.
    - Retorna uma lista contendo o primeiro item e os 6 últimos anos.

    Parâmetros:
        linha (list): Lista contendo os dados da linha da tabela.

    Retorna:
        list: Lista processada.
    """
    linha = linha[2:]  # Remove os dois primeiros elementos
    linha[1:2] = linha[1].split('\n')  # Divide o segundo item por '\n'

    # Seleciona o primeiro item e os 6 últimos valores que estão nas posições ímpares
    linha = [linha[0]] + [item for i, item in enumerate(linha) if i % 2 != 0][-6:]
    
    return linha


def processar_linha(linha):
    """
    Processa uma linha extraída de uma tabela:
    - Remove os dois primeiros elementos.
    - Divide o terceiro item por '\n' e substitui no lugar original.
    - Remove caracteres unicode indesejados.
    - Separa a linha em duas listas: valores e crescimento.
    - Adiciona o prefixo 'Cresc. ' ao primeiro item da lista de crescimento.

    Parâmetros:
        linha (list): Lista contendo os dados da linha da tabela.

    Retorna:
        tuple: (lista de valores, lista de crescimento)
    """
    
    # Remove os dois primeiros elementos da linha
    linha = linha[2:]
    
    # Divide o terceiro item na quebra de linha '\n' (se presente)
    linha[2:3] = linha[2].split('\n')  # Substitui o terceiro item pela lista de duas partes

    # Remove caracteres unicode indesejados
    linha = [re.sub(r'[\u202a\u202c\u202f]', '', item) for item in linha]
    
    # Remove caracteres unicode indesejados
    linha = [re.sub('—' , '', item) for item in linha]

    # Condição para listas com 9 ou mais itens
    if len(linha) <= 9:
        # Eliminar o 2º e o último item
        linha = linha[:1] + linha[2:-1]

        # Converter os valores numéricos (exceto o primeiro item, que é uma string)
        linha = [linha[0]] + [converter_valor(valor) for valor in linha[1:]]
        return linha  # Retorna a linha processada

    else:
        # Separar os valores (itens nas posições pares)
        linha_res = [item for i, item in enumerate(linha) if i % 2 == 0]
        
        # Converter os valores de string para número
        linha_res = [linha_res[0]] + [converter_valor(valor) for valor in linha_res[1:]]
        
        # Separar a linha de crescimento (itens nas posições ímpares)
        linha_cres = [item for i, item in enumerate(linha) if i % 2 != 0]
        
        # Adiciona o prefixo 'Cresc.' ao primeiro item da lista de crescimento
        if linha_cres:
            linha_cres[0] = 'Cresc. ' + linha_res[0]
        
        # Retorna as duas listas: valores e crescimento
        return [linha_res, linha_cres]


def converter_valor(valor):
    """
    Converte valores monetários em strings para números:
    - 'B' (bilhão) → multiplica por 1e9
    - 'M' (milhão) → multiplica por 1e6
    - 'K' (milhar) → multiplica por 1e3

    Parâmetros:
        valor (str): O valor a ser convertido.

    Retorna:
        float: O valor convertido em número.
    """
    if isinstance(valor, str):  # Garante que é uma string
        valor = valor.replace(',', '.')  # Troca vírgula por ponto
        valor = valor.replace('−', '-')  # Fix Unicode minus (U+2212)

        if valor.endswith('B'):
            return float(valor[:-1]) * 1e9
        elif valor.endswith('M'):
            return float(valor[:-1]) * 1e6
        elif valor.endswith('K'):
            return float(valor[:-1]) * 1e3
    return float(valor) if valor else None  # Retorna como está se não for uma string conversível

import pandas as pd

def criar_dataframe(tabela):
    """
    Cria um DataFrame a partir de uma tabela processada.
    A função processa o cabeçalho e as linhas da tabela, tratando casos em que
    cada linha pode ser uma única linha ou uma lista com duas linhas.

    Parâmetros:
        tabela (list): Lista contendo os dados da tabela, onde a primeira linha
                       é o cabeçalho e as demais linhas são os dados.

    Retorna:
        pd.DataFrame: DataFrame com os dados processados.
    """
    # Processa o cabeçalho
    names = processar_cabecalho(tabela[0])

    # Criar uma lista para armazenar as linhas
    dados = []

    # Processa cada linha da tabela, começando da linha 1
    for i in range(1, len(tabela)):
        linha = tabela[i]
        linha_processada = processar_linha(linha)  # Processa a linha

        # Verificar se linha_processada é uma lista com uma ou duas linhas
        if isinstance(linha_processada[0], list):
            # Se for uma lista de listas, adiciona ambas as linhas
            dados.extend(linha_processada)
        else:
            # Caso contrário, adiciona apenas uma linha
            dados.append(linha_processada)

    # Criar o DataFrame com as linhas processadas
    df = pd.DataFrame(dados, columns=names)

    return df
