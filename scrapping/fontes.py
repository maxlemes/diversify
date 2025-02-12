
# Dicionário com URLs e XPaths
FONTES = {
    "dre": {  # DRE - Tradingview
        "url": 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-income-statement/?statements-period=FY',
        "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]'
    },
    "bp": {  # Balanço Patrimonial - Tradingview
        "url": 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-balance-sheet/?statements-period=FY',
        "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]'
    },
    "fc": {  # Fluxo de Caixa - Tradingview
        "url": 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-cash-flow/?statements-period=FY',
        "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]'
    },
    "stats": {  # Indicadores - Tradingview
        "url": 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-statistics-and-ratios/?statistics-period=FY',
        "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]'
    },
    "divs": {  # Dividendos - Tradingview
        "url": 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-dividends',
        "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]'
    },
    "ests": {  # Estimativas - Tradingview
        "url": 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-earnings/?earnings-period=FY&revenues-period=FY',
        "xpath": '/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]'
    },
    "perfil_moneytimes": {  # Perfil - Moneytimes
        "url": 'https://www.moneytimes.com.br/cotacao/{}/',
        "xpath": 'XPATH_DO_PERFIL_MONEYTIMES'  # Substitua com o XPath correto
    },
    "perfil_yahoo": {  # Perfil - Yahoo Finance
        "url": 'https://finance.yahoo.com/quote/{}.SA/profile/',
        "xpath": 'XPATH_DO_PERFIL_YAHOO'  # Substitua com o XPath correto
    }
}

