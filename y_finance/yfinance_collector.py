import json
import logging

import yfinance as yf

# Logging configuration for development
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


class YFinanceCollector:
    def __init__(self, ticker: str):
        """Initializes the data collection class."""
        self.ticker = ticker
        # Load filters from filters.json
        self.filters = self._load_filters()

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
            # print(VALID_DATA_TYPES)
            # # Validates if the provided data_type is valid
            # if data_type not in VALID_DATA_TYPES:
            #     logging.error(f"Invalid data type '{data_type}' for {self.ticker}.")
            #     return None

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

    # -----------------------  Setup methods ---------------------------------------
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
    collector = YFinanceCollector("WEGE3")
    # info = collector.get_price()
    info = collector.fetch_company_profile()
    # info = collector.fetch_stock_prices()
    info = collector.fetch_data("income_stmt")
    # info = collector.fetch_balance('balance_sheet')
    # info = collector.fetch_balance('cash_flow', 'quartely')
    # info = collector.fetch_data('dividends')
    # info = collector.fetch_data('calendar')

    print(info)


VALID_DATA_TYPES = [
    "actions",  # Ações corporativas, como dividendos e splits
    "analyst_price_targets",  # Preços alvo de analistas
    "balance_sheet",  # Balanço patrimonial
    "balancesheet",  # Balanço patrimonial (outro nome)
    "basic_info",  # Informações básicas da empresa
    "calendar",  # Calendário corporativo
    "capital_gains",  # Ganhos de capital
    "cash_flow",  # Fluxo de caixa
    "cashflow",  # Fluxo de caixa (outro nome)
    "dividends",  # Dividendos pagos
    "earnings",  # Lucros da empresa
    "earnings_dates",  # Datas de lucros
    "earnings_estimate",  # Estimativas de lucros
    "earnings_history",  # Histórico de lucros
    "eps_revisions",  # Revisões de lucro por ação (EPS)
    "eps_trend",  # Tendências de lucro por ação
    "fast_info",  # Informações rápidas sobre a empresa
    "financials",  # Demonstrações financeiras (inclui balanço patrimonial e resultados)
    "fundamentals",  # Dados financeiros fundamentais
    "get_actions",  # Ações corporativas (método)
    "get_analyst_price_targets",  # Preços alvo de analistas (método)
    "get_balance_sheet",  # Balanço patrimonial (método)
    "get_balancesheet",  # Balanço patrimonial (outro nome, método)
    "get_calendar",  # Calendário corporativo (método)
    "get_capital_gains",  # Ganhos de capital (método)
    "get_cash_flow",  # Fluxo de caixa (método)
    "get_cashflow",  # Fluxo de caixa (outro nome, método)
    "get_dividends",  # Dividendos pagos (método)
    "get_earnings",  # Lucros da empresa (método)
    "get_earnings_dates",  # Datas de lucros (método)
    "get_earnings_estimate",  # Estimativas de lucros (método)
    "get_earnings_history",  # Histórico de lucros (método)
    "get_eps_revisions",  # Revisões de EPS (método)
    "get_eps_trend",  # Tendências de EPS (método)
    "get_fast_info",  # Informações rápidas (método)
    "get_financials",  # Demonstrações financeiras (método)
    "get_funds_data",  # Dados de fundos (método)
    "get_growth_estimates",  # Estimativas de crescimento (método)
    "get_history_metadata",  # Metadados de histórico (método)
    "get_income_stmt",  # Demonstração de resultados (método)
    "get_incomestmt",  # Demonstração de resultados (outro nome, método)
    "get_info",  # Informações gerais da empresa (método)
    "get_insider_purchases",  # Compras de ações por insiders (método)
    "get_insider_roster_holders",  # Acionistas insiders (método)
    "get_insider_transactions",  # Transações de insiders (método)
    "get_institutional_holders",  # Investidores institucionais (método)
    "get_isin",  # Código ISIN (método)
    "get_major_holders",  # Principais acionistas (método)
    "get_mutualfund_holders",  # Detentores de fundos mútuos (método)
    "get_news",  # Notícias relacionadas (método)
    "get_recommendations",  # Recomendações de analistas (método)
    "get_recommendations_summary",  # Resumo de recomendações (método)
    "get_revenue_estimate",  # Estimativa de receita (método)
    "get_sec_filings",  # Arquivos da SEC (método)
    "get_shares",  # Ações em circulação (método)
    "get_shares_full",  # Informações completas sobre ações (método)
    "get_splits",  # Divisão de ações (método)
    "get_sustainability",  # Dados de sustentabilidade (método)
    "get_upgrades_downgrades",  # Upgrades e downgrades de ações (método)
    "growth_estimates",  # Estimativas de crescimento (método)
    "history",  # Histórico de preços de ações
    "history_metadata",  # Metadados de histórico de preços (método)
    "income_stmt",  # Demonstração de resultados
    "incomestmt",  # Demonstração de resultados (outro nome)
    "info",  # Informações gerais da empresa
    "insider_purchases",  # Compras de ações por insiders
    "insider_roster_holders",  # Acionistas insiders
    "insider_transactions",  # Transações de insiders
    "institutional_holders",  # Investidores institucionais
    "isin",  # Código ISIN
    "major_holders",  # Principais acionistas
    "mutualfund_holders",  # Detentores de fundos mútuos
    "news",  # Notícias relacionadas
    "option_chain",  # Cadeia de opções
    "options",  # Opções de ações
    "proxy",  # Proxies relacionados
    "quarterly_balance_sheet",  # Balanço patrimonial trimestral
    "quarterly_balancesheet",  # Balanço patrimonial trimestral (outro nome)
    "quarterly_cash_flow",  # Fluxo de caixa trimestral
    "quarterly_cashflow",  # Fluxo de caixa trimestral (outro nome)
    "quarterly_earnings",  # Lucros trimestrais
    "quarterly_financials",  # Demonstrações financeiras trimestrais
    "quarterly_income_stmt",  # Demonstração de resultados trimestral
    "quarterly_incomestmt",  # Demonstração de resultados trimestral (outro nome)
    "recommendations",  # Recomendações de analistas
    "recommendations_summary",  # Resumo das recomendações de analistas
    "revenue_estimate",  # Estimativa de receita
    "sec_filings",  # Arquivos da SEC
    "session",  # Sessão de mercado
    "shares",  # Ações em circulação
    "splits",  # Divisão de ações
    "sustainability",  # Dados de sustentabilidade
    "ticker",  # Ticker da ação
    "upgrades_downgrades",  # Upgrades e downgrades de ações
]
