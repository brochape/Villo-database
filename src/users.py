import sqlite3
import re
import datetime
import random
from config import db_filename
import helpers
import math

USER_IS_ADMIN_QUERY="""
    SELECT userID 
    FROM admins 
    WHERE userID=?
"""
# TODO change login query for production
LOGIN_QUERY="""
    SELECT users.userID 
    FROM users 
    WHERE users.userID=? AND users.password=?"""
# LOGIN_QUERY="""SELECT users.userID FROM users 
#   INNER JOIN admins on admins.userID = users.userID
#   WHERE users.userID=? and users.password=? and (users.expiryDate > datetime('now') or admins.userID = users.userID)"""
USER_INSERT_QUERY="""
    INSERT INTO users (password, expiryDate, card) 
    VALUES(?, ?, ?)"""
SUBSCRIBER_INSERT_QUERY="""
    INSERT INTO subs(userID, RFID, lastname, firstname, phone, addresscity, addresscp, addressstreet, addressnumber, subscribeDate)
    VALUES(last_insert_rowid(),?,?,?,?,?,?,?,?,datetime('now'))"""
TEMPUSER_INSERT_QUERY="""
    INSERT INTO tempUsers(userID, paymentDate) 
    VALUES(last_insert_rowid(), datetime('now'))"""
USER_IS_TRAVELLING_QUERY="""
    SELECT COUNT(*)
    FROM bicycles
    WHERE user = ?
"""
SUB_RENEW_QUERY="""
    UPDATE users
    SET expiryDate=
        strftime("%Y-%m-%dT%H:%M:%S", (SELECT MAX(users.expiryDate, DATETIME('now'))
        FROM subs
        INNER JOIN users ON users.userID = subs.userID
        WHERE subs.userID = ?), '+1 year')
    WHERE users.userID = ?
"""
USERS_ONE_QUERY="""
    SELECT userID, expiryDate, card
    FROM users
    WHERE userID = ?
"""
SUBS_ONE_QUERY="""
    SELECT lastname, firstname, phone, addresscity, addresscp, addressstreet, addressnumber, subscribeDate
    FROM subs
    WHERE userID = ?
"""
SUBS_ALL_QUERY="""
    SELECT lastname, firstname, phone, addresscity, addresscp, addressstreet, addressnumber, subscribeDate, (expiryDate >= datetime('now')), subs.userID
    FROM subs
    INNER JOIN users on users.userID = subs.userID
    ORDER BY lastname ASC, firstname ASC
"""

STATS_QUERY="""
    SELECT total_trips, total_distance, total_distance/total_trips
    FROM(
        SELECT COUNT(*) AS total_trips,
            SUM(sqrt(power((s1.coordX-s2.coordX)*71, 2) + power((s1.coordY-s2.coordY)*111, 2))) AS total_distance
        FROM trips
        INNER JOIN users ON users.userID = trips.user
        INNER JOIN stations AS s1 ON s1.num = trips.start
        INNER JOIN stations AS s2 ON s2.num = trips.ending
        WHERE users.userID = ?
        GROUP BY trips.user
        ORDER BY COUNT(trips.user)
    )
"""

# TODO accents etc
attr_regex = {
    # subscribers
    "lastname": "\w{2,50}",
    "firstname": "\w{2,50}",
    "phone": "[0-9]{9,10}",
    "addresscity": "[\w-]{2,50}",
    "addresscp": "[0-9]{4}",
    "addressstreet": "[\w-]{2,50}",
    "addressnumber": "[0-9]{1,4}\w?",
    # users
    "password": "[0-9]{4}",
    "card": "[0-9]{17}"
}
    
attr_names = dict(zip(attr_regex.keys(), ["Postal code", "Phone number", "Street number", "First name", "Street name", "Last name", "Card number", "Password", "City"]))


def login(user, password):
    global LOGIN_QUERY
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(LOGIN_QUERY, (user, password))
    result = cursor.fetchone()
    db.close()
    if result:
        return True
    else:
        return False

def register(user):
    global attr_regex, attr_names

    errors = []
    attr_regex_new = {}
    if user["validity"] == "2":
        attr_regex_new = attr_regex
    elif user["validity"] == "0" or user["validity"] == "1":
        attr_regex_new = {key: attr_regex[key] for key in ["password", "card"]}
    else:
        errors.append("Validity time is not valid")
    for attr, regex in attr_regex_new.iteritems():
        if not re.match(regex, user[attr]):
            errors.append(attr_names[attr] + " is not valid")

    # TODO generate RFID
    if errors == []:
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        if user["validity"] == "2":
            duration = datetime.timedelta(days=365)
        elif user["validity"] == "0":
            duration = datetime.timedelta(days=1)
        elif user["validity"] == "1":
            duration = datetime.timedelta(days=7)
        cursor.execute(USER_INSERT_QUERY, (user["password"], datetime.datetime.now() + duration, user["card"]))
        if user["validity"] == "2":
            cursor.execute(SUBSCRIBER_INSERT_QUERY, 
                (random.randint(10000000000,999999999999), user["lastname"], user["firstname"],
                user["phone"], user["addresscity"], user["addresscp"], user["addressstreet"], user["addressnumber"]))
        elif user["validity"] == "0" or user["validity"] == "1":
            cursor.execute(TEMPUSER_INSERT_QUERY)
        db.commit()
        lastid = cursor.lastrowid
        cursor.close()
        db.close()
        return None, lastid
    else:
        return errors, None

def isTravelling(user):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(USER_IS_TRAVELLING_QUERY, (user,))
    ret = cursor.fetchone()
    cursor.close()
    db.close()
    return ret[0] == 1

def isAdmin(user):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(USER_IS_ADMIN_QUERY, (user,))
    result = cursor.fetchone()
    db.close()
    if result:
        return True
    else:
        return False

def reNewSub(user):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(SUB_RENEW_QUERY, (user,user))
    db.commit()
    cursor.close()
    db.close()

def get_one_user(user):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(USERS_ONE_QUERY,(user,))
    result = cursor.fetchone()
    ret = None
    if result:
        ret = {}
        ret["userID"] = result[0]
        ret["expiryDate"] = helpers.format_datetime(result[1])
        ret["card"] = result[2]
        ret["card"] = "".join(['*' for i in range(13)]) + ret["card"][-4:]
    cursor.close()
    db.close()
    return ret

def format_row(row):
    ret = {}
    ret["lastname"] = row[0]
    ret["firstname"] = row[1]
    ret["phone"] = row[2]
    ret["addresscity"] = row[3]
    ret["addresscp"] = row[4]
    ret["addressstreet"] = row[5]
    ret["addressnumber"] = row[6]
    ret["subscribeDate"] = helpers.format_datetime(row[7])
    return ret

def get_one_sub(user):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(SUBS_ONE_QUERY, (user,))
    result = cursor.fetchone()
    ret = None
    if result:
        ret = format_row(result)
    cursor.close()
    db.close()
    return ret

def get_all_subs():
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute(SUBS_ALL_QUERY)
    results = cursor.fetchall()
    ret = []
    for result in results:
        row = format_row(result)
        row["active"] = True if result[8] == 1 else False
        row["userID"] = result[9]
        ret.append(row)
    cursor.close()
    db.close()
    return ret

def get_stats(user):
    db = sqlite3.connect(db_filename)
    db.create_function("sqrt", 1, math.sqrt)
    db.create_function("power", 2, math.pow)
    cursor = db.cursor()
    cursor.execute(STATS_QUERY, (user,))
    result = cursor.fetchone()
    if result:
        ret = {}
        ret["total_trips"] = result[0]
        ret["total_distance"] = result[1]
        ret["mean_distance"] = result[2]
    else:
        ret = None
    cursor.close()
    db.close()
    return ret    

if __name__ == '__main__':
    reNewSub(0)
    print len(get_all_subs())