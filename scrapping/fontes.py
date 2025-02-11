# scrapping/fontes.py


# DRE - Tradingview
def dre_tradingview(ativo):
    base_url = 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-income-statement/?statements-period=FY'
    return base_url.format(ativo)

# Balanço Patrimonial - Tradingview
def bp_tradingview(ativo):
    base_url = 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-balance-sheet/?statements-period=FY'
    return base_url.format(ativo)

# Fluxo de Caixa - Tradingview
def fc_tradingview(ativo):
    base_url = 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-cash-flow/?statements-period=FY'
    return base_url.format(ativo)

# Indicadores - Tradingview
def stats_tradingview(ativo):
    base_url = 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-statistics-and-ratios/?statistics-period=FY'
    return base_url.format(ativo)

# Dividendos - Tradingview
def divs_tradingview(ativo):
    base_url = 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-dividends'
    return base_url.format(ativo)

# Estimativas - Tradingview
def ests_tradingview(ativo):
    base_url = 'https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-earnings/?earnings-period=FY&revenues-period=FY'
    return base_url.format(ativo)

# Perfil - Moneytimes
def perfil_moneytimes(ativo):
    base_url = 'https://www.moneytimes.com.br/cotacao/{}/'
    return base_url.format(ativo)

# Perfil - Yahoo Finance
def perfil_yahoo(ativo):
    base_url = 'https://finance.yahoo.com/quote/{}.SA/profile/'
    return base_url.format(ativo)
