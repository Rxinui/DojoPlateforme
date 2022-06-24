CREATE SCHEMA IF NOT EXISTS dojo_kata;
USE dojo_kata;

CREATE TABLE IF NOT EXISTS Training(
    trainingId INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    sensei VARCHAR(256) NOT NULL,
    details TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Workshop(
    workshopId INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    details TEXT NOT NULL,
    trainingId INT,
    FOREIGN KEY (trainingId)
        REFERENCES Training(trainingId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Imagebox(
    imageboxId INT AUTO_INCREMENT PRIMARY KEY,
    rootLogin VARCHAR(64) NOT NULL,
    userLogin VARCHAR(64) NOT NULL,
    userPassword VARCHAR(64) NOT NULL,
    filename VARCHAR(256) NOT NULL,
    type VARCHAR(256) NOT NULL,
    os VARCHAR(256) NOT NULL,
    accessProtocol ENUM('ssh','vnc','http') NOT NULL,
    options MEDIUMTEXT,
    workshopId INT,
    FOREIGN KEY (workshopId)
        REFERENCES Workshop(workshopId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

GRANT ALL PRIVILEGES ON dojo_kata.* TO 'sifu'@'localhost';
GRANT ALL PRIVILEGES ON dojo_kata.* TO 'sifu'@'172.20.0.%';
GRANT ALL PRIVILEGES ON dojo_kata.* TO 'sifu'@'%';