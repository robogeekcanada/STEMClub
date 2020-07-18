#cat_ears_face_detection.py

import cv2
import numpy as np

cam = cv2.VideoCapture(0)

GREEN = (0,255,0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

while (cam.isOpened()):

    ret, frame = cam.read()

    if ret:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor =1.1,
                                              minNeighbors =5, minSize= (30,30))

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), GREEN, 2)

        cv2.imshow("Faces found", frame)

        if cv2.waitKey(1) == 27:
            break

cam.release()
cv2.destroyAllWindows()
