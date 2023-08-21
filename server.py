from flask_app import app
from flask_app.controllers import controllers_blog, controllers_users, controllers_mailinglist

if __name__=="__main__":
    app.run(debug=True)