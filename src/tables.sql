-- TODO unique constraints

CREATE TABLE IF NOT EXISTS stations (
    stationID INTEGER NOT NULL, 
    name TEXT NOT NULL, 
    seller BOOLEAN NOT NULL, 
    capacity INTEGER NOT NULL, 
    coordX REAL NOT NULL, 
    coordY REAL NOT NULL

);

CREATE TABLE IF NOT EXISTS subs (
    userID INTEGER PRIMARY KEY REFERENCES users(userID),
    RFID TEXT NOT NULL,
    lastname TEXT NOT NULL,  
    firstname TEXT NOT NULL, 
    phone TEXT NOT NULL,
    addresscity TEXT NOT NULL, 
    addresscp TEXT NOT NULL, 
    addressstreet TEXT NOT NULL, 
    addressnumber INTEGER NOT NULL, 
    subscribeDate TEXT NOT NULL

);

CREATE TABLE IF NOT EXISTS admins (
    userID INTEGER  NOT NULL PRIMARY KEY REFERENCES users(userID)
    
);

CREATE TABLE IF NOT EXISTS tempUsers (
    userID INTEGER  NOT NULL PRIMARY KEY REFERENCES users(userID),
    paymentDate TEXT NOT NULL

);

CREATE TABLE IF NOT EXISTS users (
    userID INTEGER PRIMARY KEY,
    password TEXT NOT NULL, 
    expiryDate TEXT NOT NULL, 
    card TEXT NOT NULL

);

CREATE TABLE IF NOT EXISTS bicycles (
    bicycleID INTEGER PRIMARY KEY,
    servicedate TEXT NOT NULL,
    model TEXT NOT NULL,
    state BOOLEAN NOT NULL,
    stationID INTEGER REFERENCES stations(stationID) NULL,
    userID INTEGER REFERENCES users(userID) NULL
);

CREATE TABLE IF NOT EXISTS trips (
    bicycleID INTEGER REFERENCES bicycles(bicycleID) NOT NULL,
    userID INTEGER REFERENCES users(userID),
    startStation INTEGER REFERENCES stations(stationID),
    startTime TEXT,
    endingStation INTEGER REFERENCES stations(stationID),
    endingTime TEXT
);