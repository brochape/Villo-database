CREATE TABLE IF NOT EXISTS stations (
    num INTEGER, 
    name TEXT, 
    seller INTEGER, 
    capacity INTEGER NOT NULL, 
    coordX REAL, 
    coordY REAL

);

CREATE TABLE IF NOT EXISTS subs (
    userID INTEGER PRIMARY KEY REFERENCES users(userID),
    RFID INTEGER NOT NULL, # -> TEXT pour checker facilement les premiers char?
    lastname TEXT NOT NULL,  
    firstname TEXT, 
    phone INTEGER, # -> TEXT pour checker facilement les premiers char?
    addresscity TEXT, 
    addresscp INTEGER, 
    addressstreet TEXT, 
    addressnumber INTEGER, 
    subscribeDate TEXT

);

CREATE TABLE IF NOT EXISTS tempUsers (
    userID INTEGER PRIMARY KEY REFERENCES users(userID)

);

CREATE TABLE IF NOT EXISTS users (
    userID INTEGER PRIMARY KEY,
    password TEXT, 
    expiryDate TEXT, 
    card INTEGER

);

CREATE TABLE IF NOT EXISTS bicycles (
    id INTEGER PRIMARY KEY,
    servicedate TEXT,
    model TEXT,
    state BOOLEAN,
    station INTEGER REFERENCES stations(num),
    user INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS trips (
    bycicle INTEGER REFERENCES bicycles(id)
    user INTEGER REFERENCES users(userID),
    start INTEGER REFERENCES stations(num),
    startTime TEXT,
    ending INTEGER REFERENCES stations(num),
    endingTime TEXT
);