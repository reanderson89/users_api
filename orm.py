import hashlib
import uuid
from db_connection import my_db, get_cursor

# # get database connection info from environment variables
# host = os.environ.get("DB_HOST")
# user = os.environ.get("DB_USER")
# password = os.environ.get("DB_PASSWORD")
# database = os.environ.get("DATABASE")
# port = os.environ.get("DB_PORT")

# print("connecting to DB...")

# my_db = mysql.connector.connect(host=host, user=user, password=password, database=database, port=port)

# if my_db.is_connected():
#     print("connected to database")
# else:
#     print("connection to database was unsuccessful")


def check_user_exists(uuid):
    with get_cursor() as cur:
        sql = "SELECT uuid FROM user WHERE uuid=%s"
        cur.execute(sql, [uuid])
        result = cur.fetchone()
        if result != None:
            return True
        else:
            return False


def check_email_exists(email):
    with get_cursor() as cur:
        sql = "SELECT email FROM user WHERE email=%s"
        cur.execute(sql, [email])
        result = cur.fetchone()
        if result != None:
            return True
        else:
            return False


def check_sms_exists(sms):
    with get_cursor() as cur:
        sql = "SELECT sms FROM user WHERE sms=%s"
        cur.execute(sql, [sms])
        result = cur.fetchone()
        if result != None:
            return True
        else:
            return False


def generate_uuid(email):
    hash_object = hashlib.sha224(email.encode())
    uuid_string = uuid.UUID(hash_object.hexdigest()[0:32])

    return str(uuid_string)


# GET all users
def select_all():
    with get_cursor() as cur:
        # select all users from the table (READ)
        cur.execute("select uuid, username, name, email, sms from user;")
        # the fetchall() or fetchone() is going to fetch the information selected from the above query and store it on the result variable
        result = cur.fetchall()
        print(result)
        list_result = [
            {
                "uuid": row[0],
                "username": row[1],
                "name": row[2],
                "email": row[3],
                "sms": row[4],
            }
            for row in result
        ]

        return list_result


# GET one user by email, need to refactor to find by UUID
def select_one_user(uuid):
    with get_cursor() as cur:
        if check_user_exists(uuid):
            cur.execute(
                "select uuid, username, name, email, sms from user where uuid=%s",
                [uuid],
            )
            result = cur.fetchone()
            dictResult = {
                "uuid": result[0],
                "username": result[1],
                "name": result[2],
                "email": result[3],
                "sms": result[4],
            }

            return dictResult
        else:
            return False


# POST a user to the database, need to figure out how to create the UUID. Check for built-in python methods.
def create_user(args):
    with get_cursor() as cur:
        if check_email_exists(args["email"]):
            return "email"
        if check_sms_exists(args["sms"]):
            return "phone"
        uuid = generate_uuid(args["email"])
        insert_sql = "INSERT INTO user (uuid, username, name, email, sms) VALUES (%s, %s, %s, %s, %s);"
        user = [uuid, args["username"], args["name"], args["email"], args["sms"]]
        cur.execute(insert_sql, user)
        # my_db.commit() is needed to save the changes made to the db
        my_db.commit()
        user_from_db = select_one_user(uuid)
        return user_from_db


# PUT, update a user in the database. Start by finding the user and getting their information to check against the incoming information.
def update_user(args, uuid):
    with get_cursor() as cur:
        if check_user_exists(uuid):
            user_to_update = select_one_user(uuid)[0]
            email_exists = check_email_exists(args["email"])
            sms_exists = check_sms_exists(args["sms"])
            # the below condition checks for existence, and then checks if it is assigned to the user being updated. If it exists, but is not assigned to the user being updated then it sends a return statement letting the user know it is already in use.
            if email_exists and args["email"] != user_to_update["email"]:
                return "email"
            if sms_exists and args["sms"] != user_to_update["sms"]:
                return "phone"

            incoming_user_data = args
            print(incoming_user_data.keys())
            fields_to_update = list(incoming_user_data.keys())
            for field in fields_to_update:
                if incoming_user_data[field] == "" or field == "uuid":
                    continue
                user_to_update[field] = incoming_user_data[field]

            update_sql = (
                "UPDATE user SET username=%s, name=%s, email=%s, sms=%s WHERE uuid=%s"
            )
            updated_user = [
                user_to_update["username"],
                user_to_update["name"],
                user_to_update["email"],
                user_to_update["sms"],
                uuid,
            ]
            cur.execute(update_sql, updated_user)
            my_db.commit()
            user_from_db = select_one_user(user_to_update["uuid"])
            return user_from_db
        else:
            return False


def delete_user(uuid):
    with get_cursor() as cur:
        if check_user_exists(uuid):
            delete_sql = "delete from user where uuid=%s"
            cur.execute(delete_sql, [uuid])
            my_db.commit()
            message = "User with uuid: " + uuid + " has been deleted."
            return message
        else:
            return False


# TO DO:
# Figure out how to make the UUID
