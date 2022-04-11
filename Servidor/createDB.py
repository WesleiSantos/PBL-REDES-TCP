import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="weslei200"
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE CIDADE_INTELIGENTE")
mycursor.execute("USE CIDADE_INTELIGENTE")
#mycursor.execute("CREATE TABLE lixeira (id INT NOT NULL AUTO_INCREMENT,host VARCHAR(30),port INT,status BOOLEAN NOT NULL,coord_x INT NOT NULL,coord_y INT NOT NULL,capacity INT NOT NULL,qtd_used DOUBLE NOT NULL,PRIMARY KEY(coord_x, coord_y), KEY (id))")
mycursor.execute("CREATE TABLE caminhao (id INT NOT NULL AUTO_INCREMENT,status BOOLEAN NOT NULL,coord_x INT NOT NULL,coord_y INT NOT NULL,capacity INT NOT NULL,qtd_used DOUBLE NOT NULL,next_trash INT,PRIMARY KEY(id))")

