DROP DATABASE IF EXISTS tili;
CREATE DATABASE IF NOT EXISTS tili;
use tili;


drop user 'tili_admin'@'%';
flush privileges;
-- GRANT ALL PRIVILEGES ON tili.* TO 'tili_admin';
CREATE USER 'tili_admin'@'%' IDENTIFIED BY 'tiliadmin123!';
GRANT CREATE, ALTER, INDEX, LOCK TABLES, REFERENCES, UPDATE, DELETE, DROP, SELECT, INSERT ON `tili`.* TO 'tili_admin'@'%';

FLUSH PRIVILEGES;


DROP TABLE IF EXISTS words;
CREATE TABLE IF NOT EXISTS words (
    word VARCHAR(255) NOT NULL,
    definition TEXT NOT NULL
);

-- create the databases
CREATE DATABASE IF NOT EXISTS projectone;
