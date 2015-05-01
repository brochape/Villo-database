import sqlite3
from collections import OrderedDict
from CSVParser import CSVParser
from XMLParser import XMLParser
from datetime import datetime

DB_FILENAME = "../data/villo.sq3"

dicodegros = {
    "str": "TEXT",
    "int": "INTEGER",
    "float": "REAL",
    "bool": "BOOLEAN",
    "datetime": "DATETIME"
}

def listToSQL(l):
    return str(l).replace("[", "(").replace("]", ")")

def escapeToSQL(l):
    return map(lambda s: s.replace('\xcc\x81', '').replace('\xcc\x80', '').replace(" ", "_"), l)

def create_insert_statement(name, columns, row):
    statement = "INSERT INTO " + name + " " + listToSQL(columns) + " VALUES"
    statement += listToSQL(map(lambda s: '0' if s == 'False' else '1' if s == 'True' else str(s), row))
    # print statement
    return statement

def create_table(name, columns, data):
    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    # cursor.execute(create_create_statement(name, columns, constraints))
    def execute(row):
        try:
            cursor.execute(create_insert_statement(name, columns, row))
        except Exception, e:
            print e
    map(execute, data)
    db.commit()
    cursor.close()
    db.close()


def main():
    # stations
    parser = CSVParser("../data/stations.csv")
    _,parsedData = parser.parse()
    create_table("stations", ["num", "name", "seller", "capacity", "coordX", "coordY"], parsedData)
    # velos
    parser = CSVParser("../data/villos.csv")
    _, parsedData = parser.parse()
    create_table("bicycles", ["id", "servicedate", "model", "state"], parsedData)
    # utilisateurs
    parser = XMLParser("../data/users.xml")
    subscribers, temporary = parser.parseUsers()
    create_table("users", ["userID", "password", "expiryDate", "card"], map(lambda sub: [sub[0], sub[4], sub[-2], sub[-1]], subscribers))
    create_table("subs", 
        ["userID", "RFID", "lastname", "firstname", "phone", "addresscity", "addresscp", "addressstreet", "addressnumber", "subscribeDate"],
        map(lambda sub: [sub[i] for i in range(0,4)] + [sub[i] for i in range(5,11)], subscribers))
    create_table("users", ["userID", "password", "expiryDate", "card"], temporary)
    create_table("tempUsers", ["userID"], map(lambda sub: [sub[0]], temporary))
    # parser = CSVParser("../data/trips.csv")
    # columns, parsedData = parser.parse()
    # create_table("trajets", columns, [int, int, int, datetime, int, datetime], parsedData)

    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM stations")
    # for l in cursor:
    #     print(l)

if __name__ == '__main__':
    main()
