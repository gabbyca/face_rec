import faceRec as faceRec
from datetime import datetime
import schedule
from datetime import timedelta
import time


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
    for key in dict:
        arrival_time = dict[key]["Arrived"]
        departure_time = dict[key]["Left"]
        arrival_time_obj = datetime.strptime(arrival_time, '%I:%M:%S %p')
        departure_time_obj = datetime.strptime(departure_time, '%I:%M:%S %p')
        total_time = departure_time_obj - arrival_time_obj
        finalFile.write(f"{date}  \n{key} \n Arrival:{arrival_time} \n Departure:{departure_time} \n Total:{total_time} \n")
    finalFile.close()

updateFile()
schedule.every(24).hours.do(updateFile)
while True: 
    schedule.run_pending()
    time.sleep(20) 
