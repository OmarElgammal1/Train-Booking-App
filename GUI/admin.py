import tkinter
import customtkinter

class AdminWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.resizable(0, 0)

        self.labelFrame = customtkinter.CTkFrame(master=self, width=380, height=65, border_color="blue")
        self.labelFrame.place(relx=0.5, rely=0.215, anchor=tkinter.CENTER)

        self.label = customtkinter.CTkLabel(master=self.labelFrame, text="Train Booking Application", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.buttonFrame = customtkinter.CTkFrame(master=self, width=380, height=105)
        self.buttonFrame.place(relx=0.5, rely=0.685, anchor=tkinter.CENTER)

        self.viewButton = customtkinter.CTkButton(master=self.buttonFrame, text="View", command=button_function, height=40)
        self.viewButton.place(relx=0.5, rely=0.74, anchor=tkinter.CENTER)

        self.signInButton = customtkinter.CTkButton(master=self.buttonFrame, text="Sign In", command=button_function, height=40)
        self.signInButton.place(relx=0.8, rely=0.26, anchor=tkinter.CENTER)

        self.registerButton = customtkinter.CTkButton(master=self.buttonFrame, text="Register", command=button_function, height=40)
        self.registerButton.place(relx=0.2, rely=0.26, anchor=tkinter.CENTER)

    def button_function():
        print("Button Pressed admin window")


if __name__ == "__main__":
    test = AdminWindow()
    test.mainloop()