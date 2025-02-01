# Contém as funções que fazem o scraping dos dados.
# Usa o WebDriver (importado do webdriver.py).
# Abre a página do ativo desejado.
# Coleta os dados relevantes da página.

import re
from selenium.webdriver.common.by import By
from .webdriver import iniciar_navegador
from .database import salvar_ativo
from diversify.scrapping.urls import profile_yahoo

def extrair_dados(ativo):
    """Acessa a URL e retorna o título da página."""
    url = profile_yahoo(ativo)
    driver = iniciar_navegador()
    driver.get(url)

    try: 
        nome_acao = driver.find_element(By.XPATH, '/html/body/div[2]/main/section/section/section/article/section[1]/div[1]/div/div/section/h1').text 
        descricao = driver.find_element(By.XPATH, '/html/body/div[2]/main/section/section/section/article/section[3]/section[1]/p').text
        website = driver.find_element(By.XPATH, '/html/body/div[2]/main/section/section/section/article/section[2]/section[2]/div/div/a[2]').text

        dados = {
            "ticker": ativo,
            "nome": limpar_nome_empresa(nome_acao),
            "descricao": descricao,
            "website": website
        }

        salvar_ativo(dados)
        print(f"Dados de {ativo} salvos com sucesso!")

    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
        dados = None

    driver.quit()
    return dados

def limpar_nome_empresa(nome):
    """Remove 'S.A.', 'S/A' e outras informações extras do nome da empresa."""
    nome = re.sub(r"\bS\.?A\b", "", nome, flags=re.IGNORECASE).strip()  # Remove 'S.A.' ou 'SA'
    nome = re.split(r"[\(\.]", nome)[0].strip()  # Corta no primeiro '(' ou '.'
    return nome

def pegar_links(url):
    """Acessa a URL e retorna todos os links da página."""
    driver = iniciar_navegador()
    driver.get(url)

    # Espera até que o conteúdo da página seja carregado (espera por qualquer elemento na página)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

    # Pega todos os links presentes na página
    links = driver.find_elements(By.TAG_NAME, "a")
    urls = [link.get_attribute("href") for link in links if link.get_attribute("href") is not None]

    driver.quit()
    return urls

def salvar_dados_ativo(nome, descricao, url):
    """Salva os dados do ativo (nome, descrição, links) no banco de dados."""
    salvar_ativo(nome, descricao)
    ativo_id = obter_id_ativo(nome)  # Função para pegar o ID do ativo inserido
    links = pegar_links(url)
    salvar_links(ativo_id, links)

def obter_id_ativo(nome):
    """Obtém o ID de um ativo pelo nome (após inserção)."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM ativos WHERE nome = ?''', (nome,))
    ativo_id = cursor.fetchone()[0]
    conn.close()
    return ativo_id

