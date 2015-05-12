import sqlite3
from config import db_filename
import helpers

BICYCLES_ALL_QUERY="SELECT * FROM bicycles"
BICYCLE_ONE_QUERY="SELECT id, servicedate, model, state FROM bicycles WHERE id=?"
BICYCLES_STATE_QUERY="SELECT id, servicedate, model, state FROM bicycles WHERE state=?"
BICYCLE_UPDATE_STATE_QUERY="UPDATE bicycles SET state=? WHERE id=?"

def format_bicycle(row):
    ret = {}
    ret["id"] = row[0]
    ret["servicedate"] = helpers.format_datetime(row[1])
    ret["model"] = row[2]
    ret["state"] = row[3]
    return ret


def select(id):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLE_ONE_QUERY, (id,))
    result = cursor.fetchone()
    ret = None
    if result:
        ret = format_bicycle(result)
    cursor.close()
    db.close()
    return ret

def select_broken():
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLES_STATE_QUERY, (0,))
    results = cursor.fetchall()
    ret = []
    for result in results:
        ret.append(format_bicycle(result))
    cursor.close()
    db.close()
    return ret


def report(id):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLE_UPDATE_STATE_QUERY, (0, id))
    db.commit()
    cursor.close()
    db.close()

def repair(id):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLE_UPDATE_STATE_QUERY, (1, id))
    db.commit()
    cursor.close()
    db.close()

def select_all():
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLES_ALL_QUERY)
    results = cursor.fetchall()
    ret = []
    for result in results:
        bicycle = dict(zip(["id", "servicedate", "mode", "state", "station", "user"], result))
        ret.append(bicycle)
    cursor.close()
    db.close()
    return ret