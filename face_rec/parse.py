import faceRec
from datetime import datetime
import _strptime
import schedule 
from datetime import timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials 
# credentials = service_account.Credentials.from_service_account_file('credentials.json')
# sheets_api = build('sheets', 'v4', credentials=credentials)


def updateFile(): 
    #opens finalData.txt to append
    finalFile = open("finalData.txt","a")
    today = datetime.now().date()
    date = today.strftime('\n%d-%m-%Y')

    with open("logs.txt", "r") as f:
        dict = {}
        lines = f.readlines()
        for line in lines:
            name, time = line.split(",")
            name = name.strip()
            time = time.strip()
            if name not in dict:
                dict[name] = {"Arrived": time, "Left": time}
            else:
                dict[name]["Left"] = time


    for key in dict:
        arrival_time = dict[key]["Arrived"]
        departure_time = dict[key]["Left"]
        arrival_time_obj = datetime.strptime(arrival_time, '%I:%M:%S %p')
        departure_time_obj = datetime.strptime(departure_time, '%I:%M:%S %p')
        total_time = departure_time_obj - arrival_time_obj
        finalFile.write(f"{date} \n \n{key} \n Arrival:{arrival_time} \n Departure:{departure_time} \n Total:{total_time} \n")
        # updateGoogleSheet('1Bl6i6xGl2_0BQjh1pWYwI8ko4__jJZfY3hEYDO-3cpE', 'finalData.txt')

# schedule.every(24).hours.do(updateFile)

# #wait 3 mins before checking for a scheduled rule
# while True: 
#     schedule.run_pending()
#     time.sleep(180) 



# def updateGoogleSheet(sheet_id, data):
#     # Read the contents of the "finalData.txt" file
#     with open(data, "r") as file:
#         lines = file.readlines()
    
#     spreadsheet_data = []
#     for line in lines:
#         row = [item.strip() for item in line.split('\n')]
#         spreadsheet_data.extend(row)

#     # Prepare the Google Sheets API request
#     body = {
#         'values': spreadsheet_data
#     }
    
#     # Specify the sheet and range to update 
#     range_name = 'Sheet1!A1'  
#     result = sheets_api.spreadsheets().values().update(
#         spreadsheetId=sheet_id,
#         range=range_name,
#         valueInputOption='RAW',
#         body=body
#     ).execute()
    
#     print(f'{result.get("updatedCells")} cells updated in Google Sheet.')

            
            
