import pandas as pnda
pnda.set_option('display.max_columns', None)

def viewTrips(conn, cursor):

    query = """select * from trip"""
    data = pnda.read_sql(query, conn, ).to_dict()
    trips = []

    for i in data["tripID"]:
        # print(data["tripID"][i])
        date = str(data["depTime"][i]).split(' ')
        date[1] = date[1].split('.')
        trainSeats = pnda.read_sql("""select seatCount from train
        where trainID = """ + str(data["trainID"][i]), conn, ).to_dict()

        trips.append([data["tripID"][i], data["trainID"][i], data["fromLocation"][i], data["toLocation"][i], date[0], date[1][0], trainSeats["seatCount"][0], data["price"][i]])

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
    toLocation like {toLoc} AND

    """