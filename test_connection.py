
import mysql.connector
from getpass import getpass

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=getpass("Enter MySQL password: "),
    database="ecommerce"
)

if connection.is_connected():
    print("Successfully connected to MySQL database!")

    cursor = connection.cursor()

    # Retrieve total number of customers
    cursor.execute("SELECT COUNT(*) FROM customers")

    result = cursor.fetchone()

    print("Total Customers:", result[0])

    cursor.close()

connection.close()
