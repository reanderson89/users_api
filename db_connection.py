# pip install mysql-connector-python
import mysql.connector
my_db = mysql.connector.connect(host="localhost", user="root", passwd="password")

my_cursor = my_db.cursor()

# drop db if it exists and then create it again and establish usage
my_cursor.execute("drop database if exists user_db;")
my_cursor.execute("create database user_db;")
my_cursor.execute("use user_db;")

# create table
my_cursor.execute("create table user (pid int, name varchar(255));")

def select_all():
    # select all users from the table (READ)
    my_cursor.execute("select * from user;")
    # the fetchall() or fetchone() is going to fetch the information selected from the above query and store it on the result variable
    result = my_cursor.fetchall()
    for row in result:
        print(row)

# insert users into the table (CREATE)
insert_sql = "INSERT INTO user (pid, name) VALUES (%s, %s);"
users = [(1, "rob"), (2, "elsa"), (3, "appa"), (4, "goose"), (5, 'stranger danger')]
my_cursor.executemany(insert_sql, users)
# my_db.commit() is needed to save the changes made to the db
my_db.commit()
print("new users added")
select_all()

# update information on a few users
update_sql = "update user set name=%s where name=%s"
users_to_update = [('robbie', 'rob'),('elser', 'elsa')]
my_cursor.executemany(update_sql, users_to_update)
my_db.commit()
print("updated some users")
select_all()
    
# delete a user
delete_sql = "delete from user where name='stranger danger'"
my_cursor.execute(delete_sql)
my_db.commit()
print("deleted a user")
select_all()
