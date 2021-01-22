import cv2
import numpy as np
import face_recognition
import os
import ctypes
import winsound
from datetime import datetime

path ='ImageBasic'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def blockPerson():
    print("ANYONE TO BLOCK?")
    x = input()
    if x == "no" or "":
        return
    if x =="yes":
        print("WHO TO BLOCK?")
        y = input()
        return y

def tracking(name):
    with open('Tracking.csv', 'r+') as f:

        myList = f.readlines()
        nameList = []
        for line in myList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')



encodeListKnown = findEncodings(images)
blockPersonName = blockPerson()
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations((imgS))
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)

        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                tracking(name)
                if name == blockPersonName:
                    winsound.Beep(2500, 3000)
                    ctypes.windll.user32.MessageBoxW(0, "BLOCKED PERSON!", "GET OUT!!!", 1)

                y1,x2,y2,x1 = faceLoc
                cv2.rectangle(img, (x1, y1), (x2,y2), (0,0,255),2)
                cv2.rectangle(img, (x1, y2-35), (x2,y2), (0,0,255), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)


    cv2.imshow('Webcam', img)
    cv2.waitKey(1)




