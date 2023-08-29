from flask_app import app
from flask import redirect, render_template, request, flash
from flask_app.models.models_mailinglist import MailingList
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

#BUTTON ON NEWSLETTER FORM
@app.route("/mailinglist", methods=["POST"])
def mailingList():
    print("request.form", request.form)
    isValid=MailingList.MailingListValidate(request.form)
    if not isValid:
        return redirect('/')
    newdata = {
            'email' : request.form['email']
        }
    print(newdata)
    id=MailingList.saveMailingList(newdata)
    flash("Thanks for signing up!")
    return redirect('/')

#ROUTE TO ADMIN PAGE
@app.route("/admin/mailinglist")
def adminMailingList():
    all_mailinglist=MailingList.GetAllMailing()
    return render_template('admin/mailinglist.html', all_mailinglist=all_mailinglist)

#DELETE EMAIL FROM LIST
@app.route("/delete_email/<int:id>")
def deleteEmail(id):
    data = {
        "id" : id
    }
    MailingList.deleteEmail(data)
    flash("Email has been deleted.")
    return redirect('/admin/mailinglist')