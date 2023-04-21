import cv2
import time
import numpy as np
import os
from pathlib import Path
import datetime
from datetime import datetime
from pytz import timezone
import face_recognition



#camera = 'tcp://192.168.1.252:5000'
stream = cv2.VideoCapture(0)

#face_recognition
gabby_image = face_recognition.load_image_file("FacesDatabase/Gabby.png")
gabby_face_encoding = face_recognition.face_encodings(gabby_image)[0]

layne_image = face_recognition.load_image_file("FacesDatabase/Layne.png")
layne_face_encoding = face_recognition.face_encodings(layne_image)[0]

sam_image = face_recognition.load_image_file("FacesDatabase/Sam.png")
sam_face_encoding = face_recognition.face_encodings(sam_image)[0]

reid_image = face_recognition.load_image_file("FacesDatabase/Reid.png")
reid_face_encoding = face_recognition.face_encodings(reid_image)[0]

anthony_image = face_recognition.load_image_file("FacesDatabase/Anthony.png")
anthony_face_encoding = face_recognition.face_encodings(anthony_image)[0]

bella_image = face_recognition.load_image_file("FacesDatabase/Bella.png")
bella_face_encoding = face_recognition.face_encodings(bella_image)[0]

maya_image = face_recognition.load_image_file("FacesDatabase/Maya.png")
maya_face_encoding = face_recognition.face_encodings(maya_image)[0]

sara_image = face_recognition.load_image_file("FacesDatabase/Sara.png")
sara_face_encoding = face_recognition.face_encodings(sara_image)[0]

tymoffi_image = face_recognition.load_image_file("FacesDatabase/Tymoffi.png")
tymoffi_face_encoding = face_recognition.face_encodings(tymoffi_image)[0]

owen_image = face_recognition.load_image_file("FacesDatabase/Owen.png")
owen_face_encoding = face_recognition.face_encodings(owen_image)[0]

juan_image = face_recognition.load_image_file("FacesDatabase/Juan.png")
juan_face_encoding = face_recognition.face_encodings(juan_image)[0]


known_face_encodings = [
    gabby_face_encoding,
    layne_face_encoding, 
    sam_face_encoding,
    reid_face_encoding,
    anthony_face_encoding,
    bella_face_encoding,
    maya_face_encoding,
    sara_face_encoding,
    tymoffi_face_encoding, 
    owen_face_encoding, 
    juan_face_encoding,
]
known_face_names = [
    "Gabby", 
    "Layne", 
    "Sam", 
    "Reid", 
    "Anthony", 
    "Bella", 
    "Maya", 
    "Sara", 
    "Tymoffi", 
    "Owen", 
    "Juan", 
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
students = []

#write video
fps = int(stream.get(cv2.CAP_PROP_FPS))
t= time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
output = cv2.VideoWriter('videoStorage/' + current_time + '.avi',cv2.VideoWriter_fourcc('M','J','P','G'),fps,(70,70))

attendanceFile = open("DataTxtFiles/attendance.txt","w")
logsFile = open("DataTxtFiles/logs.txt","w")


while True: 
    if stream.isOpened():
        break
    print("camera not found")
    time.sleep(10)
while True:
    connected = stream.isOpened()
    if not connected: 
        print("connection lost: retrying in 10 seconds")
        time.sleep(10)
        continue 
    ret, frame = stream.read()
    if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    students.append(name)
                    utc_time = datetime.now(timezone('UTC'))
                    est_time = utc_time.astimezone(timezone('US/Eastern'))
                    time_string = est_time.strftime("%I:%M:%S %p")
                    logsFile.write(name + " , " + time_string + "\n")
                face_names.append(name)
    #!!!!!!!!!!!
    #TO DO:CONDITIONAL FOR IF FACE IS FOUND LONGER THAN THRESHOLD THEN DOC IT
    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (203, 192, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (203, 192, 2550), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 4, bottom - 4), font, 1.0, (255, 255, 255), 1)


    cv2.imshow('Webcam', frame)
    output.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

inLab = list(set(students))
for _ in inLab: 
    attendanceFile.write(_ + " was in the lab\n")



attendanceFile.close()
logsFile.close()
stream.release()
output.release()
cv2.destroyAllWindows()
