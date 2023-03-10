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
  `uuid` varchar(56) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `sms` varchar(25) DEFAULT NULL,
  `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lastUpdated` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""
)

# GET all users
def select_all():
    # select all users from the table (READ)
    my_cursor.execute("select username, name, email, sms from user;")
    # the fetchall() or fetchone() is going to fetch the information selected from the above query and store it on the result variable
    result = my_cursor.fetchall()
    dictResult = []
    for row in result:
        dictResult.append({
            "username": row[0],
            "name": row[1],
            "email": row[2],
            "sms": row[3],
        })
    return dictResult

# GET one user by email, need to refactor to find by UUID
def select_one_user(email):
    my_cursor.execute("select username, name, email, sms from user where email=%s", [email])
    result = my_cursor.fetchone()
    listResult = [{
        "username": result[0],
        "name": result[1],
        "email": result[2],
        "sms": result[3],
    }]
    return listResult

# POST a user to the database, need to figure out how to create the UUID. Check for built-in python methods.
def create_user(args):
    print("db: ", args)
    insert_sql = "INSERT INTO user (uuid, username, name, email, sms) VALUES (%s, %s, %s, %s, %s);"
    user = [args["uuid"], args["username"], args["name"], args["email"], args["sms"]]
    my_cursor.execute(insert_sql, user)
    # my_db.commit() is needed to save the changes made to the db
    my_db.commit()
    user_from_db = select_one_user(args["email"])
    return user_from_db


# TO DO:
# Figure out how to make the UUID
# Refactor the select_one_user from finding by email to finding by UUID
# Create the PUT route to update a user
# Create the DELETE route to delete a user


# insert users into the table (CREATE)
insert_sql = """
INSERT INTO user (uuid, username, name, email, sms)
VALUES(%s, %s, %s, %s, %s);
"""
users = [
    (1, "reanderson89", "Robert", "reanderson89@gmail.com", "5039279423"),
    (2, "estauder90", "Elsa", "staudere@gmail.com", "5039613187"),
    (3, "appaKnowHow", "Appa", "missKnowHow@gmail.com", "5039279423"),
    (4, "gooseyGirl", "Goose", "gooser@gmail.com", "5039613187"),
    (5, "stranger danger", "stranger", "danger@gmail.com", "1234567890"),
]
my_cursor.executemany(insert_sql, users)
# my_db.commit() is needed to save the changes made to the db
my_db.commit()
print("new users added")
select_all()

# update information on a few users
update_sql = "update user set name=%s where name=%s"
users_to_update = [("Robbie", "Robert"), ("Elser", "Elsa")]
my_cursor.executemany(update_sql, users_to_update)
my_db.commit()
print("updated users names")
select_all()

# delete a user
delete_sql = "delete from user where name='stranger'"
my_cursor.execute(delete_sql)
my_db.commit()
print("deleted a user")
select_all()
