CREATE USER 'sensei' @localhost IDENTIFIED BY 'sensei';
CREATE USER 'sensei' @0.0.0.0 IDENTIFIED BY 'sensei';
GRANT ALL PRIVILEGES ON dojoplateforme.* TO 'sensei' @localhost;
GRANT ALL PRIVILEGES ON dojoplateforme.* TO 'sensei' @0.0.0.0;