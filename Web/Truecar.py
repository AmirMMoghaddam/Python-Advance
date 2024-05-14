import re 
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import TruecarDBpart
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

#VAR Definitions 
CarsNAme = input("Car's Name : ")
url = "https://www.truecar.com/used-cars-for-sale/listings/"+ CarsNAme
DB_NAME = "Car"
Table =  ("CREATE TABLE `{}` ("
    "  `car_no` int(2) NOT NULL AUTO_INCREMENT,"
    "  `Title` varchar(50) NOT NULL,"
    "  `Price` int(10) NOT NULL,"
    "  `Milleage` int(10) NOT NULL,"
    "  PRIMARY KEY (`car_no`)"
    ") ENGINE=InnoDB").format(CarsNAme)
TruecarDBpart.InitalSQL(DB_NAME,CarsNAme,Table)

#Getting the Data 
Re = requests.get(url)

soup = BeautifulSoup(Re.text,"html.parser")


names = soup.find_all("div", attrs={"data-test":"vehicleCardTrim"})
prices = soup.find_all("span", attrs={"data-test":"vehicleCardPriceLabelAmount"})
milleage = soup.find_all("div", attrs={"data-test":"vehicleMileage"})

TruecarDBpart.WriteInDB(DB_NAME,CarsNAme,names,prices,milleage)


