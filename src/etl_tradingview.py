from src.extract_tradingview import collect
from src.load_tradingview import load_data
from src.transform_tradingview import refine


def execute_etl(ticker):
    collect(ticker)
    refine()
    load_data(ticker)


if __name__ == "__main__":
    tickers = [
        "BBAS3",
        "EZTC3",
    ]  # , "FESA4", "KLBN4", "LEVE3", "SIMH3", "SLCE3", "TUPY3"]

    for ticker in tickers:
        print(f"Processing ticker: {ticker}")
        execute_etl(ticker)
