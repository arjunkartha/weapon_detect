import mysql.connector

host = "localhost"
user = "root"
password = ""  
database_name = "videoeliha"  

def select(query, data=None):
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query, data)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return result

# def is_valid_user(email, password):
#     query = "SELECT * FROM user WHERE email = %s AND password = %s"
#     print("ddddddddddddddddddddddddddddd",query)
#     result = select(query, (email, password))
#     print("ddddddddddddddddddddddddddddd",result)
#     return len(result) > 0

def update(query, data=None):
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query, data)
    cnx.commit()
    result = cursor.rowcount
    cursor.close()
    cnx.close()
    return result

def delete(query, data=None):
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query, data)
    cnx.commit()
    result = cursor.rowcount
    cursor.close()
    cnx.close()
    return result

def insert(query, data=None):
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query, data) 
    cnx.commit()
    result = cursor.lastrowid
    cursor.close()
    cnx.close()
    return result

def inserts(query):
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query) 
    cnx.commit()
    result = cursor.lastrowid
    cursor.close()
    cnx.close()
    return result

# def save_user(user_id,login_id,fname,lname,place,phone,email):
#     query = "INSERT INTO user (user_id,login_id,fname,lname,place,phone,email) VALUES (%s, %s, %s,%s, %s, %s,%s)"
#     data = (user_id,login_id,fname,lname,place,phone,email)
#     return insert(query, data)
