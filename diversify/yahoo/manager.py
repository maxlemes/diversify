import time

from diversify.yahoo.extractor import Extractor
from diversify.yahoo.loader import SQLLoader
from diversify.yahoo.transformer import Transformer


class ETLManager:
    def __init__(self, database, ticker):
        self.db = database
        self.ticker = ticker
        self.extractor = Extractor(self.ticker)
        self.transformer = Transformer()
        if self.db.fetch_profile_id(self.ticker):
            self.profile_id = self.db.fetch_profile_id(self.ticker)
            self.loader = SQLLoader(self.db, self.profile_id)
        else:
            self.profile_id = None
            self.loader = None
            print(f"{self.ticker} ainda não está cadastrada")

    def add_perfil(self):
        """Add perfil to database"""

        data = self.extractor.fetch_company_profile()
        data = self.transformer.dict_to_tuples(data)
        self.db.insert_data("profile", data[0], data[1:])
        self.profile_id = self.db.fetch_profile_id(self.ticker)
        self.loader = SQLLoader(self.db, self.profile_id)

    def add_quotes(self):
        """Add quotes to database"""

        data = self.extractor.fetch_stock_prices()
        data = self.transformer.process_stock_prices(data)
        data = self.transformer.add_profile_id(self.profile_id, data)
        self.db.insert_data("quotes", data[0], data[1:])

    def add_balances(self):
        """Add balances to database"""

        balance_types = ["income_stmt", "balance_sheet", "cash_flow"]
        for balance_type in balance_types:

            # ------------ YEARLY ------------------------
            data = self.extractor.fetch_data(balance_type)
            data = self.transformer.process_balance(balance_type, data)
            data = self.transformer.add_profile_id(self.profile_id, data)
            self.db.insert_data(balance_type, data[0], data[1:])

            if balance_type != "balance_sheet":

                # ------------ TTM ------------------------
                quarterly_balance = "quarterly_" + balance_type
                data = self.extractor.fetch_data(quarterly_balance)
                data = self.transformer.process_balance_ttm(balance_type, data)
                data = self.transformer.add_profile_id(self.profile_id, data)
                self.db.update_data(balance_type, data[0], data[1:])

    def add_drep(self):
        """Add Dividends, Roe, Eps and Payout to database"""

        # add dividends to database
        data = self.extractor.fetch_data("dividends")
        data = self.transformer.process_dividends(data)

        results = self.db.get_data("income_stmt", profile_id=self.profile_id)
        years = [result["year"] for result in results if result["year"] != "ttm"]

        data = [data[0]] + [item for item in data[1:] if str(item[0]) in years]
        data = self.transformer.add_profile_id(self.profile_id, data)
        self.db.update_data("ests", data[0], data[1:])

        # add roe to database
        self.loader.fetch_roe()

        # add eps to database
        self.loader.fetch_eps()

        # add payout to database
        self.loader.fetch_payout()

    def add_estimates(self):
        """Add estimates to eps, payout and dividends in database"""

        # add estimated eps to database
        data = self.extractor.fetch_data("earnings_estimate")
        results = self.db.get_data("income_stmt", profile_id=self.profile_id)

        years = [result["year"] for result in results]
        years = self.transformer.estimated_years(years)

        data = self.transformer.estimated_eps(data, years)
        data = self.transformer.add_profile_id(self.profile_id, data)
        self.db.update_data("ests", data[0], data[1:])

        # add estimated_payout to database
        for year in years:
            self.loader.estimated_payout(year)
            self.loader.estimated_roe(year)

        # add estimated_dividends to database
        for year in years:
            self.loader.estimated_dividends(year)
            self.loader.estimated_roe(year)

        # add missing dividends
        self.loader.missing_dividends()

        # add payout returns
        self.loader.payout_returns()

    def teste(self):
        # add estimated eps to database
        data = self.extractor.fetch_data("earnings_estimate")
        results = self.db.get_data("income_stmt", profile_id=self.profile_id)
        years = [result["year"] for result in results]

        results = self.db.get_data("ests", profile_id=self.profile_id)
        results = [result for result in results if result["year"] in years]

        for result in results:
            print([result["year"], result["payout"]])

        years = self.transformer.estimated_years(years)

        print(years)


if __name__ == "__main__":
    import json
    from pathlib import Path

    from database.manager import DatabaseManager

    path = Path("data/files.json")  # ----------------------------------------------
    # Load the JSON file containing paths to the database and tables
    with open(path, "r") as f:
        files = json.load(f)
    # Define paths for the database and tables
    db_path = Path(files["database"])

    with DatabaseManager(db_path) as database:

        tickers = ["WEGE3", "EGIE3"]
        for ticker in tickers:
            print(f"Processando ticker: {ticker}")
            etl = ETLManager(database, ticker)

            etl.add_perfil()
            etl.add_balances()
            etl.add_quotes()

            etl.add_drep()
            etl.add_estimates()
