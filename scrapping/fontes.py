# Dicionário com URLs e XPaths
FONTES = {
    "cot": {  # Cotacao - Tradingview
        "url": "https://br.tradingview.com/symbols/BMFBOVESPA-{}/",
        "xpath": "/html/body/div[3]/div[4]/div[2]/div[1]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/span[1]",
    },
    "dre": {  # DRE - Tradingview
        "url": "https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-income-statement/?statements-period=FY",
        "xpath": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]",
        "xpath_r": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[2]/div/div/p",
    },
    "bp": {  # Balanço Patrimonial - Tradingview
        "url": "https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-balance-sheet/?statements-period=FY",
        "xpath": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]",
    },
    "fc": {  # Fluxo de Caixa - Tradingview
        "url": "https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-cash-flow/?statements-period=FY",
        "xpath": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]",
    },
    "stats": {  # Indicadores - Tradingview
        "url": "https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-statistics-and-ratios/?statistics-period=FY",
        "xpath": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]",
        "xpath_r": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[2]/div/div/p",
    },
    "divs": {  # Dividendos - Tradingview
        "url": "https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-dividends",
        "xpath": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]",
        "xpath_r": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[2]/div/div/p",
    },
    "ests": {  # Estimativas - Tradingview
        "url": "https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-earnings/?earnings-period=FY&revenues-period=FY",
        "xpath": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]",
        "xpath_r": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[2]/div/div/p",
    },
    "ests_r": {  # Estimativas - Tradingview
        "url": "https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-earnings/?earnings-period=FY&revenues-period=FY",
        "xpath": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[10]/div[2]/div/div[1]",
    },
    "rece": {  # Receitas - Tradingview
        "url": "https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-revenue/",
        "xpath": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[3]/div[3]/div[2]/div/div[1]",
        "xpath_r": "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[2]/div/div/p",
    },
    "perfil_moneytimes": {  # Perfil - Moneytimes
        "url": "https://www.moneytimes.com.br/cotacao/{}/",
        "xpath": "XPATH_DO_PERFIL_MONEYTIMES",  # Substitua com o XPath correto
    },
    "precos": {  # Perfil - Yahoo Finance
        "url": "https://finance.yahoo.com/quote/{}.SA/history/?frequency=1d&period1=1581701433&period2=1739554152",
        "xpath": "/html/body/div[2]/main/section/section/section/article/div[1]/div[3]/table",  # Substitua com o XPath correto
    },
}
