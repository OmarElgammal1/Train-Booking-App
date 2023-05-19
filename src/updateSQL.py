# Import necessary libraries
import pyodbc as odbc

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

# Connect to MS SQL Server Database
conn = odbc.connect(connection_string)
cursor = conn.cursor()

# Update existing train details (done by admins only)
# Train data must be passed in this specifc order [seatCount, trainType, trainID]
def updateTrain(trainData):
    # Check if the train exists or not before updating
    cursor.execute(f""" SELECT trainID FROM TRAIN WHERE trainID = {trainData[2]}; """)
    queryResult = cursor.fetchone()
    if queryResult is None:
        print("Train does NOT exist! Nothing to update!")
        return ""
    # Test the update query to update train details with the passed data
    try:
        cursor.execute(f"""
            UPDATE TRAIN
            SET seatCount = {trainData[0]},
            trainType = '{trainData[1]}'
            WHERE trainID = {trainData[2]};
        """)
    except Exception as e:
        cursor.rollback()
        print(e)
        print("Transaction Rollback! Insertion Failed!")
        return ""
    else:
        print("Train Updated Successfully!")
        cursor.commit()


# Update existing trip details (done by admins only)
# Trip data must be passed in this specifc order [tripID, trainID, fromLocation, toLocation, depTime, price]
def updateTrip(tripData):
    # Check if the trip exists or not before updating
    cursor.execute(f""" SELECT tripID FROM TRIP WHERE tripID = {tripData[0]}; """)
    queryResult = cursor.fetchone()
    if queryResult is None:
        print("Trip does NOT exist! Nothing to update!")
        return ""
    # Check if the train exists or not before updating
    cursor.execute(f""" SELECT trainID FROM TRAIN WHERE trainID = {tripData[1]}; """)
    queryResult = cursor.fetchone()
    if queryResult is None:
        print("Train does NOT exist! Nothing to update!")
        return ""
    # Test the update query to update trip details with the passed data
    try:
        cursor.execute(f"""
            UPDATE TRIP
            SET trainID = {tripData[1]},
            fromLocation = '{tripData[2]}',
            toLocation = '{tripData[3]}',
            depTime = '{tripData[4]}',
            price = {tripData[5]}
            WHERE tripID = {tripData[0]};
        """)
    except Exception as e:
        cursor.rollback()
        print(e)
        print("Transaction Rollback! Insertion Failed!")
        return ""
    else:
        print("Trip Updated Successfully!")
        cursor.commit()

# Test the update train
# test = [300, 'Local', 1]
# updateTrain(test)

# Test the update trip
# test = [1, 2, 'Cairo', 'Assiut', '2023-09-12 22:00:00', 100]
# updateTrip(test)

# Close the cursor and the connection
if not conn.closed:
    cursor.close()
    conn.close()
    print("Connection Closed!")