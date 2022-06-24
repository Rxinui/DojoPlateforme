CREATE SCHEMA IF NOT EXISTS dojo_auth;
USE dojo_auth;

CREATE TABLE IF NOT EXISTS Role (
    roleId VARCHAR(24) PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS User (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(24) NOT NULL UNIQUE,
    email VARCHAR(256) NOT NULL UNIQUE,
    hashPassword VARCHAR(72) NOT NULL,
    roleId VARCHAR(24) NOT NULL DEFAULT "deshi"
);

CREATE TABLE IF NOT EXISTS Scope (
    apiName VARCHAR(256) NOT NULL,
    scopeValue VARCHAR(256) NOT NULL,
    summary TINYTEXT,
    PRIMARY KEY (apiName, scopeValue)
);

CREATE TABLE IF NOT EXISTS ScopeAssignedToRole (
    roleId VARCHAR(24) NOT NULL,
    apiName VARCHAR(256) NOT NULL,
    scopeValue VARCHAR(256) NOT NULL,
    FOREIGN KEY (apiName,scopeValue) 
        REFERENCES Scope(apiName, scopeValue)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (roleId) 
        REFERENCES Role(roleId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    PRIMARY KEY (roleId,apiName,scopeValue)
);



-- CREATE TABLE IF NOT EXISTS Session(
--   sessionId VARCHAR(128) COLLATE utf8mb4_bin PRIMARY KEY NOT NULL,   
--   data MEDIUMTEXT COLLATE utf8mb4_bin DEFAULT '{}',
--   expires INT(11) UNSIGNED,
--   lastSeen DATETIME DEFAULT NOW(),
--   userId INT UNIQUE,
--   FOREIGN KEY (userId) 
--     REFERENCES User(userId)
--     ON UPDATE CASCADE
--     ON DELETE CASCADE
-- );

GRANT ALL PRIVILEGES ON dojo_auth.* TO 'sifu'@'localhost';
GRANT ALL PRIVILEGES ON dojo_auth.* TO 'sifu'@'172.20.0.%';
GRANT ALL PRIVILEGES ON dojo_auth.* TO 'sifu'@'%';
