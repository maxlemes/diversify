import pickle

from diversify import DatabaseManager, Refiner


def load_data(ticker):
    # Initialize the DatabaseManager to manage database operations
    with DatabaseManager("data/database.db") as db:

        refiner = Refiner()

        # Fetch the profile_id using the ticker from the database
        profile_id = db.fetch_profile_id(ticker)

        # Define financial statement types to process (e.g., Income Statement, Balance Sheet, Cash Flow)
        # ---------------------------------------------------------------
        balance_types = ["income_stmt", "balance_sheet", "cash_flow"]

        # Process each financial statement type
        for balance_type in balance_types:
            # Load the respective financial statement data from Pickle
            with open(f"tmp/{balance_type}_t.pkl", "rb") as f:
                data = pickle.load(f)

            # Add profile_id to the financial statement data and update the database
            data = refiner.add_profile_id(profile_id, data)
            db.update_data(balance_type, data[0], data[1:])
