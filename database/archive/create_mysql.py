import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root1234"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE hsi")