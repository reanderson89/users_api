import mysql.connector
import hashlib
import uuid
import os

# get database connection info from environment variables
host = os.environ.get("DB_HOST")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD") 
database = os.environ.get("DATABASE")
port = os.environ.get("DB_PORT")

print("connecting to DB...")

my_db = mysql.connector.connect(host=host, user=user, password=password, database=database, port=port)

if my_db.is_connected():
    print("connected to database")
else:
    print("connection to database was unsuccessful")

def get_cursor():
    return my_db.cursor()

# The below code is for working locally and having a fresh database and dummy data each time you run the application
# drop db if it exists and then create it again and establish usage
def create_db():
    with get_cursor() as cur:
        cur.execute("drop database if exists user_db;")
        cur.execute("create database user_db;")
        cur.execute("use user_db;")

def create_table():
    # create table
    with get_cursor() as cur:
        cur.execute(
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
    with get_cursor() as cur:
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
        cur.executemany(insert_sql, users)
        # my_db.commit() is needed to save the changes made to the db
        my_db.commit()
        print("adding seed data...")

# uncomment if you need to work locally and want a fresh database and dummy data 
# create_db()
# create_table()
# insert_dummy_data()
