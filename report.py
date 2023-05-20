# Import necessary libraries
import pyodbc as odbc
import pandas as pnda

# Connect to MS SQL Server Database
conn = odbc.connect(f"""
    DRIVER={"SQL SERVER"};
    SERVER={"YOUR_SERVER_NAME"};
    DATABASE={"TrainBooking"};
    Trust_Connection=yes; """)
cursor = conn.cursor()

# Get the top 5 trains (by trip count) ==> (trainID, trainType, tripsCount)
def topTrainsBySeatCount():
    query = """
        SELECT TOP 5
        trn.trainID AS TrainID, trn.trainType AS TrainType, COUNT(*) AS TripsCount
        FROM TRAIN trn
        JOIN TRIP trp
        ON trn.trainID = trp.trainID
        GROUP BY trn.trainID, trn.trainType
        ORDER BY TripsCount DESC; """
    # Run the query and get the results into a list
    results = pnda.DataFrame(cursor.execute(query)).values.tolist()
    # Parse the resulting list into 5 lists
    finalList = []
    for r in results:
        finalList.append(list(r[0]))
    # Return a list of 5 lists, each list contains exactly three values
    # As follows ==> (trainID, trainType, tripsCount)
    return finalList

# Close the cursor and the connection
cursor.close()
conn.close()