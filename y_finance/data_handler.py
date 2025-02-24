import json
from pathlib import Path

import pandas as pd

from database.db_manager import DatabaseManager
from y_finance.yfinance_collector import YFinanceCollector


class DataHandler:
    def __init__(self, db_manager):
        """
        Initializes the DataHandler with a database connection.

        :param db_connection: Database connection object.
        """
        self.db_connection = db_manager

    # -----------------------  Display methods -------------------------------------

    def dict_tuples(self, input_dict):
        """
        Transforms a dictionary into a list of two tuples: one with keys and the other with values.

        Parameters:
        - input_dict (dict): The dictionary to be transformed.

        Returns:
        - list: A list containing two tuples: one with the keys and another with the values.
        """
        # Create a tuple for keys and another for values
        keys_tuple = tuple(input_dict.keys())
        values_tuple = tuple(input_dict.values())

        # Return the two tuples in a list
        return [keys_tuple, values_tuple]

    def process_stock_prices(self, profile_id, stock_data):
        """
        Process the raw stock price data.
        :param stock_data: Raw data collected from Yahoo Finance
        :return: Processed stock price data in a list of tuples
        """
        # Format the index as a date (without time)
        # stock_data.index = stock_data.index.date

        # Clean the data (removing NaNs, etc.)
        cleaned_data = self.clean_data(stock_data)

        # Convert to a list of tuples with (date, open_price, close_price)
        processed_data = self.convert_to_tuples(cleaned_data)

        # add profile_id and ticker
        modified_data = []
        for entry in processed_data:
            modified_data.append((profile_id,) + entry)

        columns = [
            (
                "profile_id",
                "date",
                "open",
                "high",
                "low",
                "close",
                "adj_close",
                "volume",
            )
        ]

        modified_data = columns + modified_data
        # print(processed_data)

        return modified_data

    def clean_data(self, stock_data):
        """
        Clean the stock data, ensuring no NaN values and formatting the index.
        :param stock_data: Raw stock price data
        :return: Cleaned stock price data
        """
        # Format the index as a date (without time)
        stock_data.index = stock_data.index.date

        # Remove rows with NaN values
        cleaned_data = stock_data.iloc[:, :6]

        return cleaned_data

    def convert_to_tuples(self, stock_data):
        """
        Convert the DataFrame to a list of tuples (date, open_price, close_price).
        :param stock_data: Cleaned stock price data
        :return: List of tuples
        """
        # Format the index as a date (without time)
        # Passo 2: Converter os dados para uma lista de tuplas
        stock_data_tuples = [
            tuple([str(index)] + row.tolist()) for index, row in stock_data.iterrows()
        ]

        return stock_data_tuples


# ------------------- TEST ---------------------------------------------------------
if __name__ == "__main__":
    path = Path("data/files.json")  # ------------------------------------------------
    # Load the JSON file containing paths to the database and tables
    with open(path, "r") as f:
        files = json.load(f)
    # Define paths for the database and tables
    db_path = Path(files["database"])
    with DatabaseManager(db_path) as db:
        handler = DataHandler(db)
        ticker = "WEGE3"
        collector = YFinanceCollector(ticker)

        raw_data = collector.fetch_company_profile()  # Coletando dados
        proc_data = handler.dict_tuples(raw_data)  # Processando dados
        db.insert_data(
            "profile", proc_data[0], proc_data[1:]
        )  # Armazenando dados no banco de dados

        profile_id = db.fetch_profile_id(ticker)  # coletando o profile_id
        raw_data = collector.fetch_stock_prices()  # Coletando dados
        proc_data = handler.process_stock_prices(
            profile_id, raw_data
        )  # Processando dados
        db.insert_data(
            "quotes", proc_data[0], proc_data[1:]
        )  # Armazenando dados no banco de dados
