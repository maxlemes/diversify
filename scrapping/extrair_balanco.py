import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from scrapping.fontes import dre_tradingview, bp_tradingview, fc_tradingview, stats_tradingview, divs_tradingview, ests_tradingview

def extrair_balanco(self, ativo, tipo_balanco):
        """Coleta um balanço financeiro (DRE, Balanço Patrimonial, Fluxo de Caixa) do TradingView."""
        
        # Mapeamento dos balanços para URLs e tabelas
        balancos = {
            "dre": {
                "url": dre_tradingview(ativo),
                "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]'
            },
            "bp": { # Balanço Patrimonial
                "url": bp_tradingview(ativo),
                "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]'
            },
            "fc": { # Fluxo de Caixa
                "url": fc_tradingview(ativo),
                "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]'
            },
            "stats": { # Indicadores
                "url": stats_tradingview(ativo),
                "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]'
            },
            "divs": { # Dividendos
                "url": divs_tradingview(ativo),
                "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]'
            },
            "ests": { # Estimativas
                "url": ests_tradingview(ativo),
                "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]'
            }
        }
        
        if tipo_balanco not in balancos:
            raise ValueError(f"Balanço '{tipo_balanco}' não suportado.")

        # Acessando a URL
        url = balancos[tipo_balanco]["url"]
        xpath_tabela = balancos[tipo_balanco]["xpath"]
        self.driver.get(url)

        # Espera para carregar a página
        time.sleep(10)

        try:
            # Localizar a tabela
            tabela = self.driver.find_element(By.XPATH, xpath_tabela)
            linhas = tabela.find_elements(By.XPATH, "./div")

            # Extrair os dados da tabela
            dados = [[celula.text for celula in linha.find_elements(By.XPATH, "./div")] for linha in linhas]
            return dados

        except (TimeoutException, NoSuchElementException):
            print(f"Erro ao coletar {tipo_balanco} para {ativo}.")
            return None
