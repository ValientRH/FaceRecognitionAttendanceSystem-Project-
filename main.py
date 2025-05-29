import os
import pickle

import cvzone
import numpy as np
import cv2
import face_recognition

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"-------URL-----------",
    'storageBucket':"-------URL-----------"
})

bucket = storage.bucket()

# Accessing webcam
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
# importing background
Background = cv2.imread('Resources/Background.png')
# importing mode images into a list
folderModes = 'Resources/modes'
modePath = os.listdir(folderModes)
modeList = []
for path in modePath:
    modeList.append(cv2.imread(os.path.join(folderModes, path)))


print("Importing Encodings")
#Load the encodings
file = open("EncodeFile.p","rb")
currentEncodeListIds = pickle.load(file)
currentEncodeList,studentIds = currentEncodeListIds
print("Encodings Downloaded")


modeType = 0
counter = 0
Currid = -1
imgStudents = []

# video feed
while True:
    success, img = cap.read()
    # compressing Image
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgs)
    encodeCurrFrame = face_recognition.face_encodings(imgs,faceCurrFrame)



    Background[125:125 + 480, 145:145 + 640] = img
    Background[115:115+490, 820:820+340] = modeList[modeType]

    if faceCurrFrame:

        for encoFace, faceLock in zip(encodeCurrFrame,faceCurrFrame):
            matches = face_recognition.compare_faces(currentEncodeList,encoFace)
            faceDis = face_recognition.face_distance(currentEncodeList, encoFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1,x2,y2,x1 = faceLock
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                bbox = 145+x1,125+y1, x2-x1,y2-y1
                Background = cvzone.cornerRect(Background,bbox,rt=0)
                Currid = studentIds[matchIndex]
                # print(Currid)
                if counter == 0:
                    cvzone.putTextRect(Background,"Laoding",(305,395))
                    cv2.imshow("Face Attendance", Background)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter!=0:

            if counter ==1:
                #Get the data
                stutentInfo = db.reference(f'Students/{Currid}').get()
                print(stutentInfo)
                #Get the image from the storage
                blob = bucket.get_blob(f'Images/{Currid}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudents = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                # Updating attendance
                datetimeObject = datetime.strptime(stutentInfo ['time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()


                if secondsElapsed>30:     #Time control
                    ref = db.reference(f'Students/{Currid}')
                    stutentInfo['attendance'] += 1
                    ref.child('attendance').set(stutentInfo['attendance'])
                    ref.child('time').set(datetime.now().strftime( "%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    Background[115:115 + 490, 820:820 + 340] = modeList[modeType]

            if modeType !=3:

                if 10<counter<20:

                    modeType = 2

                    Background[115:115 + 490, 820:820 + 340] = modeList[modeType]

                if counter<=10:

                    cv2.putText(Background,str(stutentInfo['name']),(840,455),
                                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(Background, str(stutentInfo['attendance']), (840, 155),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(Background, str(stutentInfo['id']), (940, 490),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(Background, str(stutentInfo['Batch']), (940, 535),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(Background, str(stutentInfo['Branch']), (980, 575),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                    Background[235:235+188, 927:927+125] = imgStudents




                counter+=1

                if counter>20:
                    counter = 0
                    modeType = 0
                    stutentInfo = []
                    imgStudents = []
                    Background[115:115 + 490, 820:820 + 340] = modeList[modeType]
    else:
        modeType = 0
        counter = 0

    # cv2.imshow("webcam",img)
    cv2.imshow("Face Attendance", Background)
    cv2.waitKey(1)
