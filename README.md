# Users_API
      
  ## **Live-Link**
[Users_API](https://usersapi-production-4c1c.up.railway.app/v1.0/users)

  ## **Description**
This is a full CRUD API built using only python and gevent. The API connects to a MySQL database. Both the API and MySQL DB are hosted on [Railway](https://railway.app/)

  ## **ROUTES**

  - GET routes:
    - All users:  `<baseURL>`/v1.0/users
    - One user:  `<baseURL>`/v1.0/users/{uuid}

  - POST route:
    - Create user: `<baseURL>`/v1.0/users
    The body of the post should use Content-Type of "x-www-form-urlencoded"
    and should use the following keys to assign values:
        - username
        - name
        - email
        - sms

  - PUT route:
    - Update user: `<baseURL>`/v1.0/users/{uuid}
    The body of the post should use Content-Type of "x-www-form-urlencoded"
    and should use the following keys to assign values:
        - username
        - name
        - email
        - sms
    - You only need to use the keys that you wish to update, or you can use all of the keys and leave the value blank. Only the keys with any value given will be updated.

  - DELETE route:
    - Delete user: `<baseURL>`/v1.0/users/{uuid}

  ## **Technology-Stack**
python, gevent, mysql, railway.app


  ## **Questions**   
  ####    **For any questions please contact**
    **Robert Anderson**
  * #### **GitHub:** [@reanderson89](https://github.com/reanderson89)
  * #### **Email:** reanderson89@gmail.com

      

