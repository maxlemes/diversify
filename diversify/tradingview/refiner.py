import json
import math
import re

import pandas as pd


class Refiner:
    """Class to refiner data before insert to database"""

    def __init__(self):
        self.data = None

        with open("data/filters.json", "r") as f:
            filters = json.load(f)
            self.filters = filters["tradingview"]

        with open("data/tables.json", "r") as f:
            self.tables = json.load(f)

    def balance(self, data, balance_type):
        """Processes and transforms financial data into a structured format.

        This method performs several key tasks:
        1. It iterates over the rows of financial data, cleaning and formatting the lines by removing empty items, unwanted characters, and splitting multi-line values.
        2. It applies predefined filters to the first item in each line based on specific balance types such as 'income_stmt', 'balance_sheet', and 'cash_flow'.
        3. It separates the main financial values (even indices) and growth rate values (odd indices) for lines that have the maximum length, converting the values into their appropriate numeric formats.
        4. The method returns the processed data in the form of an immutable tuple of tuples, making it easier to work with without risking accidental changes.

        Returns:
            tuple: A tuple of tuples containing the processed and cleaned financial data.
        """

        self.data = data

        # Helper function to clean a line by removing unwanted characters
        def clean_line(line):
            line = [item for item in line if item != ""]  # Remove empty items
            line = [
                re.sub(r"[\u202a\u202c\u202f]", "", item) for item in line
            ]  # Remove specific Unicode characters
            line[1:2] = line[1].split("\n")  # Split line[1] by newline character
            line = [re.sub("—", "", item) for item in line]  # Remove dash characters

            return line

        head = clean_line(data[0])
        head = [item for i, item in enumerate(head) if i % 2 != 0]
        head = ["ttm" if item == "TTM" else item for item in head]

        # Initialize an empty list to store processed data
        data = []

        # Process each row of data starting from the second row
        for i in range(1, len(self.data)):
            line = self.data[i]
            line = clean_line(line)
            data.append(line)

        # Map filters to corresponding balance types if applicable
        if data[0][0] in self.filters[balance_type].keys():
            for line in data:
                line[0] = self.filters[balance_type].get(
                    line[0], line[0]
                )  # Update the line's first item

        # Initialize an auxiliary list to store the final processed data
        aux = []
        line_min_length = min(len(line) for line in data)  # Get the minimum line length
        line_max_length = max(len(line) for line in data)  # Get the maximum line length

        if line_min_length < line_max_length:
            head = head[-(line_min_length - 1) :]
        else:
            head = head[-math.floor(line_min_length / 2) :]

        aux = [tuple(["year"] + head)]

        # Process each line
        for line in data:
            if len(line) == line_max_length:
                # Separate the main values (even indices) and growth rates (odd indices)
                main_values = [line[0]] + [
                    item for i, item in enumerate(line[1:]) if i % 2 == 0
                ]
                main_values[1:] = [
                    self._convert_value(value) for value in main_values[1:]
                ]
                aux.append(tuple(main_values))

                growth_values = ["growth_" + line[0]] + [
                    item for i, item in enumerate(line[1:]) if i % 2 != 0
                ]
                aux.append(tuple(growth_values))
            else:
                # For shorter lines, simply convert the values
                line[1:] = [self._convert_value(value) for value in line[1:]]
                aux.append(tuple(line))

        # Convert the final data to a tuple of tuples
        data = tuple(aux)

        data = tuple(t for t in data if t[0] in self.tables[balance_type].keys())

        data = tuple(zip(*data))

        # Output the final data
        return data

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

        self.data = data

        # Add ('profile_id', ) to the first tuple and (profile_id,) to the others
        data = (
            ("profile_id",) + data[0],  # Add ('profile_id',) to the first tuple
        ) + tuple(
            (tuple([profile_id] + list(t))) for t in data[1:]
        )  # Add (profile_id,) to the others

        # Return the modified list of tuples
        return data

    # -----------------------  Setup methods -------------------------------------------
    @staticmethod
    def _convert_value(value):
        """
        Converts monetary values in strings to numbers:
        - 'T' (trillion) → multiplies by 1e12
        - 'B' (billion) → multiplies by 1e9
        - 'M' (million) → multiplies by 1e6
        - 'K' (thousand) → multiplies by 1e3

        Parameters:
            value (str): The value to be converted.

        Returns:
            float: The converted value as a number.
        """
        if isinstance(value, str):  # Ensures that it's a string
            value = value.replace(",", ".")  # Replace comma with a dot
            value = value.replace(
                ".", "", value.count(".") - 1
            )  # Remove '.' except for the last one
            value = value.replace("−", "-")  # Fix Unicode minus (U+2212)
            value = value.replace("%", "")  # Remove percentage symbols

            if value.endswith("T"):
                return float(value[:-1]) * 1e12
            elif value.endswith("B"):
                return float(value[:-1]) * 1e9
            elif value.endswith("M"):
                return float(value[:-1]) * 1e6
            elif value.endswith("K"):
                return float(value[:-1]) * 1e3
        return (
            float(value) if value else None
        )  # Return as it is if not a convertible string


# ------------------- TEST ---------------------------------------------------------
if __name__ == "__main__":
    from etl_tradinview.dados_teste import DADOS_TESTE

    data = DADOS_TESTE["dre"]
    refiner = Refiner()
    balance_type = "income_stmt"
    refiner.balance(data, balance_type)
    # print(data)
