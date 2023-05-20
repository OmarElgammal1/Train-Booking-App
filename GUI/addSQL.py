# Add a new train to the database (done by admins only)
# Train data must be passed in this specifc order [seatCount, trainType]
def addTrain(cursor, trainData):
    # Test the insert query to add new train with the passed data
    cursor.execute(f""" INSERT INTO TRAIN VALUES ({trainData[0]}, '{trainData[1]}'); """)
    cursor.commit()

# Add a new trip to the database (done by admins only)
# Trip data must be passed in this specifc order [trainID, fromLocation, toLocation, depTime, price]
def addTrip(cursor, tripData):
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
        cursor.commit()
    else:
        return False
    
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
    import pandas as pnda
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
    return True

# # Testing the addition of a new train
# # test = [500, 'Express']
# # addTrain(test)

# # Testing the addition of a new trip
# # test = [1, 'Tanta', 'Cairo', '2024-07-25 07:30:00', 50.0]
# # addTrip(test)

# # Close the cursor and the connection
# if not conn.closed:
#     cursor.close()
#     conn.close()
#     print("Connection Closed!")
