import pickle

from diversify import Collector, Scraper


def collect(ticker):
    """
    Collects and saves financial data for a given ticker.
    """

    # Initialize the browser
    scraper = Scraper()

    # Initialize the data collector
    collector = Collector(ticker, scraper)

    # Financial statements to collect
    balance_types = ["income_stmt", "balance_sheet", "cash_flow"]

    for balance_type in balance_types:
        # Collect data for the specific statement
        data = collector.balance(balance_type)

        # Save data as a Pickle file
        with open(f"tmp/{balance_type}.pkl", "wb") as f:
            pickle.dump(data, f)

    # Close the browser
    scraper.close_browser()
