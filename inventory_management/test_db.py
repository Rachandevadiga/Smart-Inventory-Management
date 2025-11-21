import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pratham923801",  # your password
        database="inventory"
    )
    if conn.is_connected():
        print("Database connected successfully!")
except Error as e:
    print("Error:", e)
finally:
    if conn.is_connected():
        conn.close()
