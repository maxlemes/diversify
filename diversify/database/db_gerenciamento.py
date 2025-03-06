import logging
import sqlite3
import traceback

from database.db_connection import DatabaseConnection

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DatabaseManager(DatabaseConnection):

    # -----------------------  Display methods -------------------------------------

    def insert_data(self, table, data):
        """Inserts data into a table."""
        if not data:
            logging.warning("No data provided for insertion.")
            return
        try:
            if table in [
                "quotes",
                "income_statement",
                "balance_sheet",
                "cash_flow",
                "stats",
            ]:
                # Get the ticker from the first dictionary
                ticker = data[0].get("ticker")
                if not ticker:
                    logging.warning("No ticker found in the data.")
                    return

                # Fetch the corresponding profile_id
                profile_id = self._fetch_profile_id(ticker)
                if profile_id is None:
                    logging.warning(f"Ticker {ticker} not found in the profile table.")
                    return  # Do not insert if profile_id is not found

                # Remove the ticker and add profile_id to all dictionaries
                data.remove({"ticker": ticker})

                for entry in data:
                    entry["profile_id"] = profile_id

            columns = list(data[0].keys())
            placeholders = ", ".join([f":{col}" for col in columns])
            query = (
                f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            )
            self.cursor.executemany(query, data)
            self.commit()
            logging.debug(f"Data inserted into table {table} successfully.")

        except sqlite3.IntegrityError as e:
            logging.error(f"Integrity error inserting data: {e}")
            self.rollback()
        except Exception as e:
            logging.error(f"Error inserting data into table {table}: {e}")
            logging.debug(traceback.format_exc())
            self.rollback()

    def insert_stats(self, table, columns, data):
        """Generic function to insert data into any table in the database."""
        try:
            columns_str = ", ".join(columns)
            placeholders = ", ".join(["?" for _ in columns])
            update_str = ", ".join([f"{column} = ?" for column in columns])

            query = f"""
                INSERT INTO {table} ({columns_str})
                VALUES ({placeholders})
                ON CONFLICT(profile_id, year) DO UPDATE SET {update_str};
            """
            for entry in data:
                self.cursor.execute(query, entry + entry)

            self.conn.commit()
            print(f"Data successfully inserted into table {table}!")
        except sqlite3.Error as e:
            print(f"Error inserting data into table {table}: {e}")

    # -----------------------  Setup methods ---------------------------------------
