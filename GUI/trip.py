import tkinter
import customtkinter
from datetime import datetime

class ScrollableFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, email="", isSearching=False, command=None, **kwargs):
        
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,6,7,8), weight=1)
        self.grid_columnconfigure((2,3), weight=4)
        self.grid_columnconfigure((4,5), weight=1)
        self.command = command
        self.labelList = []
        self.buttonList = []
        self.email = email
        self.isSearching = isSearching
        
    def addItem(self, item):
        tripLabel = customtkinter.CTkLabel(self, text=item[0], compound="left", padx=10)
        trainLabel = customtkinter.CTkLabel(self, text=item[1], compound="left", padx=10)
        fromLabel = customtkinter.CTkLabel(self, text=item[2], compound="left", padx=10)
        toLabel = customtkinter.CTkLabel(self, text=item[3], compound="left", padx=10)
        dateLabel = customtkinter.CTkLabel(self, text=item[4], compound="left", padx=10)
        timeLabel = customtkinter.CTkLabel(self, text=item[5], compound="left", padx=10)
        seatsLabel = customtkinter.CTkLabel(self, text=item[6], compound="left", padx=10)
        priceLabel = customtkinter.CTkLabel(self, text=item[7], compound="left", padx=10)
        button = customtkinter.CTkButton(self, text="Cancel", width=80, height=30)

        if self.email=="":
            button.configure(state="disabled", fg_color="#042970")
        
        if self.isSearching:
            button.configure(text="View")

        if self.command is not None:
            button.configure(command=lambda: self.command(item))

        tripLabel.grid(row=len(self.labelList), column=0, pady=(0,10))
        trainLabel.grid(row=len(self.labelList), column=1, pady=(0,10))
        fromLabel.grid(row=len(self.labelList), column=2, pady=(0,10))
        toLabel.grid(row=len(self.labelList), column=3, pady=(0,10))
        dateLabel.grid(row=len(self.labelList), column=4, pady=(0,10))
        timeLabel.grid(row=len(self.labelList), column=5, pady=(0,10))
        seatsLabel.grid(row=len(self.labelList), column=6, pady=(0,10))
        priceLabel.grid(row=len(self.labelList), column=7, pady=(0,10))
        button.grid(row=len(self.buttonList), column=8, pady=(0,10), padx=5)

        self.labelList.append([tripLabel, trainLabel, fromLabel, toLabel, dateLabel, timeLabel, seatsLabel, priceLabel])
        self.buttonList.append(button)

    def removeItems(self):
        for arr in self.labelList:
            for label in arr:
                label.grid_remove()

        for button in self.buttonList:
            button.grid_remove()

        self.labelList.clear()
        self.buttonList.clear()

class TripWindow(customtkinter.CTk):
    def __init__(self, email="", data=[]):
        super().__init__()
        self.geometry("600x300")
        self.resizable(0, 0)
        self.isSearching = True
        self.winTitle = "Search for Trips"

        if data == []:
            self.isSearching = False
            self.winTitle = "View Trips"

        self.title(self.winTitle)
        self.data = data
        self.email = email

        self.tripFrame = ScrollableFrame(master=self, email=self.email, isSearching=self.isSearching, command=self.continueButton, width=560, height=218)
        self.tripFrame.place(x=10, y=10, anchor=tkinter.NW)

        self.backButton = customtkinter.CTkButton(master=self, text="Go Back", command=self.destroy, height=40, width=125)
        self.backButton.place(x=10, y=290, anchor=tkinter.SW)

        self.loadData()

    def loadData(self):
        from connect import connect, close
        from extra import availableSeats

        conn = connect()

        if self.isSearching:
            from viewSQL import viewTripsFiltered
            trips = viewTripsFiltered(conn, conn.cursor(), self.data)
            for i in trips:
                i[6] = availableSeats(conn.cursor(), i[0])
                self.tripFrame.addItem(i)

        else:
            from extra import getCustomerID
            from tripsSQL import viewCustomerTrips
            trips = viewCustomerTrips(conn.cursor(), '1')

            for i in trips:
                self.tripFrame.addItem(i)

    def continueButton(self, item):
        from connect import connect, close
        if self.isSearching:
            from view import ViewTripWindow
            window = ViewTripWindow(item, self.email)
            window.mainloop()
        else:
            from tripsSQL import cancelTrip
            from extra import getCustomerID
            conn = connect()
            cancelTrip(conn.cursor(), getCustomerID(conn.cursor(), self.email), item[0])
            conn.commit()
            self.tripFrame.removeItems()
            self.loadData()

if __name__ == "__main__":
    # test = TripWindow("omar13", ["Cairo", "Hell", datetime.strptime("22/05/15 18:00:00", '%y/%m/%d %H:%M:%S'), 
    #     datetime.strptime("24/05/15 18:00:00", '%y/%m/%d %H:%M:%S'), 15])
    test = TripWindow()
    test.mainloop()