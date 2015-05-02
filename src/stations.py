import sqlite3
from config import db_filename

STATIONS_QUERY="""
    SELECT stations.num, stations.name, stations.seller, stations.capacity, stations.coordX, stations.coordY
    FROM stations"""


def query_all():
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(STATIONS_QUERY)
    results = []
    for row in cursor.fetchall():
        result = {}
        result["num"] = row[0]
        result["name"] = row[1]
        result["seller"] = row[2]
        result["capacity"] = row[3]
        result["coordX"] = row[4]
        result["coordY"] = row[5]
        results.append(result)
    cursor.close()
    db.close()
    return results
