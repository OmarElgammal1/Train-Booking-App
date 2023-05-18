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
        button = customtkinter.CTkButton(self, text="View", width=80)

        if self.command is not None:
            button.configure(command=lambda: self.command(item))

        tripLabel.grid(row=len(self.labelList), column=0, pady=(0,10))
        fromLabel.grid(row=len(self.labelList), column=1, pady=(0,10))
        toLabel.grid(row=len(self.labelList), column=2, pady=(0,10))
        dateLabel.grid(row=len(self.labelList), column=3, pady=(0,10))
        seatsLabel.grid(row=len(self.labelList), column=4, pady=(0,10))
        priceLabel.grid(row=len(self.labelList), column=5, pady=(0,10))
        button.grid(row=len(self.buttonList), column=5, pady=(0,10), padx=5)

        self.labelList.append(item)
        self.buttonList.append(button)

class ViewWindow(customtkinter.CTk):
    def __init__(self, email="", password="", isAdmin=False):
        super().__init__()
        self.geometry("600x400")
        self.resizable(0, 0)

        self.testFrame = customtkinter.CTkFrame(master=self, width=445, height=100)
        self.testFrame.place(x=145, y=10, anchor=tkinter.NW)

        self.formFrame = ScrollableFrame(master=self, command=self.viewButton, width=423, height=230)
        self.formFrame.place(x=590, y=390, anchor=tkinter.SE)

        self.labelHead = customtkinter.CTkLabel(master=self, text="       Trip             From                       To                     Date      Seats", width=445, height=20, anchor="w")
        self.labelHead.place(x=145, y=120 ,anchor=tkinter.NW)

        self.loadData()

        self.rightFrame = customtkinter.CTkFrame(master=self, width=125, height=330)
        self.rightFrame.place(x=10, y=10, anchor=tkinter.NW)

        self.backButton = customtkinter.CTkButton(master=self, text="Go Back", command=self.backFunction, height=40, width=125)
        self.backButton.place(x=10, y=390, anchor=tkinter.SW)

    def loadData(self):
        # self.formFrame.addItem(["Trip", "From", "To", "Date", "Seats"])
        self.formFrame.addItem(["1", "Cairo", "Alexandria", "05/25", "230", "6$"])
        self.formFrame.addItem(["2", "Cairo", "Aswan", "05/29", "240", "6$"])
        self.formFrame.addItem(["3", "Alexandria", "Aswan", "05/18", "220", "6$"])
        self.formFrame.addItem(["4", "Alexandria", "Sharm El Sheikh", "12/31", "110", "6$"])
        self.formFrame.addItem(["5", "Aswan", "Alexandria", "01/13", "130", "6$"])
        self.formFrame.addItem(["6", "Cairo", "Sharm El Sheikh", "06/21", "220", "6$"])
        self.formFrame.addItem(["7", "Alexandria", "Cairo", "05/18", "200", "6$"])
        self.formFrame.addItem(["8", "Aswan", "Cairo", "02/29", "250", "6$"])

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
    test = ViewWindow()
    test.mainloop()