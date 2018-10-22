from flask import render_template, url_for, flash, redirect
from functional import app, db, bcrypt
from functional.forms import RegistrationForm, LoginForm
from functional.models import User, Post


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])  # Allow to get and post to the route
def register():
    form = RegistrationForm()  # Instance of reg form
    if form.validate_on_submit():  # If the data doesn't conflict with any of the validators
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # hash their password for security
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # create user object
        db.session.add(user)  # add user
        db.session.commit()  # commit changes and ADD the user
        flash(f'Account created for {form.username.data}!', 'success')  # give them a message saying they have been added
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # if no problems are found with the entered data
        user = User.query.filter_by(email=form.email.data).first()  # Get the data of the user with the entered email address
        flash(f'You have been logged in!', 'success')  # flash a success message
        return redirect(url_for('home'))  # redirect them to home page
    else:  # if the credentials are invalid
        flash('Login Unsuccessful. Please check username and password', 'danger')  # flash a message at the user
    return render_template('login.html', title='Login', form=form)
