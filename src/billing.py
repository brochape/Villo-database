import sqlite3
from config import db_filename
import datetime
import math
from dateutil.relativedelta import relativedelta


SUBS_QUERY="""
	SELECT COUNT(*) 
	FROM users
	INNER JOIN subs ON subs.userID = users.userID
	WHERE subs.subscribeDate <= ?
	AND (strftime('%m/%Y', users.expiryDate) = ? OR strftime('%Y', users.expiryDate) = ?) 
		OR strftime('%m/%Y', subs.subscribeDate) = ? OR strftime('%Y', subs.subscribeDate) = ?
"""

TEMP_USERS_QUERY="""
	SELECT COUNT(*)
	FROM tempUsers
	INNER JOIN users ON tempUsers.userID = users.userID
	WHERE users.expiryDate >= ? AND users.expiryDate <= ?
	AND CAST((julianday(users.expiryDate) - julianday(tempUsers.paymentDate)) AS INTEGER) == ?
"""

TRIPS_QUERY="""
	SELECT
		SUM(CASE 
			WHEN duration = 1 THEN 0 
			WHEN duration = 2 THEN 0.5 
			WHEN duration = 3 THEN 1.5 
			ELSE (duration-3) * 2 + 1.5 
		END)
	FROM 
	(SELECT CAST((CEIL((julianday(endingTime) - julianday(startTime)) * 48.0)) AS INTEGER) AS duration
	FROM trips
	WHERE startTime >= ? AND startTime <= ? AND endingStation IS NOT NULL AND endingTime IS NOT NULL)
"""

def compute_dates(date):
	try:
		[month, year] = date.split("/")
		dateBeg = datetime.datetime(int(year), int(month), 1)
		dateEnd = dateBeg + relativedelta(months=+1)
	except Exception, e:
		dateBeg = datetime.datetime(int(date), 1, 1)
		dateEnd = dateBeg + relativedelta(years=+1)
	return dateBeg, dateEnd

def subscribers(date):
	""" Return number of subscribers that will pay their bill on `date` 
		`date` is a year or a month (month/year) """
	db = sqlite3.connect(db_filename)
	cursor = db.cursor()
	dateBeg, dateEnd = compute_dates(date)
	cursor.execute(SUBS_QUERY, (dateEnd, date, date, date, date))
	nb = cursor.fetchone()[0]
	cursor.close()
	db.close()
	return nb

def temp(date, days):
	""" Return number of temporary users with a ticket for `days` days on `date` 
		`date` is a year or a month (month/year) """
	db = sqlite3.connect(db_filename)
	cursor = db.cursor()
	dateBeg, dateEnd = compute_dates(date)
	cursor.execute(TEMP_USERS_QUERY, (dateBeg, dateEnd, days))
	nb = cursor.fetchone()[0]
	cursor.close()
	db.close()
	return nb

def OneDayUsers(date):
	return temp(date, 1)

def OneWeekUsers(date):
	return temp(date, 7)

def tempUsers(date):
	return OneDayUsers(date) + OneWeekUsers(date)

def billing_subscribers(date):
	return subscribers(date) * 30

def billing_oneweek(date):
	return OneWeekUsers(date) * 7

def billing_oneday(date):
	return OneDayUsers(date) * 1.5

def billing_tempusers(date):
	return billing_oneweek(date) + billing_oneday(date)

def billing_trips(date):
	db = sqlite3.connect(db_filename)
	db.create_function("ceil", 1, math.ceil)
	cursor = db.cursor()
	dateBeg, dateEnd = compute_dates(date)
	cursor.execute(TRIPS_QUERY, (dateBeg, dateEnd))
	result = cursor.fetchone()[0]
	cursor.close()
	db.close()
	if result:
		return result
	else:
		return 0

def billing_users(date):
	return billing_subscribers(date) + billing_oneweek(date) + billing_oneday(date)

def billing_total(date):
	return billing_trips(date) + billing_users(date)

if __name__ == '__main__':
	assert(compute_dates("12/2005") == (datetime.datetime(2005, 12, 1, 0, 0), datetime.datetime(2006, 1, 1, 0, 0)))
	assert(compute_dates("2015") == (datetime.datetime(2015, 1, 1, 0, 0), datetime.datetime(2016, 1, 1, 0, 0)))
	assert(subscribers("2011") == 552)
	assert(subscribers("10/2011") == 46)
	assert(OneDayUsers("2010") == 0)
	assert(OneWeekUsers("2010") == 0)

	# test present
	month2010 = [("0"+str(i) if i < 10 else str(i)) +"/2010" for i in range(1,13)]

	assert(billing_users("2010") == 16560.0)
	users2010 = sum(map(billing_users, month2010))
	assert(users2010 == billing_users("2010"))

	assert(billing_trips("2010") == 6429433.0)
	trips2010 = sum(map(billing_trips, month2010))
	assert(trips2010 == billing_trips("2010"))

	assert(billing_total("2010") == 6445993.0)
	total2010 = sum(map(billing_total, month2010))
	assert(total2010 == billing_total("2010"))

	# test future
	month2011 = [("0"+str(i) if i < 10 else str(i)) +"/2011" for i in range(1,13)]

	subs2011 = sum(map(subscribers, month2011))
	assert(subs2011 == subscribers("2011"))

	sum2011 = sum(map(billing_users, month2011))
	assert(sum2011 == billing_users("2011"))