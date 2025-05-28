import os
import pickle

import cvzone
import numpy as np
import cv2
import face_recognition

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
# video feed
while True:
    success, img = cap.read()
    # compressing Image
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgs)
    encodeCurrFrame = face_recognition.face_encodings(imgs,faceCurrFrame)



    Background[125:125 + 480, 145:145 + 640] = img
    Background[115:115+490, 820:820+340] = modeList[0]

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



    # cv2.imshow("webcam",img)
    cv2.imshow("Face Attendance", Background)
    cv2.waitKey(1)
