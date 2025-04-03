# Configuration file for Stegosaurus

# 🔹 REDSHIFT DATABASE SETTINGS
REDSHIFT_CONFIG = {
    "host": "redshift-cluster.cnigckkzorkw.us-east-2.redshift.amazonaws.com",
    "port": 5439,
    "database": "parker",
    # Credentials are entered dynamically
}

POSTGRES_CONFIG = {
    "host": "parker.cluster-ro-cldpilcb9tyc.us-east-2.rds.amazonaws.com",
    "port": 5432,
    "database": "parker",
}

# 🔹 GOOGLE SHEETS SETTINGS
GOOGLE_SHEET_ID = '1x_dbVtZHyGLz_7ntXZaBWbCDmnSTwOrQ-cwppnwDUt8'
SQL_RANGE = 'Steg!$A$2:$K$51'  # Default range for query inputs in Stegosaurus

# 🔹 OG TEMPLATE SHEET FOR TYRANNOSAURUS RISK
TEMPLATE_SHEET_ID = '1rJoKSYKl4xAmtn1OL0gOuwSbNrt-IH2MKooa2a6GgNA'
DESTINATION_FOLDER_ID = '1e1gElWeOQ5UIAaAyMg_8rQcyXnHkrRk-'  # Replace with your Drive folder ID

# 🔹 HELP TEXT FOR CLI COMMANDS
HELP_TEXT = """
🔹 Stegosaurus CLI Commands:

📌 PIPELINE MODE:
    - steg create <pipeline_name> <sheet_id>  → Create a pipeline linked to a Google Sheet.
    - steg list                               → List all saved pipelines.
    - steg delete <pipeline_name>             → Delete a specific pipeline.
    - steg run <pipeline_name>                → Run a saved pipeline (reads queries from Google Sheet).

📌 INTERACTIVE MODE:
    - steg run  → If no pipeline name is given, prompts user:
        1. Stegosaurus (directly executes queries from a specified Google Sheet).
        2. Tyrannosaurus Risk (copies an OG template, then executes a pre-defined query using input Workspace ID).

📌 EXAMPLES:
    - Create a pipeline:
      $ steg create ltv_analysis_sheet 1x_dbVtZHyGLz_7ntXZaBWbCDmnSTwOrQ-cwppnwDUt8

    - Run a saved pipeline:
      $ steg run ltv_analysis_sheet

    - Directly execute queries in a spreadsheet:
      $ steg run
      (Select "1" for Stegosaurus and enter the Spreadsheet ID)

    - Execute Tyrannosaurus Risk query:
      $ steg run
      (Select "2", then enter Business Name and Workspace ID)

📌 HELP:
    - steg help  → Show this help message.

📌 CONTACT:
    If you encounter issues, reach out to: neel@getparker.com
"""
