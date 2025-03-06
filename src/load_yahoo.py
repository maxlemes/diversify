import pickle

from diversify import DatabaseManager, SQLLoader, Transformer


def load(ticker):
    # Initialize the DatabaseManager to manage database operations
    with DatabaseManager("data/database.db") as db:

        # Initialize Transformer instance to handle data transformations
        transformer = Transformer()

        # Load profile data from Pickle and insert it into the database
        # --------------------------------------------------------------
        with open("tmp/profile.pkl", "rb") as f:
            data = pickle.load(f)

        # Insert the first element of the data as the profile into the database
        db.insert_data("profile", data[0], data[1:])

        # Fetch the profile_id using the ticker from the database
        profile_id = db.fetch_profile_id(ticker)

        # Load quotes data from Pickle and insert it into the database
        # ------------------------------------------------------------
        with open("tmp/quotes_t.pkl", "rb") as f:
            data = pickle.load(f)

        # Add profile_id to the quotes data and print it
        data = transformer.add_profile_id(profile_id, data)

        # Insert quotes data into the database
        db.insert_data("quotes", data[0], data[1:])

        # Define financial statement types to process (e.g., Income Statement, Balance Sheet, Cash Flow)
        # ---------------------------------------------------------------
        balance_types = ["income_stmt", "balance_sheet", "cash_flow"]

        # Process each financial statement type
        for balance_type in balance_types:
            # Load the respective financial statement data from Pickle
            with open(f"tmp/{balance_type}_t.pkl", "rb") as f:
                data = pickle.load(f)

            # Add profile_id to the financial statement data and update the database
            data = transformer.add_profile_id(profile_id, data)
            db.update_data(balance_type, data[0], data[1:])

        # Load dividends data from Pickle and process it
        # ------------------------------------------------
        with open("tmp/dividends_t.pkl", "rb") as f:
            data = pickle.load(f)

        # Fetch income statement data for the given profile_id
        results = db.get_data("income_stmt", profile_id=profile_id)

        # Filter the years excluding 'ttm' (Trailing Twelve Months)
        years = [result["year"] for result in results if result["year"] != "ttm"]

        # Filter dividends data to only include the years present in the income statement data
        data = [data[0]] + [item for item in data[1:] if str(item[0]) in years]

        # Add profile_id to the dividends data and update the database
        data = transformer.add_profile_id(profile_id, data)
        db.update_data("ests", data[0], data[1:])

        # Initialize SQLLoader instance for handling specific data loading tasks
        loader = SQLLoader(db, profile_id)

        # Load and insert financial metrics (e.g., Return on Equity, Earnings per Share, Payout Ratio)
        # --------------------------------------------------------------------------------------------------
        loader.fetch_roe()  # Add Return on Equity (ROE) to the database
        loader.fetch_eps()  # Add Earnings Per Share (EPS) to the database
        loader.fetch_payout()  # Add Payout Ratio to the database

        # Load earnings estimate data from Pickle
        # -------------------------------------------------
        with open("tmp/earnings_estimate.pkl", "rb") as f:
            data = pickle.load(f)

        # Fetch income statement data to get the years
        results = db.get_data("income_stmt", profile_id=profile_id)

        # Extract years from the results and transform them (e.g., to match estimated years)
        years = [result["year"] for result in results]
        years = transformer.estimated_years(years)

        # Estimate EPS for the specified years and add profile_id to the data
        data = transformer.estimated_eps(data, years)
        data = transformer.add_profile_id(profile_id, data)

        # Update the database with the estimated EPS data
        db.update_data("ests", data[0], data[1:])

        # Add estimated financial metrics for each year
        # ---------------------------------------------------
        for year in years:
            loader.estimated_payout(year)  # Add estimated payout for each year
            loader.estimated_roe(year)  # Add estimated ROE for each year

        # Add estimated dividends data for each year
        for year in years:
            loader.estimated_dividends(year)  # Add estimated dividends for each year
            loader.estimated_roe(year)  # Add estimated ROE for each year

        # Add missing dividends for the profile
        loader.missing_dividends()

        # Add payout returns to the database
        loader.payout_returns()
