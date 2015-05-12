import sqlite3
from config import db_filename as DB_FILENAME
import re
from datetime import datetime

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

def format_date(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y")

def format_time(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").strftime("%H:%M:%S")