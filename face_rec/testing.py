import cv2

camera = 0
stream = cv2.VideoCapture(camera)


while True:
    ret, frame = stream.read()
    cv2.imshow('Webcam', frame)  
          
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break