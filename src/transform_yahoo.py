import json
import os
import pickle

from diversify import Transformer


def transform():
    # Initialize the Transformer instance
    transformer = Transformer()

    # Load company profile data from JSON --------------------------
    with open("tmp/profile.json", "r") as f:
        data = json.load(f)

    # Convert dictionary to tuples
    data = transformer.dict_to_tuples(data)

    # Save transformed profile data as Pickle
    with open("tmp/profile.pkl", "wb") as f:
        pickle.dump(data, f)

    # Load stock price data from Pickle ----------------------------
    with open("tmp/quotes.pkl", "rb") as f:
        data = pickle.load(f)

    # process stock prices
    data = transformer.process_stock_prices(data)

    # Save transformed stock prices
    with open("tmp/quotes_t.pkl", "wb") as f:
        pickle.dump(data, f)

    # Define financial statements to process -----------------------
    balance_types = ["income_stmt", "balance_sheet", "cash_flow"]

    for balance_type in balance_types:
        # Load financial statement data
        with open(f"tmp/{balance_type}.pkl", "rb") as f:
            data = pickle.load(f)

        # Process balance data
        data = transformer.process_balance(balance_type, data)

        # Load quarterly financial data
        with open(f"tmp/quarterly_{balance_type}.pkl", "rb") as f:
            q_data = pickle.load(f)

        # Process TTM (Trailing Twelve Months) data
        q_data = transformer.process_balance_ttm(balance_type, q_data)

        # Merge TTM data if the first elements match
        if data[0] == q_data[0]:
            data = tuple([data[0]] + [q_data[1]] + data[1:])

        # Save transformed financial data
        with open(f"tmp/{balance_type}_t.pkl", "wb") as f:
            pickle.dump(data, f)

    # Load dividend data --------------------------------------------
    with open("tmp/dividends.pkl", "rb") as f:
        data = pickle.load(f)

    # Process dividend data
    data = transformer.process_dividends(data)

    # Convert to tuple format
    data = tuple(data)

    # Save transformed dividend data
    with open("tmp/dividends_t.pkl", "wb") as f:
        pickle.dump(data, f)
