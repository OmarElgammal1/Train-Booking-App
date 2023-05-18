import pyodbc as odbc
import pandas as pnda
import sys

SERVER_NAME = 'DESKTOP-UF4LPT6'
DATABASE_NAME = 'TrainBooking'

connection_string = f"""
    DRIVER={"SQL SERVER"};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

try:
    conn = odbc.connect(connection_string)
except Exception as e:
    print(e)
    print("Task is Terminated!")
    sys.exit(0)
else:
    cursor = conn.cursor()


def sign_in(email, password, admin):
    if admin:
        nameAndPassQuery = """select admin.email, [user].password from admin 
        join [user] on admin.Email like [user].Email where [user].email = ? and [user].password = ?"""
        result = pnda.DataFrame(cursor.execute(
            nameAndPassQuery, (email, password)))
        if result.empty:
            return False
        else:
            return True
    else:
        nameAndPassQuery = '''select CUSTOMER.Email, [USER].Password from CUSTOMER
        join [USER] on CUSTOMER.Email like [USER].Email where [USER].email = ? and [USER].password = ?'''
        result = pnda.DataFrame(cursor.execute(
            nameAndPassQuery, (email, password)))
        if result.empty:
            return False
        else:
            return True

# customer try to sign_up so sign_up parameters will be as follow (email, password, name, phoneNum)
def sign_up(email, password, *args):
    if len(args) == 0:
        insertEmailAndPassQuery = '''
                insert into [USER] (email, password) values (?, ?);
                insert into admin (Email)
                select [USER].Email from [USER]
                where [USER].Email like ?;
          '''
        cursor.execute(insertEmailAndPassQuery, (email, password, email))
        conn.commit()
        adminID = pnda.DataFrame(cursor.execute(
            'select Admin_Id from admin where Email = ?', (email,)))
        return adminID[0][0][0]
    else:
        insertCustomerDataQuery = '''
                insert into [USER] (email, password) values (?, ?);
                insert into customer (Name, Email, PhoneNum)
                select ?, [USER].Email, ? from [USER]
                where [USER].Email like ?;
                '''
        cursor.execute(insertCustomerDataQuery,
                       (email, password, args[0], args[1], email))
        conn.commit()
        customerID = pnda.DataFrame(cursor.execute(
            'select customerID from customer where Email = ?', (email,)))
        return customerID[0][0][0]

print(sign_up('mohamedamgad233@gmail.com','b10159h3','Mohamed Amgad','01206212820'))
conn.close()
