import sqlite3
from config import db_filename
import helpers
from datetime import datetime

TRIPS_USER_QUERY="""
    SELECT trips.bicycle, trips.startTime, s1.name, trips.endingTime, s2.name
    FROM trips
    INNER JOIN stations as s1 ON trips.start == s1.num
    INNER JOIN stations as s2 ON trips.ending == s2.num
    WHERE trips.user=?
    ORDER BY trips.startTime DESC"""

TRIPS_USER_PERIOD_QUERY="""
    SELECT trips.startTime, s1.coordX, s1.coordY, trips.endingTime, s2.coordX, s2.coordY
    FROM trips
    INNER JOIN stations as s1 ON trips.start == s1.num
    INNER JOIN stations as s2 ON trips.ending == s2.num
    WHERE trips.user=? AND trips.startTime >= ? AND trips.startTime <= ? 
        AND trips.ending IS NOT NULL AND trips.endingTime IS NOT NULL
    ORDER BY trips.startTime ASC
"""

TRIPS_BICYCLE_PERIOD_QUERY="""
    SELECT trips.startTime, s1.coordX, s1.coordY, trips.endingTime, s2.coordX, s2.coordY
    FROM trips
    INNER JOIN stations as s1 ON trips.start == s1.num
    INNER JOIN stations as s2 ON trips.ending == s2.num
    WHERE trips.bicycle=? AND trips.startTime >= ? AND trips.startTime <= ? 
        AND trips.ending IS NOT NULL AND trips.endingTime IS NOT NULL
    ORDER BY trips.startTime ASC
"""
def format_trips_row(row):
    result = {}
    result["bicycle"] = row[0]
    result["startDate"] = helpers.format_date(row[1])
    result["startTime"] = helpers.format_time(row[1])
    result["start"] = row[2]
    result["endingDate"] = helpers.format_date(row[3])
    result["endingTime"] = helpers.format_time(row[3])
    result["ending"] = row[4]
    return result


def query_all(user):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(TRIPS_USER_QUERY, (user,))
    results = []
    for row in cursor.fetchall():
        results.append(format_trips_row(row))
    cursor.close()
    db.close()
    return results

def query_last(user):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(TRIPS_USER_QUERY + " LIMIT 1", (user,))
    result = cursor.fetchone()
    if result:
        ret = format_trips_row(result)
    else:
        ret = None
    cursor.close()
    db.close()
    return ret

def format_period_row(row):
    ret = {}
    ret["startTime"] = row[0]
    ret["s1_coordX"] = row[1]
    ret["s1_coordY"] = row[2]
    ret["endingTime"] = row[3]
    ret["s2_coordX"] = row[4]
    ret["s2_coordY"] = row[5]
    return ret

def query_user_period(user, dateBeg, dateEnd):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(TRIPS_USER_PERIOD_QUERY, (user, dateBeg, dateEnd))
    results = cursor.fetchall()
    ret = []
    for row in results:
        ret.append(format_period_row(row))
    cursor.close()
    db.close()
    return ret

def query_bicycle_period(bicycle, dateBeg, dateEnd):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(TRIPS_BICYCLE_PERIOD_QUERY, (bicycle, dateBeg, dateEnd))
    results = cursor.fetchall()
    ret = []
    for row in results:
        ret.append(format_period_row(row))
    cursor.close()
    db.close()
    return ret

if __name__ == '__main__':
    assert(len(query_user_period(0, "2010-01-01T00:00:00", "2011-01-01T00:00:00")) == 409)
    assert(len(query_bicycle_period(0, "2010-01-01T00:00:00", "2011-01-01T00:00:00")) == 18)