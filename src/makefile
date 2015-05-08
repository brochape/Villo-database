DBFILE=../data/villo.sq3
MATH_FILE=math-ext.so

all: math-ext.so
	python2 main.py

${MATH_FILE}: extension-functions.c 
	gcc -fPIC -Wno-unused-parameter -shared -o $@ $< -lm

database: create_db populate_db

create_db:
	sqlite3 ${DBFILE} < tables.sql

populate_db: create_db
	python2 populate_db.py

open_db: ${MATH_FILE}
	sqlite3 -cmd ".load ./${MATH_FILE}" ${DBFILE}

rm_db:
	rm ${DBFILE}

.PHONY:
	clean

clean:
	rm *.pyc
	rm ${MATH_FILE}

