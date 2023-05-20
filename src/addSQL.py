# Import necessary libraries
# import pandas as pnda

# Add a new train to the database (done by admins only)
# Train data must be passed in this specifc order [seatCount, trainType]
def addTrain(conn, cursor, trainData):
    cursor.execute(f""" INSERT INTO TRAIN VALUES ({trainData[0]}, '{trainData[1]}'); """)
    return True

# Add a new trip to the database (done by admins only)
# Trip data must be passed in this specifc order [trainID, fromLocation, toLocation, depTime, price]
def addTrip(tripData):
    # Check if the train exists or not before adding trip
    cursor.execute(f""" SELECT trainID FROM TRAIN WHERE trainID = {tripData[0]}; """)
    queryResult = cursor.fetchone()
    if queryResult is None:
        print("Train does NOT exist! Cannot add trip!")
        return ""
    # Test the insert query to add a new trip with the passed data
    # Check for duplicate trips before adding a new one
    try:
        cursor.execute(f"""
            INSERT INTO TRIP (trainID, fromLocation, toLocation, depTime, price)
            SELECT {tripData[0]}, '{tripData[1]}', '{tripData[2]}', '{tripData[3]}', {tripData[4]}
            WHERE NOT EXISTS (
                SELECT * FROM TRIP
                WHERE trainID = {tripData[0]}
                AND depTime = '{tripData[3]}'
            );
        """)
        # Check the number of affected rows
        if cursor.rowcount > 0:
            print(cursor.rowcount, "row(s) affected!")
        else:
            print("There is already a trip on this train at the same time!")
            print("Cannot add the same trip details more than one time!")
            return ""
    except Exception as e:
        cursor.rollback()
        print(e)
        print("Transaction Rollback! Insertion Failed!")
        return ""
    else:
        print("Trip Added Successfully!")
        cursor.commit()
    # Select query to get the trip ID
    selectQuery = f"""
        SELECT tripID FROM TRIP
        WHERE trainID = {tripData[0]}
        AND fromLocation = '{tripData[1]}'
        AND toLocation = '{tripData[2]}'
        AND depTime = '{tripData[3]}'
        AND price = {tripData[4]};
    """
    # Parse the DataFrame into a list
    listOfIDs = pnda.DataFrame(cursor.execute(selectQuery)).values.tolist()
    # Check for the returned number of ids, if they're more than one id
    # Return the last tripID that was added, otherwise return the first one
    if(len(listOfIDs) > 1):
        tripID = listOfIDs[-1][-1][0]
    else:
        tripID = listOfIDs[0][0][0]
    # Get the number of seats of the selected train
    trainSeatCount = cursor.execute(f"""
        SELECT seatCount FROM TRAIN
        WHERE trainID = {tripData[0]}; """).fetchone()[0]
    # Insert new records in the SEAT table with customerID set to NULL
    # According to the number of seats in the train associated with the added trip
    while trainSeatCount >= 1:
        cursor.execute(f" INSERT INTO SEAT VALUES ({tripID}, NULL); ")
        trainSeatCount -= 1
    cursor.commit()
    # Return the trip id that was just added
    print("Added trip ID:", tripID)
    return tripID

# Testing the addition of a new train
# test = [500, 'Express']
# addTrain(test)

# Testing the addition of a new trip
# test = [1, 'Tanta', 'Cairo', '2024-07-25 07:30:00', 50.0]
# addTrip(test)
