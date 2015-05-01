DBFILE=../data/villo.sq3

database: create insert

create:
	sqlite3 ${DBFILE} < tables.sql

insert:
	python2 populate_db.py

sqlite:
	sqlite3 ${DBFILE}

clean:
	rm ${DBFILE}
