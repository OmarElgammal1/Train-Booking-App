import tkinter
import customtkinter

class LogInWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.resizable(0, 0)

        self.formFrame = customtkinter.CTkFrame(master=self, width=480, height=280)
        self.formFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.label = customtkinter.CTkLabel(master=self.formFrame, text="Log In", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.label.place(relx=0.5, rely=0.125, anchor=tkinter.CENTER)

        self.eMailEntry = customtkinter.CTkEntry(master=self.formFrame, placeholder_text="E-Mail", height=40, width=205)
        self.eMailEntry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.passwordEntry = customtkinter.CTkEntry(master=self.formFrame, show="*", placeholder_text="Password", height=40, width=205)
        self.passwordEntry.place(relx=0.5, rely=0.475, anchor=tkinter.CENTER)
        
        self.adminCheck = customtkinter.CTkCheckBox(master=self.formFrame, text="LogIn as Admin", height=40, width=205)
        self.adminCheck.place(relx=0.5, rely=0.625, anchor=tkinter.CENTER)

        self.registerButton = customtkinter.CTkButton(master=self.formFrame, text="Log In", command=self.logInFunction, height=40, width=205)
        self.registerButton.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.backButton = customtkinter.CTkButton(master=self.formFrame, text="Go Back", command=self.backFunction, height=40, width=80)
        self.backButton.place(relx=0.1, rely=0.9, anchor=tkinter.CENTER)

    def logInFunction(self):
        from connect import connect, close
        from userSQL import sign_in
        conn = connect("Zayat")

        if sign_in(conn, conn.cursor(), self.eMailEntry.get(), self.passwordEntry.get(), self.adminCheck.get()):
            print("True")
            conn.close()

            from view import ViewWindow
            view = ViewWindow(self.eMailEntry.get(), self.adminCheck.get())
            self.destroy()
            view.mainloop()
        print("False")

    def backFunction(self):
        from app import mainApp
        self.destroy()
        app = mainApp()
        app.mainloop()

if __name__ == "__main__":
    test = LogInWindow()
    test.mainloop()