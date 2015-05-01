DBFILE=../data/villo.sq3

all:
	python2 main.py

clean:
	rm *.pyc

database: create_db populate_db

create_db:
	sqlite3 ${DBFILE} < tables.sql

populate_db:
	python2 populate_db.py

open_db:
	sqlite3 ${DBFILE}

rm_db:
	rm ${DBFILE}

.PHONY:
	clean

