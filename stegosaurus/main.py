import argparse
from stegosaurus.pipeline import PipelineManager
from stegosaurus.interactive import interactive_run
from stegosaurus.config import HELP_TEXT

def main():
    parser = argparse.ArgumentParser(description="Stegosaurus CLI")
    parser.add_argument("command", nargs="?", help="Command to execute")
    parser.add_argument("args", nargs="*", help="Arguments for the command")
    
    args = parser.parse_args()
    command = args.command
    arguments = args.args

    manager = PipelineManager()

    if not command:
        print(HELP_TEXT)
        return

    if command == "create":
        if len(arguments) != 2:
            print("Usage: steg create <pipeline_name> <sheet_id>")
        else:
            pipeline_name, sheet_id = arguments
            manager.create_pipeline(pipeline_name, sheet_id)

    elif command == "list":
        manager.list_pipelines()

    elif command == "delete":
        if len(arguments) != 1:
            print("Usage: steg delete <pipeline_name>")
        else:
            pipeline_name = arguments[0]
            manager.delete_pipeline(pipeline_name)

    elif command == "run":
        if len(arguments) == 1:
            # Saved pipeline mode: run the pipeline by its name
            pipeline_name = arguments[0]
            manager.run_pipeline(pipeline_name)
        else:
            # Interactive mode: no pipeline name provided
            interactive_run()

    elif command == "clear_credentials":
        from stegosaurus.database import clear_credentials
        clear_credentials()

    elif command == "help":
        print(HELP_TEXT)

    else:
        print("Unknown command. Use 'steg help'")

if __name__ == "__main__":
    main()
