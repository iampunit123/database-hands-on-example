import mysql.connector

# Connect to MySQL Server
conn = mysql.connector.connect(
    host="localhost",
    user="", # Add user
    password="" # Add your password
)

# Create a cursor object
cursor = conn.cursor()

# Create a new database
database_name = "" # Add a unique Database name
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

print(f"Database '{database_name}' created successfully!")

# Close the connection
cursor.close()
conn.close()
