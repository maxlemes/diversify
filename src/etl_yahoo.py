from src.extract_yahoo import extract
from src.transform_yahoo import transform

# from src.load_yahoo import load


def execute_etl(ticker):
    # extract(ticker)
    transform()
    # load()


if __name__ == "__main__":
    ticker = "WEGE3"
    execute_etl(ticker)
