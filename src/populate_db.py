import sqlite3
from collections import OrderedDict
from CSVParser import CSVParser
from XMLParser import XMLParser
from datetime import datetime
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
    statement = "UPDATE bicycles SET station=" + station + " WHERE id=" + velo
    return statement


def veloToUser(velo, user):
    statement = "UPDATE bicycles SET user=" + user + " WHERE id=" + velo
    return statement


def populate_trips(data):
    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    cursor.execute("PRAGMA temp_store = 2")
    populate_table("trips", ["bicycle", "user", "start", "startTime", "ending", "endingTime"], data)
    for row in data:
        # trip is still pending
        if row[4] == "None":
            cursor.execute(veloToUser(row[0], row[1]))
        else:
            cursor.execute(veloToStation(row[0], row[4]))
    db.commit()
    cursor.close()
    db.close()

def create_admin():
    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    cursor.execute(create_insert_statement("users", ["userID", "password", "expiryDate", "card"], ["1000", "admin", "", ""]))
    cursor.execute(create_insert_statement("admins", ["userID"], ["1000"]))
    db.commit()
    cursor.close()
    db.close()

def main():
    # stations
    parser = CSVParser("../data/stations.csv")
    _, parsedData = parser.parse()
    populate_table("stations", ["num", "name", "seller", "capacity", "coordX", "coordY"], parsedData)
    # velos
    parser = CSVParser("../data/villos.csv")
    _, parsedData = parser.parse()
    populate_table("bicycles", ["id", "servicedate", "model", "state"], parsedData)
    # utilisateurs
    parser = XMLParser("../data/users.xml")
    subscribers, temporary = parser.parseUsers()
    populate_table("users", ["userID", "password", "expiryDate", "card"], map(lambda sub: [sub[0], sub[4], sub[-2], sub[-1]], subscribers))
    populate_table("subs",
        ["userID", "RFID", "lastname", "firstname", "phone", "addresscity", "addresscp", "addressstreet", "addressnumber", "subscribeDate"],
        map(lambda sub: [sub[i] for i in range(0,4)] + [sub[i] for i in range(5,11)], subscribers))
    populate_table("users", ["userID", "password", "expiryDate", "card"], temporary)
    populate_table("tempUsers", ["userID"], map(lambda sub: [sub[0]], temporary))
    # trajets
    parser = CSVParser("../data/trips.csv")
    _, parsedData = parser.parse()
    populate_trips(parsedData)

    create_admin()

    # db = sqlite3.connect(DB_FILENAME)
    # cursor = db.cursor()
    # cursor.execute("SELECT * FROM stations")
    # for l in cursor:
    #     print(l)

if __name__ == '__main__':
    main()
