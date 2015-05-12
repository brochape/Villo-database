import sqlite3
from config import db_filename
import helpers
import datetime

STATIONS_ALL_QUERY="""
    SELECT stations.num, stations.name, stations.seller, stations.capacity, stations.coordX, stations.coordY, COUNT(bicycles.station)
    FROM stations
    LEFT OUTER JOIN bicycles ON stations.num = bicycles.station
    GROUP BY bicycles.station"""

BICYCLE_TAKE_QUERY="""
    UPDATE bicycles
    SET station=NULL, user=?
    WHERE id=?
"""

START_TRIP_QUERY="""
    INSERT INTO trips (bicycle,user,start,startTime)
    VALUES (?,?,?,?)
"""

BICYCLE_PUT_QUERY="""
    UPDATE bicycles
    SET station=?, user=NULL
    WHERE id=?
"""

END_TRIP_QUERY="""
    UPDATE trips
    SET ending=?, endingTime=?
    WHERE user=? AND ending IS NULL AND endingTime IS NULL
"""

BICYCLES_STATION_QUERY="""
    SELECT bicycles.id
    FROM bicycles
    WHERE bicycles.station=?
"""

BICYCLES_USER_QUERY="""
    SELECT id
    FROM bicycles
    WHERE user=?
"""

def query_all():
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(STATIONS_ALL_QUERY)
    results = []
    for row in cursor.fetchall():
        result = {}
        result["num"] = row[0]
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
        currentTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        cursor.execute(START_TRIP_QUERY, (bicycleID, user, station, currentTime))
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
        currentTime = datetime.datetime.now();
        timeStr =   str(currentTime.year)+"-"+\
                    "%02d"%currentTime.month+"-"+\
                    "%02d"%currentTime.day+"T"+\
                    "%02d"%currentTime.hour+":"+\
                    "%02d"%currentTime.minute+":"+\
                    "%02d"%currentTime.second
        cursor.execute(END_TRIP_QUERY, (station, timeStr, user))

    db.commit()
    cursor.close()
    db.close()