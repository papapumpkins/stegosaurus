import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import date, datetime


class GoogleSheetsClient:
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds = self._authenticate()
        self.service = build('sheets', 'v4', credentials=self.creds)
    
    def _authenticate(self):
        """Handles OAuth 2.0 authentication flow for user."""
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
        """Reads a specified range of cells from the Google Sheet."""
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.sheet_id, range=range_name).execute()
        values = result.get('values', [])
        return values

    def write_range(self, output_sheet_id, range_name, values):
        serialized_values = [
            [str(item) if isinstance(item, (date, datetime)) else item for item in row]
            for row in values
        ]

        sheet = self.service.spreadsheets()
        body = {'values': serialized_values}
        sheet.values().update(
            spreadsheetId=output_sheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
