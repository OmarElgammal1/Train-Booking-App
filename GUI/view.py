import tkinter
import customtkinter


class ScrollableFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.command = command
        self.labelList = []
        self.buttonList = []
        

    def addItem(self, item):
        tripLabel = customtkinter.CTkLabel(self, text=item[0], compound="left", padx=10)
        fromLabel = customtkinter.CTkLabel(self, text=item[1], compound="left", padx=10)
        toLabel = customtkinter.CTkLabel(self, text=item[2], compound="left", padx=10)
        dateLabel = customtkinter.CTkLabel(self, text=item[3], compound="left", padx=10)
        seatsLabel = customtkinter.CTkLabel(self, text=item[4], compound="left", padx=10)
        priceLabel = customtkinter.CTkLabel(self, text=item[5], compound="left", padx=10)
        button = customtkinter.CTkButton(self, text="View", width=80, height=30)

        if self.command is not None:
            button.configure(command=lambda: self.command(item))

        tripLabel.grid(row=len(self.labelList), column=0, pady=(0,10))
        fromLabel.grid(row=len(self.labelList), column=1, pady=(0,10))
        toLabel.grid(row=len(self.labelList), column=2, pady=(0,10))
        dateLabel.grid(row=len(self.labelList), column=3, pady=(0,10))
        seatsLabel.grid(row=len(self.labelList), column=4, pady=(0,10))
        priceLabel.grid(row=len(self.labelList), column=5, pady=(0,10))
        button.grid(row=len(self.buttonList), column=6, pady=(0,10), padx=5)

        self.labelList.append(item)
        self.buttonList.append(button)

class ViewWindow(customtkinter.CTk):
    def __init__(self, email="", isAdmin=False):
        self.email = email
        self.isAdmin = isAdmin
        super().__init__()
        self.geometry("800x400")
        self.resizable(0, 0)

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

        self.searchButton = customtkinter.CTkButton(master=self.searchFrame, width=80, height=35, text="Search")
        self.searchButton.place(x=635, y=90, anchor=tkinter.SE)

        self.tripFrame = ScrollableFrame(master=self, command=self.viewButton, width=623, height=230)
        self.tripFrame.place(x=790, y=390, anchor=tkinter.SE)


        self.labelHead = customtkinter.CTkLabel(master=self, text="       Trip             From                       To                     Date      Seats", 
            width=445, height=20, anchor="w")
            
        self.labelHead.place(x=145, y=120 ,anchor=tkinter.NW)

        self.loadData()

        self.userFrame = customtkinter.CTkFrame(master=self, width=125, height=90)
        self.userFrame.place(x=10, y=45, anchor=tkinter.NW)

        self.userTitle = customtkinter.CTkLabel(master=self.userFrame, text="User Panel", height=40, width=105, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.userTitle.place(x=10, y=0, anchor=tkinter.NW)

        self.adminFrame = customtkinter.CTkFrame(master=self, width=125, height=192)
        self.adminFrame.place(x=10, y=340, anchor=tkinter.SW)

        self.adminTitle = customtkinter.CTkLabel(master=self.adminFrame, text="Admin Panel", height=40, width=105, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.adminTitle.place(x=10, y=2, anchor=tkinter.NW)

        self.accountLabel = customtkinter.CTkLabel(master=self, text="Logged In: ", width=50, height=10)
        self.accountLabel.place(x=15, y=10, anchor=tkinter.NW)

        self.adminLabel = customtkinter.CTkLabel(master=self, text="Is Admin: ", width=50, height=10)
        self.adminLabel.place(x=15, y=25, anchor=tkinter.NW)

        self.loadLeftFrame(email, isAdmin)

        self.backButton = customtkinter.CTkButton(master=self, text="Go Back", command=self.backFunction, height=40, width=125)
        self.backButton.place(x=10, y=390, anchor=tkinter.SW)


    def loadLeftFrame(self, email, isAdmin):
        self.updateButton = customtkinter.CTkButton(master=self.userFrame, text="Update Info", height=40, width=105)
        self.updateButton.place(x=10, y=80, anchor=tkinter.SW)

        self.editTrainButton = customtkinter.CTkButton(master=self.adminFrame, text="Update Train", height=40, width=105)
        self.editTrainButton.place(x=10, y=82, anchor=tkinter.SW)

        self.addTripButton = customtkinter.CTkButton(master=self.adminFrame, text="Add Trip", height=40, width=105)
        self.addTripButton.place(x=10, y= 132, anchor=tkinter.SW)

        self.addTrainButton = customtkinter.CTkButton(master=self.adminFrame, text="Add Train", height=40, width=105)
        self.addTrainButton.place(x=10, y= 182, anchor=tkinter.SW)

        self.accountLabelAnswer = customtkinter.CTkLabel(master=self, height=10, width=50)
        self.accountLabelAnswer.place(x=135, y=10, anchor=tkinter.NE)

        self.adminLabelAnswer = customtkinter.CTkLabel(master=self, height=10, width=50)
        self.adminLabelAnswer.place(x=135, y=25, anchor=tkinter.NE)

        if self.email == "":
            self.updateButton.configure(state="DISABLED", fg_color="#042970")
            self.accountLabelAnswer.configure(text_color="red", text="False")
        else:
            self.accountLabelAnswer.configure(text_color="green", text="True")

        if self.isAdmin == False:
            self.editTrainButton.configure(state="DISABLED", fg_color="#042970")
            self.addTrainButton.configure(state="DISABLED", fg_color="#042970")
            self.addTripButton.configure(state="DISABLED", fg_color="#042970")
            self.adminLabelAnswer.configure(text_color="#A04353", text="False")
        else:
            self.adminLabelAnswer.configure(text_color="green", text="True")

    def loadData(self):
        # self.tripFrame.addItem(["Trip", "From", "To", "Date", "Time", "Seats", "Price"])
        self.tripFrame.addItem(["1", "Cairo", "Alexandria", "05/25", "230", "6$"])
        self.tripFrame.addItem(["2", "Cairo", "Aswan", "05/29", "240", "6$"])
        self.tripFrame.addItem(["3", "Alexandria", "Aswan", "05/18", "220", "6$"])
        self.tripFrame.addItem(["4", "Alexandria", "Sharm El Sheikh", "12/31", "110", "6$"])
        self.tripFrame.addItem(["5", "Aswan", "Alexandria", "01/13", "130", "6$"])
        self.tripFrame.addItem(["6", "Cairo", "Sharm El Sheikh", "06/21", "220", "6$"])
        self.tripFrame.addItem(["7", "Alexandria", "Cairo", "05/18", "200", "6$"])
        self.tripFrame.addItem(["8", "Aswan", "Cairo", "02/29", "250", "6$"])

    def registerFunctionFunction(self):
        print("Button Pressed admin window")
        self.backFunction()

    def backFunction(self):
        from app import mainApp
        self.destroy()
        app = mainApp()
        app.mainloop()

    def viewButton(self, item):
        print("Button pressed: ", item)

if __name__ == "__main__":
    test = ViewWindow("a", False)
    test.mainloop()