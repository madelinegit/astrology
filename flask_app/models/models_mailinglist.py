from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import os
import re
db=os.environ["MYSQL_DATABASE_NAME"]
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")

class MailingList:
    def __init__(self, data):
        self.id = data['id'],
        self.email = data['email']

    #REGISTER NEW MAILING LIST
    @classmethod
    def saveMailingList (cls, newdata):
        query="""
        INSERT INTO mailinglist (email)
        VALUES (%(email)s);
        """
        print("ran mailing list save query")
        return connectToMySQL(db).query_db(query,newdata)

    #MAILING LIST GET ALL ADMIN PAGE
    @classmethod
    def GetAllMailing(cls):
        query = "SELECT * FROM mailinglist;"
        results = connectToMySQL(db).query_db(query)
        all_mailinglist = []
        for row in results:
            all_mailinglist.append(cls(row))
        return all_mailinglist

    @classmethod
    def deleteEmail(cls, data):
        query = "DELETE FROM mailinglist WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def MailingListValidate(mailinglist):
        isValid = True
        query = "SELECT * FROM mailinglist WHERE email=%(email)s"
        results = connectToMySQL(db).query_db(query, mailinglist)
        if len(results)>=1:
            isValid=False
        if not EMAIL_REGEX.match(mailinglist['email']):
            isValid=False
        return isValid