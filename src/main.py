import sqlite3
from CSVParser import CSVParser


def main():
    filename = "../data/villo.sq3"
    parser = CSVParser("../data/stations.csv")
    _,parsedData = parser.parse()
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS stations (numero INTEGER, nom TEXT, borne INTEGER, capacite INTEGER, coordX REAL, coordY REAL)")
    basicstring = "INSERT INTO stations (numero,nom,borne,capacite,coordX,coordY) VALUES("
    finalstring = basicstring
    for item in parsedData:
        for caract in item:
            try:
                float(caract)
            except ValueError:
                if caract == 'True':
                    finalstring += "1"
                elif caract == 'False':
                    finalstring += "0"
                else:  # String
                    finalstring += "'" + caract.replace("'", "''") + "'"
            else:
                finalstring += caract
            finalstring += ", "

        finalstring = finalstring[:-2] + ")"
        cursor.execute(finalstring)
        finalstring = basicstring

    db.commit()
    cursor.close()
    db.close()

    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM stations")
    for l in cursor:
        print(l)

if __name__ == '__main__':
    main()
