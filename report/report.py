from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib import fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pyodbc as odbc
import pandas as pnda

# Create a new Canvas object based on the template
output_path = "RailScapeSummaryReport.pdf"
canvas = canvas.Canvas(output_path, pagesize=letter)

# Get the top 5 trains by trip count
def topTrainsBySeatCount(cursor):
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
    # Parse the resulting list into 5 lists after header
    finalList = [["Train ID", "Train Type", "Number of Trips"]]
    for r in results:
        finalList.append(list(r[0]))
    # Return a list of 5 lists, each list contains exactly three values
    # As follows ==> (trainID, trainType, tripsCount)
    return finalList


# Get the top 5 trips with most profit
def topTripsWithMostProfit(cursor):
    query = f"""
        SELECT TOP 5
        trp.tripID AS TripID,
        trp.trainID AS TrainID,
        trp.fromLocation AS Source,
        trp.toLocation AS Destination,
        (trp.price * (trn.seatCount - COUNT(st.tripID))) AS Profit
        FROM TRIP trp JOIN TRAIN trn
        ON trp.trainID = trn.trainID
        LEFT JOIN SEAT st
        ON trp.tripID = st.tripID
        WHERE st.customerID IS NULL
        GROUP BY
            trp.tripID,
            trp.trainID,
            trp.fromLocation,
            trp.toLocation,
            trp.price,
            trn.seatCount
        HAVING COUNT(st.tripID) > 0
        ORDER BY Profit DESC; """
    # Run the query and get the results into a list
    results = pnda.DataFrame(cursor.execute(query)).values.tolist()
    # Parse the resulting list into 5 lists after header
    finalList = [["Trip ID", "Train ID", "Source", "Destination", "Profit"]]
    for r in results:
        finalList.append(list(r[0]))
    # Return a list of 5 lists, each list contains exactly five values
    # As follows ==> (tripID, trainID, fromLocation, toLocation, profit)
    return finalList


# Get the top 5 customers
def topCustomers(cursor):
    query = """
        SELECT TOP 5
        [CUSTOMER].customerID, [CUSTOMER].[name], COUNT([SEAT].seatNum) AS numOfSeat
        FROM CUSTOMER JOIN SEAT
        ON CUSTOMER.customerID = SEAT.customerID
        GROUP BY [CUSTOMER].customerID, [CUSTOMER].name
        ORDER BY numOfSeat DESC; """
    # Run the query and get the results into a list
    results = pnda.DataFrame(cursor.execute(query)).values.tolist()
    # Parse the resulting list into 5 lists after header
    finalList = [["Customer ID", "Customer Name", "Tickets Bought"]]
    for r in results:
        finalList.append(list(r[0]))
    # Return a list of 5 lists, each list contains exactly three values
    # As follows ==> (customerID, name, numOfSeat)
    return finalList


# Get the profit per trip
def profitPerTrip(cursor):
    query = """
        SELECT [SEAT].tripID, [TRIP].fromLocation, [TRIP].toLocation,
        (COUNT([SEAT].seatNum) * [TRIP].price), ([TRAIN].seatCount - COUNT([SEAT].seatNum))
        FROM SEAT, TRIP, TRAIN
        WHERE [TRIP].tripID = [SEAT].tripID
        AND [TRIP].trainID = [TRAIN].trainID
        AND customerID IS NOT NULL
        AND [TRIP].price = (
            SELECT [TRIP].price FROM [TRIP]
            WHERE [TRIP].tripID = [SEAT].tripID)
        GROUP BY [SEAT].tripID, [TRIP].fromLocation,
        [TRIP].toLocation, [TRIP].price, [TRAIN].seatCount; """
    # Run the query and get the results into a list
    results = pnda.DataFrame(cursor.execute(query)).values.tolist()
    # Parse the resulting list into 5 lists after header
    finalList = [["Trip ID", "Source", "Destination", "Price", "Empty Seats"]]
    for r in results:
        finalList.append(list(r[0]))
    # Return a list of 5 lists, each list contains exactly five values
    # As follows ==> (tripID, fromLocation, toLocation, price, emptySeatCount)
    return finalList

def generateReport(cursor):
    page_width = 612
    page_height = 792

    # Define the table data
    table_data = topTrainsBySeatCount(cursor)

    # Load fonts
    pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", "arial-bold.ttf"))

    # Set font and font size for the title
    canvas.setFont("Arial-Bold", 24)

    # Add the title
    title = "RailScape Summary Report"
    canvas.drawCentredString(page_width/2, 750, title)  # Adjust the position as desired

    # Add the icons
    canvas.drawImage("icon.jpg", x = 50, y = 730, width =50,height = 50, preserveAspectRatio=True)  # Adjust the position and size as desired
    canvas.drawImage("icon-reversed.jpg", x = page_width - 100, y = 730, width =50,height = 50, preserveAspectRatio=True)  # Adjust the position and size as desired

    # Set font and font size for the subtitle
    canvas.setFont("Arial", 18)

    # Add the text subtitle
    subtitle = "Top 5 trains by trip count:"
    canvas.drawString(50, 650, subtitle)  

    # Create the table
    table = Table(table_data)

    # Set the table style
    table_style = TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold font for header row
        ("BACKGROUND", (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Background color for header row
        ("TEXTCOLOR", (0, 0), (-1, 0), "black"),  # Text color for header row
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center alignment for all cells
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),  # Font for data rows
        ("FONTSIZE", (0, 1), (-1, -1), 10),  # Font size for data rows
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Bottom padding for header row
        ("BACKGROUND", (0, 1), (-1, -1), "white"),  # Background color for data rows
        ("GRID", (0, 0), (-1, -1), 0.5, "black"),  # Grid lines
    ])

    table.setStyle(table_style)

    # Set the table width
    table._width = 500

    # Calculate table height to fit on the page
    table.wrapOn(canvas, 500, 400)
    table.drawOn(canvas, 200, 500)

    # Set font and font size for the subtitle
    canvas.setFont("Arial", 18)

    # Add the text subtitle right after the table
    subtitle = "Top 5 customers by seat count:"
    canvas.drawString(50, 400, subtitle)  # Adjust the position as desired
    # Create the table
    table = Table(topCustomers(cursor))
    # Set the table style
    table.setStyle(table_style)
    # Set the table width
    table._width = 500
    # Calculate table height to fit on the page
    table.wrapOn(canvas, 500, 400)
    table.drawOn(canvas, 175, 250)
    

    # New page
    canvas.showPage()

    # Set font and font size for the subtitle
    canvas.setFont("Arial", 18)
    # Add the text subtitle right after the table
    subtitle = "Top 5 trips by profit:"
    canvas.drawString(50, 750, subtitle)  # Adjust the position as desired
    # Create the table
    table = Table(topTripsWithMostProfit(cursor))
    # Set the table style
    table.setStyle(table_style)
    # Set the table width
    table._width = 500
    # Calculate table height to fit on the page
    table.wrapOn(canvas, 500, 400)
    table.drawOn(canvas, 175, 600)

    # Set font and font size for the subtitle
    canvas.setFont("Arial", 18)
    # Add the text subtitle right after the table
    subtitle = "Profit for All Trips:"
    canvas.drawString(50, 500, subtitle)  # Adjust the position as desired

    # Create a table in a loop that adds a new page if the table height is more than the page height
    # cause the table might take multiple pages (nRows undefined)
    table_data = profitPerTrip(cursor)
    table = Table(table_data)
    table.setStyle(table_style)
    table._width = 500
    table.wrapOn(canvas, 500, 400)
    table.drawOn(canvas, 175, 350)
    # Save the modified PDF
    canvas.save()