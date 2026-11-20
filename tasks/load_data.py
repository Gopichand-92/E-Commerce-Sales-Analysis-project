import mysql.connector
import pandas as pd
from getpass import getpass

# Step 1: Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=getpass("Enter MySQL password: "),
    database="ecommerce"
)

print("Successfully connected to MySQL!")

# Step 2: Load MySQL tables into Pandas DataFrames
customers_df = pd.read_sql("SELECT * FROM customers", connection)
categories_df = pd.read_sql("SELECT * FROM categories", connection)
products_df = pd.read_sql("SELECT * FROM products", connection)
orders_df = pd.read_sql("SELECT * FROM orders", connection)
order_items_df = pd.read_sql("SELECT * FROM order_items", connection)
payments_df = pd.read_sql("SELECT * FROM payments", connection)

# Step 3: Display record counts
print("\nTable Record Counts:")

print("Customers:", len(customers_df))
print("Categories:", len(categories_df))
print("Products:", len(products_df))
print("Orders:", len(orders_df))
print("Order Items:", len(order_items_df))
print("Payments:", len(payments_df))

# Inspect customer data
print("\nFirst 5 Customer Records:")
print(customers_df.head())

print("\nCustomer Data Shape:")
print(customers_df.shape)

print("\nCustomer Data Information:")
customers_df.info()

print("\nProduct Data Description:")
print(products_df.describe())

print("\nOrder Items Data Description:")
print(order_items_df.describe())


# Check missing values in all tables
print("\nMissing Values:")

print("\nCustomers:")
print(customers_df.isnull().sum())

print("\nProducts:")
print(products_df.isnull().sum())

print("\nOrders:")
print(orders_df.isnull().sum())

print("\nOrder Items:")
print(order_items_df.isnull().sum())

print("\nPayments:")
print(payments_df.isnull().sum())


# Check payment status counts
print("\nPayment Status Counts:")
print(payments_df["payment_status"].value_counts())

# Check payment methods
print("\nPayment Method Counts:")
print(payments_df["payment_method"].value_counts())


# Check missing payment dates by payment status
print("\nMissing Payment Dates by Status:")

print(
    payments_df.groupby("payment_status")["payment_date"]
    .apply(lambda x: x.isnull().sum())
)


# Check order status counts
print("\nOrder Status Counts:")
print(orders_df["order_status"].value_counts())

# Step 4: Close connection
connection.close()