import sqlite3
from config import db_filename

# should check expiry date
ISADMIN_QUERY="SELECT userID FROM admins WHERE userID=?"
LOGIN_QUERY="SELECT userID FROM users WHERE userID=? and password=?"

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

def isAdmin(user):
	global ISADMIN_QUERY
	db = sqlite3.connect(db_filename)
	cursor = db.cursor()
	cursor.execute(ISADMIN_QUERY, (user,))
	result = cursor.fetchone()
	db.close()
	if result:
		return True
	else:
		return False