import sqlite3
from config import db_filename
import datetime
from dateutil.relativedelta import relativedelta


SUBS_QUERY="""
	SELECT COUNT(*) 
	FROM users
	INNER JOIN subs ON subs.userID = users.userID
	WHERE users.expiryDate >= ? and users.expiryDate <= ?
"""

TEMP_USERS_QUERY="""
	SELECT COUNT(*)
	FROM tempUsers
	INNER JOIN users ON tempUsers.userID = users.userID
	WHERE users.expiryDate >= ? AND users.expiryDate <= ?
	AND CAST((julianday(users.expiryDate) - julianday(tempUsers.paymentDate)) AS INTEGER) == ?
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
	cursor.execute(SUBS_QUERY, (dateBeg, dateEnd))
	nb = cursor.fetchone()[0]
	cursor.close()
	db.close()
	return nb

def OneDayUsers(date):
	""" Return number of temporary users on `date` 
		`date` is "month" or "year" """
	db = sqlite3.connect(db_filename)
	cursor = db.cursor()
	dateBeg, dateEnd = compute_dates(date)
	cursor.execute(TEMP_USERS_QUERY, (dateBeg, dateEnd, 1))
	nb = cursor.fetchone()[0]
	cursor.close()
	db.close()
	return nb

def OneWeekUsers(date):
	""" Return number of temporary users on `date` 
		`date` is "month" or "year" """
	db = sqlite3.connect(db_filename)
	cursor = db.cursor()
	dateBeg, dateEnd = compute_dates(date)
	cursor.execute(TEMP_USERS_QUERY, (dateBeg, dateEnd, 7))
	nb = cursor.fetchone()[0]
	cursor.close()
	db.close()
	return nb

if __name__ == '__main__':
	assert(compute_dates("12/2005") == (datetime.datetime(2005, 12, 1, 0, 0), datetime.datetime(2006, 1, 1, 0, 0)))
	assert(compute_dates("2015") == (datetime.datetime(2015, 1, 1, 0, 0), datetime.datetime(2016, 1, 1, 0, 0)))
	assert(subscribers("2011") == 552)
	assert(subscribers("10/2011") == 46)
	assert(OneDayUsers("2010") == 0)