import sqlite3
from config import db_filename as DB_FILENAME
import re

def listToSQL(l):
    return str(l).replace("[", "(").replace("]", ")").replace('\'NULL\'', 'NULL')


def escapeToSQL(l):
    return map(lambda s: s.replace('\xcc\x81', '').replace('\xcc\x80', '').replace(" ", "_"), l)


def create_insert_statement(name, columns, row):
    statement = "INSERT INTO " + name + " " + listToSQL(columns) + " VALUES"
    statement += listToSQL(map(lambda s: '0' if s == 'False' else '1' if s == 'True' else str(s), row))
    return statement


def populate_table(name, columns, data):
    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    cursor.execute("PRAGMA temp_store = 2")
    
    def execute(row):
        try:
            cursor.execute(create_insert_statement(name, columns, row))
        except Exception, e:
            print e
    map(execute, data)
    db.commit()
    cursor.close()
    db.close()

def format_date(datetime):
    print datetime
    res = re.split(r'[:T\- ]+',datetime)
    year = res[0]
    month = res[1]
    day = res[2]
    hour = res[3]
    minute = res[4]
    second = res[5]
    return year,month,day,hour,minute,second