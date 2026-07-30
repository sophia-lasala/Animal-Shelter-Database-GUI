import sqlite3 #Provides SQL support 
import hashlib #Allows for Hashes 
import secrets #Adds 'salt" to hashes to make them stronger
from datetime import date #Takes value of current date

conn = sqlite3.connect("shelter.db") #non lo so
cursor = conn.cursor() 

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    salt TEXT,
    pass_hash TEXT,
    role TEXT,
    intake_date TEXT
)
""") 
#Table: Users (id, username, salt, pass_hash, role, intake_date)
conn.commit()

#Variables for Users table

username = " "

salt = secrets.token_hex(16)

password = " "

hashed = hashlib.sha256((salt + password).encode()).hexdigest() #Creates hash with salt 

role = " " #Admin, User - make that drop down menu 

today = date.today()
formatted_date = today.strftime("%m/%d/%Y") #mm-dd-YYYY


user_data = (username, salt, hashed, role, formatted_date)
cursor.execute("INSERT INTO Users (username, salt, pass_hash, role, intake_date) VALUES (?, ?, ?, ?, ?)", user_data)

def login_page(): 
    while ((user_input != "1") or (user_input != "2")):
        print("Are you a first-time or existing user? Type: 1 - first-time || 2 - existing")
        user_input = input()
    if (user_input == "1"):
        print("Sign Up:")
        username = input("What would you like your username to be?")
        password = input("What would you like your password to be?")
        role = input("What is your role? Type: 'Admin' or 'User'")
        hashed = hashlib.sha256((salt + password).encode()).hexdigest()
        today = date.today()
        formatted_date = today.strftime("%m/%d/%Y") #mm-dd-YYYY
        user_data = (username, salt, hashed, role, formatted_date)
        cursor.execute("INSERT INTO Users (username, salt, pass_hash, role, intake_date) VALUES (?, ?, ?, ?, ?)", user_data)
        print ("Thank you!")
    print("Login:")


def print_database(): 
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
