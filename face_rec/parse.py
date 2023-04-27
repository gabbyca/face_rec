import faceRec as faceRec
from datetime import datetime
import schedule
from datetime import timedelta
import time
import sheets
from googleapiclient.errors import HttpError

SPREADSHEET_ID = '1OrLQDqKI6KA9PZvGapLAwvGDrYo_2giCfR3ikD-B_G8'
RANGE_NAME = 'Sheet1!A1'

def appendToSheet(service, range_name, values):
    try:
        body = {'values': values}
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, range=range_name,
            valueInputOption='RAW', insertDataOption='INSERT_ROWS',
            body=body).execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended to the spreadsheet.")
    except HttpError as error:
        print(f"An error occurred: {error}")
        result = None
    return result


def updateFile(): 
    finalFile = open("DataTxtFiles/finalData.txt","a") #open as append? 
    today = datetime.now().date()
    date = today.strftime('\n%m/%d/%Y')

    with open("DataTxtFiles/logs.txt", "r") as f:
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
    #might not need
    for key in dict:
        arrival_time = dict[key]["Arrived"]
        departure_time = dict[key]["Left"]
        arrival_time_obj = datetime.strptime(arrival_time, '%I:%M:%S %p')
        departure_time_obj = datetime.strptime(departure_time, '%I:%M:%S %p')
        total_time = departure_time_obj - arrival_time_obj
        finalFile.write(f"{date}  \n{key} \n Arrival:{arrival_time} \n Departure:{departure_time} \n Total:{total_time} \n")
    #end might not need
    service = sheets.get_service()
    for key in dict:
        arrival_time = dict[key]["Arrived"]
        departure_time = dict[key]["Left"]
        arrival_time_obj = datetime.strptime(arrival_time, '%I:%M:%S %p')
        departure_time_obj = datetime.strptime(departure_time, '%I:%M:%S %p')
        total_time = departure_time_obj - arrival_time_obj
        data_to_append = [
            [date, key, f"Arrival: {arrival_time}", f"Departure: {departure_time}", f"Total: {total_time}"]
        ]
        appendToSheet(service, RANGE_NAME, data_to_append)
    finalFile.close()

updateFile()
schedule.every(24).hours.do(updateFile)
while True: 
    schedule.run_pending()
    time.sleep(20) 
