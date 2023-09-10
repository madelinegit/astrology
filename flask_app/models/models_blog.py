from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
import base64
from flask_app.models.models_user import User
db='blogs_astro'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")

class Blog:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.metatitle = data['metatitle']
        self.slug = data['slug']
        self.date = data['date']
        self.category = data['category']
        self.content = data['content']
        self.user_id = data['user_id']
        self.image=data['image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = User.get_one_user({ 'id' : data['user_id'] })

    @classmethod
    def get_one_blog(cls, data):
        query = """
            SELECT * FROM blogs
            WHERE id = %(id)s;
            """
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    #GET USERS WITH BLOGS
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM blogs
            JOIN users
            ON users.id = blogs.user_id
            """
        results = connectToMySQL(db).query_db(query)
        chefs=[]
        for user in results:
            one_chef = cls(user)
            user_data = {
                    'id' : user['users.id'], #id of the whole table(model)
                    #tried user_id same Type error
                    'firstname' : user['firstname'],
                    'email' : user['email'],
                    'password' : user['password'],
                    'created_at' : user['users.created_at'],
                    'updated_at' : user['users.updated_at']
                }
            one_chef.cook=User(user_data)
            chefs.append(one_chef)
        return chefs

    @classmethod
    def blog_create (cls, newdata):
        print("NEWDATA AT MODEL", newdata)
        query="""
        INSERT INTO blogs (title, metatitle, slug, date, category, content, image, user_id)
        VALUES (%(title)s, %(metatitle)s, %(slug)s, %(date)s, %(category)s, %(content)s, %(image)s, %(user_id)s);
        """
        print("QUERY*****:", query)
        return connectToMySQL(db).query_db(query,newdata)

    @classmethod
    def update (cls, newdata, id):
        # image_data_binary = request.files['image'].read()                   image = %(image)s
        # image_data = (base64.b64encode(image_data_binary)).decode('ascii')
        query = f"UPDATE blogs SET title = %(title)s, metatitle = %(metatitle)s, slug = %(slug)s, date = %(date)s, category = %(category)s, content = %(content)s,  image = %(image)s WHERE id={id};"
        #don't mention foregn key
        print("ran query line 109)")
        return connectToMySQL(db).query_db(query, newdata)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM blogs WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)


#CHECK VALIDATIONS
    @staticmethod
    def validateBlog(blogs):
        isValid = True
        query = "SELECT * FROM blogs WHERE id={id};"
        results = connectToMySQL(db).query_db(query, blogs)
        if len(blogs['title']) < 3:
            isValid=False
            flash("Name must be at least 3 characters.")
        if len(blogs['slug']) < 3:
            isValid=False
            flash("Slug must be at least 3 characters, use-proper-format.")
        return isValid
