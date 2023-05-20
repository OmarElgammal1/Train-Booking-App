def deleteTrip(cursor, tripID):
    cursor.execute(f"""
        DELETE FROM SEAT
        WHERE tripID = {int(tripID)};
        DELETE FROM TRIPS
        WHERE tripID = {int(tripID)};
    """)

def deleteTrain(cursor, trainID):
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