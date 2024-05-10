import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(user='root',password = "p@sswordis1379",
                                database='world')
  print("Connected SucsessFully!")
except mysql.connector.Error as err:
  print("NOT CONNECTED!")
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()
  print("CONECTION CLOSED")