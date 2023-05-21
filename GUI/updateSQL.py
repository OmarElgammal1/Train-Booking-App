# Update existing train details (done by admins only)
# Train data must be passed in this specifc order [seatCount, trainType, trainID]
def updateTrain(cursor, trainData):
    # Update query to update train details with the passed data
    cursor.execute(f"""
        UPDATE TRAIN
        SET seatCount = {trainData[0]},
        trainType = '{trainData[1]}'
        WHERE trainID = {trainData[2]}; """)
    cursor.commit()


# Update existing trip details (done by admins only)
# Trip data must be passed in this specifc order [tripID, trainID, fromLocation, toLocation, depTime, price]
def updateTrip(cursor, tripData):
    # Update query to update trip details with the passed data
    cursor.execute(f"""
        UPDATE TRIP
        SET trainID = {tripData[1]},
        fromLocation = '{tripData[2]}',
        toLocation = '{tripData[3]}',
        depTime = '{tripData[4]}',
        price = {tripData[5]}
        WHERE tripID = {tripData[0]};
        DELETE SEAT
        WHERE tripID = {tripData[0]};
        DECLARE @seatCount INT
        DECLARE @i INT = 0
        SELECT @seatCount = seatCount FROM TRAIN
        WHERE trainID  = {tripData[1]};
        WHILE @i < @seatCount
        BEGIN
            SET @i = @i + 1
            INSERT INTO SEAT (SEAT.tripID)
            SELECT TRIP.tripID FROM TRIP
            WHERE TRIP.tripID = {tripData[0]};
        END """)
    cursor.commit()


# Update existing user details (done by both admins & users)
# In case of ADMIN pass ==> [cursor, isAdmin, email, password]
# In case of CUSTOMER pass ==> [cursor, isAdmin, email, password, name, phoneNum]
def updateUser(cursor, isAdmin, email, password, *userData):
    # Update query to change admin password according to email
    if isAdmin:
        cursor.execute(f"""
            UPDATE [USER]
            SET password = '{password}'
            WHERE [USER].email = (
                SELECT email FROM ADMIN
                WHERE email = '{email}'); """)
        cursor.commit()
    # Update query to update customer details according to email
    else:
        cursor.execute(f"""
            UPDATE [USER]
            SET password = '{password}'
            WHERE [USER].email = (
                SELECT email FROM CUSTOMER
                WHERE email = '{email}');
            UPDATE [CUSTOMER]
            SET name = '{userData[0]}', phoneNum = '{userData[1]}'
            WHERE email = '{email}'; """)
        cursor.commit()
