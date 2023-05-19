import tkinter
import customtkinter

class AdminWindow(customtkinter.CTk):
    def __init__(self, data):

        self.data = data
        super().__init__()

        self.resizable(0, 0)
        self.geometry("400x190")
        self.title("Trip Viewer")

        self.tripID = customtkinter.CTkLabel(self, text="Trip ID: " + data[0], height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.tripID.place(x=10, y=10, anchor=tkinter.NW)

        self.trainID = customtkinter.CTkLabel(self, text=("Train ID: " + data[1]), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.trainID.place(x=390, y=10, anchor=tkinter.NE)

        self.fromAddress = customtkinter.CTkLabel(self, text=("From: " + data[2]), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.fromAddress.place(x=10, y=40, anchor=tkinter.NW)

        self.toAddress = customtkinter.CTkLabel(self, text=("To: " + data[3]), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.toAddress.place(x=390, y=40, anchor=tkinter.NE)

        self.price = customtkinter.CTkLabel(self, text=("Price/Ticket: " + data[7]), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.price.place(x=10, y=70, anchor=tkinter.NW)

        self.availableSeats = customtkinter.CTkLabel(self, text=("Available Seats: " + data[6]), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.availableSeats.place(x=390, y=70, anchor=tkinter.NE)

        self.departure = customtkinter.CTkLabel(self, text=("Departure: " + data[4] + " at " + data[5]), height=20, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.departure.place(x=200, y=110, anchor=tkinter.CENTER)

        self.ticketNum = customtkinter.CTkEntry(self, placeholder_text="Number of Tickets", height=40, width=160)
        self.ticketNum.place(x=120, y=140, anchor=tkinter.NW)

        self.exitButton = customtkinter.CTkButton(self, text="Go Back", command=self.destroy, height=40, width=100)
        self.exitButton.place(x=10, y=140, anchor=tkinter.NW)

        self.continueButton = customtkinter.CTkButton(self, text="Book Tickets", height=40, width=100)
        self.continueButton.place(x=390, y=140, anchor=tkinter.NE)


if __name__ == "__main__":
    test = AdminWindow(["1", "Spanish 1", "Sharm El Sheikh", "Alexandria", "2023/05/19", "18:00", "230", "100$"])
    test.mainloop()