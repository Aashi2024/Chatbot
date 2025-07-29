import pyrebase

config = {
  "apiKey": "AIzaSyDXobsjqjHPq_QbYSlIb7q7H-ap09Ru9AQ",
  "authDomain": "first-dbproject.firebaseapp.com",
  "databaseURL": "https://first-dbproject-default-rtdb.asia-southeast1.firebasedatabase.app",
  "storageBucket": "first-dbproject.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the database service
db = firebase.database()

#to check
print(db)

# Write some data
data = {"name": "John", "age": 30}
db.child("users").push(data)

# Read data
users = db.child("users").get()
for user in users.each():
    print(user.key(), user.val())