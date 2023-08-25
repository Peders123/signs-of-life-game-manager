import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError




class Sheet():

    def __init__(self):

        self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        self.spreadsheet_id = "1q7hGgx_9-XTWRJkwQyD6vq-oBcFCR5rZHqvp0hjsJWQ"

        credentials = None

        if os.path.exists("sheets/token.json"):
            credentials = Credentials.from_authorized_user_file("sheets/token.json", self.scopes)

        if not credentials or not credentials.valid:

            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file("sheets/credentials.json", self.scopes)
                credentials = flow.run_local_server(port=0)

            with open("sheets/token.json", "w") as token:
                token.write(credentials.to_json())

        self.credentials = credentials


    def get_games_num(self):

        try:
            service = build("sheets", "v4", credentials=self.credentials)
            sheets = service.spreadsheets()

            result = sheets.values().get(spreadsheetId=self.spreadsheet_id, range="Overview!C3").execute()

            values = result.get("values", [])

            return values[0][0]

        except HttpError as error:
            print(error)

            return -1
        
    
    def write_game_data(self, data):

        keys = ['A','B','C','D','E','F','G','H','I']

        with open('sheets/layout.json', 'r') as f:
            layout = json.load(f)["Game"][0]

        for col in keys:

            try:
                service = build("sheets", "v4", credentials=self.credentials)
                sheets = service.spreadsheets()

                sheets.values().update(spreadsheetId=self.spreadsheet_id, range=f"Game - Data!{col}2",
                                       valueInputOption="USER_ENTERED", body={"values": [[data[layout[col]]]]}).execute()

            except HttpError as error:
                print(error)
