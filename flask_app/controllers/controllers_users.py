from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.models_user import User
# from flask_app.models.models_mailinglist import MailingList
# from flask_app.models.models_blog import Blog
# from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/login_user', methods = ["post"])
def login_user(): #user_id variable created here
    print("login_user")
    data = {
        'firstname' : request.form['firstname']
    }
    print("line 15 data: ", data)
    user = User.getName(data)
    print(user['password'])
    print(" line 18 user: ", user, "user.password: ", user['password'])
    #if Not user
    if user == False:
        flash("Not in database.")
        redirect('/login')
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash ("Wrong Password")
        print(request.form['password'], "line 21")
        print(user.password)
        return redirect('/login')
    # else:
    session['user_id'] = user['id']
    flash("welcome back")
    print('in session')
    return redirect ('/dashboard')

# @app.route('/login_user_test', methods = ["post"])
# def login_user_test(): #user_id variable created here
#     data = {
#         'email' : request.form['email'],
#     }
#     print("in login_user_test")
#     print(data)
#     user = User.getEmail(data)
#     print("USER: ", user)
#     print("back in")
#     if not user:
#         print("That email is not in the database register.")
#         redirect('/login')
#     # if not bcrypt.check_password_hash(user.password, request.form['password']):
#     #     flash ("Wrong Password")
#     #     print("wrong password")
#     #     print(request.form['password'], "login_user_test line 45")
#     #     print(user.password)
#     #     return redirect('/')
#     else:
#         print("login_user_test line 49")
#         print("USER ", user_id)
#         session['user_id'] = user_id #it got us a whole dictionary, and now we are calling on just the ID
#         # flash("welcome back")
#         print("welcome back")
#         return redirect ('/dashboard')

@app.route('/register_user', methods=['post'])
def register_user():
    print("register")
    isValid=User.validate(request.form)
    if not isValid:
        print("controller user line41")
        flash("Use Valid Inputs Please")
        return redirect('/register')
    else:
        print(request.form)
        newdata = {
            'firstname' : request.form.get('firstname'),##issue was DATABASE 1049 unknown database
            'email' : request.form['email'],
            'password' : bcrypt.generate_password_hash(request.form['password']),
            'confirm' : bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.save(newdata)
        print("ID: ", id)
    print("user saved")
    if not id:
        flash("something went wrong")
        return redirect('/register')
    else:
        session['user_id'] = id #here I defined user_id
        print("login successful")
        return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged Out")
    return redirect('/bloghome')