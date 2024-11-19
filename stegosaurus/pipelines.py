import json
import os

class PipelineManager:
    PIPELINES_FILE = os.path.join(os.path.expanduser("~"), ".stegosaurus_pipelines.json")

    def __init__(self):
        if not os.path.exists(self.PIPELINES_FILE):
            with open(self.PIPELINES_FILE, "w") as f:
                json.dump({}, f)

    def _load_pipelines(self):
        with open(self.PIPELINES_FILE, "r") as f:
            return json.load(f)

    def _save_pipelines(self, pipelines):
        with open(self.PIPELINES_FILE, "w") as f:
            json.dump(pipelines, f, indent=4)

    def create_pipeline(self, name, sheet_id):
        pipelines = self._load_pipelines()
        if name in pipelines:
            print(f"Pipeline '{name}' already exists.")
            return
        pipelines[name] = {"sheet_id": sheet_id}
        self._save_pipelines(pipelines)
        print(f"Pipeline '{name}' created.")

    def run_pipeline(self, name, workflow_class):
        pipelines = self._load_pipelines()
        if name not in pipelines:
            print(f"Pipeline '{name}' does not exist.")
            return
        sheet_id = pipelines[name]["sheet_id"]
        print(f"Running pipeline '{name}' with sheet ID: {sheet_id}")
        workflow = workflow_class(sheet_id=sheet_id)
        workflow.execute_workflow()

    def list_pipelines(self):
        pipelines = self._load_pipelines()
        if not pipelines:
            print("No pipelines saved.")
            return
        print("Saved Pipelines:")
        for name, config in pipelines.items():
            print(f"- {name}: Sheet ID = {config['sheet_id']}")

    def delete_pipeline(self, name):
        pipelines = self._load_pipelines()
        if name not in pipelines:
            print(f"Pipeline '{name}' does not exist.")
            return
        del pipelines[name]
        self._save_pipelines(pipelines)
        print(f"Pipeline '{name}' deleted.")
