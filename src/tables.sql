-- TODO unique constraints
-- TODO card number in text
-- TODO RFID in text
-- TODO NOT NULL and NULL constraints

CREATE TABLE IF NOT EXISTS stations (
    num INTEGER NOT NULL, 
    name TEXT NOT NULL, 
    seller INTEGER NOT NULL, 
    capacity INTEGER NOT NULL, 
    coordX REAL NOT NULL, 
    coordY REAL NOT NULL

);

CREATE TABLE IF NOT EXISTS subs (
    userID INTEGER PRIMARY KEY REFERENCES users(userID),
    RFID INTEGER NOT NULL, -- -> TEXT pour checker facilement les premiers char?
    lastname TEXT NOT NULL,  
    firstname TEXT, 
    phone INTEGER, -- -> TEXT pour checker facilement les premiers char?
    addresscity TEXT, 
    addresscp INTEGER, 
    addressstreet TEXT, 
    addressnumber INTEGER, 
    subscribeDate TEXT NOT NULL

);

CREATE TABLE IF NOT EXISTS admins (
    userID INTEGER PRIMARY KEY REFERENCES users(userID)
    
);

CREATE TABLE IF NOT EXISTS tempUsers (
    userID INTEGER PRIMARY KEY REFERENCES users(userID)

);

CREATE TABLE IF NOT EXISTS users (
    userID INTEGER PRIMARY KEY,
    password TEXT NOT NULL, 
    expiryDate TEXT , 
    card INTEGER NOT NULL

);

CREATE TABLE IF NOT EXISTS bicycles (
    id INTEGER PRIMARY KEY,
    servicedate TEXT,
    model TEXT NOT NULL,
    state BOOLEAN NOT NULL,
    station INTEGER REFERENCES stations(num) NULL,
    user INTEGER REFERENCES users(id) NULL
);

CREATE TABLE IF NOT EXISTS trips (
    bicycle INTEGER REFERENCES bicycles(id) NOT NULL,
    user INTEGER REFERENCES users(userID),
    start INTEGER REFERENCES stations(num),
    startTime TEXT,
    ending INTEGER REFERENCES stations(num) NOT NULL,
    endingTime TEXT NOT NULL
);