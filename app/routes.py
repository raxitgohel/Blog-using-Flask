from flask import render_template, url_for, flash, redirect, request
from app.form import LoginForm, RegestrationForm, UpdateAccountForm
from app.models import User, Post
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [{
    'author': 'John Doe',
    'title': 'First post',
    'content': 'Content of 1st post.',
    'date_posted': '22-12-2023'
}]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods = ["GET", "POST"])
def register():
    form = RegestrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename=f'profile_pics/{current_user.profile_image}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)
