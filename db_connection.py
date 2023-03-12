# pip install mysql-connector-python
import mysql.connector

my_db = mysql.connector.connect(host="localhost", user="root", password="password")

my_cursor = my_db.cursor()

# drop db if it exists and then create it again and establish usage
my_cursor.execute("drop database if exists user_db;")
my_cursor.execute("create database user_db;")
my_cursor.execute("use user_db;")

# create table
my_cursor.execute(
    """
CREATE TABLE `user` (
  `pid` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `uuid` varchar(56) DEFAULT NULL UNIQUE,
  `username` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL UNIQUE,
  `sms` varchar(25) DEFAULT NULL UNIQUE,
  `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lastUpdated` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""
)

insert_sql = """
INSERT INTO user (uuid, username, name, email, sms)
VALUES(%s, %s, %s, %s, %s);
"""
users = [
    (1, "reanderson89", "Robert", "reanderson89@gmail.com", "5039279423"),
    (2, "estauder90", "Elsa", "staudere@gmail.com", "5039613187"),
    (3, "appaKnowHow", "Appa", "missKnowHow@gmail.com", "5039279424"),
    (4, "gooseyGirl", "Goose", "gooser@gmail.com", "5039613188"),
]
my_cursor.executemany(insert_sql, users)
# my_db.commit() is needed to save the changes made to the db
my_db.commit()
print("initial data added")






