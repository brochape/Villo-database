import sqlite3
from config import db_filename
import helpers
import datetime

STATIONS_QUERY="""
    SELECT stations.num, stations.name, stations.seller, stations.capacity, stations.coordX, stations.coordY, COUNT(bicycles.station)
    FROM stations
    LEFT OUTER JOIN bicycles ON stations.num = bicycles.station
    GROUP BY bicycles.station"""

TAKEBIKE_QUERY="""
    UPDATE bicycles
    SET station=NULL, user=?
    WHERE id=?
"""

START_TRIP_QUERY="""
    INSERT INTO trips (bycicle,user,start,startTime)
    VALUES (?,?,?,?)
"""

BICYCLES_QUERY="""
    SELECT bicycles.id
    FROM bicycles
    WHERE bicycles.station=?
"""

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
        result["bicycles"] = row[6]
        results.append(result)
    cursor.close()
    db.close()
    return results

def select_bicycles(stationID):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(BICYCLES_QUERY,(stationID))
    results = []
    for row in cursor.fetchall():
        results.append(row)
    cursor.close()
    db.close()
    return results


def take_bicycle(user, station):
    try:
        bicycleID = select_bicycles(station)[0]
    except Exception, e:
        return None
    else:
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        cursor.execute(TAKEBIKE,(user,bycicleID))
        currentTime = datetime.datetime.now();
        timeStr =   str(currentTime.year)+"-"+\
                    "%02d"%currentTime.month+"-"+\
                    "%02d"%currentTime.day+"T"+\
                    "%02d"%currentTime.hour+":"+\
                    "%02d"%currentTime.minute+":"+\
                    "%02d"%currentTime.second
        cursor.execute(START_TRIP_QUERY, (bycicleID, user, station, timeStr))
        db.commit()
        cursor.close()
        db.close()
