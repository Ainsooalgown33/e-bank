import sys
import random
import mysql.connector as local
conn = local.connect(host="127.0.0.1", user="root", passwd="", database="sqistudent")
mycursor = conn.cursor()
myquery = "INSERT INTO firstbank (FirstName, LastName, contact, line, account_number, password, account_balance) VALUES (%s, %s, %s, %s, %s, %s, %s)"
def operation():
    global func
    print(""" Welcome to First bank, The people"s bank. what operation would you like to perform?!!!
    1. Create an account with us.
    2. login to your account.
    3. Exit""")
    option = input(">>> ")

    if option=="1":
        func = "membership"
        membership()
    elif option=="2":
        func = "login"
        login()
    elif option=="3":
        func = "exit"
        exit()
    else:
        print("invalid input")
        operation()

def tryagain():
    print("Enter 1. to go to menu\n 2. exit")
    user = input(">>> ")
    if user=="1":
        operation()
    elif user=="2":
        exit()
    else:
        print("invalid input")
    tryagain()

def valid_phone_number(phone_number):
    return len(phone_number) == 11 

def linen(contact):
    if contact.startswith("0802") or contact.startswith("0808") or contact.startswith("0708") or contact.startswith("0812") or contact.startswith("0701") or contact.startswith("0902") or contact.startswith("0901") or contact.startswith("0904") or contact.startswith("0907") or contact.startswith("0912"):
        return "AIRTEL NG"
    elif  contact.startswith("0803") or contact.startswith("0806") or contact.startswith("0703") or contact.startswith("0706") or contact.startswith("0813") or contact.startswith("0816") or contact.startswith("0810") or contact.startswith("0814") or contact.startswith("0903") or contact.startswith("0906") or contact.startswith("0913") or contact.startswith("0916") or contact.startswith("07025") or contact.startswith("07026") or contact.startswith("0704"):
        return "MTN NG"
    elif contact.startswith("0805") or contact.startswith("0807") or contact.startswith("0705") or contact.startswith("0815") or contact.startswith("0811") or contact.startswith("0905") or contact.startswith("0915"):
        return "GLO NG"
    elif contact.startswith("0809") or contact.startswith("0818") or contact.startswith("0817") or contact.startswith("0909") or contact.startswith("0908"):
        return "9MOBILE NG"
    else:
        return "UNKNOWN"
    

def membership():
    print("please make sure to fill the out the following inputs correctly")
    firstName = (input("Enter your first name >"))
    lastName = (input("Enter your last name >" )) 
    contact= (input("phone number must not be less or greater than 11 digits >"))
    if not valid_phone_number(contact):
        print('Invalid phone number',), membership()

    line = linen(contact)

    account_number = random.randint(1000000000, 9999999999)

    password = input("Enter your password (must be in digits and at least 4 digits long) >")
    if not password.isdigit() or len(password) < 4:
        print("Password must be only integers and at least 4 digits long.")
        membership()
        
    confirm_password = input("Please confirm your password >")
    if password != confirm_password:
        print("Passwords do not match.")
        membership()

    account_balance = ("0")
    val = (firstName, lastName, int(contact), line, int(account_number), password, account_balance)
    mycursor.execute(myquery, val)
    conn.commit()
    print(mycursor.rowcount, "bank record updated successfully, welcome to First bank " + firstName  +  lastName, " your account number is " + str(account_number))

def login():
    account_number = input("Enter your account number >")
    password = input("Enter your password >")
    query = "SELECT * FROM firstbank WHERE account_number=%s AND password=%s"
    val = (int(account_number), int(password))
    mycursor.execute(query, val)
    result = mycursor.fetchone()

    if result is not None:
        firstName = result[1]
        lastName = result[2]
        account_balance = result[7]
        print(f"Welcome {firstName} {lastName}. Your current account balance is {account_balance}")
        print("What would you like to do?")
        print("1. Deposit money")
        print("2. Transfer money")
        print("3. Exit")

        option = input(">>> ")

        if option == "1":
            deposit_amount = input("Enter amount to deposit >")
            new_balance = int(account_balance) + int(deposit_amount)
            query = "UPDATE firstbank SET account_balance=%s WHERE account_number=%s"
            val = (str(new_balance), int(account_number))
            mycursor.execute(query, val)
            conn.commit()
            print(f"Deposit of {deposit_amount} was successful. Your new account balance is {new_balance}")
            tryagain()

        elif option == "2":
            fast = input("Enter bank name")
            receiver_account_number = input("Enter receiver's account number >")
            query = "SELECT * FROM accessbank WHERE account_number=%s UNION SELECT * FROM firstbank WHERE account_number=%s UNION SELECT * FROM ubabank WHERE account_number=%s"
            val = (receiver_account_number, receiver_account_number, receiver_account_number)
            mycursor.execute(query, val)
            receiver_result = mycursor.fetchone()


            if receiver_result is not None:
                transfer_amount = input("Enter amount to transfer >")
                if int(transfer_amount) > int(account_balance):
                    print("Insufficient funds.")
                    tryagain()

                else:
                    new_sender_balance = int(account_balance) - int(transfer_amount)
                    new_receiver_balance = int(receiver_result[7]) + int(transfer_amount)

                    query1 = "UPDATE accessbank SET account_balance=%s WHERE account_number=%s"
                    val1 = (str(new_sender_balance), int(account_number))
                    mycursor.execute(query1, val1)

                    query2 = "UPDATE firstbank SET account_balance=%s WHERE account_number=%s"
                    val2 = (str(new_sender_balance), int(account_number))
                    mycursor.execute(query2, val2)

                    query3 = "UPDATE ubabank SET account_balance=%s WHERE account_number=%s"
                    val3 = (str(new_sender_balance), int(account_number))
                    mycursor.execute(query3, val3)

                
                    query4 = "UPDATE accessbank  SET account_balance=%s WHERE account_number=%s"
                    val4 = (str(new_receiver_balance), int(receiver_account_number))
                    mycursor.execute(query4, val4)

                    query5 = "UPDATE firstbank  SET account_balance=%s WHERE account_number=%s"
                    val5 = (str(new_receiver_balance), int(receiver_account_number))
                    mycursor.execute(query5, val5)

                    query6 = "UPDATE ubabank  SET account_balance=%s WHERE account_number=%s"
                    val6 = (str(new_receiver_balance), int(receiver_account_number))
                    mycursor.execute(query6, val6)

                    conn.commit()
                    print(f"Transfer of {transfer_amount} to {receiver_result[1]} {receiver_result[2]} {fast} was successful.")
                    print(f"Your new account balance is {new_sender_balance}")
                    tryagain()
            else:
                print("Invalid receiver account number or password.")
                tryagain()

        elif option == "3":
            exit()

        else:
            print("Invalid input")
            login()

    else:
        print("Invalid account number or password.")
        tryagain()
operation()