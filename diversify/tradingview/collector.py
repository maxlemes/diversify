import json
import logging
from pathlib import Path

from etl_tradinview.scraper import Scraper

# Logging configuration for development
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Collector:
    def __init__(self, ticker, scraper):
        """Inicializa a classe de coleta dos dados."""
        self.ticker = ticker
        self.scraper = scraper
        # Scraper(url=None, xpath=None)

        with open("data/sources.json", "r") as f:
            self.sources = json.load(f)

    def set_params(self, url, xpath):
        """Sets URL and XPath before scraping."""
        self.scraper.url = url
        self.scraper.xpath = xpath

    def balance(self, balance_type):
        """Collects the balance sheet and stores it in the database."""

        if balance_type not in self.sources:
            raise ValueError(
                f"Invalid balance type '{balance_type}'. Choose from: {list(self.sources.keys())}"
            )

        try:
            # Defining the balance sheet URL and XPath
            url = self.sources[balance_type]["url"].format(self.ticker)
            xpath = self.sources[balance_type]["xpath_t"]

            # Set the scraper parameters to collect data
            # self.set_params(url, xpath)
            self.scraper.access_site(url)

            # Collect the data table
            data = self.scraper.collect_table_div(xpath)

            logging.info(
                f"Balance sheet data for asset '{self.ticker}' successfully collected."
            )

            return data

        except Exception as e:
            # Capture any exception and log the error
            logging.error(
                f"Error collecting or inserting balance sheet data for asset {self.ticker}: {e}"
            )
            print(f"Error processing the balance sheet for asset {self.ticker}: {e}")

        finally:
            # Close the browser, ensuring this always happens
            if "scraper" in locals():
                self.scraper.close_browser()
                logging.info(f"Browser closed for asset {self.ticker}.")


# ------------------- TEST ---------------------------------------------------------
if __name__ == "__main__":

    ticker = "WEGE3"

    # # Create the database connection and initialize the tables
    collector = Collector(ticker)
    data = collector.balance("income_stmt")
    print(data)
