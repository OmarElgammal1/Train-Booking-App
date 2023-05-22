# Import necessary libraries
import pyodbc as odbc
import sys

# Connect to our database TrainBooking
# Run ```SELECT @@SERVERNAME``` on MS SQL server to find YOUR_SERVER_NAME
def connect():
    try:
        connection = odbc.connect(f"""
            DRIVER={"SQL SERVER"};
            SERVER={"YOUR_SERVER_NAME"};
            DATABASE={"TrainBooking"};
            Trust_Connection=yes; """)
    except Exception as e:
        print(e)
        print("Task is Terminated!")
        sys.exit(0)
    return connection

# Close & end the connection with the database
def close(connection):
    if not connection.closed:
        connection.close()
