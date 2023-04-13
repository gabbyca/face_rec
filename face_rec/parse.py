import faceRec
from datetime import datetime
import _strptime
import schedule 
from datetime import timedelta


def updateFile(): 
    finalFile = open("finalData.txt","w")
    today = datetime.now().date()
    date = today.strftime('%d-%m-%Y')

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

schedule.every(24).hours.do(updateFile)

while True: 
    schedule.run_pending()
    time.sleep(180)


            
            
