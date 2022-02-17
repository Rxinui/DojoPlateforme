CREATE USER IF NOT EXISTS 'sensei' @localhost IDENTIFIED BY 'sensei';
CREATE USER IF NOT EXISTS 'sensei' @0.0.0.0 IDENTIFIED BY 'sensei';
GRANT ALL PRIVILEGES ON dojo.* TO 'sensei' @localhost;
GRANT ALL PRIVILEGES ON dojo.* TO 'sensei' @0.0.0.0;