import sqlite3
from config import db_filename

BICYCLE_ALL_QUERY="SELECT * FROM bicycles"
BICYCLE_ONE_QUERY="SELECT servicedate, model, state FROM bicycles WHERE id=?"
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
        bicycle = dict(zip(["id", "servicedate", "mode", "state", "state", "user"], result))
        ret.append(bicycle)
    cursor.close()
    db.close()
    return ret