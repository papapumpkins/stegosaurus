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
            print("Using existing database connection.\n")
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
            print("Successfully connected to Redshift.\n")

            if not (saved_user and saved_password):
                keyring.set_password(self.service_name, "username", user)
                keyring.set_password(self.service_name, "password", password)

        except OperationalError as e:
            print(f"Error connecting to Redshift: {e}")
            self.conn = None

    def execute_query(self, query, params=None):
        if not self.conn:
            raise ValueError("No database connection. Please call connect() first.")
        try:
            self.cursor.execute(query, params)
            column_names = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            processed_rows = [[self._convert_value(value) for value in row] for row in rows]
            return [column_names] + processed_rows
        except Exception as e:
            print(f"FAILURE. Error executing query: {e}")
            self.conn.rollback()
            return None

    @staticmethod
    def _convert_value(value):
        if isinstance(value, Decimal):
            return float(value) if value % 1 else int(value)
        return value

    def close_connection(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Database connection closed. Ciao")
            self.conn = None

class PostgresClient:
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.conn = None
        self.cursor = None
        self.service_name = "stegosaurus_postgres"

    def connect(self):
        if self.conn:
            print("Using existing Postgres connection.\n")
            return
        try:
            saved_user = keyring.get_password(self.service_name, "username")
            saved_password = keyring.get_password(self.service_name, "password")

            if saved_user and saved_password:
                print("Using saved Postgres credentials.")
                user, password = saved_user, saved_password
            else:
                user = input("Enter Postgres username: ")
                password = getpass.getpass("Enter Postgres password: ")

            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.database,
                user=user,
                password=password
            )
            self.cursor = self.conn.cursor()
            print("Successfully connected to Postgres.\n")

            if not (saved_user and saved_password):
                keyring.set_password(self.service_name, "username", user)
                keyring.set_password(self.service_name, "password", password)

        except OperationalError as e:
            print(f"Error connecting to Postgres: {e}")
            self.conn = None

    def execute_query(self, query, params=None):
        if not self.conn:
            raise ValueError("No database connection. Please call connect() first.")
        try:
            self.cursor.execute(query, params)
            column_names = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            processed_rows = [[self._convert_value(value) for value in row] for row in rows]
            return [column_names] + processed_rows
        except Exception as e:
            print(f"FAILURE. Error executing Postgres query: {e}")
            self.conn.rollback()
            return None

    @staticmethod
    def _convert_value(value):
        if isinstance(value, Decimal):
            return float(value) if value % 1 else int(value)
        return value

    def close_connection(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Postgres connection closed.")
            self.conn = None


def clear_credentials():
    import keyring
    service_name = "stegosaurus_redshift"
    keyring.delete_password(service_name, "username")
    keyring.delete_password(service_name, "password")
    print("Credentials cleared.")
