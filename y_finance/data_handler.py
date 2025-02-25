import datetime as dt
import json
import logging
from pathlib import Path

import pandas as pd

from database.db_manager import DatabaseManager
from y_finance.sql_finder import SQLFinder
from y_finance.yfinance_collector import YFinanceCollector


class DataHandler:
    def __init__(self, db_manager):
        """
        Initializes the DataHandler with a database connection.

        :param db_connection: Database connection object.
        """
        self.db_connection = db_manager
        # Load filters from filters.json
        self.filters = self._load_filters()

    # -----------------------  Display methods -------------------------------------

    def add_profile_id(self, profile_id, data):
        """
        Adds a 'profile_id' as the first element of each entry in the given data.

        Parameters:
        - profile_id: The ID to be added to each row of data.
        - data: A list of tuples, where the first tuple contains column headers,
                and the following tuples contain data entries.

        Returns:
        - A new list of tuples with 'profile_id' added as the first element in each row.
        """

        # Initialize a new list to store the modified data
        modified_data = []

        # Add 'profile_id' as a column header
        modified_data.append(("profile_id",) + data[0])

        # Iterate through the remaining rows and prepend the profile_id to each entry
        for entry in data[1:]:
            modified_data.append((profile_id,) + entry)

        # Return the modified list of tuples
        return modified_data

    def process_stock_prices(self, data):
        """
        Processes raw stock price data by cleaning, converting to tuples, and adding column headers.

        :param data: Raw data collected from Yahoo Finance as a DataFrame.
        :return: A list of tuples containing processed stock price data,
                including column headers.
        """

        # Clean the data (remove NaN values and format the index as date)
        data.index = data.index.date  # Format index as date (without time)
        data_cleaned = data.iloc[
            :, :6
        ]  # Keep only the first 6 columns (date, open, high, low, close, volume)

        # Convert cleaned DataFrame into a list of tuples
        processed_data = self.dataframe_to_tuples(data_cleaned)

        # Define column headers
        columns = [("date", "open", "high", "low", "close", "adj_close", "volume")]

        # Combine headers with processed data
        modified_data = columns + processed_data

        return modified_data

    def process_balance(self, balance_type, data):
        """
        Processes raw income statement data by cleaning and formatting it.

        :param data: Raw income statement data as a DataFrame.
        :return: A list of tuples containing processed data, including headers.
        """

        # Convert column names to years
        data.columns = [pd.to_datetime(col).year for col in data.columns]

        # Transpose the data (flip rows and columns)
        data = data.T

        # Filter and rename columns based on the income statement filter
        filtered_columns = [
            col for col in data.columns if col in self.filters[balance_type]
        ]
        data = data[filtered_columns].rename(columns=self.filters[balance_type])

        # Convert DataFrame to a list of tuples and add 'year' as the first column
        processed_data = self.dataframe_to_tuples(data)
        columns = tuple(["year"] + list(data.columns))

        # Add header and return the final data
        return [columns] + processed_data

    def process_balance_ttm(self, balance_type, data):
        """
        Processes raw balance sheet or income statement data by cleaning and formatting it.

        :param balance_type: Type of balance data, either "balance_sheet" or another type.
        :param data: Raw financial data as a DataFrame.
        :return: A list of tuples containing processed data, including headers.
        """

        # Calculate 'ttm' (Trailing Twelve Months) based on balance type
        if balance_type != "balance_sheet":
            # For income statement data, sum the last four quarters
            data["ttm"] = data.iloc[:, :4].sum(axis=1)
        else:
            # For balance sheet data, take the average of the last four quarters
            data["ttm"] = data.iloc[:, :4].mean(axis=1)

        # Transpose the DataFrame to switch rows and columns
        data = data.T

        # Keep only the 'ttm' row to focus on the processed values
        data = data[data.index == "ttm"]

        # Filter columns to include only those specified in self.filters[balance_type]
        filtered_columns = [
            col for col in data.columns if col in self.filters[balance_type]
        ]
        data = data[filtered_columns].rename(columns=self.filters[balance_type])

        # Convert the cleaned DataFrame to a list of tuples
        processed_data = self.dataframe_to_tuples(data)

        # Create column headers, adding 'year' as the first column
        columns = tuple(["year"] + list(data.columns))

        # Return the final structured data with headers
        return [columns] + processed_data

    def process_dividends(self, data):
        """
        Processes raw dividend data by aggregating it yearly and formatting it.

        :param data: A pandas Series with dates as the index and dividends as values.
        :return: A list of tuples containing processed dividend data, including headers.
        """

        # Group the data by year and sum the dividends for each year
        data = data.groupby(data.index.year).sum()

        # Convert the Series into a list of tuples (year, total dividends)
        modified_data = [(index, value) for index, value in data.items()]

        # Define column headers
        columns = [("year", "dividends")]

        # Return the headers followed by the processed dividend data
        return columns + modified_data

    def estimated_eps(self, data, years):
        """
        Processes raw dividend data by aggregating it yearly and formatting it.

        :param data: A pandas Series with dates as the index and dividends as values.
        :return: A list of tuples containing processed dividend data, including headers.
        """

        # Define years
        current_year = years[0]
        next_year = years[1]

        list_data = [
            (current_year, float(data.loc["0y", "avg"])),
            (next_year, float(data.loc["+1y", "avg"])),
        ]

        # Return the headers followed by the processed dividend data
        return [("year", "eps")] + list_data

    def payout_estimate(self, data, years):
        """
        Processes raw dividend data by aggregating it yearly and formatting it.

        :param data: A pandas Series with dates as the index and dividends as values.
        :return: A list of tuples containing processed dividend data, including headers.
        """

        # define years
        current_year = years[0]
        next_year = years[1]

        list_data = [
            (current_year, float(data.loc["0y", "avg"])),
            (next_year, float(data.loc["+1y", "avg"])),
        ]

        # Return the headers followed by the processed dividend data
        return [("year", "eps")] + list_data

    def estimated_years(self, years):
        filtered_years = [year for year in years if year != "ttm"]
        max_year = max(filtered_years)
        current_year = int(max_year) + 1
        next_year = current_year + 1
        return [current_year, next_year]

    # -----------------------  Setup methods ---------------------------------------

    def dict_to_tuples(self, input_dict):
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

    def dataframe_to_tuples(self, data):
        """
        Convert the DataFrame to a list of tuples (date, open_price, close_price).
        :param data: Cleaned stock price data
        :return: List of tuples
        """
        # Format the index as a date (without time)
        # Passo 2: Converter os dados para uma lista de tuplas
        data_tuples = [
            tuple([str(index)] + row.tolist()) for index, row in data.iterrows()
        ]

        return data_tuples

    def _load_filters(self):
        """
        Loads filter definitions from filters.json to select relevant financial metrics.
        """
        try:
            with open("data/filters.json", "r") as f:
                filters = json.load(f)
            return filters
        except Exception as e:
            logging.error(f"Error loading filters from filters.json: {e}")
            return {}


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
        finder = SQLFinder(db)

        # raw_data = collector.fetch_company_profile()  # Coletando dados
        # proc_data = handler.dict_to_tuples(raw_data)  # Processando dados
        # db.insert_data(
        #     "profile", proc_data[0], proc_data[1:]
        # )  # Armazenando dados no banco de dados

        profile_id = db.fetch_profile_id(ticker)  # coletando o profile_id

        # raw_data = collector.fetch_stock_prices()  # Coletando dados
        # proc_data = handler.process_stock_prices(raw_data)  # Processando dados
        # proc_data = handler.add_profile_id(profile_id, proc_data)
        # print(proc_data[:3])
        # db.insert_data(
        #     "quotes", proc_data[0], proc_data[1:]
        # )  # Armazenando dados no banco de dados

        # balance_types = ["income_stmt", "balance_sheet", "cash_flow"]
        # for balance_type in balance_types:
        #     raw_data = collector.fetch_data(balance_type)  # Coletando dados
        #     proc_data = handler.process_balance(
        #         balance_type, raw_data
        #     )  # Processando dados
        #     proc_data = handler.add_profile_id(profile_id, proc_data)
        #     print(proc_data[:3])
        #     db.insert_data(
        #         balance_type, proc_data[0], proc_data[1:]
        #     )  # Armazenando dados no banco de dados

        #     # ------------ TTM ------------------------

        #     quarterly_balance = "quarterly_" + balance_type
        #     raw_data = collector.fetch_data(quarterly_balance)  # Coletando dados
        #     proc_data = handler.process_balance_ttm(
        #         balance_type, raw_data
        #     )  # Processando dados
        #     proc_data = handler.add_profile_id(profile_id, proc_data)
        #     print(proc_data[:3])
        #     db.update_data(
        #         balance_type, proc_data[0], proc_data[1:]
        #     )  # Armazenando dados no banco de dados

        # raw_data = collector.fetch_data("dividends")
        # proc_data = handler.process_dividends(raw_data)
        # proc_data = handler.add_profile_id(profile_id, proc_data)
        # print(proc_data[:3])
        # db.update_data(
        #     "ests", proc_data[0], proc_data[1:]
        # )  # Armazenando dados no banco de dados

        # add roe to 'ests'
        raw_data = finder.fetch_roe(profile_id)
        # print(raw_data)

        # add eps to 'ests'
        raw_data = finder.fetch_eps(profile_id)
        # print(raw_data)

        # add payout to 'ests'
        finder.fetch_payout(profile_id)
        # print(raw_data)

        # add estimated eps to 'ests'
        raw_data = collector.fetch_data("earnings_estimate")
        years = db.query_table("income_stmt", "year")
        estimated_years = handler.estimated_years(years)
        raw_data = handler.estimated_eps(raw_data, estimated_years)
        proc_data = handler.add_profile_id(profile_id, raw_data)
        db.update_data("ests", proc_data[0], proc_data[1:])

        # add current_payout
        current_year = estimated_years[0]
        proc_data = finder.current_payout(profile_id, current_year)

        # add estimated_payout
        next_year = estimated_years[1]
        proc_data = finder.estimated_payout(profile_id, next_year)

        # add estimated_dividends
        next_year = estimated_years[1]
        proc_data = finder.estimated_dividends(profile_id, next_year)

        # print(proc_data)
