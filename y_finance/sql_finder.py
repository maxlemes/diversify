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

    import logging

    def fetch_roe(self, profile_id):
        """
        Calculates the ROE (Return on Equity) for a specific asset based on its profile ID
        and stores the results in the 'ests' table.

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
            JOIN balance_sheet ON income_stmt.profile_id = balance_sheet.profile_id 
                AND income_stmt.year = balance_sheet.year
            WHERE income_stmt.profile_id = ? 
                AND balance_sheet.stockholders_equity IS NOT NULL;
            """

            # Execute the query and get the result
            self.db.cursor.execute(query_roe, (profile_id,))
            results = self.db.cursor.fetchall()

            columns = ("profile_id", "year", "roe")
            self.db.update_data("ests", columns, results)

            return results

        except Exception as e:
            logging.error(
                f"Error fetching and storing ROE for profile_id {profile_id}: {e}"
            )
            return []

    import logging

    def fetch_eps(self, profile_id):
        """
        Calculates the EPS (Earnings Per Share) for a specific asset based on its profile ID
        and stores the results in the 'ests' table.

        Parameters:
            profile_id (int): The ID of the profile for which to calculate EPS.

        Returns:
            list: A list of tuples containing (profile_id, year, eps).
        """
        try:
            # Query to fetch EPS based on profile_id
            query_eps = """
            SELECT 
                income_stmt.profile_id,   -- Fetch profile ID from the income statement
                income_stmt.year,         -- Fetch year from the income statement
                (income_stmt.net_income / NULLIF(balance_sheet.ordinary_shares, 0)) AS eps
                -- Calculate EPS by dividing net income by ordinary shares (avoid division by 0 with NULLIF)
            FROM income_stmt
            JOIN balance_sheet 
                ON income_stmt.profile_id = balance_sheet.profile_id 
                AND income_stmt.year = balance_sheet.year
            WHERE income_stmt.profile_id = ? 
                AND balance_sheet.ordinary_shares IS NOT NULL;
                -- Filter by profile_id and ensure ordinary_shares is not null
            """

            # Execute the query and get the result
            self.db.cursor.execute(query_eps, (profile_id,))
            result = self.db.cursor.fetchall()

            columns = ("profile_id", "year", "eps")
            self.db.update_data("ests", columns, result)

            # Return the result (list of tuples)
            return result

        except Exception as e:
            # Log the error with the profile_id for better debugging
            logging.error(
                f"Error calculating and storing EPS for profile_id {profile_id}: {e}"
            )
            # Return an empty list in case of error
            return []

        import logging

    def fetch_payout(self, profile_id):
        """
        Calculates the Payout Ratio for a specific asset based on its profile ID
        and stores the results in the 'ests' table.

        The Payout Ratio is calculated as:
            payout = -dividends_paid / net_income

        Parameters:
            profile_id (int): The ID of the profile for which to calculate the Payout Ratio.

        Returns:
            list: A list of tuples containing (profile_id, year, payout).
        """
        try:
            # Query to fetch Dividends Paid and Net Income for calculating the payout ratio
            query_payout = """
            SELECT 
                income_stmt.profile_id,   -- Fetch profile ID from the income statement
                income_stmt.year,         -- Fetch year from the income statement
                (-cash_flow.dividends_paid / NULLIF(income_stmt.net_income, 0)) AS payout
                -- Calculate payout ratio: -dividends_paid / net_income (avoid division by 0 with NULLIF)
            FROM income_stmt
            JOIN cash_flow 
                ON income_stmt.profile_id = cash_flow.profile_id 
                AND income_stmt.year = cash_flow.year
            WHERE income_stmt.profile_id = ? 
                AND cash_flow.dividends_paid < 0 
                AND income_stmt.net_income IS NOT NULL
                AND cash_flow.dividends_paid IS NOT NULL;
                -- Ensure that dividends_paid is negative and both values are not NULL
            """

            # Execute the query and get the result
            self.db.cursor.execute(query_payout, (profile_id,))
            result = self.db.cursor.fetchall()

            columns = ("profile_id", "year", "payout")
            self.db.update_data("ests", columns, result)

            # Return the result (list of tuples)
            return result

        except Exception as e:
            # Log the error with the profile_id for better debugging
            logging.error(
                f"Error calculating and storing Payout for profile_id {profile_id}: {e}"
            )
            # Return an empty list in case of error
            return []

    def current_payout(self, profile_id, current_year):
        """
        Estimates the payout for a specific profile_id using the formula: payout = dividends / eps
        for the given year, and stores the result in the 'ests' table.

        Parameters:
            profile_id (int): The ID of the profile for which to calculate the payout.
            year (str): The year for which the payout should be calculated.

        Returns:
            tuple: A tuple containing (year, payout).
        """
        try:
            # Prepare the query to fetch the relevant data from the 'ests' table
            query = """
            SELECT year, dividends, eps
            FROM ests
            WHERE profile_id = ? AND year = ?
            """

            # Execute the query with the profile_id and year as parameters
            self.db.cursor.execute(query, (profile_id, current_year))
            result = self.db.cursor.fetchone()

            # Calculate the payout if data is available
            if result:
                year, dividends, eps = result

                # Ensure that dividends and eps are not None and eps is not zero
                if dividends is not None and eps is not None and eps != 0:
                    payout = dividends / eps

                    columns = ("profile_id", "year", "payout")
                    values = [(profile_id, year, payout)]

                    self.db.update_data("ests", columns, values)

                    return values
                else:
                    # If data is invalid (None or zero eps), set payout to None
                    return result
            else:
                logging.warning(
                    f"No data found for profile_id {profile_id} and year {year}."
                )
                return result

        except Exception as e:
            logging.error(
                f"Error calculating and storing payout estimate for profile_id {profile_id} and year {year}: {e}"
            )
            return (year, None)

    def estimated_payout(self, profile_id, next_year):
        """
        Calculates the average payout for the 5 years before and including years[0],
        and stores the result in the year specified by next_year.

        Parameters:
            profile_id (int): The ID of the profile for which to calculate the average payout.
            years (list): A list containing two years, where years[0] is the last year to calculate the average,
                        and next_year is the year to store the calculated average payout.

        Returns:
            tuple: A tuple containing (year, average_payout).
        """
        try:
            # Fetch the 5 years of payout data from the 'ests' table
            start_year = int(next_year) - 5  # Calculate the start year (5 years before)
            end_year = int(next_year) - 1  # The last year is years[

            query = """
            SELECT payout
            FROM ests
            WHERE profile_id = ? AND year BETWEEN ? AND ?
            """

            # Execute the query to fetch payouts for the specified years
            self.db.cursor.execute(query, (profile_id, start_year, end_year))
            results = self.db.cursor.fetchall()

            # Calculate the average payout if data is available
            if results:
                payouts = [result[0] for result in results if result[0] is not None]

                if payouts:
                    average_payout = sum(payouts) / len(payouts)

                    columns = ("profile_id", "year", "payout")
                    values = [(profile_id, next_year, average_payout)]

                    self.db.update_data("ests", columns, values)

                    return values

                else:
                    logging.warning(
                        f"No valid payouts found for profile_id {profile_id} from {start_year} to {end_year}."
                    )
                    return (next_year, None)
            else:
                logging.warning(
                    f"No payout data found for profile_id {profile_id} in the years {start_year}-{end_year}."
                )
                return (next_year, None)

        except Exception as e:
            logging.error(
                f"Error calculating and storing payout estimate for profile_id {profile_id} and years {years[0]}-{next_year}: {e}"
            )
            return (next_year, None)

    def estimated_dividends(self, profile_id, next_year):
        """
        Calculates the dividends for the 'ttm' year and the specified year in next_year,
        and stores the results in the 'ests' table.

        Parameters:
            profile_id (int): The ID of the profile for which to calculate dividends.
            years (list): A list containing two years, where years[0] is the last year to calculate the dividends
                        and next_year is the year to store the calculated dividends.

        Returns:
            tuple: A tuple containing (year, calculated_dividends).
        """
        try:
            # Fetch the payout and eps for 'ttm' and next_year from the 'ests' table
            query = """
            SELECT year, payout, eps
            FROM ests
            WHERE profile_id = ? AND year IN ('ttm', ?)
            """

            next_year = str(next_year)
            # Execute the query
            self.db.cursor.execute(query, (profile_id, next_year))
            results = self.db.cursor.fetchall()

            # Check if we have results for 'ttm' and next_year
            if len(results) < 2:
                logging.warning(
                    f"Not enough data found for profile_id {profile_id} in 'ttm' and year {next_year}."
                )
                return (next_year, None)

            # Create a dictionary for the results for easy access
            data = {
                result[0]: {"payout": result[1], "eps": result[2]} for result in results
            }

            # Calculate dividends for 'ttm' and next_year
            dividends_ttm = (
                data["ttm"]["payout"] * data["ttm"]["eps"]
                if data["ttm"]["payout"] and data["ttm"]["eps"]
                else None
            )
            dividends_year = (
                data[next_year]["payout"] * data[next_year]["eps"]
                if data[next_year]["payout"] and data[next_year]["eps"]
                else None
            )

            columns = ("profile_id", "year", "dividends")

            values = [(profile_id, next_year, dividends_year)]
            values = [(profile_id, "ttm", dividends_ttm)] + values

            self.db.update_data("ests", columns, values)

            return values

        except Exception as e:
            logging.error(
                f"Error calculating and storing dividends estimate for profile_id {profile_id} and years {years[0]}-{years[1]}: {e}"
            )
            return (next_year, None)

        # -----------------------  Display methods -------------------------------------
