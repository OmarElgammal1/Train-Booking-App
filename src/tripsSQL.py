# Import necessary libraries
import sys
import pyodbc as odbc
import pandas as pnda

SERVER_NAME = 'YOUR_SERVER_NAME'
DATABASE_NAME = 'TrainBooking'

connection_string = f"""
    DRIVER={"SQL SERVER"};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

def bookTrip(customerID, tripID, nSeats):
    # Connect to the database
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    # Check if the customer is already booked on the trip
    cursor.execute(f"""
        UPDATE SEAT
        SET customerID = '{customerID}'
        WHERE (tripID = '{tripID}' AND customerID IS NULL)
        LIMIT {nSeats};
    """)
    
    # Close the connection
    if not conn.closed:
        conn.close()
    return True;

def cancelTrip(customerID, tripID):
    # Connect to the database
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    # Check if the customer is already booked on the trip
    cursor.execute(f"""
        UPDATE SEAT
        SET customerID = NULL
        WHERE (tripID = '{tripID}' AND customerID = '{customerID}');
    """)
    
    # Close the connection
    if not conn.closed:
        conn.close()
    return True;


def viewCustomerTrips(customerID):

    #["Trip", "Train", "From", "To", "Date", "Time", "Seats", "Price"]
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT SEAT.tripID, TRIP.trainID, TRIP.fromLocation, TRIP.toLocation, TRIP.depTime, COUNT(SEAT.seatNum) AS TotalSeats, TRIP.price
        FROM TRIP
        INNER JOIN SEAT ON TRIP.tripID = SEAT.tripID
        WHERE SEAT.customerID = '{customerID}'
        GROUP BY SEAT.tripID, TRIP.trainID, TRIP.fromLocation, TRIP.toLocation, TRIP.depTime, TRIP.price;
    """)

    rows = cursor.fetchall()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    # ! split DATETIME and add it correctly to list
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
