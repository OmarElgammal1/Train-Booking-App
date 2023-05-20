def tripEmpty(cursor, tripID):
    # RETURNS ROWS WHERE TICKETS ARE BOOKED
    cursor.execute(f"""
        SELECT * from Seat
        WHERE tripID IS {tripID} AND 
        customerID NOT NULL;
    """)
    # IF THERE ARE NO ROWS OF BOOKS
    if cursor.fetchone() is None:
        return True
    else:
        return False
