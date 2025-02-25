import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SQLFinder:
    def __init__(self, db_manager):
        """
        Initializes the DataHandler with a database connection.

        :param db_connection: Database connection object.
        """
        self.db = db_manager

    def fetch_roe(self, profile_id):
        """
        Calculates the ROE (Return on Equity) for a specific asset based on its profile ID.

        Parameters:
            profile_id (int): The ID of the profile for which to calculate ROE.

        Returns:
            list: A list of tuples containing (profile_id, year, roe).
        """
        try:
            # Query to fetch ROE based on profile_id
            query_roe = """
            SELECT 
                income_stmt.profile_id,
                income_stmt.year, 
                (income_stmt.net_income / NULLIF(balance_sheet.stockholders_equity, 0)) AS roe
            FROM income_stmt
            JOIN balance_sheet ON income_stmt.profile_id = balance_sheet.profile_id AND income_stmt.year = balance_sheet.year
            WHERE income_stmt.profile_id = ? AND balance_sheet.stockholders_equity IS NOT NULL;
            """

            # Execute the query and return the result
            result = self.db._execute_query(query_roe, (profile_id,))

            # Check if result is empty and log it
            if not result:
                logging.warning(f"No ROE data found for profile_id {profile_id}.")

            return result

        except Exception as e:
            # Log the error with the profile_id for better debugging
            logging.error(f"Error calculating ROE for profile_id {profile_id}: {e}")
            return []

    def fetch_eps(self, profile_id):
        """
        Calculates the ROE (Return on Equity) for a specific asset based on its profile ID.

        Parameters:
            profile_id (int): The ID of the profile for which to calculate ROE.

        Returns:
            list: A list of tuples containing (profile_id, year, roe).
        """
        try:
            # Query to fetch ROE based on profile_id
            query_roe = """
            SELECT 
                income_stmt.profile_id,
                income_stmt.year, 
                (income_stmt.net_income / NULLIF(balance_sheet.ordinary_shares, 0)) AS eps
            FROM income_stmt
            JOIN balance_sheet ON income_stmt.profile_id = balance_sheet.profile_id AND income_stmt.year = balance_sheet.year
            WHERE income_stmt.profile_id = ? AND balance_sheet.ordinary_shares IS NOT NULL;
            """

            # Execute the query and return the result
            result = self.db._execute_query(query_roe, (profile_id,))

            # Check if result is empty and log it
            if not result:
                logging.warning(f"No EPS data found for profile_id {profile_id}.")

            return result

        except Exception as e:
            # Log the error with the profile_id for better debugging
            logging.error(f"Error calculating EPS for profile_id {profile_id}: {e}")
            return []

    # -----------------------  Display methods -------------------------------------
