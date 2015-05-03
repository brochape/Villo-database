import sqlite3
from config import db_filename

TRIPS_QUERY="""
    SELECT trips.bicycle, trips.startTime, s1.name, trips.endingTime, s2.name
    FROM trips
    INNER JOIN stations as s1 ON trips.start == s1.num
    INNER JOIN stations as s2 ON trips.ending == s2.num
    WHERE trips.user=?
    ORDER BY trips.startTime DESC"""

def query_all(user):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(TRIPS_QUERY, (user,))
    results = []
    for row in cursor.fetchall():
        result = {}
        result["bicycle"] = row[0]
        result["startTime"] = row[1]
        result["start"] = row[2]
        result["endingTime"] = row[3]
        result["ending"] = row[4]
        results.append(result)
    cursor.close()
    db.close()
    return results
