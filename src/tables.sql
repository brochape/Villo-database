-- TODO unique constraints
-- TODO card number in text
-- TODO RFID in text
-- TODO NOT NULL and NULL constraints

CREATE TABLE IF NOT EXISTS stations (
    num INTEGER NOT NULL, 
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
    id INTEGER PRIMARY KEY,
    servicedate TEXT NOT NULL,
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
    ending INTEGER REFERENCES stations(num),
    endingTime TEXT
);