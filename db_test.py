from mysql.connector import connect, Error
from getpass import getpass
import hashlib
import datetime
import os

# salt for phone numbers
# Given a Cameroonian phone number (num)  in format "xxx-xxx-xxx"
# Salt = (num + 907)*(953)

def check_balance(phone_num=0, username=""):
    """checks user account balance in db
    returns balance[account_balance, ref_account_balance, referral_id]"""
    phone_salt = lambda phone_num : (phone_num + 907)*(953)
    balance = {'acc_bal':0, 'ref_bal':0,
        'ref_id':0, 'loyalty_bonus':0}

    if phone_num!=0:
        phone_num = phone_salt(phone_num)

    try:
        with connect(
            host = "localhost",
            user = input("Enter username: "),
            password = getpass("Enter password: "),
            database = "bd_megakom",
            ) as connection:
            with connection.cursor() as cursor:
                query = """SELECT DISTINCT account_balance, ref_account_balance,
                        referral_id, loyalty_bonus 
                        FROM user WHERE (deleted=0) 
                        AND (username=%s OR phone_num=%s);"""
                cursor.execute(query, (username, phone_num,))
                if cursor.with_rows:
                    result = cursor.fetchall()
                    balance['acc_bal'] = result[0][0]  #append acc_bal
                    balance['ref_bal'] = result[0][1]  #append ref_bal
                    balance['ref_id'] = result[0][2]  #append ref_id
                    balance['loyalty_bonus'] = result[0][3]  #append loyalty bonus
                else:
                    balance = [-1,-1,0,0]           
                    
    except Error as e:
        print(e)
        connection = None
        result = False
        balance = [-1,-1,0,0] ## returned list in case of error
    return balance


def delete_user(phone_num=0, username="")->bool:
    phone_salt = lambda phone_num : (phone_num + 907)*(953)
    phone_num = phone_salt(phone_num)
    result = False
    try:
        with connect(
            host = "localhost",
            user = input("Enter username: "),
            password = getpass("Enter password: "),
            database = "bd_megakom",
            ) as connection:
            with connection.cursor() as cursor:
                query = """UPDATE user 
                        SET deleted=1
                        WHERE (username=%s OR phone_num=%s);"""
                cursor.execute(query, (username, phone_num,))
                connection.commit()  #always use after performing any modifications to a table
                result = True
                ##connection.rollback() #always use to cancel all data changes
                    
    except Error as e:
        print(e)
        connection = None
        result = False
    return result


def increment_balance(amt:float, phone_num=0, username="")->bool:
    """adds money to user account balance in db"""
    prev_amt = check_balance(phone_num, username)
    #print(prev_amt)
    #prev_referrer_amt = check_balance(prev_amt[2], username="")
    loyalty = prev_amt['loyalty_bonus']
    amt = round(amt + (amt*loyalty)/100, 2)
    #ref_amt = round(amt*0.10, 2)
    #new_amt = round((prev_amt['acc_bal'] + amt), 2)
    #print(new_amt)
    phone_salt = lambda phone_num : (phone_num + 907)*(953)
    if phone_num!=0:
        phone_num = phone_salt(phone_num)

    result = False

    try:
        with connect(
            host = "localhost",
            user = input("Enter username: "),
            password = getpass("Enter password: "),
            database = "bd_megakom",
            ) as connection:
            with connection.cursor() as cursor:
                query1 = """UPDATE user 
                        SET account_balance=account_balance+%s
                        WHERE (username=%s OR phone_num=%s);"""
                        # UPDATE user 
                        # SET ref_account_balance = ref_account_balance + %s
                        # WHERE (phone_num=%s);"""
                        
                val_tuple = (
                    amt, username, phone_num,)
                    #round(amt*0.10, 2),)
                    #prev_amt['ref_id'],)
                cursor.execute(query1, val_tuple)#, multi=True)
                connection.commit()  #always use after performing any modifications to a table
                query2 = """UPDATE user 
                        SET ref_account_balance = ref_account_balance + %s
                        WHERE (phone_num=%s);"""
                        
                val_tuple = (round(amt*0.10, 2),
                    prev_amt['ref_id'],)
                cursor.execute(query2, val_tuple)
                connection.commit() 
                result = True
                # connection.rollback() #always use to cancel all data changes
                    
    except Error as e:
        print(e)
        connection = None
        result = False
    return result

def hash_password(password:str, salt:str)->str:
    key = hashlib.pbkdf2_hmac('sha256', 
        password.encode(encoding='utf-8'), 
        bytes.fromhex(salt), #convert hex salt to bytes
        iterations=123456
        )  
    return key.hex()

def get_password_salt(phone_num=0, username=""):
    result = False
    phone_salt = lambda phone_num : (phone_num + 907)*(953)
    if phone_salt != 0:
        phone_num = phone_salt(phone_num)

    try:
        with connect(
            host = "localhost",
            user = input("Enter username: "),
            password = getpass("Enter password: "),
            database = "bd_megakom",
            ) as connection:
            with connection.cursor() as cursor:
                query ="""SELECT DISTINCT salt FROM user WHERE 
                        (username=%s OR phone_num=%s) LIMIT 1;"""
                cursor.execute(query, (username, phone_num,))
                if cursor.with_rows:
                    result = cursor.fetchall()
                    hashed = result[0][0]
                    return hashed
                else:
                     return False

    except Error as e:
        print(e)
        connection = None
        return False
    
    return

def check_password(passhash:str, username="", phone_num=0)->bool:
    salt = get_password_salt(phone_num, username)
    if salt == False:
        print("No salt found !!")
        return False

    phone_salt = lambda phone_num : (phone_num + 907)*(953)
    if phone_num!=0:
        phone_num = phone_salt(phone_num)

    passhash = hash_password(passhash, salt)

    result = []
    try:
        with connect(
            host = "localhost",
            user = input("Enter username: "),
            password = getpass("Enter password: "),
            database = "bd_megakom",
            ) as connection:
            with connection.cursor() as cursor:
                query = """SELECT DISTINCT * FROM user WHERE (passhash=%s AND deleted=0) 
                        AND (username=%s OR phone_num=%s);"""
                cursor.execute(query, (passhash, username, phone_num,))
                if cursor.with_rows:
                    result = cursor.fetchall()
                else:
                    result = None
                    
    except Error as e:
        print(e)
        connection = None
        result = None
    
    if result != None and len(result)>0:
        return True
    else:
        return False


def check_if_user_exists(phone_num=1, username="bl", 
    OM_num=1, Momo_num=1, email="bl"):
    phone_salt = lambda phone_num : (phone_num + 907)*(953)
    phone_num = phone_salt(phone_num)
    OM_num = phone_salt(OM_num)
    Momo_num = phone_salt(Momo_num)
    ans = {0:False}
    
    try:
        with connect(
            host = "localhost",
            user = input("Enter username: "),
            password = getpass("Enter password: "),
            database = "bd_megakom",
            ) as connection:
            with connection.cursor() as cursor:
                query1 = """SELECT DISTINCT * FROM user WHERE (deleted=0) 
                        AND (username=%s) LIMIT 1;"""
                query2 = """SELECT DISTINCT * FROM user WHERE (deleted=0) 
                        AND (email=%s) LIMIT 1;"""
                query3 = """SELECT DISTINCT * FROM user WHERE (deleted=0) 
                        AND (phone_num=%s) LIMIT 1;"""
                query4 = """SELECT DISTINCT * FROM user WHERE (deleted=0) 
                        AND (OM_num=%s) LIMIT 1;"""
                query5 = """SELECT DISTINCT * FROM user WHERE (deleted=0) 
                        AND (Momo_num=%s) LIMIT 1;"""
                cursor.execute(query1, (username,))
                if cursor.with_rows:
                    result = cursor.fetchall()
                    if ( len(result) != 0):
                        ans[1] = "username exists"
                        return ans[1]
                
                cursor.execute(query2, (email,))
                if cursor.with_rows:
                    result = cursor.fetchall()
                    if ( len(result) != 0):
                        ans[2] = "email exists"
                        return ans[2]
                
                cursor.execute(query3, (phone_num,))
                if cursor.with_rows:
                    result = cursor.fetchall()
                    if ( len(result) != 0):
                        ans[3] = "phone_num exists"
                        return ans[3]
                
                cursor.execute(query4, (OM_num,))
                if cursor.with_rows:
                    result = cursor.fetchall()
                    if ( len(result) != 0):
                        ans[4] = "OM_num exists"
                        return ans[4]

                cursor.execute(query5, (Momo_num,))
                if cursor.with_rows:
                    result = cursor.fetchall()
                    if ( len(result) != 0):
                        ans[5] = "Momo_num exists"
                        return ans[5]

    except Error as e:
        print("Error ")
        print(e)
        connection = None
        result = None
    return ans[0]

def add_user(phone_num:int, username:str, passwd:str, first_name:str,
    last_name:str, birthday:str, email:str, gender:str, town:str, nationality:str, 
    business=0, OM_num=0, Momo_num=0, referral_id=0)->bool:
    result = False
    phone_salt = lambda phone_num : (phone_num + 907)*(953)
    phone_num = phone_salt(phone_num)
    if OM_num != 0:
        OM_num = phone_salt(OM_num)
    
    if Momo_num != 0:
        Momo_num = phone_salt(Momo_num)
    
    registration_date = last_activity = datetime.datetime.now()
    salt = os.urandom(32)
    salt = salt.hex() # convert salt from bytes to str
    passhash = hash_password(passwd, salt)
    account_balance = 0
    ref_account_balance = 0

    try:
        with connect(
            host = "localhost",
            user = input("Enter username: "),
            password = getpass("Enter password: "),
            database = "bd_megakom",
            ) as connection:
            with connection.cursor() as cursor:

                query = """INSERT INTO user(phone_num, passhash, first_name, last_name,
                     birthday, username, email, gender, referral_id, registration_date,
                    ref_account_balance, Momo_num, OM_num, account_balance, town,
                    nationality, business, last_activity, salt) VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                
                val_tuple = (phone_num, passhash, first_name, last_name,
                     birthday, username, email, gender, referral_id, registration_date,
                    ref_account_balance, Momo_num, OM_num, account_balance, town,
                    nationality, business, last_activity, salt)

                cursor.execute(query, val_tuple)
                connection.commit()
                result = True
                return True

    except Error as e:
        print(e)
        print("Insertion failed")
        connection = None
        return False

    return result

# print(add_user(phone_num=690090909, username="fthierry", passwd="password", first_name="Foyet",
#     last_name="Loic", birthday="2002-02-18", email="thl@gmail.com", gender="M", 
#     referral_id=646011474696, OM_num=690090909, Momo_num=0, town="Douala", nationality="Cameroon"))

# print(check_password("password", phone_num=677870525))

# print(check_balance(username="njoel"))

# print(delete_user(username="njoel"))

# print(increment_balance(85.0, phone_num=690090909))