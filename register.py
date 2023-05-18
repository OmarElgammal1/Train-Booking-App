import tkinter
import customtkinter
# from app import mainApp


class RegisterWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.resizable(0, 0)

        self.formFrame = customtkinter.CTkFrame(master=self, width=480, height=280)
        self.formFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.label = customtkinter.CTkLabel(master=self.formFrame, text="Register", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.label.place(relx=0.5, rely=0.125, anchor=tkinter.CENTER)

        self.eMailEntry = customtkinter.CTkEntry(master=self.formFrame, placeholder_text="E-Mail", height=40, width=225)
        self.eMailEntry.place(relx=0.25, rely=0.5, anchor=tkinter.CENTER)

        self.nameEntry = customtkinter.CTkEntry(master=self.formFrame, placeholder_text="Name", height=40, width=465)
        self.nameEntry.place(relx=0.5, rely=0.325, anchor=tkinter.CENTER)

        self.passwordReEntry = customtkinter.CTkEntry(master=self.formFrame, show="*", placeholder_text="Enter Password", height=40, width=225)
        self.passwordReEntry.place(relx=0.25, rely=0.675, anchor=tkinter.CENTER)

        self.passwordEntry = customtkinter.CTkEntry(master=self.formFrame, show="*", placeholder_text="Re-Enter Password", height=40, width=225)
        self.passwordEntry.place(relx=0.75, rely=0.675, anchor=tkinter.CENTER)

        self.phoneEntry = customtkinter.CTkEntry(master=self.formFrame, placeholder_text="Phone Number", height=40, width=225)
        self.phoneEntry.place(relx=0.75, rely=0.5, anchor=tkinter.CENTER)

        self.registerButton = customtkinter.CTkButton(master=self.formFrame, text="Register", command=self.registerFunctionFunction, height=40, width=225)
        self.registerButton.place(relx=0.75, rely=0.9, anchor=tkinter.CENTER)

        self.backButton = customtkinter.CTkButton(master=self.formFrame, text="Go Back", command=self.backFunction, height=40, width=80)
        self.backButton.place(relx=0.1, rely=0.9, anchor=tkinter.CENTER)

    def registerFunctionFunction(self):
        print("Button Pressed admin window")
        self.backFunction()

    def backFunction(self):
        from app import mainApp
        self.destroy()
        app = mainApp()
        app.mainloop()

if __name__ == "__main__":
    test = RegisterWindow()
    test.mainloop()