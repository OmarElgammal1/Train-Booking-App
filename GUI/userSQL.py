import pandas as pnda
from connect import connect, close

def sign_in(conn, cursor, email, password, admin):
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
def sign_up(conn, cursor, email, password, *args):
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
            'select email from admin where Email = ?', (email,)))
        return email[0][0][0]
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
