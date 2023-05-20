import pyodbc as odbc
import sys
from datetime import datetime

def connect(SERVER_NAME):
    DATABASE_NAME = 'TrainBooking'

    connection_string = f"""
        DRIVER={"SQL SERVER"};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trust_Connection=yes;
    """

    try:
        conn = odbc.connect(connection_string)
    except Exception as e:
        print(e)
        print("Task is Terminated!")
        sys.exit(0)

    return conn

def close(conn):
    conn.close()


conn = connect("Zayat")
cursor = conn.cursor()
from GUI.addSQL import addTrip


# Trip data must be passed in this specifc order [trainID, fromLocation, toLocation, depTime, price]
# addTrip(cursor, [1, "Cairo", "Alexandria", datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 7.5])
# addTrip(cursor, [2, "Cairo", "Sharm El Sheikh", datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 7.5])
# addTrip(cursor, [3, "Cairo", "Aswan", datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 10])
# addTrip(cursor, [20, "Sharm El Sheikh", "Alexandria", datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 15])
# addTrip(cursor, [21, "Sharm El Sheikh", "Cairo", datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 20])
# addTrip(cursor, [28, "Sharm El Sheikh", "Aswan", datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 25])
# addTrip(cursor, [1, "Alexandria", "Sharm El Sheikh",datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 15])
# addTrip(cursor, [2, "Alexandria", "Cairo",datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 7.5])
# addTrip(cursor, [3, "Alexandria", "Aswan",datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 20])
# addTrip(cursor, [20, "Aswan", "Alexandria",datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 20])
# addTrip(cursor, [21, "Aswan", "Sharm El Sheikh",datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 25])
# addTrip(cursor, [28, "Aswan", "Cairo",datetime.strptime("23/04/15 18:00:00", '%y/%m/%d %H:%M:%S'), 10])


from src.deleteSQL import deleteTrip

deleteTrip(cursor, 7)

close(conn)



