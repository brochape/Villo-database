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

def create_create_statement(name, columns, constraints):
    statement = "CREATE TABLE IF NOT EXISTS " + name + " ("
    for column, typ in columns.iteritems():
        statement += column + " " + dicodegros[typ.__name__] + ","
    if "primary" in constraints:
        statement += "PRIMARY KEY " + str(constraints["primary"]).replace("[", "(").replace("]", ")") + ","
    if "unique" in constraints:
        for unik in constraints["unique"]:
            statement += "UNIQUE " + str(unik).replace("[", "(").replace("]", ")") + ","
    if "foreign" in constraints:
        for key, value in constraints["foreign"].iteritems():
            statement += "FOREIGN KEY " + key + " REFERENCES " + value
    statement = statement[:-1] + ")"
    print statement
    return statement

def create_insert_statement(name, columns, row):
    statement = "INSERT INTO " + name + " " + str(columns.keys()).replace("[", "(").replace("]", ")") + " VALUES"
    statement += str(map(lambda s: '0' if s == 'False' else '1' if s == 'True' else s, row)).replace("[", "(").replace("]", ")")
    print statement
    return statement

def create_table(name, columns, types, data, constraints):
    columns = OrderedDict(zip(map(lambda s: s.replace('\xcc\x81', '').replace('\xcc\x80', '').replace(" ", "_"), columns), types))
    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    cursor.execute(create_create_statement(name, columns, constraints))
    for row in data:
        try:
            cursor.execute(create_insert_statement(name, columns, row))
        except Exception, e:
            print e
    db.commit()
    cursor.close()
    db.close()


def main():
    parser = CSVParser("../data/stations.csv")
    columns,parsedData = parser.parse()
    create_table("stations", columns, [int, str, int, int, float, float], parsedData, {"primary": ["numero"], "unique": [["nom"], ["coordonnee_X", "coordonnee_Y"]]})
    parser = CSVParser("../data/villos.csv")
    columns, parsedData = parser.parse()
    create_table("velos", columns, [int, datetime, str, bool], parsedData, {"primary": ["numero"]})
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
