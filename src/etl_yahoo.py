from src.extract_yahoo import extract
from src.load_yahoo import load
from src.transform_yahoo import transform


def execute_etl(ticker):
    extract(ticker)
    transform()
    load(ticker)


if __name__ == "__main__":
    tickers = ["BBAS3", "EZTC3", "FESA4", "KLBN4", "LEVE3", "SIMH3", "SLCE3", "TUPY3"]

    for ticker in tickers:
        print(f"Processing ticker: {ticker}")
        execute_etl(ticker)
