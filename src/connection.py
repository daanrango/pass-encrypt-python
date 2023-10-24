import mysql.connector


def conection_mysql():
    connection = mysql.connector.connect(
        host="172.24.34.43",
        user="root",
        port="3307",
        password="Admin_1234",
        database="test"
    )
    return connection
