import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="usuario",
        password="password", 
        database="inventario_api"
    )
