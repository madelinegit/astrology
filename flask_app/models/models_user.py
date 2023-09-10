from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import os
import re
db=os.environ["MYSQL_DATABASE_NAME"]
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")

class User:
    def __init__(self, data):
        self.id = data['id'],
        self.firstname = data['firstname'],
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    #REGISTER USER
    @classmethod
    def save (cls, newdata):
        query="""
        INSERT INTO users (firstname, email, password)
        VALUES (%(firstname)s, %(email)s, %(password)s);
        """
        return connectToMySQL(db).query_db(query,newdata)

    #NEW BLOG
    @classmethod
    def blog_create (cls, newdata):
        query="""
        INSERT INTO mailinglist (email)
        VALUES (%(email)s);
        """
        return connectToMySQL(db).query_db(query,newdata)

    #LOGIN GET FROM NAME
    @classmethod
    def getName(cls, data):
        print("getName")
        query = """SELECT * FROM users
                WHERE firstname = %(firstname)s;
                """
        print("ran query")
        results = connectToMySQL(db).query_db(query,data)
        return results

    #USED??
    @classmethod
    def getEmail(cls, data):
        query= """
            SELECT * FROM users
            WHERE email = %(email)s;
            """
        results= connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    #Validates New Admin Account from User Controller
    @staticmethod
    def validate(users):
        isValid = True
        query = "SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL(db).query_db(query, users)
        if len(results)>=1:
            isValid=False
            flash("Email is already in use.")
        if len(users['firstname']) < 3:
            isValid=False
            flash("Name must be at least 3 characters.")
        if len(users['password']) < 7:
            isValid=False
            flash("Password must be at least 7 characters.")
        if not EMAIL_REGEX.match(users['email']):
            isValid=False
            flash("please use a real email address.")
        if users['password'] != users['confirm']:
            isValid=False
            flash("Password doesn't match.")
        return isValid