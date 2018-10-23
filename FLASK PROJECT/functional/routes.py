import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from functional import app, db, bcrypt, mail
from functional.forms import RegistrationForm, LoginForm, SendEmailForm, UpdateAccountForm, PostForm
from functional.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


admins = ['owenthroup@gmail.com']


@app.route("/")
def home():
    posts = Post.query.all()  # get posts
    return render_template("home.html", posts=posts)  # pass in posts


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():  # make sure no errors
        post = Post(title=form.title.data, content=form.content.data, author=current_user)  # set instance with vals from form
        db.session.add(post)  # add
        db.session.commit()  # ADD
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)


@app.route("/post/<int:post_id>")  # site.com/post/1 will be post 1, post/2 = post 2 etc (each post has an ID)
def post(post_id):
    post = Post.query.get_or_404(post_id)  # get post with that ID. If it can't it will return a 404 error.
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update")
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)  # get post with that ID. If it can't it will return a 404 error.
    if post.author != current_user:  # If the current user is NOT the author
        abort(403)  # 403 - Forbidden
    form = PostForm()
    return render_template('create_post.html', title='Update Post', form=form)  # I can use create post form cos it's the same shit we want


@app.route('/register', methods=['GET', 'POST'])  # Allow to get and post to the route
def register():
    if current_user.is_authenticated:  # if they are already logged in
        return redirect(url_for('home'))  # send them back!
    form = RegistrationForm()  # Instance of reg form
    if form.validate_on_submit():  # If the data doesn't conflict with any of the validators
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # hash their password for security
        if form.email.data in admins:  # if they are in specified admin list
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_admin=True, subscribed=form.subscribe.data)
        else:
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, subscribed=form.subscribe.data)  # create user object
        db.session.add(user)  # add user
        db.session.commit()  # commit changes and ADD the user
        send_registration_confirmation(user)
        flash(f'Account created for {form.username.data}!', 'success')  # give them a message saying they have been added
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # if they are already logged in
        return redirect(url_for('home'))  # send them back!
    form = LoginForm()
    if form.validate_on_submit():  # if no problems are found with the entered data
        user = User.query.filter_by(email=form.email.data).first()  # if no user is found with the entered email this is None
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # if user returns something (there is a user) and hashed password is the same as their password hashed
            login_user(user, remember=form.remember.data)  # log in the user using the flask-login. remember is defined in the form
            return redirect(url_for('home'))
        else:  # if no user is found or password is incorrect
            flash('Login Unsuccessful. Please check email and password', 'danger')  # flash a message at the user
    return render_template('login.html', title='Login', form=form)


@app.route('/admin', methods=['GET', 'POST'])  # used for admin controls page
def admin():
    if current_user.is_authenticated:  # check if they're logged in
        if current_user.is_admin == True:  # check if they're an admin
            form = SendEmailForm()
            if form.validate_on_submit():
                subscribed_users = User.query.filter_by(subscribed=True)
                send_admin_email(form.title.data, form.content.data, subscribed_users)
                flash('Email(s) Sent!', 'success')
                return redirect(url_for('home'))
            return render_template('admin.html', form=form)  # if they are both, give them the admin page
    else:  # if they're not logged in
        return redirect(url_for('login'))  # direct them to log in


@app.route('/logout')
def logout():
    logout_user()  # logout the user
    return redirect(url_for('home'))  # send them back home


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # to save in profile pics folder
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():  # if no problem occur in the submission of the form
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


def send_admin_email(title, content, users):
    with mail.connect() as conn:
        for user in users:
            msg = Message(recipients=[user.email],
                          body=f'Hello, {user.username} \n {content}',
                          subject=title,
                          sender=os.environ['EMAIL_ADDRESS'])
            conn.send(msg)


def send_registration_confirmation(user):
    msg = Message('Thanks for joining!',
                  sender=os.environ['EMAIL_ADDRESS'],
                  recipients=[user.email])
    msg.body = f'''Hello {user.username}. Thanks for registering.'''
    mail.send(msg)
