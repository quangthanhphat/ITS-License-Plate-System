import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",   # đổi nếu MySQL của bạn khác
            database="traffic_violation_system"
        )

        return connection

    except Error as e:
        print(f"Lỗi kết nối MySQL: {e}")
        return None


def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
