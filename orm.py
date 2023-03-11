from db_connection import my_db, my_cursor

def check_user_exists(uuid):
    sql = "SELECT uuid FROM user WHERE uuid=%s"
    my_cursor.execute(sql, [uuid])
    result = my_cursor.fetchone()
    if result != None:
        return True
    else:
        return False
    
def check_email_exists(email):
    sql = "SELECT email FROM user WHERE email=%s"
    my_cursor.execute(sql, [email])
    result = my_cursor.fetchone()
    if result != None:
        return True
    else:
        return False
    
def check_sms_exists(sms):
    sql = "SELECT sms FROM user WHERE sms=%s"
    my_cursor.execute(sql, [sms])
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
    if check_email_exists(args["email"]):
        return "That email address is already in use"
    if check_sms_exists(args["sms"]):
        return "That phone number is already in use"
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
        user_to_update = select_one_user(uuid)[0]
        email_exists = check_email_exists(args["email"])
        sms_exists = check_sms_exists(args["sms"])
        # the below condition checks for existence, and then checks if it is assigned to the user being updated. If it exists, but is not assigned to the user being updated then it sends a return statement letting the user know it is already in use.
        if email_exists and args["email"] != user_to_update["email"]:
            return "That email address is already in use"
        if sms_exists and args["sms"] != user_to_update["sms"]:
            return "That phone number is already in use"
        
        incoming_user_data = args
        print("User before updates: ", user_to_update)
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



