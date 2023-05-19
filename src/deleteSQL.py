# Import necessary libraries
import pyodbc as odbc

# Define the needed attributes for the connection string
# Run ```SELECT @@SERVERNAME``` on MS SQL server to find YOUR_SERVER_NAME
SERVER_NAME = 'DESKTOP-UF4LPT6'
DATABASE_NAME = 'TrainBooking'

connection_string = f"""
    DRIVER={"SQL SERVER"};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""
# Connect to the database
conn = odbc.connect(connection_string)
cursor = conn.cursor()

def deleteTrip(tripID):

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
    cursor.commit()
    # Close the connection
    if not conn.closed:
        conn.close()
    return True

def deleteTrain(trainID):
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
    cursor.commit()
    return True

def deleteUser(email):
    cursor.execute(f'''
        DELETE FROM [USER]
        WHERE [USER].email = '{email}'
    ''')
    cursor.commit()
    return True