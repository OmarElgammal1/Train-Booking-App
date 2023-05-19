# Import necessary libraries
import sys
import pyodbc as odbc
import pandas as pnda

# Define the needed attributes for the connection string
# Run ```SELECT @@SERVERNAME``` on MS SQL server to find YOUR_SERVER_NAME
SERVER_NAME = 'YOUR_SERVER_NAME'
DATABASE_NAME = 'TrainBooking'

connection_string = f"""
    DRIVER={"SQL SERVER"};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

def deleteTrip(tripID):
    # Connect to the database
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    # Check if the customer is already booked on the trip
    cursor.execute(f"""
        SELECT tripID From SEAT
        Where tripID = {tripID} AND customerID IS NOT NULL
    """)

    # Check if the customer is already booked on the trip
    if cursor.fetchone() is not None:
        return False;

    # If no seats reserved for this trip then it gets deleted
    cursor.execute(f"""
        DELETE FROM SEAT
        WHERE tripID = {tripID};
        DELETE FROM TRIPS
        WHERE tripID = {tripID};
    """)

    
    # Close the connection
    if not conn.closed:
        conn.close()
    return True;

def deleteTrain(trainID):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()


    # Check if Train has no pending trips
    cursor.execute(f"""
        SELECT tripID From TRIP
        Where trainID = {trainID} AND depTime > GETDATE();
    """)

    # Check if the customer is already booked on the trip
    if cursor.fetchone() is not None:
        return False;

    # If no trips for this train it gets deleted
    cursor.execute(f"""
        DELETE FROM TRAIN
        WHERE trainID = {trainID};
    """)
    return True;
