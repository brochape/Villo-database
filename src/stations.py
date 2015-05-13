import sqlite3
from config import db_filename
import helpers
import datetime

STATIONS_ALL_QUERY="""
    SELECT stations.stationID, stations.name, stations.seller, stations.capacity, stations.coordX, stations.coordY, COUNT(bicycles.stationID)
    FROM stations
    LEFT OUTER JOIN bicycles ON stations.stationID = bicycles.stationID
    GROUP BY bicycles.stationID"""

BICYCLE_TAKE_QUERY="""
    UPDATE bicycles
    SET stationID=NULL, userID=?
    WHERE bicycleID=?
"""

START_TRIP_QUERY="""
    INSERT INTO trips (bicycleID,userID,startStation,startTime)
    VALUES (?,?,?,STRFTIME("%Y-%m-%dT%H:%M:%S",'now'))
"""

BICYCLE_PUT_QUERY="""
    UPDATE bicycles
    SET stationID=?, userID=NULL
    WHERE bicycleID=?
"""

END_TRIP_QUERY="""
    UPDATE trips
    SET endingStation=?, endingTime=STRFTIME("%Y-%m-%dT%H:%M:%S",'now')
    WHERE userID=? AND endingStation IS NULL AND endingTime IS NULL
"""

BICYCLES_STATION_QUERY="""
    SELECT bicycleID
    FROM bicycles
    WHERE stationID=?
"""

BICYCLES_USER_QUERY="""
    SELECT bicycleID
    FROM bicycles
    WHERE userID=?
"""

def query_all():
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(STATIONS_ALL_QUERY)
    results = []
    for row in cursor.fetchall():
        result = {}
        result["stationID"] = row[0]
        result["name"] = row[1]
        result["seller"] = "Yes" if row[2] else "No"
        result["capacity"] = row[3]
        result["coordX"] = row[4]
        result["coordY"] = row[5]
        result["bicycles"] = row[6]
        results.append(result)
    cursor.close()
    db.close()
    return results

def select_bicycles(stationID):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLES_STATION_QUERY,(stationID,))
    results = []
    for row in cursor.fetchall():
        results.append(row)
    cursor.close()
    db.close()
    return results


def take_bicycle(user, station):
    try:
        bicycleID = select_bicycles(station)[0][0]
    except Exception, e:
        print e
        return None
    else:
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        cursor.execute(BICYCLE_TAKE_QUERY,(user,bicycleID))
        cursor.execute(START_TRIP_QUERY, (bicycleID, user, station))
        db.commit()
        cursor.close()
        db.close()

def put_bicycle(user, station):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    try:
        cursor.execute(BICYCLES_USER_QUERY, (user,))
        bicycleID = cursor.fetchone()[0]
    except Exception, e:
        print e
        cursor.close()
        db.close()
        return None
    else:
        cursor.execute(BICYCLE_PUT_QUERY, (station, bicycleID))
        cursor.execute(END_TRIP_QUERY, (station, user))

    db.commit()
    cursor.close()
    db.close()