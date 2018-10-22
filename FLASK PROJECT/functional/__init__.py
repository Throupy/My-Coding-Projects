from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'de86667ac73a96c68ffb641c150f4b84'  # Make env var
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# import routes AFTER app is made otherwise the routes.py will try to
# import the app but the app wouldn't have been made yet. This is called a circular import.
from functional import routes
