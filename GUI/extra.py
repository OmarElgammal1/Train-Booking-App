# Check if a certain trip is empty
def tripEmpty(cursor, tripID):
    # RETURNS ROWS WHERE TICKETS ARE BOOKED
    cursor.execute(f"""
        SELECT * FROM SEAT
        WHERE tripID = {tripID}
        AND customerID IS NOT NULL; """)
    # IF THERE ARE NO ROWS OF BOOKS
    if cursor.fetchone() is None:
        return True
    else:
        return False


# Check for remaining available seats in a certain trip
def availableSeats(cursor, tripID):
    # Import necessary library
    import pandas as pnda
    remainingSeats = pnda.DataFrame(cursor.execute(f"""
        SELECT COUNT(*) AS RemainingSeats FROM SEAT
        WHERE tripID = {tripID} AND customerID IS NULL;
    """)).values.tolist()[0][0][0]
    return remainingSeats


# Check if a certain email is already registered
def emailExists(cursor, email):
    cursor.execute(f" SELECT email FROM [USER] WHERE email = '{email}'; ")
    if cursor.fetchone() is not None:
        return True
    else:
        return False


# Get certain customerID from his/her email
def getCustomerID(cursor, email):
    cursor.execute(f" SELECT customerID FROM CUSTOMER WHERE email = '{email}'; ")
    queryResult = cursor.fetchone()
    return queryResult[0]


# Check if certain train has trips or not
def trainFree(cursor, trainID):
    cursor.execute(f" SELECT trainID FROM TRIP WHERE trainID = {trainID}; ")
    # If the train has trips allocated to it cannot delete, return False
    if cursor.fetchone() is not None:
        return False
    # Otherwise, the train is free and ready for deletion, return True
    return True
