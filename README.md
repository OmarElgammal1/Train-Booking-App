# Project #3 - Train Booking Application

## Description

This is a collaboration to complete the group project in the **Intro to Database Systems** Course at FCAI-CU.  
The train booking application is a graphical user interface (GUI) application made with `customtkinter` python library.  
The application is an implementation of what we've learned this semester about managing databases and dealing with `MS SQL Server` queries.


## Program Functionalities

- Signing up a new user (e.g. admin, customer)
- Updating a user's details
- Adding a train (by admin)
- Updating a train details (by admin)
- Adding a trip (by admin)
- Updating a trip details (by admin)
- Showing a list of available seats that satisfy certain criteria  
(e.g. date, time, source, destination, required number of seats…)
- Performing operations on trips: Booking and Canceling.

## Prerequisites
- MS SQL Server Management Studio
- Python (version 3.8+)

## Instructions to try the application

1. Clone the repo to your local machine via the following command:
> ```bash
> git clone https://github.com/iSeFz/Train-Booking-App.git && cd Train-Booking-App
> ```
2. Download the required packages via the following command:
> ```bash
> python -m pip install -r requirements.txt
> ```

3. Open [`TrainBooking.sql`](https://github.com/iSeFz/Train-Booking-App/blob/main/SQL/TrainBooking.sql) on your MS SQL Server Management Studio
4. Execute the query to create the database on your local machine
5. Open [`fillDataBase.sql`](https://github.com/iSeFz/Train-Booking-App/blob/main/SQL/fillDataBase.sql) on your MS SQL Server Management Studio
6. Execute the query to fill the database with dummy data to test the application
7. Enter your server name instead of "YOUR_SERVER_NAME" in [`connect.py`](https://github.com/iSeFz/Train-Booking-App/blob/main/GUI/connect.py) at line 11
8. Run the application via terminal or through any code editor or IDE that support python  
> ```bash
> python GUI/app.py
> ```
9. That's it! Enjoy the application!
