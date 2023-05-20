import tkinter
import customtkinter
# from admin import AdminWindow
from login import LogInWindow
from register import RegisterWindow
from view import ViewWindow

class mainApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.resizable(0, 0)

        buttonFrame = customtkinter.CTkFrame(master=self, width=480, height=280)
        buttonFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        label = customtkinter.CTkLabel(master=buttonFrame, text="Train Booking Application", font=customtkinter.CTkFont(size=30, weight="bold"))
        label.place(relx=0.5, rely=0.125, anchor=tkinter.CENTER)

        viewButton = customtkinter.CTkButton(master=buttonFrame, text="View", command=self.view, height=40, width=100)
        viewButton.place(relx=0.75, rely=0.325, anchor=tkinter.CENTER)

        viewLabel = customtkinter.CTkLabel(master=buttonFrame, text="View Available Trips", font=customtkinter.CTkFont(size=20, weight="bold"))
        viewLabel.place(relx=0.375, rely=0.325, anchor=tkinter.CENTER)

        signInButton = customtkinter.CTkButton(master=buttonFrame, text="Sign In", command=self.signIn, height=40, width=100)
        signInButton.place(relx=0.75, rely=0.5, anchor=tkinter.CENTER)

        logInLabel = customtkinter.CTkLabel(master=buttonFrame, text="Sign into Your Account", font=customtkinter.CTkFont(size=20, weight="bold"))
        logInLabel.place(relx=0.375, rely=0.5, anchor=tkinter.CENTER)

        registerButton = customtkinter.CTkButton(master=buttonFrame, text="Register", command=self.register, height=40, width=100)
        registerButton.place(relx=0.75, rely=0.675, anchor=tkinter.CENTER)

        registerLabel = customtkinter.CTkLabel(master=buttonFrame, text="Register a New Account", font=customtkinter.CTkFont(size=20, weight="bold"))
        registerLabel.place(relx=0.375, rely=0.675, anchor=tkinter.CENTER)

        exitButton = customtkinter.CTkButton(master=buttonFrame, text="Exit", command=self.destroy, height=40, width=80)
        exitButton.place(relx=0.1, rely=0.9, anchor=tkinter.CENTER)
    
    def view(self):
        self.destroy()
        view = ViewWindow()
        view.mainloop()

    def signIn(self):
        self.destroy()
        log = LogInWindow()
        log.mainloop()

    def register(self):
        self.destroy()
        reg = RegisterWindow()
        reg.mainloop()

if __name__ == "__main__":
    app = mainApp()
    app.mainloop()