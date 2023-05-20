# Import necessary libraries
import pyodbc as odbc

# Define the needed attributes for the connection string
# Run ```SELECT @@SERVERNAME``` on MS SQL server to find YOUR_SERVER_NAME

# Connect to MS SQL Server Database
conn = odbc.connect(f"""
    DRIVER={"SQL SERVER"};
    SERVER={"iSeFz-PC"};
    DATABASE={"TrainBooking"};
    Trust_Connection=yes; """)
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
            WHERE trainID = {trainData[2]}; """)
    except Exception as e:
        cursor.rollback()
        print(e)
        print("Transaction Rollback! Update Failed!")
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
            WHERE tripID = {tripData[0]}; """)
    except Exception as e:
        cursor.rollback()
        print(e)
        print("Transaction Rollback! Update Failed!")
        return ""
    else:
        print("Trip Updated Successfully!")
        cursor.commit()


# Update existing user details (done by both admins & users)
# In case of ADMIN pass ==> [isAdmin, email, password]
# In case of CUSTOMER pass ==> [isAdmin, email, password, name, phoneNum]
def updateUser(isAdmin, email, password, *userData):
    # Update query to change admin password according to email
    if isAdmin:
        try:
            cursor.execute(f"""
                UPDATE [USER]
                SET password = '{password}'
                WHERE [USER].email = (
                    SELECT email FROM ADMIN
                    WHERE email = '{email}'); """)
        except Exception as e:
            cursor.rollback()
            print(e)
            print("Transaction Rollback! Update Failed!")
            return ""
        else:
            print("Admin Password Changed Successfully!")
            cursor.commit()
    # Update query to update customer details according to email
    else:
        try:
            cursor.execute(f"""
                UPDATE [USER]
                SET password = '{password}'
                WHERE [USER].email = (
                    SELECT email FROM CUSTOMER
                    WHERE email = '{email}');
                UPDATE [CUSTOMER]
                SET name = '{userData[0]}', phoneNum = '{userData[1]}'
                WHERE email = '{email}'; """)
        except Exception as e:
            cursor.rollback()
            print(e)
            print("Transaction Rollback! Update Failed!")
            return ""
        else:
            print("Customer Data Updated Successfully!")
            cursor.commit()


# Close the cursor and the connection
if not conn.closed:
    cursor.close()
    conn.close()
    print("Connection Closed!")