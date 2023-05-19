import tkinter
import customtkinter
# from app import mainApp


class RegisterWindow(customtkinter.CTk):
    def __init__(self, edit=False, admin=False, email=""):
        super().__init__()

        self.admin = admin
        self.email = email
        self.edit = edit

        title = ""
        if edit:
            title = "Edit"
        else:
            title = "Register"

        self.geometry("500x300")
        self.resizable(0, 0)

        self.formFrame = customtkinter.CTkFrame(master=self, width=480, height=280)
        self.formFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.label = customtkinter.CTkLabel(master=self.formFrame, text=title, font=customtkinter.CTkFont(size=30, weight="bold"))
        self.label.place(relx=0.5, rely=0.125, anchor=tkinter.CENTER)

        self.nameEntry = customtkinter.CTkEntry(master=self.formFrame, placeholder_text="Name", height=40, width=465)
        self.nameEntry.place(relx=0.5, rely=0.325, anchor=tkinter.CENTER)

        self.eMailEntry = customtkinter.CTkEntry(master=self.formFrame, placeholder_text="E-Mail", height=40, width=200)
        self.eMailEntry.place(relx=0.225, rely=0.5, anchor=tkinter.CENTER)

        self.phoneEntry = customtkinter.CTkEntry(master=self.formFrame, placeholder_text="Phone Number", height=40, width=125)
        self.phoneEntry.place(relx=0.6, rely=0.5, anchor=tkinter.CENTER)

        self.adminCheck = customtkinter.CTkCheckBox(master=self.formFrame, text="Register as\nAdmin", height=40, width=100, command=self.adminCheckToggled)
        self.adminCheck.place(relx=0.775, rely=0.5, anchor=tkinter.W)

        self.passwordEntry = customtkinter.CTkEntry(master=self.formFrame, show="*", placeholder_text="Enter Password", height=40, width=225)
        self.passwordEntry.place(relx=0.25, rely=0.675, anchor=tkinter.CENTER)
        
        self.passwordReEntry = customtkinter.CTkEntry(master=self.formFrame, show="*", placeholder_text="Re-Enter Password", height=40, width=225)
        self.passwordReEntry.place(relx=0.75, rely=0.675, anchor=tkinter.CENTER)

        self.registerButton = customtkinter.CTkButton(master=self.formFrame, text=title, command=self.registerFunction, height=40, width=225)
        self.registerButton.place(relx=0.75, rely=0.9, anchor=tkinter.CENTER)

        self.backButton = customtkinter.CTkButton(master=self.formFrame, text="Go Back", command=self.backFunction, height=40, width=80)
        self.backButton.place(relx=0.1, rely=0.9, anchor=tkinter.CENTER)

        if self.edit:
            self.loadData()

    def loadData(self):
        self.adminCheck.destroy()

        self.phoneEntry.place(relx=0.75, rely=0.5, anchor=tkinter.CENTER)
        self.phoneEntry.configure(width=225)

        self.eMailEntry.insert(0, "yousefalzayat02@yahoo.com")
        self.eMailEntry.configure(width=225)
        self.eMailEntry.place(relx=0.25)

        if self.admin == False:
            self.nameEntry.insert(0, "Yousef Ahmed AlZayat")
            self.phoneEntry.insert(0, "01002684347")
        else:
            self.nameEntry.configure(state="disabled")
            self.phoneEntry.configure(state="disabled")



    def adminCheckToggled(self):
        if self.adminCheck.get():
            self.phoneEntry.configure(state="disabled")
            self.nameEntry.configure(state="disabled")
        else:
            self.phoneEntry.configure(state="normal", placeholder_text="Phone Number")
            self.nameEntry.configure(state="normal", placeholder_text="Name")

    def registerFunction(self):

        if self.edit == True:
            print("Update...")

        else:
            from connect import connect, close
            from userSQL import sign_up
            conn = connect("Zayat")
            done = False
            if self.admin:
                if sign_up(conn, conn.cursor(), self.eMailEntry.get(), self.passwordEntry.get(), self.admin):
                    done = True
            else:
                if sign_up(conn, conn.cursor(), self.eMailEntry.get(), self.passwordEntry.get()):
                    done = True

            if done:
                from view import ViewWindow
                view = ViewWindow(self.eMailEntry.get(), self.adminCheck.get())
                self.destroy()
                view.mainloop()

    def backFunction(self):
        from app import mainApp
        self.destroy()
        app = mainApp()
        app.mainloop()

if __name__ == "__main__":
    test = RegisterWindow()
    test.mainloop()