all:
	rm dist/projet.zip
	zip dist/projet.zip src/*.py src/templates/* src/extension-functions.c src/static/* rapport/rapport.pdf README.md requirements.txt data/*.csv data/*.xml src/makefile src/tables.sql
