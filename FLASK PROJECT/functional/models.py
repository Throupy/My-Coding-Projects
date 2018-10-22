from datetime import datetime
from functional import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # relationship to post model
    # backref allows us to use author attr to get post
    # lazy = true means sql alchemy will load the data only when nessicary

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Now parenthesis because we want to pass in function,nottime
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # means we have a relationship with author

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
