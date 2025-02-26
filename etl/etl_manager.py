import time


class ETLManager:
    def __init__(self, database, extractor, transformer, loader):
        self.db = database
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.profile = None

    def add_perfil(self):
        """Add perfil to database"""

        data = self.extractor.fetch_company_profile()
        data = self.transformer.dict_to_tuples(data)
        self.db.insert_data("profile", data[0], data[1:])
        self.profile_id = db.fetch_profile_id(ticker)

    def add_quotes(self):
        """Add quotes to database"""

        data = extractor.fetch_stock_prices()
        data = transformer.process_stock_prices(data)
        data = transformer.add_profile_id(self.profile_id, data)
        self.db.insert_data("quotes", data[0], data[1:])

    def add_balances(self):
        """Add balances to database"""

        balance_types = ["income_stmt", "balance_sheet", "cash_flow"]
        for balance_type in balance_types:

            # ------------ YEARLY ------------------------
            data = extractor.fetch_data(balance_type)
            data = transformer.process_balance(balance_type, data)
            data = transformer.add_profile_id(self.profile_id, data)
            self.db.insert_data(balance_type, data[0], data[1:])

            # ------------ TTM ------------------------
            quarterly_balance = "quarterly_" + balance_type
            data = extractor.fetch_data(quarterly_balance)
            data = transformer.process_balance_ttm(balance_type, data)
            data = transformer.add_profile_id(self.profile_id, data)
            self.db.update_data(balance_type, data[0], data[1:])

    def add_drep(self):
        """Add Dividends, Roe, Eps and Payout to database"""

        # add dividends to database
        data = extractor.fetch_data("dividends")
        data = transformer.process_dividends(data)
        data = transformer.add_profile_id(self.profile_id, data)
        self.db.update_data("ests", data[0], data[1:])

        # add roe to database
        loader.fetch_roe()

        # add eps to database
        loader.fetch_eps()

        # add payout to database
        loader.fetch_payout()

    def add_estimates(self):
        """Add estimates to eps, payout and dividends in database"""

        # add estimated eps to database
        data = extractor.fetch_data("earnings_estimate")
        years = db.query_table("income_stmt", "year")
        years = transformer.estimated_years(years)
        data = transformer.estimated_eps(data, years)
        data = transformer.add_profile_id(self.profile_id, data)
        self.db.update_data("ests", data[0], data[1:])

        # add current_payout to database
        current_year = years[0]
        data = loader.current_payout(current_year)

        # add estimated_payout to database
        next_year = years[1]
        data = loader.estimated_payout(next_year)

        # add estimated_dividends to database
        data = loader.estimated_dividends(next_year)


if __name__ == "__main__":
    import json
    from pathlib import Path

    from database.db_manager import DatabaseManager
    from etl.extractor import Extractor
    from etl.loader import SQLLoader
    from etl.transformer import Transformer

    path = Path("data/files.json")  # ----------------------------------------------
    # Load the JSON file containing paths to the database and tables
    with open(path, "r") as f:
        files = json.load(f)
    # Define paths for the database and tables
    db_path = Path(files["database"])

    with DatabaseManager(db_path) as db:

        ticker = "WEGE3"

        extractor = Extractor(ticker)  # Your extraction class
        transformer = Transformer(db)  # Your transformation class
        loader = SQLLoader(db, ticker)  # Your loading class
        etl = ETLManager(db, extractor, transformer, loader)

        etl.add_perfil()
        etl.add_quotes()
        etl.add_balances()
        etl.add_drep()
        etl.add_estimates()
