import logging

from database.db_manager import DatabaseConnection

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DatabaseQueries(DatabaseConnection):

    # -----------------------  Display methods -------------------------------------

    def fetch_data(self, table, **filters):
        """
        Retrieves data from any database table based on provided filters.

        Parameters:
            table (str): Name of the table to query.
            **filters (kwargs): Filters in the format column=value.

        Returns:
            list[dict]: A list of dictionaries containing the query results.
        """
        query = f"SELECT * FROM {table} WHERE 1=1"
        parameters = []

        for column, value in filters.items():
            query += f" AND {column} = ?"
            parameters.append(value)

        try:
            self.cursor.execute(query, tuple(parameters))
            columns = [desc[0] for desc in self.cursor.description]  # Get column names
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except Exception as e:
            logging.error(f"Error fetching data from table {table}: {e}")
            return []

    def search_profile(self, name=None, ticker=None, sector=None, subsector=None):
        """
        Searches records in the 'profile' table based on the provided filters.

        Parameters:
            name (str, optional): Company name.
            ticker (str, optional): Asset code.
            sector (str, optional): Company sector.
            subsector (str, optional): Company subsector.

        Returns:
            list: List of tuples with found results.
        """
        query = "SELECT * FROM profile WHERE 1=1"
        parameters = []

        if name:
            query += " AND name LIKE ?"
            parameters.append(f"%{name}%")
        if ticker:
            query += " AND ticker = ?"
            parameters.append(ticker)
        if sector:
            query += " AND sector LIKE ?"
            parameters.append(f"%{sector}%")
        if subsector:
            query += " AND subsector LIKE ?"
            parameters.append(f"%{subsector}%")

        profile = self._execute_query(query, tuple(parameters))

        if profile:
            columns = [
                "id",
                "name",
                "ticker",
                "sector",
                "subsector",
                "website",
                "description",
            ]
            result = dict(zip(columns, profile[0]))
        else:
            result = None

        return result

    def search_profile_by_id(self, ticker):
        """
        Searches for the profile_id of an asset based on the ticker.

        Parameters:
            ticker (str): Asset ticker.

        Returns:
            int | None: The corresponding profile_id or None if not found.
        """
        try:
            query = "SELECT id FROM profile WHERE ticker = ?;"
            result = self._execute_query(query, (ticker,))

            if result:
                return result[0][0]  # Returns the found profile_id
            else:
                logging.warning(f"Ticker '{ticker}' not found in the 'profile' table.")
                return None

        except Exception as e:
            logging.error(f"Error searching for profile_id for {ticker}: {e}")
            return None

    def search_quotes(self, ticker):
        """
        Queries the quotes of a company based on the given ticker.

        Parameters:
            ticker (str): The ticker of the company to query.

        Returns:
            list[dict]: List of dictionaries containing the company's quotes.
        """
        query = """
            SELECT c.*
            FROM quotes c
            JOIN profile p ON c.profile_id = p.id
            WHERE p.ticker = ?;
        """
        result = self._execute_query(query, (ticker,))

        # Converting to a list of dictionaries
        columns = [
            "profile_id",
            "date",
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]
        return [dict(zip(columns, row)) for row in result]

    def search_income_statement(self, ticker):
        """
        Queries the Income Statement (DRE) data of a company based on the given ticker.

        Parameters:
            ticker (str): The ticker of the company to query.

        Returns:
            list[dict]: List of dictionaries containing the company's income statement data.
        """
        query = """
            SELECT d.*
            FROM income_statement d
            JOIN profile p ON d.profile_id = p.id
            WHERE p.ticker = ?;
        """
        result = self._execute_query(query, (ticker,))

        # Define the column names as per the income_statement table structure
        columns = [
            "profile_id",
            "year",
            "total_revenue",
            "cost_of_revenue",
            "gross_profit",
            "operating_expenses",
            "operating_profit",
            "profit_before_taxes",
            "tax_provision",
            "net_profit",
            "basic_eps",
            "total_expenses",
            "normalized_profit",
            "interest_received",
            "interest_paid",
            "profit_interest",
            "ebit",
            "ebitda",
            "depreciation",
            "normalized_ebitda",
        ]

        return [dict(zip(columns, row)) for row in result]

    # -----------------------  Setup methods ---------------------------------------

    def _fetch_profile_id(self, ticker):
        """Fetches the profile_id from the profile table for a single ticker."""
        query = "SELECT id FROM profile WHERE ticker = ?"
        result = self.cursor.execute(query, (ticker,)).fetchone()
        return result[0] if result else None
