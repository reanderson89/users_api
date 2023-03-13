import mysql.connector
import hashlib
import uuid
import os

host = os.environ.get("LOCAL_DB_HOST")
user = os.environ.get("LOCAL_DB_USER")
password = os.environ.get("LOCAL_DB_PASSWORD") 

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



def generate_uuid(email):
    hash_object = hashlib.sha224(email.encode())
    uuid_string = uuid.UUID(hash_object.hexdigest()[0:32])

    return str(uuid_string)

def insert_dummy_data():
    users = [
        (
            generate_uuid("reanderson89@gmail.com"),
            "reanderson89",
            "Robert",
            "reanderson89@gmail.com",
            "5039279423",
        ),
        (
            generate_uuid("staudere@gmail.com"),
            "estauder90",
            "Elsa",
            "staudere@gmail.com",
            "5039613187",
        ),
        (
            generate_uuid("missKnowHow@gmail.com"),
            "appaKnowHow",
            "Appa",
            "missKnowHow@gmail.com",
            "5039279424",
        ),
        (
            generate_uuid("gooser@gmail.com"),
            "gooseyGirl",
            "Goose",
            "gooser@gmail.com",
            "5039613188",
        ),
    ]
    insert_sql = """
    INSERT INTO user (uuid, username, name, email, sms)
    VALUES(%s, %s, %s, %s, %s);
    """
    my_cursor.executemany(insert_sql, users)
    # my_db.commit() is needed to save the changes made to the db
    my_db.commit()
    print("adding seed data...")

insert_dummy_data()
