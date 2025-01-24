
-- a Mysql script to prepare
-- MySQL server for the project
CREATE DATABASE IF NOT EXISTS HBNB_MYSQL_DB;
CREATE USER IF NOT EXISTS "hbnb_test"@"localhost" IDENTIFIED BY "HBNB_MYSQL_PWD";
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO "hbnb_test"@"localhost";
GRANT SELECT ON performance_schema.* TO "hbnb_test"@"localhost";
