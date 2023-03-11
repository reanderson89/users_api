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

def check_user_exists(uuid):
    sql = "SELECT uuid FROM user WHERE uuid=%s"
    my_cursor.execute(sql, [uuid])
    result = my_cursor.fetchone()
    if result != None:
        return True
    else:
        return False

# GET all users
def select_all():
    # select all users from the table (READ)
    my_cursor.execute("select uuid, username, name, email, sms from user;")
    # the fetchall() or fetchone() is going to fetch the information selected from the above query and store it on the result variable
    result = my_cursor.fetchall()
    dictResult = []
    for row in result:
        dictResult.append({
            "uuid": row[0],
            "username": row[1],
            "name": row[2],
            "email": row[3],
            "sms": row[4],
        })
    return dictResult

# GET one user by email, need to refactor to find by UUID
def select_one_user(uuid):
    if check_user_exists(uuid):
        my_cursor.execute("select uuid, username, name, email, sms from user where uuid=%s", [uuid])
        result = my_cursor.fetchone()
        listResult = [{
            "uuid": result[0],
            "username": result[1],
            "name": result[2],
            "email": result[3],
            "sms": result[4],
        }]
        return listResult
    else:
        return "No user with uuid: "+uuid+" exists in the database"

# POST a user to the database, need to figure out how to create the UUID. Check for built-in python methods.
def create_user(args):
    insert_sql = "INSERT INTO user (uuid, username, name, email, sms) VALUES (%s, %s, %s, %s, %s);"
    user = [args["uuid"], args["username"], args["name"], args["email"], args["sms"]]
    my_cursor.execute(insert_sql, user)
    # my_db.commit() is needed to save the changes made to the db
    my_db.commit()
    user_from_db = select_one_user(args["uuid"])
    return user_from_db

# PUT, update a user in the database. Start by finding the user and getting their information to check against the incoming information.
def update_user(args, uuid):
    if check_user_exists(uuid):
        incoming_user_data = args
        user_to_update = select_one_user(uuid)[0]
        print("User before updates: ", user_to_update)
        # min = a if a < b else b
        user_to_update["username"] = incoming_user_data["username"] if user_to_update["username"] != incoming_user_data["username"] else user_to_update["username"]
        user_to_update["name"] = incoming_user_data["name"] if user_to_update["name"] != incoming_user_data["name"] else user_to_update["name"]
        user_to_update["email"] = incoming_user_data["email"] if user_to_update["email"] != incoming_user_data["email"] else user_to_update["email"]
        user_to_update["sms"] = incoming_user_data["sms"] if user_to_update["sms"] != incoming_user_data["sms"] else user_to_update["sms"]
        update_sql = "UPDATE user SET username=%s, name=%s, email=%s, sms=%s WHERE uuid=%s"
        user = [user_to_update["username"], user_to_update["name"], user_to_update["email"], user_to_update["sms"], user_to_update["uuid"]]
        my_cursor.execute(update_sql, user)
        my_db.commit()
        user_from_db = select_one_user(user_to_update["uuid"])
        return user_from_db
    else:
        return "No user with uuid: "+uuid+" exists in the database"

def delete_user(uuid):
    if check_user_exists(uuid):
        delete_sql = "delete from user where uuid=%s"
        my_cursor.execute(delete_sql, [uuid])
        my_db.commit()
        message = "User with uuid: "+uuid+" has been deleted."
        return message
    else:
        return "There is no current user with uuid: "+uuid+" in the database."


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
    (3, "appaKnowHow", "Appa", "missKnowHow@gmail.com", "5039279424"),
    (4, "gooseyGirl", "Goose", "gooser@gmail.com", "5039613188"),
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
