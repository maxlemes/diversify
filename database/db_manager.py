import json
import logging
import sqlite3
from pathlib import Path

# Logging configuration for development
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DatabaseManager:
    def __init__(self, file):
        """
        Constructor for the DatabaseConnection class.

        This method is automatically called when an instance of the class is created.
        It initializes the database connection and prepares the environment for operations.

        Paremeters:
            file (str): Path to the SQLite database file.
        """
        self.file = file  # Stores the database file path
        self.conn = None  # Initializes the connection as None
        self.cursor = None  # Initializes the cursor as None

    # -----------------------  Display methods -------------------------------------

    def connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.file)  # Connects to the database
            self.cursor = self.conn.cursor()  # Creates a cursor for executing queries
        except sqlite3.Error as e:
            logging.error(f"Error connecting to the database: {e}")
            raise  # Raises the exception to be handled by the calling code

    def disconnect(self):
        """Closes the database connection."""
        try:
            if self.conn:
                self.conn.close()  # Closes the connection
        except sqlite3.Error as e:
            logging.error(f"Error closing the connection: {e}")
            raise  # Raises the exception if an error occurs

    def commit(self):
        """Commits the changes to the database."""
        try:
            self.conn.commit()  # Saves the changes
        except sqlite3.Error as e:
            logging.error(f"Error committing changes to the database: {e}")
            raise  # Raises the exception to be handled by the calling code

    def create_table(self, table_name, columns):
        """Creates a table if it does not exist."""
        if self.table_exists(table_name):
            return
        try:
            columns_sql = ", ".join(
                [f"{column} {type}" for column, type in columns.items()]
            )
            query = f"CREATE TABLE {table_name} ({columns_sql});"
            self.cursor.execute(query)
        except Exception as e:
            logging.error(f"Error creating table {table_name}: {e}")

    def delete_table(self, table_name):
        """Deletes a table if it exists."""
        if not self.table_exists(table_name):
            return

        try:
            query = f"DROP TABLE {table_name};"
            self.cursor.execute(query)
        except Exception as e:
            logging.error(f"Error deleting table {table_name}: {e}")

    def create_initial_tables(self, tables):
        """Creates the initial tables in the database using the definitions from a JSON file.

        :param table: Dictionary with definitions of tables.
        """

        # Create the tables from the JSON file
        for name, columns in tables.items():
            self.create_table(name, columns)

    def table_exists(self, table_name):
        """Checks if a table exists in the database."""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
        result = self.cursor.execute(query, (table_name,)).fetchone()
        return result is not None

    def column_exists(self, table_name, column_name):
        """Checks if a column exists in a table in the database."""
        query = "PRAGMA table_info(?);"
        result = self.cursor.execute(query, (table_name,)).fetchall()

        # Check if the column is present in the results
        for column in result:
            if column[1] == column_name:
                return True
        return False

    def data_exists(self, table, conditions, column):
        """
        Checks if the specified column value is NULL for a given record based on conditions.
        Returns True if the value is NULL, otherwise False.

        :param table: Name of the table to query.
        :param conditions: A dictionary where the keys are column names and the values are the values to check.
        :param column: The column to check for NULL value.
        """
        # Create the WHERE clause dynamically from the conditions dictionary
        where_clause = " AND ".join([f"{key} = ?" for key in conditions.keys()])
        query = f"SELECT {column} FROM {table} WHERE {where_clause}"

        # Execute the query with the values from the conditions
        self.cursor.execute(query, tuple(conditions.values()))
        result = self.cursor.fetchone()

        if result is None:
            # If no result is found, return False
            print(f"Record with conditions {conditions} not found.")
            return False

        column_value = result[0]

        # Return True if the column value is NULL, False otherwise
        return column_value is None

    def add_column(self, table_name, column_name, column_type):
        """Adds a column to an existing table."""
        if self.column_exists(table_name, column_name):
            return

        try:
            query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
            self.cursor.execute(query)
        except Exception as e:
            logging.error(
                f"Error adding column {column_name} to table {table_name}: {e}"
            )

    def list_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        return [t[0] for t in self.cursor.execute(query).fetchall()]

    def query_table(self, table, column):
        """
        Returns a list of unique (DISTINCT) values from the specified column in a table.

        Parameters:
            table (str): The name of the table to query.
            column (str): The name of the column whose distinct values will be returned.

        Returns:
            list: A list of unique values from the specified column, sorted in ascending order.
        """
        # Construct the SQL query to select distinct values from the column and sort them
        query = f"SELECT DISTINCT {column} FROM {table} ORDER BY {column};"

        # Execute the query and return a list containing only the column values
        return [t[0] for t in self.cursor.execute(query).fetchall()]

    def insert_data(self, table, columns, data):
        """Generic function to insert data into any table in the database."""
        try:
            columns_str = ", ".join(columns)
            placeholders = ", ".join(["?" for _ in columns])

            query = f"""
                INSERT INTO {table} ({columns_str})
                VALUES ({placeholders});
            """
            for entry in data:
                self.cursor.execute(query, entry)

            self.conn.commit()
            print(f"Data successfully inserted into table {table}!")
        except sqlite3.Error as e:
            print(f"Error inserting data into table {table}: {e}")

    def update_data(self, table, columns, data):
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

    def get_data(self, table, **filters):
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

    def fetch_profile_id(self, ticker):
        """Fetches the profile_id from the profile table for a single ticker."""
        query = "SELECT id FROM profile WHERE ticker = ?"
        result = self.cursor.execute(query, (ticker,)).fetchone()
        return result[0] if result else None

    def rollback(self):
        """Rolls back the last transaction."""
        self.conn.rollback()  # Rollback is supported by the connection

    # -----------------------  Setup methods ---------------------------------------
    def __enter__(self):
        self.connect()
        return self  # Returns the instance to be used within the 'with' block

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()  # Automatically closes the connection


# ------------------- TEST ---------------------------------------------------------
if __name__ == "__main__":
    path = Path("data/files.json")  # ------------------------------------------------
    # Load the JSON file containing paths to the database and tables
    with open(path, "r") as f:
        files = json.load(f)
    # Define paths for the database and tables
    db_path = Path(files["database"])
    tables_path = Path(files["tables"])
    # Load the table definitions from the tables JSON file
    with open(tables_path, "r") as f:
        tables = json.load(f)
    # print(tables)
    # Create the database connection and initialize the tables
    with DatabaseManager(db_path) as conn:
        conn.create_initial_tables(tables)
