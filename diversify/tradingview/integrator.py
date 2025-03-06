import time

from etl_tradinview.collector import Collector
from etl_tradinview.dataloader import DataLoader
from etl_tradinview.refiner import Refiner


class ETLIntegrator:
    def __init__(self, database, ticker, scraper):
        self.db = database
        self.ticker = ticker
        self.collector = Collector(self.ticker, scraper)
        self.refiner = Refiner()
        if self.db.fetch_profile_id(self.ticker):
            self.profile_id = self.db.fetch_profile_id(self.ticker)
            self.loader = DataLoader(self.db, self.profile_id)
        else:
            self.profile_id = None
            self.loader = None
            print(f"{self.ticker} ainda não está cadastrada")

    def add_balances(self):
        balance_types = ["income_stmt", "balance_sheet", "cash_flow"]
        for balance_type in balance_types:
            data = self.collector.balance(balance_type)
            data = self.refiner.balance(data, balance_type)

            data = self.refiner.add_profile_id(self.profile_id, data)
            # print(data)
            self.db.update_data(balance_type, data[0], data[1:])


# ------------------- TEST ---------------------------------------------------------
if __name__ == "__main__":
    import json
    import time
    from pathlib import Path

    from etl_tradinview.scraper import Scraper

    from diversify.database.manager import DatabaseManager

    path = Path("data/files.json")  # ----------------------------------------------
    # Load the JSON file containing paths to the database and tables
    with open(path, "r") as f:
        files = json.load(f)
    # Define paths for the database and tables
    db_path = Path(files["database"])

    with DatabaseManager(db_path) as database:

        scraper = Scraper()
        tickers = ["EGIE3"]  # , "WEGE3"]

        for ticker in tickers:
            print(f"Processando ticker: {ticker}")
            etl = ETLIntegrator(database, ticker, scraper)

            try:
                etl.add_balances()
            except Exception as e:
                print(f"Erro ao processar {ticker}: {e}")

        scraper.close_browser()
