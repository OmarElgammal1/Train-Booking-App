# Import necessary libraries
import sys
import pyodbc as odbc
import pandas as pnda

# Define the needed attributes for the connection string
# Run ```SELECT @@SERVERNAME``` on MS SQL server to find YOUR_SERVER_NAME
SERVER_NAME = 'YOUR_SERVER_NAME'
DATABASE_NAME = 'TrainBooking'

connection_string = f"""
    DRIVER={"SQL SERVER"};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

# Store records as list of lists
records = [
    ['moamgad@gmdan.net', 'strongpassword'],
    ['omar@da3s.com', 'tryhardpassword'],
    ['yalzayat@gui.com', 'nicepassword'],
    ['seifyahia@nice.gg', 'thisisapassword']
]

# Trial to test the connection with MS SQL Server
try:
    conn = odbc.connect(connection_string)
except Exception as e:
        print(e)
        print("Task is Terminated!")
        sys.exit(0)
else:
    cursor = conn.cursor()

# Using the pyodbc library to insert records into the database
print("\tInserting data into the database!")
insert_statement = """ INSERT INTO \"USER\" VALUES(?, ?) """

try:
    for record in records:
        print(record)
        cursor.execute(insert_statement, record)
except Exception as e:
    cursor.rollback()
    print(e)
    print("Transaction Rollback!")
else:
    print("\tRecords Inserted Successfully!\n")
    cursor.commit()

# Using pandas library to read data from sql into python
sqlQuery = """SELECT * FROM \"USER\" """

# Read table with headers into dataframe
firstResult = pnda.read_sql(sqlQuery, conn)
print("\n\tReading from the database into a dataframe!")
print("Query results with table headers:")
print(firstResult)

# Read table without headers into dataframe
cursor = conn.cursor()
secondResult = pnda.DataFrame(cursor.execute(sqlQuery))
print("\nQuery results withOUT table headers:")
print(secondResult)

# Close the connection at the end of the program
if not conn.closed:
    conn.close()
    print("\n\tConnection Closed!")