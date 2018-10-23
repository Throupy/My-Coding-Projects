import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'get your own secret key bro!'  # Make env var
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['EMAIL_ADDRESS']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASS']
mail = Mail(app)
# import routes AFTER app is made otherwise the routes.py will try to
# import the app but the app wouldn't have been made yet. This is called a circular import.
from functional import routes
