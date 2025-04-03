from datetime import datetime
from stegosaurus.database import RedshiftClient, PostgresClient
from stegosaurus.config import REDSHIFT_CONFIG, POSTGRES_CONFIG

class StegosaurusWorkflow:
    def __init__(self, sheets_client, sql_range):
        self.sheets_client = sheets_client
        self.sql_range = sql_range

    def execute_workflow(self):
        print("Fetching SQL queries from Google Sheets...")
        sheet_info = self.sheets_client.read_range(self.sql_range)

        query_titles = [row[2] for row in sheet_info if row]
        query_output_sheets = [row[4] for row in sheet_info if row]
        query_output_tabs = [row[5] for row in sheet_info if row]
        sql_queries = [row[6] for row in sheet_info if row]
        query_databases = [row[7].lower() for row in sheet_info if row]  # new column
        execute_flags = [row[8] for row in sheet_info if row]  # Switch column now at index 8

        if not sql_queries:
            raise ValueError("No SQL queries found.")

        print(f"Executing {len(sql_queries)} queriesssss...")

        for i, query in enumerate(sql_queries):
            print("Here")
            if execute_flags[i] == "1":
                db_type = query_databases[i]
                print(db_type)
                print(f"Executing query {i + 1}: {query_titles[i]} on {db_type}...")
                
                if db_type == "postgres":
                    db_client = PostgresClient(**POSTGRES_CONFIG)
                else:
                    db_client = RedshiftClient(**REDSHIFT_CONFIG)

                db_client.connect()
                results = db_client.execute_query(query)
                db_client.close_connection()

                if results:
                    try:
                        output_sheet = query_output_sheets[i]
                        output_tab = query_output_tabs[i]
                        self.sheets_client.clear_range(output_sheet, f"{output_tab}!A:Z")
                        self.sheets_client.write_range(output_sheet, f"{output_tab}!A1", values=results)
                        self.sheets_client.write_range(
                            self.sheets_client.sheet_id, f"steg!J{i+2}", values=[["PASS"]])
                        self.sheets_client.write_range(
                            self.sheets_client.sheet_id, f"steg!I{i+2}", 
                            values=[[datetime.now().strftime("%Y-%m-%d %H:%M:%S")]])
                        print(f"SUCCESS. Results written to {output_tab}.\n")
                    except Exception as e:
                        print(f"FAILURE. Error: {e}\n")
                        self.sheets_client.write_range(self.sheets_client.sheet_id, f"steg!J{i+2}", values=[["FAIL"]])
                else:
                    self.sheets_client.write_range(self.sheets_client.sheet_id, f"steg!J{i+2}", values=[["FAIL"]])