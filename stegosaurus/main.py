import argparse
import keyring
from stegosaurus.sheets import GoogleSheetsClient
from stegosaurus.database import RedshiftClient
from stegosaurus.workflow import StegosaurusWorkflow
from stegosaurus.config import REDSHIFT_CONFIG, SQL_RANGE
from stegosaurus.pipelines import PipelineManager


def clear_credentials():
    service_name = "stegosaurus_redshift"
    keyring.delete_password(service_name, "username")
    keyring.delete_password(service_name, "password")
    print("Credentials cleared.")


def show_help():
    help_text = """
    Stegosaurus commands:
    - steg create <pipeline_name> <sheet_id>: create new pipeline
    - steg run <pipeline_name>: run specified pipeline
    - steg list: list all saved pipelines
    - steg delete <pipeline_name>: delete specified pipeline
    - steg clear_credentials: clear saved db credentials

    contact: neel@getparker.com
    """
    print(help_text)


def run_workflow(sheet_id):    
    sheets_client = GoogleSheetsClient(sheet_id=sheet_id)
    db_client = RedshiftClient(**REDSHIFT_CONFIG)
    workflow = StegosaurusWorkflow(
        sheets_client=sheets_client,
        db_client=db_client,
        sql_range=SQL_RANGE
    )
    workflow.execute_workflow()


def main():
    parser = argparse.ArgumentParser(description="Stegosaurus CLI")
    parser.add_argument("command", nargs="?", help="")
    parser.add_argument("args", nargs="*", help="")

    args = parser.parse_args()
    command = args.command
    arguments = args.args

    manager = PipelineManager()

    if not command:
        print(f"<< STEGOSAURUS CLI >> \n {show_help()}")

    if command == "create":
        if len(arguments) != 2:
            print("Usage: steg create <pipeline_name> <sheet_id>")
        else:
            pipeline_name, sheet_id = arguments
            manager.create_pipeline(pipeline_name, sheet_id)

    elif command == "run":
        if len(arguments) != 1:
            print("Usage: steg run <pipeline_name>")
        else:
            pipeline_name = arguments[0]
            pipelines = manager._load_pipelines()
            if pipeline_name not in pipelines:
                print(f"Pipeline '{pipeline_name}' does not exist.")
            else:
                sheet_id = pipelines[pipeline_name]["sheet_id"]
                run_workflow(sheet_id)

    elif command == "list":
        manager.list_pipelines()

    elif command == "delete":
        if len(arguments) != 1:
            print("Usage: steg delete <pipeline_name>")
        else:
            pipeline_name = arguments[0]
            manager.delete_pipeline(pipeline_name)

    elif command == "clear_credentials":
        clear_credentials()

    elif command == "help":
        show_help()

    else:
        print("Unknown command. Use 'steg help'")


if __name__ == "__main__":
    main()
