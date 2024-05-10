import mysql.connector
from mysql.connector import errorcode

DEL = True
# define a name for our DB
DB_NAME = "universityt1"

# --------------------------------------------------------------------------
# define the tables
Tables = {}

Tables['students'] = (
    "CREATE TABLE `students` ("
    "  `student_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `major` enum('E','M') NOT NULL,"
    "  `entry_date` date NOT NULL,"
    "  PRIMARY KEY (`student_no`)"
    ") ENGINE=InnoDB")
Tables['professor'] = (
    "CREATE TABLE `professor` ("
    "  `prof_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `major` enum('E','M') NOT NULL,"
    "  `degree` enum('DR','ENG', 'AP', 'PROF') NOT NULL,"
    "  `emp_date` date NOT NULL,"
    "  PRIMARY KEY (`prof_no`)"
    ") ENGINE=InnoDB")


# --------------------------------------------------------------------------
# try to connect to SQL server 
try:
  cnx = mysql.connector.connect(user='root',password = "p@sswordis1379")
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
  
  

# --------------------------------------------------------------------------
# create and use DB 
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cursor.execute("USE {}".format(DB_NAME))
    else:
        print(err)
        exit(1)

# --------------------------------------------------------------------------
#creating the tables 
for table_name in Tables:
    table_description = Tables[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
# --------------------------------------------------------------------------
#Deleting  
if DEL:
    try:
        cursor.execute(
            "DROP DATABASE {}".format(DB_NAME))
        print("Database Deleted sucsessfully")
    except mysql.connector.Error as err:
        print("Failed deleting database: {}".format(err))
        exit(1)
cursor.close()
cnx.close()