import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="weslei200"
)

mycursor = mydb.cursor()
mycursor.execute("USE CIDADE_INTELIGENTE")
mycursor.execute("DROP TABLE IF EXISTS caminhao;")
mycursor.execute("DROP TABLE IF EXISTS lixeira;")

