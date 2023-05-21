# Import necessary library
import pandas as pnda

# Sign in a previously registered customer
def sign_in(cursor, email, password, admin):
    if admin:
        nameAndPassQuery = f"""
            SELECT ADMIN.email, [USER].password FROM ADMIN 
            JOIN [USER] ON ADMIN.email LIKE [USER].email
            WHERE [USER].email = '{email}' AND [USER].password = '{password}' """
        result = pnda.DataFrame(cursor.execute(nameAndPassQuery))
        if result.empty:
            return False
        else:
            return True
    else:
        nameAndPassQuery = f"""
            SELECT CUSTOMER.email, [USER].password FROM CUSTOMER
            JOIN [USER] ON CUSTOMER.email LIKE [USER].email
            WHERE [USER].email = '{email}' AND [USER].password = '{password}' """
        result = pnda.DataFrame(cursor.execute(nameAndPassQuery))
        if result.empty:
            return False
        else:
            return True

# Sign up a new user on the system database
# If CUSTOMER pass the following ==> (cursor, email, password, name, phoneNum)
# If ADMIN pass the following ==> (cursor, email, password)
def sign_up(cursor, email, password, *args):
    # If the user is ADMIN
    if len(args) == 0:
        insertEmailAndPassQuery = f"""
            INSERT INTO [USER] VALUES ('{password}', '{email}');
            INSERT INTO ADMIN
            SELECT [USER].email FROM [USER]
            WHERE [USER].email LIKE '{email}'; """
        cursor.execute(insertEmailAndPassQuery)
        cursor.commit()
        adminID = pnda.DataFrame(cursor.execute(f" SELECT adminID FROM ADMIN WHERE email = '{email}'; "))
        return adminID[0][0][0]
    # If the user is CUSTOMER
    else:
        insertCustomerDataQuery = f"""
            INSERT INTO [USER] VALUES ('{password}', '{email}');
            INSERT INTO CUSTOMER
            SELECT '{args[0]}', '{args[1]}', [USER].email FROM [USER]
            WHERE [USER].email LIKE '{email}'; """
        cursor.execute(insertCustomerDataQuery)
        cursor.commit()
        customerID = pnda.DataFrame(cursor.execute(f" SELECT customerID FROM CUSTOMER WHERE email = '{email}'; "))
        return customerID[0][0][0]

# Get certain user information via email
def getInfo(cursor, email, admin):
    # If the user is ADMIN
    if admin:
        nameAndPassQuery = f"""
            SELECT [USER].email, [USER].password FROM [USER]
            JOIN [ADMIN] ON [USER].email LIKE [ADMIN].email
            WHERE [USER].email = '{email}' """
        result = pnda.DataFrame(cursor.execute(nameAndPassQuery))
        return result[0][0]
    # If the user is CUSTOMER
    else:
        nameAndPassQuery = f"""
            SELECT [CUSTOMER].customerID, [CUSTOMER].name,
            [CUSTOMER].phoneNum, [USER].email, [USER].password FROM [USER]
            JOIN [CUSTOMER] ON [USER].email LIKE [CUSTOMER].email
            WHERE [USER].email = '{email}' """
        result = pnda.DataFrame(cursor.execute(nameAndPassQuery))
        return result[0][0]
