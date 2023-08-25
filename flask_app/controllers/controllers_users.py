from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.models_user import User
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/login_user', methods = ["post"])
def login_user():
    print("login_user")
    data = {
        'firstname' : request.form['firstname']
    }
    user = User.getName(data)
    if not user:
        flash("Not in database! Contact Admin to restore account.")
        return redirect('/login')
    if not bcrypt.check_password_hash(user[0]['password'], request.form['password']):
        flash ("Wrong Password, do try again :p")
        return redirect('/login')
    session['user_id'] = user[0]['id']
    flash("Welcome back")
    return redirect ('/dashboard')

#Check Validations
@app.route('/register_user', methods=['post'])
def register_user():
    isValid=User.validate(request.form)
    if not isValid:
        flash("Try again")
        return redirect('/register')
    else:
        newdata = {
            'firstname' : request.form.get('firstname'),
            'email' : request.form['email'],
            'password' : bcrypt.generate_password_hash(request.form['password']),
            'confirm' : bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.save(newdata)
    if not id:
        flash("something went wrong")
        return redirect('/register')
    else:
        session['user_id'] = id
        print("login successful")
        return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged Out")
    return redirect('/bloghome')