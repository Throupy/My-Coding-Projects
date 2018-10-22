from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from functional.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])  # Email makes sure it's a valid email
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):  # pass in input field to be validated (username in this case)
        user = User.query.filter_by(username=username.data).first()  # if there is no user already in the database with these credentials. then this variable will be None.
        if user:  # if the entered crentials are taken
            raise ValidationError('That username is taken. Please use a different one!')  # raise an error
            #this error will be the 'gucci' one that is displayed underneath the input box in a nice red text! (I <3 Bootstrap!)

    def validate_email(self, email):  # pass in input field to be validated (username in this case)
        user = User.query.filter_by(email=email.data).first()  # if there is no user already in the database with these credentials. then this variable will be None.
        if user:  # if the entered crentials are taken
            raise ValidationError('That email is taken. Please use a different one!')  # raise an error
            #this error will be the 'gucci' one that is displayed underneath the input box in a nice red text! (I <3 Bootstrap!)
