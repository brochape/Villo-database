import sqlite3
from config import db_filename

BICYCLE_ONE_QUERY="SELECT servicedate, model, state FROM bicycles WHERE id=?"
BICYCLE_REPORT_QUERY="UPDATE bicycles SET state=0 WHERE id=?"

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
    cursor.execute(BICYCLE_REPORT_QUERY, (id,))
    db.commit()
    cursor.close()
    db.close()

def repair(id):
    pass

def select_all():
    pass