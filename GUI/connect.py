import pyodbc as odbc
import sys

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