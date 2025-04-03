import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import date, datetime
import webbrowser

class GoogleSheetsClient:
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        # Added Drive scope for copy operations
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = self._authenticate()
        self.service = build('sheets', 'v4', credentials=self.creds)
    
    def _authenticate(self):
        token_path = os.path.join(os.path.expanduser("~"), ".stegosaurus", "token.json")
        credentials_path = "client_secret.json"
        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.scopes)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.scopes)
                creds = flow.run_local_server(port=0)
            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())
        return creds

    def read_range(self, range_name):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.sheet_id, range=range_name).execute()
        return result.get('values', [])
    
    def write_range(self, output_sheet_id, range_name, values):
        def serialize_item(item):
            if isinstance(item, (date, datetime)):
                return str(item)
            elif isinstance(item, (list, tuple)):
                # Convert lists/tuples to a comma-separated string.
                return ', '.join(str(x) for x in item)
            else:
                return item

        serialized_values = [
            [serialize_item(item) for item in row] for row in values
        ]
        sheet = self.service.spreadsheets()
        body = {'values': serialized_values}
        sheet.values().update(
            spreadsheetId=output_sheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()

    def clear_range(self, output_sheet_id, range_name):
        sheet = self.service.spreadsheets()
        sheet.values().clear(
            spreadsheetId=output_sheet_id,
            range=range_name,
            body={}
        ).execute()

    def copy_sheet(self, template_sheet_id, new_sheet_name, destination_folder_id):
        """
        Copies the template sheet to create a new sheet with new_sheet_name,
        and places it in the specified destination folder.
        Returns the new sheet's ID.
        """
        drive_service = build('drive', 'v3', credentials=self.creds)
        file_metadata = {
            "name": new_sheet_name,
            "parents": [destination_folder_id]
        }
        copied_file = drive_service.files().copy(
            fileId=template_sheet_id,
            body=file_metadata,
            fields="id"
        ).execute()
        return copied_file.get("id")

def open_sheet(sheet_id):
    """Opens the Google Sheet in the default web browser."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    webbrowser.open(url)
