from scrapping.scraper import pegar_titulo, pegar_links

url = "https://br.tradingview.com/symbols/BMFBOVESPA-FESA4/financials-income-statement/?statements-period=FY"
print("Título da página:", pegar_titulo(url))
print("Links na página:", pegar_links(url))

