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
canvas = canvas.Canvas(output_path , pagesize=letter)


# Get the top 5 trains (by trip count) ==> (trainID, trainType, tripsCount)
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
    # Parse the resulting list into 5 lists
    finalList = []
    for r in results:
        finalList.append(list(r[0]))
    # Return a list of 5 lists, each list contains exactly three values
    # As follows ==> (trainID, trainType, tripsCount)
    # Inserts table header
    finalList.insert(0, ["Train ID", "Train Type", "Number of Trips"])
    return finalList

# Get the top 5 customers
def topCustomers(cursor):
    query = '''
        select top 5 [CUSTOMER].customerID, [CUSTOMER].[name], COUNT([SEAT].seatNum) as numOfSeat
        from CUSTOMER join SEAT on CUSTOMER.customerID = SEAT.customerID
        group by [CUSTOMER].customerID,[customer].name
        order by numOfSeat desc;
    '''
    results = pnda.DataFrame(cursor.execute(query)).values.tolist()
    finalList = []
    for r in results:
        finalList.append(list(r[0]))
    # Return a list of 5 lists, each list contains exactly three values
    # As follows ==> (customerID, name, numOfSeat)
    # Inserts table header
    finalList.insert(0, ["Customer ID", "Customer Name", "Number of Seats"])
    return finalList
# Get the profit per trip
def profitPerTrip(cursor):
    query = '''
        select [SEAT].tripID,[TRIP].fromLocation,[TRIP].toLocation,count([SEAT].seatNum) * [TRIP].price,[TRAIN].seatCount - count([SEAT].seatNum) from SEAT,TRIP,TRAIN
        where [TRIP].tripID = [SEAT].tripID and [TRIP].trainID = [TRAIN].trainID
        and customerID is not null
        and [TRIP].price = (select [TRIP].price from [TRIP] where [TRIP].tripID = [SEAT].tripID)
        group by [SEAT].tripID,[TRIP].fromLocation,[TRIP].toLocation,[TRIP].price,[TRAIN].seatCount;
    '''
    results = pnda.DataFrame(cursor.execute(query)).values.tolist()
    finalList = []
    for r in results:
        finalList.append(list(r[0]))

    # Return a list of lists, each list contains exactly five values
    # As follows ==> (tripID, fromLocation, toLocation, price, emptySeatCount)
    # Inserts table header
    finalList.insert(0, ["Trip ID", "From Location", "To Location", "Price", "Empty Seats"])
    return finalList
# Function to generate the table data
def topTrains():
    trains = [
        ["12345", "Express", "10"],
        ["67890", "Local", "15"],
        ["54321", "Freight", "5"],
        ["98765", "Passenger", "20"],
        ["24680", "High-Speed", "8"]
    ]
    trains.insert(0, ["Train ID", "Train Type", "Number of Trips"])
    return trains

def generateReport(cursor):
    page_width = 612
    page_height = 792

    # Define the table data
    table_data = topTrains()
    # table_data = topTrainsBySeatCount(cursor)

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
    canvas.drawString(50, 650, subtitle)  # Adjust the position as desired

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
    table.drawOn(canvas, 150, 500)

    # Save the modified PDF
    canvas.save()
