import tkinter
import customtkinter

class AdminTripWindow(customtkinter.CTk):
    def __init__(self, tripData):
        super().__init__()

        self.tripData = tripData
        self.data = []
        self.edit = False

        if self.tripData != []:
            title = "Edit"
            self.edit = True
        else:
            title = "Add"

        self.resizable(0, 0)
        self.geometry("300x250")
        self.title("Trip Viewer")


        self.string = tkinter.StringVar(self)
        self.string.set("Train ID")
        self.trainID = customtkinter.CTkOptionMenu(self, height=20, width=100, variable=self.string, font=customtkinter.CTkFont(size=16, weight="bold"), command=self.loadData)
        self.trainID.place(x=10, y=15, anchor=tkinter.NW)

        if self.edit:
            self.tripNameLabel = customtkinter.CTkLabel(self, text="Trip ID: " + str(tripData[0]), height=16, font=customtkinter.CTkFont(size=16, weight="bold"))
            self.tripNameLabel.place(x=290, y=15, anchor=tkinter.NE)

        self.trainNameLabel = customtkinter.CTkLabel(self, text="Train Name", height=16, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.trainNameLabel.place(x=12, y=45, anchor=tkinter.NW)

        self.trainName = customtkinter.CTkEntry(self, height=20, width=135, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.trainName.place(x=10, y=65, anchor=tkinter.NW)

        self.trainSeatsLabel = customtkinter.CTkLabel(self, text="Train Seats", height=16, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.trainSeatsLabel.place(x=157, y=45, anchor=tkinter.NW)

        self.trainSeats = customtkinter.CTkEntry(self, height=20, width=135, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.trainSeats.place(x=155, y=65, anchor=tkinter.NW)

        self.fromLabel = customtkinter.CTkLabel(self, text="From", height=16, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.fromLabel.place(x=12, y=95, anchor=tkinter.NW)

        self.fromEntry = customtkinter.CTkEntry(self, height=20, width=135, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.fromEntry.place(x=10, y=115, anchor=tkinter.NW)

        self.toLabel = customtkinter.CTkLabel(self, text="To", height=16, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.toLabel.place(x=157, y=95, anchor=tkinter.NW)

        self.toEntry = customtkinter.CTkEntry(self, height=20, width=135, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.toEntry.place(x=155, y=115, anchor=tkinter.NW)

        self.depTimeLabel = customtkinter.CTkLabel(self, height=16, text="Departure Time", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.depTimeLabel.place(x=12, y=145, anchor=tkinter.NW)

        self.depTimeEntry = customtkinter.CTkEntry(self, height=20, width=180, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.depTimeEntry.place(x=10, y=165, anchor=tkinter.NW)

        self.priceLabel = customtkinter.CTkLabel(self, height=16, text="Price", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.priceLabel.place(x=202, y=145, anchor=tkinter.NW)

        self.priceEntry = customtkinter.CTkEntry(self, height=20, width=90, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.priceEntry.place(x=200, y=165, anchor=tkinter.NW)

        self.exitButton = customtkinter.CTkButton(self, text="Go Back", command=self.destroy, height=40, width=100)
        self.exitButton.place(x=10, y=240, anchor=tkinter.SW)

        self.continueButton = customtkinter.CTkButton(self, text=title, height=40, width=100, command=self.continueTrip)
        self.continueButton.place(x=290, y=240, anchor=tkinter.SE)

        self.loadCheckBox()
        self.onStart()

    def isEditable(self, tripID):
        from extra import tripEmpty
        from connect import connect
        return tripEmpty(connect().cursor(), tripID)

    def adminTripReady(self):
        import re
        from datetime import datetime


        if self.trainName.get() == "":
            return False

        if self.trainSeats.get() == "":
            return False
            
        if self.trainID.get() == "Train ID":
            return False

        if self.fromEntry.get() == "":
            return False

        if self.toEntry.get() == "":
            return False

        if re.match("^\d+?\.\d+?$", self.priceEntry.get()) is None:
            if not self.priceEntry.get().isdigit():
                return False
        
        try:
            datetime.strptime(self.depTimeEntry.get(), '%y/%m/%d %H:%M:%S')
            return True
        except:
            return False

    def onStart(self):
        if self.tripData != []:
            print(self.tripData)
            depTime = self.tripData[4][2:].replace('-', '/') + " " + self.tripData[5]
            self.toEntry.insert(0, self.tripData[2])
            self.fromEntry.insert(0, self.tripData[3])
            self.depTimeEntry.insert(0, depTime)
            self.priceEntry.insert(0, self.tripData[7])
            self.loadData(self.tripData[1])

            if self.isEditable(self.tripData[0]) == False:
                tkinter.messagebox.showinfo("This Trip is Not Editable", "There already are booked seats")
                self.destroy()

    def loadData(self, ID):
        for i in self.data:
            if str(ID) == str(i[0]):
                self.trainSeats.configure(state="normal")
                self.trainSeats.delete(0, 255)
                self.trainSeats.insert(0, str(i[2]))
                self.trainSeats.configure(state="disabled")

                self.trainID.set(str(ID))

                self.trainName.configure(state="normal")
                self.trainName.delete(0, 255)
                self.trainName.insert(0, str(i[1]))
                self.trainName.configure(state="disabled")

    def loadCheckBox(self):
        from viewSQL import viewTrains
        from connect import connect
        conn = connect()
        self.data = viewTrains(conn, conn.cursor())
        trainIDs = []
        for i in self.data:
            trainIDs.append(str(i[0]))
        self.trainID.configure(values=trainIDs)

    def continueTrip(self):

        if not self.adminTripReady():
            tkinter.messagebox.showinfo("Error", "The info you have entered is incorrect\nPlease make sure all the fields are written and in the correct format.")
            return

        from connect import connect
        from datetime import datetime
        if self.edit:
            from updateSQL import updateTrip
            updateTrip(connect().cursor(), [int(self.tripData[0]), int(self.trainID.get()), self.fromEntry.get(), self.toEntry.get(), 
                datetime.strptime(self.depTimeEntry.get(), '%y/%m/%d %H:%M:%S'), float(self.priceEntry.get())])
            tkinter.messagebox.showinfo("Trip Edited", "Success")
            self.destroy()
        else:
            from addSQL import addTrip
            if(addTrip(connect().cursor(), [int(self.trainID.get()), self.fromEntry.get(), self.toEntry.get(), 
                datetime.strptime(self.depTimeEntry.get(), '%y/%m/%d %H:%M:%S'), float(self.priceEntry.get())])):
                tkinter.messagebox.showinfo("Trip Added", "Success")
                self.destroy()
            else:
                tkinter.messagebox.showinfo("Trip Add Failed", "Train has another trip")

class ViewTripWindow(customtkinter.CTk):
    def __init__(self, data, email):
        super().__init__()

        self.data = data
        self.email = email
        self.resizable(0, 0)
        self.geometry("400x190")
        self.title("Trip Viewer")

        self.tripID = customtkinter.CTkLabel(self, text="Trip ID: " + str(self.data[0]), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.tripID.place(x=10, y=10, anchor=tkinter.NW)

        self.trainID = customtkinter.CTkLabel(self, text=("Train ID: " + str(self.data[1])), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.trainID.place(x=390, y=10, anchor=tkinter.NE)

        self.fromAddress = customtkinter.CTkLabel(self, text=("From: " + self.data[2]), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.fromAddress.place(x=10, y=40, anchor=tkinter.NW)

        self.toAddress = customtkinter.CTkLabel(self, text=("To: " + self.data[3]), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.toAddress.place(x=390, y=40, anchor=tkinter.NE)

        self.price = customtkinter.CTkLabel(self, text=("Price/Ticket: " + str(self.data[7])), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.price.place(x=10, y=70, anchor=tkinter.NW)

        self.availableSeats = customtkinter.CTkLabel(self, text=("Available Seats: " + str(self.data[6])), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.availableSeats.place(x=390, y=70, anchor=tkinter.NE)

        self.departure = customtkinter.CTkLabel(self, text=("Departure: " + data[4] + " at " + self.data[5]), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.departure.place(x=200, y=110, anchor=tkinter.CENTER)

        self.ticketNum = customtkinter.CTkEntry(self, placeholder_text="Number of Tickets", height=40, width=160)
        self.ticketNum.place(x=120, y=140, anchor=tkinter.NW)

        self.exitButton = customtkinter.CTkButton(self, text="Go Back", command=self.destroy, height=40, width=100)
        self.exitButton.place(x=10, y=140, anchor=tkinter.NW)

        self.continueButton = customtkinter.CTkButton(self, text="Book Tickets", command=self.book, height=40, width=100)
        self.continueButton.place(x=390, y=140, anchor=tkinter.NE)

    def book(self):

        if not self.ticketNum.get().isdigit() and self.ticketNum.get()[0] != '-':
            tkinter.messagebox.showinfo("Error", "Please enter a valid amount of tickets")
            return
        
        from connect import connect
        from extra import getCustomerID
        from tripsSQL import bookTrip

        cust_ID = getCustomerID(connect().cursor(), self.email)

        if(bookTrip(connect().cursor(), cust_ID, int(self.data[0]), int(self.ticketNum.get()))):
            tkinter.messagebox.showinfo("Trip Booked", "Success")
            self.destroy()

class TrainWindow(customtkinter.CTk):
    def __init__(self, isEditing):
        super().__init__()

        self.isEditing = isEditing
        self.data = []

        if self.isEditing:
            title = "Edit"
        else:
            title = "Add"

        self.resizable(0, 0)
        self.geometry("300x150")
        self.title("Train Viewer")

        self.string = tkinter.StringVar(self)
        self.string.set("Train ID")
        self.trainID = customtkinter.CTkOptionMenu(self, height=20, width=100, variable=self.string, font=customtkinter.CTkFont(size=16, weight="bold"), command=self.loadData)
        self.trainID.place(x=150, y=15, anchor=tkinter.N)

        self.trainNameLabel = customtkinter.CTkLabel(self, text="Train Type", height=16, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.trainNameLabel.place(x=12, y=45, anchor=tkinter.NW)

        self.trainName = customtkinter.CTkEntry(self, height=20, width=135, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.trainName.place(x=10, y=65, anchor=tkinter.NW)

        self.trainSeatsLabel = customtkinter.CTkLabel(self, text="Train Seats", height=16, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.trainSeatsLabel.place(x=157, y=45, anchor=tkinter.NW)

        self.trainSeats = customtkinter.CTkEntry(self, height=20, width=135, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.trainSeats.place(x=155, y=65, anchor=tkinter.NW)

        self.exitButton = customtkinter.CTkButton(self, text="Go Back", command=self.destroy, height=40, width=100)
        self.exitButton.place(x=10, y=140, anchor=tkinter.SW)

        self.continueButton = customtkinter.CTkButton(self, text=title, height=40, width=100, command=self.addTrain)
        self.continueButton.place(x=290, y=140, anchor=tkinter.SE)

        if self.isEditing:
            self.loadCheckBox()
        else:
            self.trainID.configure(state="disabled")

    def loadData(self, ID):
        for i in self.data:
            if ID == str(i[0]):
                self.trainSeats.delete(0, 255)
                self.trainSeats.insert(0, str(i[2]))

                self.trainName.delete(0, 255)
                self.trainName.insert(0, str(i[1]))

    def loadCheckBox(self):
        from viewSQL import viewTrains
        from connect import connect
        conn = connect()
        self.data = viewTrains(conn, conn.cursor())
        trainIDs = []
        for i in self.data:
            trainIDs.append(str(i[0]))
        self.trainID.configure(values=trainIDs)  

    def trainReady(self):
        if self.trainName.get() == "":
            return False

        if not self.trainSeats.get().isdigit():
            return False

        if self.isEditing and self.trainID.get() == "Train ID":
            return False

        return True

    def addTrain(self):

        if not self.trainReady():
            tkinter.messagebox.showinfo("Error", "Please check the info you have provided")
            return

        from connect import connect
        cursor = connect().cursor()

        if self.isEditing:
            from updateSQL import updateTrain
            updateTrain(cursor, [int(self.trainSeats.get()), self.trainName.get(), int(self.trainID.get())])
            tkinter.messagebox.showinfo("Train Edited", "Success")
        else:
            from addSQL import addTrain
            addTrain(cursor, [int(self.trainSeats.get()), self.trainName.get()])
            tkinter.messagebox.showinfo("Train Added", "Success")

        self.destroy()

class ScrollableFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, email="", isAdmin=False, command=None, **kwargs):
        
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,6,7,8), weight=1)
        self.grid_columnconfigure((2,3), weight=4)
        self.grid_columnconfigure((4,5), weight=1)
        self.command = command
        self.labelList = []
        self.buttonList = []
        self.email = email
        self.isAdmin = isAdmin
        
    def addItem(self, item):
        tripLabel = customtkinter.CTkLabel(self, text=item[0], compound="left", font=customtkinter.CTkFont(size=12))
        trainLabel = customtkinter.CTkLabel(self, text=item[1], compound="left", font=customtkinter.CTkFont(size=12))
        fromLabel = customtkinter.CTkLabel(self, text=item[2], compound="left", font=customtkinter.CTkFont(size=12))
        toLabel = customtkinter.CTkLabel(self, text=item[3], compound="left", font=customtkinter.CTkFont(size=12))
        dateLabel = customtkinter.CTkLabel(self, text=item[4], compound="left", font=customtkinter.CTkFont(size=12))
        timeLabel = customtkinter.CTkLabel(self, text=item[5], compound="left", font=customtkinter.CTkFont(size=12))
        seatsLabel = customtkinter.CTkLabel(self, text=item[6], compound="left", font=customtkinter.CTkFont(size=12))
        priceLabel = customtkinter.CTkLabel(self, text=item[7], compound="right", font=customtkinter.CTkFont(size=12))
        button = customtkinter.CTkButton(self, text="View", width=69, compound="right", height=30)

        if self.email=="":
            button.configure(state="disabled", fg_color="#042970")
        
        if self.isAdmin:
            button.configure(text="Edit")

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
        button.grid(row=len(self.buttonList), column=8, pady=(0,10))

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

class ViewWindow(customtkinter.CTk):
    def __init__(self, email="", isAdmin=False):
        self.email = email
        self.isAdmin = isAdmin
        super().__init__()
        self.geometry("800x510")
        self.resizable(0, 0)
        self.title("RailScape")

        self.searchFrame = customtkinter.CTkFrame(master=self, width=645, height=100)
        self.searchFrame.place(x=145, y=10, anchor=tkinter.NW)
        
        self.fromEntry = customtkinter.CTkEntry(master=self.searchFrame, width=305, height=35, placeholder_text="From")
        self.fromEntry.place(x=10, y=10, anchor=tkinter.NW)

        self.toEntry = customtkinter.CTkEntry(master=self.searchFrame, width=305, height=35, placeholder_text="To")
        self.toEntry.place(x=635, y=10, anchor=tkinter.NE)

        self.startEntry = customtkinter.CTkEntry(master=self.searchFrame, width=200, height=35, placeholder_text="Starting From")
        self.startEntry.place(x=10, y=90, anchor=tkinter.SW)

        self.endEntry = customtkinter.CTkEntry(master=self.searchFrame, width=200, height=35, placeholder_text="Ending At")
        self.endEntry.place(x=220, y=90, anchor=tkinter.SW)

        self.ticketEntry = customtkinter.CTkEntry(master=self.searchFrame, width=115, height=35, placeholder_text="Num. of Tickets")
        self.ticketEntry.place(x=545, y=90, anchor=tkinter.SE)

        self.searchButton = customtkinter.CTkButton(master=self.searchFrame, width=80, command=self.search, height=35, text="Search")
        self.searchButton.place(x=635, y=90, anchor=tkinter.SE)

        self.tripFrame = ScrollableFrame(master=self, email=email, isAdmin=isAdmin, command=self.viewButton, width=623, height=340)
        self.tripFrame.place(x=790, y=500, anchor=tkinter.SE)


        self.labelHead = customtkinter.CTkLabel(master=self, text="   Trip  Train                From                                      To" + 
        "                            Date              Time                    Price", width=445, height=20, anchor="w")
        self.labelHead.place(x=145, y=120 ,anchor=tkinter.NW)

        self.labelHead2 = customtkinter.CTkLabel(master=self, text="Available\nSeats")
        self.labelHead2.place(x=605, y=115, anchor=tkinter.NW)


        self.loadData()

        self.userFrame = customtkinter.CTkFrame(master=self, width=125, height=140)
        self.userFrame.place(x=10, y=55, anchor=tkinter.NW)

        self.userTitle = customtkinter.CTkLabel(master=self.userFrame, text="User Panel", height=40, width=105, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.userTitle.place(x=62.5, y=0, anchor=tkinter.N)

        self.adminFrame = customtkinter.CTkFrame(master=self, width=125, height=242)
        self.adminFrame.place(x=10, y=450, anchor=tkinter.SW)

        self.adminTitle = customtkinter.CTkLabel(master=self.adminFrame, text="Admin Panel", height=40, width=105, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.adminTitle.place(x=10, y=2, anchor=tkinter.NW)

        self.accountLabel = customtkinter.CTkLabel(master=self, text="Logged In: ", width=50, height=10)
        self.accountLabel.place(x=15, y=15, anchor=tkinter.NW)

        self.adminLabel = customtkinter.CTkLabel(master=self, text="Is Admin: ", width=50, height=10)
        self.adminLabel.place(x=15, y=30, anchor=tkinter.NW)

        self.loadLeftFrame(email, isAdmin)

        self.refreshButton = customtkinter.CTkButton(master=self, text="Refresh", command=self.refresh, height=25, width=80)
        self.refreshButton.place(x=780, y=117, anchor=tkinter.NE)

        self.backButton = customtkinter.CTkButton(master=self, text="Go Back", command=self.backFunction, height=40, width=125)
        self.backButton.place(x=10, y=500, anchor=tkinter.SW)

    def loadLeftFrame(self, email, isAdmin):
        self.updateButton = customtkinter.CTkButton(master=self.userFrame, text="Update Info", command=self.updateInfo, height=40, width=105)
        self.updateButton.place(x=10, y=80, anchor=tkinter.SW)

        self.viewCustomerTripsButton = customtkinter.CTkButton(master=self.userFrame, text="View Trips", height=40, width=105, command=self.viewCustomerTrips)
        self.viewCustomerTripsButton.place(x=10, y=130, anchor=tkinter.SW)

        self.updateTrainButton = customtkinter.CTkButton(master=self.adminFrame, text="Update Train", command=self.updateTrain,  height=40, width=105)
        self.updateTrainButton.place(x=10, y=82, anchor=tkinter.SW)

        self.addTripButton = customtkinter.CTkButton(master=self.adminFrame, text="Add Trip", command=self.addTrip, height=40, width=105)
        self.addTripButton.place(x=10, y= 132, anchor=tkinter.SW)

        self.addTrainButton = customtkinter.CTkButton(master=self.adminFrame, text="Add Train", command=self.addTrain, height=40, width=105)
        self.addTrainButton.place(x=10, y= 182, anchor=tkinter.SW)

        self.printReportButton = customtkinter.CTkButton(master=self.adminFrame, text="Make Report", command=self.printReport, height=40, width=105)
        self.printReportButton.place(x=10, y=232, anchor=tkinter.SW)

        self.accountLabelAnswer = customtkinter.CTkLabel(master=self, height=10, width=50)
        self.accountLabelAnswer.place(x=135, y=15, anchor=tkinter.NE)

        self.adminLabelAnswer = customtkinter.CTkLabel(master=self, height=10, width=50)
        self.adminLabelAnswer.place(x=135, y=30, anchor=tkinter.NE)

        if self.email == "":
            self.updateButton.configure(state="disabled", fg_color="#042970")
            self.accountLabelAnswer.configure(text_color="#A04353", text="False")
            self.viewCustomerTripsButton.configure(state="disabled", fg_color="#042970")
        else:
            self.accountLabelAnswer.configure(text_color="green", text="True")

        if self.isAdmin == False:
            self.updateTrainButton.configure(state="disabled", fg_color="#042970")
            self.printReportButton.configure(state="disabled", fg_color="#042970")
            self.addTrainButton.configure(state="disabled", fg_color="#042970")
            self.addTripButton.configure(state="disabled", fg_color="#042970")
            self.adminLabelAnswer.configure(text_color="#A04353", text="False")
        else:
            self.adminLabelAnswer.configure(text_color="green", text="True")
            self.viewCustomerTripsButton.configure(state="disabled", fg_color="#042970")

    def viewCustomerTrips(self):
        from trip import TripWindow
        from datetime import datetime
        trp = TripWindow(self.email)
        trp.mainloop()        

    def loadData(self):
        from viewSQL import viewTrips
        from connect import connect, close
        from extra import availableSeats
        conn = connect()

        data = viewTrips(conn, conn.cursor())

        for i in data:
            i[6] = availableSeats(conn.cursor(), i[0])
            self.tripFrame.addItem(i)

    def updateInfo(self):
        from register import RegisterWindow
        reg = RegisterWindow(True, self.isAdmin, self.email)
        self.destroy()
        reg.mainloop()

    def updateTrain(self):
        window = TrainWindow(True)
        window.mainloop()

    def addTrain(self):
        window = TrainWindow(False)
        window.mainloop()
    
    def addTrip(self):
        window = AdminTripWindow([])
        window.mainloop()

    def backFunction(self):
        from app import mainApp
        self.destroy()
        app = mainApp()
        app.mainloop()

    def readyForSearch(self):
        if self.fromEntry.get() == "": 
            return False
        if self.toEntry.get() == "": 
            return False
        if self.startEntry.get() == "": 
            return False
        if self.endEntry.get() == "":
            return False
        if self.ticketEntry.get() == "":
            return False
        return True

    def search(self):

        if not self.readyForSearch():
            tkinter.messagebox.showinfo("Invalid Info", "Please enter all the data in their correct formats\nDate: yy/mm/dd hh:mm:ss")
            return

        from trip import TripWindow
        from datetime import datetime
        trp = TripWindow(self.email, [self.fromEntry.get(), self.toEntry.get(), 
            datetime.strptime(self.startEntry.get(), '%y/%m/%d %H:%M:%S'), datetime.strptime(self.endEntry.get(), '%y/%m/%d %H:%M:%S'), int(self.ticketEntry.get())])
        trp.mainloop()

    def viewButton(self, item):
        if self.isAdmin:
            window = AdminTripWindow(item)
            window.mainloop()
        else:
            window = ViewTripWindow(item, self.email)
            window.mainloop()

    def printReport(self):
        from report.report import generateReport
        from connect import connect
        generateReport(connect().cursor())
        tkinter.messagebox.showinfo("Success", "The PDF report has been saved.\nPlease find it in /report")
        self.printReportButton.configure(state="disabled", fg_color="#042970")

    def refresh(self):
        self.tripFrame.removeItems()
        self.loadData()

if __name__ == "__main__":
    test = ViewWindow()
    test.mainloop()