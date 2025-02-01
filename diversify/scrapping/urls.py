# urls.py

def eps_tradingview(ativo):
    base_url = "https://br.tradingview.com/symbols/BMFBOVESPA-{}/financials-income-statement/?statements-period=FY"
    return base_url.format(ativo)

def descricao_moneytimes(ativo):
    base_url = "https://www.moneytimes.com.br/cotacao/{}/"
    return base_url.format(ativo)

def profile_yahoo(ativo):
    base_url = "https://finance.yahoo.com/quote/{}.SA/profile/"
    return base_url.format(ativo)

