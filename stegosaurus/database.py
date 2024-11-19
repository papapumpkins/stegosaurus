import psycopg2
from psycopg2 import OperationalError
from decimal import Decimal
import getpass
import keyring

class RedshiftClient:
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.conn = None
        self.cursor = None
        self.service_name = "stegosaurus_redshift"

    def connect(self):

        if self.conn:
            print("Using existing database connection. \n")
            return
        try:
            saved_user = keyring.get_password(self.service_name, "username")
            saved_password = keyring.get_password(self.service_name, "password")

            if saved_user and saved_password:
                print("Using saved credentials.")
                user, password = saved_user, saved_password
            else:
                user = input("Enter Redshift username: ")
                password = getpass.getpass("Enter Redshift password: ")

            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.database,
                user=user,
                password=password
            )
            self.cursor = self.conn.cursor()
            print("Successfully connected to Redshift. \n")

            if not (saved_user and saved_password):
                keyring.set_password(self.service_name, "username", user)
                keyring.set_password(self.service_name, "password", password)

        except OperationalError as e:
            print(f"Error connecting to Redshift: {e}")
            self.conn = None

    def execute_query(self, query):
        """Executes a SQL query and returns the results with column headers."""
        if not self.conn:
            raise ValueError("No database connection. Please call connect() first.")
        try:
            self.cursor.execute(query)

            # Fetch column names
            column_names = [desc[0] for desc in self.cursor.description]

            # Fetch all rows and convert problematic types
            rows = self.cursor.fetchall()
            processed_rows = [
                [self._convert_value(value) for value in row] for row in rows
            ]

            # Combine column names and rows
            results = [column_names] + processed_rows
            return results
        except Exception as e:
            print(f"FAILURE. Error executing query: {e}")
            self.conn.rollback()
            return None

    @staticmethod
    def _convert_value(value):
        """Converts problematic data types to native Python types."""
        if isinstance(value, Decimal):
            return float(value) if value % 1 else int(value)  # Convert Decimal to int or float
        return value

    def close_connection(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Database connection closed. Ciao")
            self.conn = None
