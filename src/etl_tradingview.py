from src.extract_tradingview import extract
from src.load_tradingview import load
from src.transform_tradingview import transform


def execute_etl():
    extract()
    transform()
    load()


if __name__ == "__main__":
    execute_etl()
