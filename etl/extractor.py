import logging

import yfinance as yf

from data.data_types import VALID_DATA_TYPES

# Logging configuration for development
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Extractor:
    def __init__(self, ticker: str):
        """Initializes the data collection class."""
        self.ticker = ticker

    # -----------------------  Display methods -------------------------------------

    def get_price(self) -> float | bool:
        """Fetches the current stock price using `info["currentPrice"]`."""

        try:
            # Retrieve stock data
            stock = yf.Ticker(self.ticker + ".SA")

            # Get current price
            price = stock.info.get("currentPrice")

            # Ensure the info dictionary is not None
            if price:
                return price
            else:
                print("No data returned!")
                return False

        except Exception as e:
            # Log any exception that occurs
            logging.error(f"Error fetching stock price for {self.ticker}: {e}")
        return None

    def fetch_stock_prices(self, period="5y"):
        """
        Fetches the historical stock price data for a given ticker from Yahoo Finance.
        - Appends ".SA" for Brazilian B3 stocks.
        - Returns raw data for further processing.

        Args:
            period (str): The period of historical data to fetch (default is '5y').
                        Other options include '1d', '1mo', '3mo', '1y', '2y', '10y', 'ytd', 'max'.

        Returns:
            pandas.DataFrame: Historical stock data for the specified period, or False if no data is found or an error occurs.
        """
        try:
            # Fetch historical stock data for the specified period
            stock = yf.Ticker(self.ticker + ".SA")
            data = stock.history(period=period, auto_adjust=False)

            if data.empty:
                logging.error(f"No data found for {self.ticker}")
                return False

            return data

        except Exception as e:
            # Captures any exception and logs the error
            logging.error(f"Error fetching stock price data for {self.ticker}: {e}")

        return False

    def fetch_company_profile(self):
        """
        Fetches basic information about a company from Yahoo Finance.

        Returns a dictionary containing:
        - 'name' (str): Full company name.
        - 'ticker' (str): Stock ticker.
        - 'sector' (str): Industry sector of the company.
        - 'subsector' (str): Specific industry subsector.
        - 'website' (str): Official website URL.
        - 'description' (str): Brief description of the company.

        If an error occurs, logs the error and returns None.
        """
        try:
            # Get the company profile from Yahoo Finance
            stock = yf.Ticker(self.ticker + ".SA")
            info = stock.info

            # Prepare the company data, ensuring all keys are present
            company_data = {
                "name": info.get("longName", "N/A"),
                "ticker": self.ticker,
                "sector": info.get("sector", "N/A"),
                "subsector": info.get("industry", "N/A"),
                "website": info.get("website", "N/A"),
                "description": info.get("longBusinessSummary", "N/A"),
            }

            return company_data

        except Exception as e:
            # Logs any exception and the error message
            logging.error(f"Error fetching company profile for {self.ticker}: {e}")
            return None  # Returns None in case of error

    def fetch_data(self, data_type: str):
        """
        Fetches data for a given type of data (e.g., 'dividends', 'splits') from Yahoo Finance.

        Returns a list of dictionaries containing the data.

        Args:
            data_type (str): The type of data to fetch.
                - 'balance_sheet' (str): Balance sheet data (Balanço patrimonial).
                - 'income_stmt' (str): Income statement data (Demonstração de Resultados).
                - 'cashflow' (str): Cash flow statement data (Fluxo de caixa).
                - 'dividends' (str): Dividend data (Dividendos pagos).
                - 'splits' (str): Stock split data (Divisão de ações).
                - 'sustainability' (str): Sustainability data (Dados de sustentabilidade).
                - 'calendar' (str): Corporate calendar data (Calendário corporativo).
                - 'options' (str): Options data (Informações sobre opções de ações).
                - 'major_holders' (str): Major holders data (Principais acionistas).
                - 'institutional_holders' (str): Institutional investors data (Investidores institucionais).
                - 'fundamentals' (str): Financial fundamentals data (Dados financeiros fundamentais).
                - 'history' (str): Stock price history (Histórico de preços de ações).
                - 'actions' (str): Corporate actions data (Ações corporativas como dividendos e splits).

        Returns:
            list: A list of dictionaries containing the requested data, or None if an error occurs.
        """
        try:
            # Validates if the provided data_type is valid
            if data_type not in VALID_DATA_TYPES:
                logging.error(f"Invalid data type '{data_type}' for {self.ticker}.")
                return None

            # Connect to Yahoo Finance
            stock = yf.Ticker(self.ticker + ".SA")

            # Get data using the provided data_type
            data = getattr(stock, data_type, None)

            if data is None:
                logging.error(f"Data for '{data_type}' not found for {self.ticker}")
                return None

            return data

        except Exception as e:
            logging.error(f"Error fetching data for {self.ticker}: {e}")
            return None

    # # -----------------------  Setup methods ---------------------------------------


# ------------------- TEST ---------------------------------------------------------
if __name__ == "__main__":
    collector = Extractor("WEGE3")
    # info = collector.get_price()
    info = collector.fetch_company_profile()
    # info = collector.fetch_stock_prices()
    info = collector.fetch_data("income_stmt")
    # info = collector.fetch_data('balance_sheet')
    # info = collector.fetch_data('cash_flow')
    # info = collector.fetch_data('dividends')
    # info = collector.fetch_data('calendar')

    print(info)
