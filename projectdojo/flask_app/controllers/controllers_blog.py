from flask_app import app
from flask import render_template, redirect, session, request, flash
import base64
from flask_app.models.models_user import User
from flask_app.models.models_blog import Blog
from flask_app.config.mysqlconnection import connectToMySQL


@app.route('/')
def index():
    return render_template('/public/index2.html')

#ABOUT
@app.route('/about')
def about():
    return render_template('/public/about.html')

#MENU/BOOK
@app.route('/menu')
def menubook():
    return render_template('/public/menu.html')

#HIDDEN REGISTRATION
@app.route('/register')
def register():
    print('going to register page')
    return render_template('/admin/register.html')

#HIDDEN LOGIN
@app.route('/login')
def login():
    return render_template('/admin/login.html')

#BLOGHOME
@app.route('/bloghome')
def bloghome():
    all_blogs = Blog.get_all()
    print("all_blogs", all_blogs)
    return render_template('/public/bloghome.html', all_blogs=all_blogs)

#BOOKHOME
@app.route('/book')
def book():
    return render_template('/public/book.html')

#BOOK
@app.route('/book30')
def book30():
    return render_template('/public/book30min.html')

#BOOK
@app.route('/book60')
def book60():
    return render_template('/public/book60min.html')

#BOOK
@app.route('/book90')
def book90():
    return render_template('/public/book90min.html')

#BLOG
@app.route('/blog1')
def blog1():
    return render_template('blog1.html')

@app.route('/blogstyle')
def blogstyle():
    return render_template('/public/blogstyle.html')

################################################################

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    # user_data = {
    #     'id' : session ['user_id']
    #     }
    # print("user_data: ", user_data)
    # user = User.get_one(user_data)user=user,
    all_blogs = Blog.get_all()
    print("**********ALL_BLOGS ********** ", all_blogs)
    return render_template('/admin/admin_dashboard.html',  all_blogs=all_blogs)

@app.route('/create')
def create():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('admin/blog_create.html')

#ADD VALIDATIONS?
@app.route("/blog_create", methods=["POST"])
def blog_create():
    print("request.form", request.form)
    # print("request.files****************", request.files['image'].read())
    # isValid=Blog.blog_validate(request.form)
    # if not isValid:
        # return redirect('/blog_create')
    image_data_binary = request.files['image'].read()
    image_data = (base64.b64encode(image_data_binary)).decode('ascii')
    newdata = {
            'title' : request.form['title'],
            'metatitle' : request.form['metatitle'],
            'slug' : request.form['slug'],
            'date' : request.form['date'],
            'category' : request.form['category'],
            'content' : request.form['content'],
            'image' : image_data,
            'user_id' : session['user_id']
        }
    print("****NEWDATA*****", newdata)
    id=Blog.blog_create(newdata) ####NEWDATA
    print("blog saved")
    return redirect('/dashboard')

@app.route('/blog/<int:id>/<slug>')
def blog_read(id, slug):
    blog_data = {
        'id' : id
    }
    blog=Blog.get_one_blog(blog_data)
    # print("BLOG: ", blog.content)
    return render_template('/admin/blogstyle.html', blog=blog)

@app.route('/blog_edit/<int:id>')
def blog_read_edit(id):
    if 'user_id' not in session:
        return redirect('/login')
    blog_data = {
        'id' : id
    }
    print("**BLOG_DATA***", blog_data)
    blog=Blog.get_one_blog(blog_data)
    return render_template('/admin/blog_edit.html', blog=blog)

@app.route('/blog_update/<int:id>', methods = ["POST"])
def blog_update(id):
    if 'user_id' not in session:
        return redirect('/login')
    image_data_binary = request.files['image'].read()
    image_data = (base64.b64encode(image_data_binary)).decode('ascii')
    newdata= {
        'title' : request.form['title'],
        'metatitle' : request.form['metatitle'],
        'slug' : request.form['slug'],
        'date' : request.form['date'],
        'category' : request.form['category'],
        'content' : request.form['content'],
        'image' : image_data
        }
    # isValid=Blog.validateBlog(request.form)
    # if not isValid:
    #     flash("Fill all forms, & use proper-slug-format.")
    #     print("line 139 controller")
    #     return redirect(f'/blog_edit/{id}')
    print("controller line 139")
    # data = {
    #     "id" : id
    # }
    # print("***DATA FOR MODEL ln144****")
    # print("request.form", request.form)
    id=Blog.update(newdata, id)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def blog_delete(id):
    data = {
        "id" : id
    }
    Blog.delete(data)
    flash("Blog has been deleted.")
    return redirect('/dashboard')