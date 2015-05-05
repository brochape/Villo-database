import sqlite3
from config import db_filename

TRIPS_QUERY="""
    SELECT trips.bicycle, trips.startTime, s1.name, trips.endingTime, s2.name
    FROM trips
    INNER JOIN stations as s1 ON trips.start == s1.num
    INNER JOIN stations as s2 ON trips.ending == s2.num
    WHERE trips.user=?
    ORDER BY trips.startTime DESC"""

TRIPS_USER_QUERY="""
    SELECT trips.startTime, s1.coordX, s1.coordY, trips.endingTime, s2.coordX, s2.coordY
    FROM trips
    INNER JOIN stations as s1 ON trips.start == s1.num
    INNER JOIN stations as s2 ON trips.ending == s2.num
    WHERE trips.user=? AND trips.startTime >= ? AND trips.startTime <= ? 
        AND trips.ending IS NOT NULL AND trips.endingTime IS NOT NULL
    ORDER BY trips.startTime ASC
"""

TRIPS_BICYCLE_QUERY="""
    SELECT trips.startTime, s1.coordX, s1.coordY, trips.endingTime, s2.coordX, s2.coordY
    FROM trips
    INNER JOIN stations as s1 ON trips.start == s1.num
    INNER JOIN stations as s2 ON trips.ending == s2.num
    WHERE trips.bicycle=? AND trips.startTime >= ? AND trips.startTime <= ? 
        AND trips.ending IS NOT NULL AND trips.endingTime IS NOT NULL
    ORDER BY trips.startTime ASC
"""

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

def query_user_period(user, dateBeg, dateEnd):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(TRIPS_USER_QUERY, (user, dateBeg, dateEnd))
    results = cursor.fetchall()
    ret = []
    for result in results:
        row = {}
        row["startTime"] = result[0]
        row["s1.coordX"] = result[1]
        row["s1.coordY"] = result[2]
        row["endingTime"] = result[3]
        row["s2.coordX"] = result[4]
        row["s2.coordY"] = result[5]
        ret.append(row)
    cursor.close()
    db.close()
    return ret

def query_bicycle_period(bicycle, dateBeg, dateEnd):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(TRIPS_BICYCLE_QUERY, (bicycle, dateBeg, dateEnd))
    results = cursor.fetchall()
    ret = []
    for result in results:
        row = {}
        row["startTime"] = result[0]
        row["s1.coordX"] = result[1]
        row["s1.coordY"] = result[2]
        row["endingTime"] = result[3]
        row["s2.coordX"] = result[4]
        row["s2.coordY"] = result[5]
        ret.append(row)
    cursor.close()
    db.close()
    return ret

if __name__ == '__main__':
    assert(len(query_user_period(0, "2010-01-01T00:00:00", "2011-01-01T00:00:00")) == 409)
    assert(len(query_bicycle_period(0, "2010-01-01T00:00:00", "2011-01-01T00:00:00")) == 18)