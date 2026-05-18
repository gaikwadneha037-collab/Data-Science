import mysql.connector

#mysql connection
conn  = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Neha@2503"
)

cursor = conn.cursor()

print("Connected Successfully!")