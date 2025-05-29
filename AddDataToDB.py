import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://image-database-40958-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref = db.reference('Students')

data = {
    "100101":
        {
            "name": "Shubham Kumar",
            "Branch": "CSE",
            "Batch": "2021-2015",
            "id": 1,
            "attendance":0,
            "time":"2025-05-05 00:54:34"
        },
    "100102":
        {
            "name": "Divyansh Kaushik",
            "Branch": "CSE",
            "Batch": "2021-2015",
            "id": 2,
            "attendance":0,
            "time":"2025-05-05 00:54:34"
        },
    "100104":
        {
            "name": "Navin Yadav",
            "Branch": "CSE",
            "Batch": "2021-2015",
            "id":4,
            "attendance":0,
            "time":"2025-05-05 00:54:34"
        }
}

for key,value in data.items():
    ref.child(key).set(value)

