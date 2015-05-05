import sqlite3
from config import db_filename

BICYCLE_ALL_QUERY="SELECT * FROM bicycles"
BICYCLE_ONE_QUERY="SELECT servicedate, model, state FROM bicycles WHERE id=?"
BICYCLE_BROKEN_QUERY="SELECT id, servicedate, model, state FROM bicycles WHERE state=?"
BICYCLE_UPDATE_QUERY="UPDATE bicycles SET state=? WHERE id=?"


def select(id):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLE_ONE_QUERY, (id,))
    result = cursor.fetchone()
    ret = None
    if result:
        ret = {}
        ret["servicedate"] = result[0]
        ret["model"] = result[1]
        ret["state"] = result[2]
    cursor.close()
    db.close()
    return ret

def select_broken():
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLE_BROKEN_QUERY, (0,))
    results = cursor.fetchall()
    ret = []
    for result in results:
        bicycle = dict(zip(["id", "servicedate", "model", "state"], result))
        ret.append(bicycle)
    print ret
    cursor.close()
    db.close()
    return ret


def report(id):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLE_UPDATE_QUERY, (0, id))
    db.commit()
    cursor.close()
    db.close()

def repair(id):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLE_UPDATE_QUERY, (1, id))
    db.commit()
    cursor.close()
    db.close()

def select_all():
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLE_ALL_QUERY)
    results = cursor.fetchall()
    ret = []
    for result in results:
        bicycle = dict(zip(["id", "servicedate", "mode", "state", "station", "user"], result))
        ret.append(bicycle)
    cursor.close()
    db.close()
    return ret