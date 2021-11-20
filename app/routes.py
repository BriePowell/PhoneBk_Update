from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import UserInfoForm, PostForm, LoginForm
from app.models import User, Post

@app.route('/')
def index():
    name = 'Brie'
    title = 'My First Flask'
    return render_template('index.html', name_of_user=name, title=title)

@app.route('/top5')
def topfive(): 
    title = 'My Top 5'
    #scifi = ['Stargate SG-1', 'Star Trek (1966-2005)', 'Doctor Who (2005-)', 'The Fifth Element', 'Rick and Morty' ]
    return render_template('top5.html', title=title) #scifi=scifi

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        existing_user = User.query.filter_by(username=username).all()

        if existing_user:
            flash(f'The username {username} is already in use. Please select another.', danger)
            return redirect(url_for('register'))

        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Thank you {username}, you have succesfully registered!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Incorrect username or password', 'danger')
            return redirect(url_for('login'))

        login_user(user)

        flash(f'Welcome {user.username}. You are now logged in.', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', login_form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_post = Post(title, content, current_user.id)
        db.session.add(new_post)
        db.session.commit()

        flash(f'The post {title} has been created.', 'primary')
        return redirect(url_for('index'))

    return render_template('createpost.html', form=form)
