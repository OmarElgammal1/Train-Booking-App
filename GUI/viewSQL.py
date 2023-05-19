from connect import connect, close
import pandas as pnda
pnda.set_option('display.max_columns', None)

def viewTrips(conn, cursor):

    query = """select * from trip"""
    data = pnda.read_sql(query, conn, ).to_dict()

    trips = []

    for i in data["tripID"]:
        # print(data["tripID"][i])
        trips.append([data["tripID"][i], data["trainID"][i], data["fromLocation"][i], data["toLocation"][i], data["depTime"][i], data["price"][i]])

    return trips

def viewTrains(conn, cursor):
    query = """select * from train"""
    data = pnda.read_sql(query, conn, ).to_dict()

    trains = []

    for i in data["trainID"]:
        trains.append([data["trainID"][i], data["trainType"][i], data["seatCount"][i]])

    return trains

def viewTripsFiltered(conn, cursor, fromLoc, toLoc, startingFrom, endingAt, requiredTickets):
    query = f"""select * from trip
    WHERE
    fromLocation like {fromLoc} AND
    toLocation like {toLoc}
    """

conn = connect("Zayat")

print(viewTrains(conn, conn.cursor()))
# viewTrips(conn, conn.cursor())
