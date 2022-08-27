from typing import ClassVar
import cv2
import numpy as np
import os
from datetime import datetime
import face_recognition
from face_recognition.api import compare_faces, face_distance

pathToImages1 = '/home/jetno/Desktop/VSC/Advanced AI_Assistant/source/riva_face_recognition/Images/images1'
pathToImages2 = '/home/jetno/Desktop/VSC/Advanced AI_Assistant/source/riva_face_recognition/Images/images2'
images1 = []
images2 = []
classNames = []
classNamesA = []

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

mylist = os.listdir(pathToImages1)
for cls in mylist:
    curImg = cv2.imread(f'{pathToImages1}/{cls}')
    images1.append(curImg)
    classNames.append(os.path.splitext(cls)[0])

encodeListAccess = findEncodings(images1)
print('Encoding1 Complete')

mylist = os.listdir(pathToImages2)
for cl in mylist:
    curImg = cv2.imread(f'{pathToImages2}/{cl}')
    images2.append(curImg)
    classNamesA.append(os.path.splitext(cl)[0])

encodeListNoAccess = findEncodings(images2)
print('Encoding2 Complete')    

def markTime(name):
    with open('/home/jetno/Desktop/VSC/Advanced AI_Assistant/source/riva_face_recognition/time.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}') 

def start_face_rec():

    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    rows, cols, _ = frame.shape

    while True:

        success, img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matchesAccess = face_recognition.compare_faces(encodeListAccess, encodeFace)
            faceDisAccess = face_recognition.face_distance(encodeListAccess, encodeFace)
            matchesNoAccess = face_recognition.compare_faces(encodeListNoAccess, encodeFace)
            faceDisNoAccess = face_recognition.face_distance(encodeListNoAccess, encodeFace)
            matchIndexA = np.argmin(faceDisAccess)
            matchIndexNA = np.argmin(faceDisNoAccess)

            if matchesAccess[matchIndexA]:
                name = classNames[matchIndexA].upper() 
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                markTime(name)
                # print(faceDisAccess)

                cv2.putText(img,'success',(x1+8,y1-10),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.rectangle(img, (x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

            if matchesNoAccess[matchIndexNA]:
                name = classNamesA[matchIndexNA].upper() 
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                markTime(name)
                # print(faceDisNoAccess)

                cv2.putText(img,'FAIL',(x1+30,y1-10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                cv2.rectangle(img, (x1,y1),(x2,y2),(0,0,255),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

        cv2.imshow('Webcam', img)
        key = cv2.waitKey(1)

        if key == 27:
            break

    print("Stopping as you wish.")
    cap.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     start_face_rec()
    