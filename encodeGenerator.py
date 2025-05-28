import cv2
import face_recognition
import pickle
import os

# importing students images
folderPath = 'Images'
imagePath = os.listdir(folderPath)
imageList = []
studentIds = []
for path in imagePath:
    imageList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
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
