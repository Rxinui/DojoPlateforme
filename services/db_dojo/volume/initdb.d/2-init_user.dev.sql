CREATE USER IF NOT EXISTS 'shihan' @localhost IDENTIFIED BY 'shihan';
CREATE USER IF NOT EXISTS 'shihan' @0.0.0.0 IDENTIFIED BY 'shihan';
GRANT ALL PRIVILEGES ON dojo.* TO 'shihan' @localhost;
GRANT ALL PRIVILEGES ON dojo.* TO 'shihan' @0.0.0.0;