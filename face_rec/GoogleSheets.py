import os
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

def get_credentials():
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return creds


def append_data_to_sheet(sheet_id, sheet_name, data):
    try:
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)

        request = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range=sheet_name + '!A1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': data}
        )
        response = request.execute()
        return response

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def main():
    sheet_id = 'YOUR_SPREADSHEET_ID'  # Replace with your Google Sheet ID
    sheet_name = 'RoboticsLabData'  # Replace with your desired sheet name

    with open("finalData.txt", "r") as f:
        lines = f.readlines()
        data = [line.strip().split('\n') for line in lines if line.strip()]

    response = append_data_to_sheet(sheet_id, sheet_name, data)

    if response:
        print("Data successfully added to the Google Sheet.")


if __name__ == '__main__':
    main()
