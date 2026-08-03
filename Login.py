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

def verify_login(): #I have no clue how functions work in Python having to define before calling it is utterly ridiculous I must be doing something wrong
    #Verifies username and password to see if they match preexisting data in Users table 
    verify_user = input("Username: ")
    verify_pass = input("Password: ")

    cursor.execute(
        "SELECT salt, pass_hash FROM Users WHERE username = ?",
        (verify_user,)
    )
    #Looking for salt and hashed password based on username

    user_record = cursor.fetchone()

    if user_record is None:
        #if no username exists
        print("Username or password is incorrect.")
        return

    stored_salt = user_record[0] #Based on username get salt
    stored_hash = user_record[1] #Based on username get hash

    verify_hash = hashlib.sha256(
        (stored_salt + verify_pass).encode()
    ).hexdigest() #Recreate hash using inputted password and salt in table for username

    if verify_hash == stored_hash:
        #If it's the same hash it's the same password so everything's good!
        print("Welcome", verify_user)
    else:
        print("Username or password is incorrect.")

def login_page(): #Yet again the function system is so silly
    user_input = "0" #This doesn't mean anything I just needed it for my while loop
    while ((user_input != "1") and (user_input != "2")):
        print("Are you a first-time or existing user? Type: 1 - first-time || 2 - existing ")
        user_input = input() 
    if (user_input == "1"): #Pretty self explanatory, getting everything to make a new account
        print("Sign Up:")
        username = input("What would you like your username to be? ")
        password = input("What would you like your password to be? ")
        while (username == password):
            print("Note: password can not be same as username. ")
            password = input()
        role = input("What is your role? Type: 'Admin' or 'User' ") #I am not going to tackle this issue right now
        hashed = hashlib.sha256((salt + password).encode()).hexdigest()
        today = date.today()
        formatted_date = today.strftime("%m/%d/%Y") #mm-dd-YYYY
        user_data = (username, salt, hashed, role, formatted_date)
        cursor.execute("INSERT INTO Users (username, salt, pass_hash, role, intake_date) VALUES (?, ?, ?, ?, ?)", user_data)
        conn.commit()
        print ("Thank you!")
    verify_login() #call verify_login() function 

login_page() #call login_page function


def print_database(): #To test - prints every row of SQL User Table 
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

print_database() #call print_database() function 
