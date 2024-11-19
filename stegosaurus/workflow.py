from datetime import datetime


class StegosaurusWorkflow:
    def __init__(self, sheets_client, db_client, sql_range):
        self.sheets_client = sheets_client
        self.db_client = db_client
        self.sql_range = sql_range

    def execute_workflow(self):
        print("Fetching SQL queries from Google Sheets...")
        sheet_info = self.sheets_client.read_range(self.sql_range)

        query_titles = [row[2] for row in sheet_info if row]
        query_output_sheets = [row[4] for row in sheet_info if row]
        query_output_tabs = [row[5] for row in sheet_info if row]
        sql_queries = [row[6] for row in sheet_info if row]
        execute_flags = [row[7] for row in sheet_info if row]

        if not sql_queries:
            raise ValueError("No SQL queries found.")

        print(f"Executing {len(sql_queries)} queries...")
        self.db_client.connect()

        for i, query in enumerate(sql_queries):
            if execute_flags[i] == "1":
                print(f"Executing query {i + 1}: {query_titles[i]} ..")
                results = self.db_client.execute_query(query)
                if results:
                    try:
                        self.sheets_client.write_range(query_output_sheets[i], f"{query_output_tabs[i]}!A1", results)
                        self.sheets_client.write_range(self.sheets_client.sheet_id, f"steg!J{i+2}", [["PASS"]])
                        current_timestamp = datetime.now()
                        self.sheets_client.write_range(self.sheets_client.sheet_id, f"steg!I{i+2}", [[current_timestamp.strftime("%Y-%m-%d %H:%M:%S")]])
                        
                        print(f"SUCCESS. Results written to {query_output_tabs[i]}.. \n")
                    except:
                        print("FAILURE. Check if output tab exists. \n")
                        self.sheets_client.write_range(self.sheets_client.sheet_id, f"steg!J{i+2}", [["FAIL"]])
                else:
                    self.sheets_client.write_range(self.sheets_client.sheet_id, f"steg!J{i+2}", [["FAIL"]])
        self.db_client.close_connection()
