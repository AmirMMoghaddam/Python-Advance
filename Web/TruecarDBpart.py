import mysql.connector
from mysql.connector import errorcode
import re
def create_database(DB_NAME,cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def UseDB(DB_NAME,cursor):
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(DB_NAME,cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cursor.execute("USE {}".format(DB_NAME))
        else:
            print(err)
            exit(1)
def CreatingTable(Name,Table,cursor):
    try:
        print("Creating table {}: ".format(Name), end='')
        cursor.execute(Table)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
def InitalSQL(DB_NAME,TableName,Table):
    try:
        cnx = mysql.connector.connect(user='root',password = "")
        print("Connected SucsessFully!")
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        print("NOT CONNECTED!")
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
             print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)  
    UseDB(DB_NAME,cursor)
    CreatingTable(TableName,Table,cursor)
def WriteInDB(DB_NAME,TableName,names,prices,milleage):
    try:
        cnx = mysql.connector.connect(user='root',password = "")
        print("Connected SucsessFully!")
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        print("NOT CONNECTED!")
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
             print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)  
    UseDB(DB_NAME,cursor)
    add_DATA = ("INSERT INTO {}"
                "(Title, Price, Milleage) "
                "VALUES (%s ,%s ,%s)").format(TableName)
    for i in range(len(names)):
        P = re.findall(r"\$(\d*),(\d*)",prices[i].text)
        M = re.findall(r"(\d*)",milleage[i].text)
        T = names[i].text
        DATA = (T, int(P[0][0]+P[0][1]), int(M[0]))
        #print(T, " ", len(T))
        try : 
            cursor.execute(add_DATA,DATA)
            cnx.commit()
            print("Row inserted successfully")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

            

    
    