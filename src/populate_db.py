import sqlite3
from collections import OrderedDict
from CSVParser import CSVParser
from XMLParser import XMLParser
from datetime import datetime, timedelta
from helpers import create_insert_statement, populate_table

DB_FILENAME = "../data/villo.sq3"

dicodegros = {
    "str": "TEXT",
    "int": "INTEGER",
    "float": "REAL",
    "bool": "BOOLEAN",
    "datetime": "DATETIME"
}

def veloToStation(velo, station):
    statement = "UPDATE bicycles SET stationID=" + station + " WHERE bicycleID=" + velo
    return statement


def veloToUser(velo, user):
    statement = "UPDATE bicycles SET userID=" + user + " WHERE bicycleID=" + velo
    return statement


def populate_trips(data):
    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    cursor.execute("PRAGMA temp_store = 2")
    populate_table("trips", ["bicycleID", "userID", "startStation", "startTime", "endingStation", "endingTime"], data)

    for row in data:
        # trip is still pending
        if row[4] == "NULL":
            cursor.execute(veloToUser(row[0], row[1]))
            cursor.execute(veloToStation(row[0], "NULL"))
        else:
            cursor.execute(veloToUser(row[0], "NULL"))
            cursor.execute(veloToStation(row[0], row[4]))
    db.commit()
    cursor.close()
    db.close()

def create_admin():
    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    cursor.execute(create_insert_statement("users", ["userID", "password", "expiryDate", "card"], ["1000", "1111", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "00000000000000000"]))
    cursor.execute(create_insert_statement("admins", ["userID"], ["1000"]))
    db.commit()
    cursor.close()
    db.close()

def main():
    # stations
    parser = CSVParser("../data/stations.csv")
    _, parsedData = parser.parse()
    populate_table("stations", ["stationID", "name", "seller", "capacity", "coordX", "coordY"], parsedData)
    # velos
    parser = CSVParser("../data/villos.csv")
    _, parsedData = parser.parse()
    populate_table("bicycles", ["bicycleID", "servicedate", "model", "state"], parsedData)
    # utilisateurs
    parser = XMLParser("../data/users.xml")
    subscribers, temporary = parser.parseUsers()
    populate_table("users", ["userID", "password", "expiryDate", "card"], map(lambda sub: [sub[0], sub[4], sub[-2], sub[-1]], subscribers))
    populate_table("subs",
        ["userID", "RFID", "lastname", "firstname", "phone", "addresscity", "addresscp", "addressstreet", "addressnumber", "subscribeDate"],
        map(lambda sub: [sub[i] for i in range(0,4)] + [sub[i] for i in range(5,11)], subscribers))
    populate_table("users", ["userID", "password", "expiryDate", "card"], temporary)
    populate_table("tempUsers", ["userID", "paymentDate"], map(lambda sub: [sub[0], datetime.strptime(sub[2], "%Y-%m-%dT%H:%M:%S") - timedelta(days=7)], temporary))
    # trajets
    parser = CSVParser("../data/trips.csv")
    _, parsedData = parser.parse()
    populate_trips(parsedData)

    create_admin()

if __name__ == '__main__':
    main()
