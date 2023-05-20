def tripEmpty(cursor, tripID):
    # RETURNS ROWS WHERE TICKETS ARE BOOKED
    cursor.execute(f"""
        SELECT * from Seat
        WHERE tripID = {tripID} AND 
        customerID IS NOT NULL;
    """)
    # IF THERE ARE NO ROWS OF BOOKS
    if cursor.fetchone() is None:
        return True
    else:
        return False

def availableSeats(cursor, tripID):
    import pandas as pnda
    remainingSeats = pnda.DataFrame(cursor.execute(f"""
        SELECT COUNT(*) AS RemainingSeats FROM SEAT
        WHERE tripID = {tripID} AND customerID IS NULL;
    """)).values.tolist()[0][0][0]
    return remainingSeats

def emailExists(cursor, email):
    cursor.execute(f"""
        SELECT email FROM [USER]
        WHERE email = '{email}';
    """)
    if cursor.fetchone() is not None:
        return True
    else:
        return False

def getCustomerID(cursor, email):
    cursor.execute(f""" SELECT customerID FROM CUSTOMER WHERE email = '{email}'; """)
    queryResult = cursor.fetchone()
    return queryResult[0]