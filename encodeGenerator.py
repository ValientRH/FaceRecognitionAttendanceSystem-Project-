import cv2
import face_recognition
import pickle
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"-------URL-----------",
    'storageBucket':"-------URL-----------"
})

# importing students images
folderPath = 'Images'
imagePath = os.listdir(folderPath)
imageList = []
studentIds = []
for path in imagePath:
    imageList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
# Encoding Every Image
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("Encoding Started ... ... ")
currentEncodeList = findEncodings(imageList)
currentEncodeListIds = [currentEncodeList,studentIds]
print("Encoding Complete")
# print(currentEncodeList)

file = open("EncodeFile.p","wb")
pickle.dump(currentEncodeListIds,file)
file.close()
print("File saved")
