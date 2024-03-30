import cv2
from pyzbar.pyzbar import decode
import time
import mysql.connector
import datetime
import csv
import pywhatkit
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

# Function to count occurrences of a value in a dictionary
def countVal(dict, value):
    count = 0
    for keys, values in dict.items():
        if values == value:
            count += 1
    return count

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="first"
)
mycursor = mydb.cursor()

# Create a table to store attendance data if not exists
#mycursor.execute("CREATE TABLE IF NOT EXISTS Attendance (name VARCHAR(255), attendance VARCHAR(255), date DATE)")

# Open webcam
cap = cv2.VideoCapture(0)
delay_time = 1

# Initialize attendance variables
#attendance_list = {'ABHAY': 'Absent', 'vaishnav': 'Absent', 'SAYANGH': 'Absent'}
present_count = 0
absent_count = 0

# Loop to capture frames and process QR codes
while True:
    ret, frame = cap.read()
    qr_codes = decode(frame)

    if len(qr_codes) > 0:
        qr_code = qr_codes[0]
        name = qr_code.data.decode('utf-8')
        print(name)
        query = "SELECT * FROM dataset WHERE name = %s"
        mycursor.execute(query, (name,))
        result = mycursor.fetchone()  # Fetch one row
        
        if result:
            # Print values from the database
            print(f"Roll.No: {result[0]}")  # Assuming name is the first column
            print(f"Name: {result[1]}")
            print(f"sem: {result[2]}")
        else:
            print("Data not found")

        # Insert attendance data into MySQL table
        #sql = "INSERT INTO Attendance (name, attendance, date) VALUES (%s, %s, %s)"
        #val = (name, attendance_list[name], datetime.date.today())
        #mycursor.execute(sql, val)
        #mydb.commit()

        time.sleep(delay_time)

    cv2.imshow('Attendance', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        absent_count = countVal(attendance_list, "Absent")
        break

# Release webcam and close windows
cap.release()
cv2.destroyAllWindows()