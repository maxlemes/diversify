import json
import os

from diversify import Extractor


def extract(ticker):
    extractor = Extractor(ticker)  # Initialize the Extractor for the given ticker

    # Fetch and save company profile as JSON
    data = extractor.fetch_company_profile()
    with open("tmp/profile.json", "w") as f:
        json.dump(data, f, indent=4)

    # Fetch and save profile_id as a Pickle file
    # df = db.fetch_profile_id(ticker)
    # df.to_pickle("tmp/profile_id.pkl")

    # Fetch and save stock prices as a Pickle file
    df = extractor.fetch_stock_prices()
    df.to_pickle("tmp/quotes.pkl")

    # List of financial data types to download
    financials_data = [
        "income_stmt",
        "balance_sheet",
        "cash_flow",
        "quarterly_income_stmt",
        "quarterly_balance_sheet",
        "quarterly_cash_flow",
        "dividends",
        "earnings_estimate",
    ]

    # Fetch and save each data type as a Pickle file
    for item in financials_data:
        df = extractor.fetch_data(item)
        df.to_pickle(f"tmp/{item}.pkl")


def dict_to_json(dict, name):
    # Get the absolute path of the current script (this file)
    # os.path.abspath(__file__) returns the full path of the current file.
    # os.path.dirname(__file__) gives the directory of the current file.
    # os.path.dirname(os.path.dirname(__file__)) moves up two levels to get to the parent folder.
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Define the path for the 'tmp' directory, which will be created in the parent folder of 'src'.
    tmp_dir = os.path.join(project_dir, "tmp")

    # Define the full file path where the data will be saved (profile.json inside the 'tmp' directory).
    file_path = os.path.join(tmp_dir, f"{name}.json")

    # Create the 'tmp' directory if it doesn't exist, using 'exist_ok=True' to avoid errors if it already exists.
    os.makedirs(tmp_dir, exist_ok=True)

    # Open the file in write mode ('w'), and dump the 'data' dictionary into the file in JSON format.
    with open(file_path, "w") as f:
        # Use json.dump() to convert the 'data' dictionary into a JSON string and save it to the file.
        json.dump(dict, f)
