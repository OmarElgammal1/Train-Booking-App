def bookTrip(cursor, customerID, tripID, nSeats):
    # Check if the customer is already booked on the trip
    cursor.execute(f"""
        UPDATE TOP ({nSeats}) SEAT
        SET customerID = '{customerID}'
        WHERE (tripID = '{tripID}' AND customerID IS NULL);
    """)
    cursor.commit()
    return True;

def cancelTrip(cursor, customerID, tripID):
    # Check if the customer is already booked on the trip
    cursor.execute(f"""
        UPDATE SEAT
        SET customerID = NULL
        WHERE (tripID = '{tripID}' AND customerID = '{customerID}');
    """)
    return True;

def viewCustomerTrips(cursor, customerID):
    cursor.execute(f"""
        SELECT SEAT.tripID, TRIP.trainID, TRIP.fromLocation, TRIP.toLocation, TRIP.depTime, COUNT(SEAT.seatNum) AS TotalSeats, TRIP.price
        FROM TRIP
        INNER JOIN SEAT ON TRIP.tripID = SEAT.tripID
        WHERE SEAT.customerID = '{customerID}'
        GROUP BY SEAT.tripID, TRIP.trainID, TRIP.fromLocation, TRIP.toLocation, TRIP.depTime, TRIP.price;
    """)

    rows = cursor.fetchall()

    # split DATETIME and add it correctly to list
    # Convert the rows to a Python list
    result_list = []
    for row in rows:
        row = [str(x).split(" ") for x in row]
        res = []
        for el in row:
            if len(el) > 1:
                res.append(el[0])
                res.append(el[1])
            else:
                res.append(el[0])
        result_list.append(res)
    return result_list;
