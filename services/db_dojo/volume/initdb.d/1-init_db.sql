CREATE DATABASE IF NOT EXISTS dojo;
USE dojo;

CREATE TABLE IF NOT EXISTS User (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(24) NOT NULL UNIQUE,
    email VARCHAR(256) NOT NULL  UNIQUE,
    hashPassword VARCHAR(72) NOT NULL  UNIQUE
);

CREATE TABLE IF NOT EXISTS Scope (
    apiName VARCHAR(256) NOT NULL UNIQUE,
    scopeValue VARCHAR(256) NOT NULL,
    summary TINYTEXT,
    PRIMARY KEY (apiName, scopeValue)
);

CREATE TABLE IF NOT EXISTS ScopeAssignedToUser (
    userId INT NOT NULL UNIQUE,
    apiName VARCHAR(256) NOT NULL UNIQUE,
    scopeValue VARCHAR(256) NOT NULL,
    FOREIGN KEY (apiName,scopeValue) 
        REFERENCES Scope(apiName, scopeValue)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (userId) 
        REFERENCES User(userId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    PRIMARY KEY (userId,apiName,scopeValue)
);