DBFILE=../data/villo.sq3

all: create insert

create:
	cat tables.sql | sqlite3 ${DBFILE}

insert:
	python2 main.py

sqlite:
	sqlite3 ${DBFILE}

clean:
	rm ${DBFILE}
