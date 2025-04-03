import json
import os
from stegosaurus.sheets import GoogleSheetsClient
from stegosaurus.database import RedshiftClient
from stegosaurus.workflow import StegosaurusWorkflow
from stegosaurus.config import REDSHIFT_CONFIG, SQL_RANGE

PIPELINES_FILE = os.path.expanduser("~/.stegosaurus_pipelines.json")

class PipelineManager:
    def __init__(self):
        if not os.path.exists(PIPELINES_FILE):
            with open(PIPELINES_FILE, "w") as f:
                json.dump({}, f)

    def _load_pipelines(self):
        with open(PIPELINES_FILE, "r") as f:
            return json.load(f)

    def _save_pipelines(self, pipelines):
        with open(PIPELINES_FILE, "w") as f:
            json.dump(pipelines, f, indent=4)

    def create_pipeline(self, name, sheet_id):
        pipelines = self._load_pipelines()
        pipelines[name] = {"sheet_id": sheet_id}
        self._save_pipelines(pipelines)
        print(f"Pipeline '{name}' created successfully.")

    def list_pipelines(self):
        pipelines = self._load_pipelines()
        if not pipelines:
            print("No pipelines saved.")
            return
        for name, config in pipelines.items():
            print(f"- {name}: Sheet ID = {config['sheet_id']}")

    def delete_pipeline(self, name):
        pipelines = self._load_pipelines()
        if name in pipelines:
            del pipelines[name]
            self._save_pipelines(pipelines)
            print(f"Pipeline '{name}' deleted successfully.")
        else:
            print(f"Pipeline '{name}' not found.")

    def run_pipeline(self, name):
        pipelines = self._load_pipelines()
        if name not in pipelines:
            print(f"Pipeline '{name}' does not exist.")
            return

        sheet_id = pipelines[name]["sheet_id"]
        print(f"Running pipeline '{name}' on sheet ID: {sheet_id}")
        sheets_client = GoogleSheetsClient(sheet_id=sheet_id)
        db_client = RedshiftClient(**REDSHIFT_CONFIG)
        workflow = StegosaurusWorkflow(sheets_client, SQL_RANGE)
        workflow.execute_workflow()
