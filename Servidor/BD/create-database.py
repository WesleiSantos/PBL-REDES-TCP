import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="weslei200"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE CIDADE_INTELIGENTE")
