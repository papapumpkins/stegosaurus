from stegosaurus.sheets import GoogleSheetsClient, open_sheet
from stegosaurus.database import RedshiftClient
from stegosaurus.query_loader import load_query
from stegosaurus.config import REDSHIFT_CONFIG, TEMPLATE_SHEET_ID, DESTINATION_FOLDER_ID

def run_stegosaurus_interactive():
    """Runs the Stegosaurus workflow interactively by asking for Spreadsheet ID."""
    sheet_id = input("Enter Spreadsheet ID: ").strip()
    from stegosaurus.sheets import GoogleSheetsClient
    from stegosaurus.database import RedshiftClient
    from stegosaurus.workflow import StegosaurusWorkflow
    from stegosaurus.config import REDSHIFT_CONFIG, SQL_RANGE
    sheets_client = GoogleSheetsClient(sheet_id=sheet_id)
    db_client = RedshiftClient(**REDSHIFT_CONFIG)
    workflow = StegosaurusWorkflow(sheets_client, db_client, SQL_RANGE)
    workflow.execute_workflow()

def run_tyrannosaurus_risk_interactive():
    """
    Handles Tyrannosaurus Risk functionality interactively.
    
    Prompts for Business Name and Workspace ID.
    Copies the OG template sheet (using TEMPLATE_SHEET_ID) into the destination folder,
    naming it "Parker Underwriting Form V0.1 - <Business Name>".
    Loads the static query from queries.sql, replaces <workspace_id> with the input,
    executes the query on Redshift, clears the "input" tab of the new sheet, writes results there,
    and opens the new sheet in the browser.
    """
    business_name = input("Enter Business Name: ").strip()
    workspace_id = input("Enter Workspace ID: ").strip()

    # Construct new sheet name
    new_sheet_name = f"Parker Underwriting Form V0.2 - {business_name}"

    # Copy the template sheet into the destination folder
    from stegosaurus.config import TEMPLATE_SHEET_ID, DESTINATION_FOLDER_ID
    sheets_client = GoogleSheetsClient(sheet_id=TEMPLATE_SHEET_ID)  # for authentication
    new_sheet_id = sheets_client.copy_sheet(TEMPLATE_SHEET_ID, new_sheet_name, DESTINATION_FOLDER_ID)
    print(f"New sheet created with ID: {new_sheet_id}")

    # Load the static query from queries.sql and replace the workspace placeholder
    query = load_query("Tyrannosaurus Risk")
    if not query:
        print("Error: Query 'Tyrannosaurus Risk' not found in queries.sql.")
        return
    query = query.replace("<workspace_id>", workspace_id).strip()

    # Execute the query on Redshift
    db_client = RedshiftClient(**REDSHIFT_CONFIG)
    db_client.connect()
    results = db_client.execute_query(query)
    db_client.close_connection()

    if results is None:
        print("Error: Query execution returned no results or encountered an error.")
        return

    # Write the results to the "input" tab of the new sheet.
    # Clear the "input" tab first.
    new_sheet_client = GoogleSheetsClient(sheet_id=new_sheet_id)
    new_sheet_client.clear_range(new_sheet_id, "input!A:Z")
    new_sheet_client.write_range(new_sheet_id, "input!A1", values=results)
    print(f"Query results pasted into new sheet (tab 'input').")

    # Open the new sheet in the browser.
    open_sheet(new_sheet_id)

def interactive_run():
    """Interactive run mode when no pipeline name is provided.
    Prompts the user to select between Stegosaurus and Tyrannosaurus Risk.
    """
    print("Select your tool:")
    print("1. Stegosaurus")
    print("2. Tyrannosaurus Risk")
    
    choice = input("Enter Number: ").strip()
    
    if choice == "1":
        run_stegosaurus_interactive()
    elif choice == "2":
        run_tyrannosaurus_risk_interactive()
    else:
        print("Invalid selection.")
