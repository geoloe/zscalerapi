from flask import Blueprint, make_response, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
import time

auth = Blueprint('auth', __name__)

remember_user = ''
remember_password = ''

@auth.route('/get-cookie/')
def get_cookie():
    id = request.cookies.get('user')
    return id

@auth.route('/login')
def login():
    user = get_cookie()
    if not user:
        return render_template('login.html')
    return render_template('login.html', user=user)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    time.sleep(3)
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Bitte prüfe deine Anmeldedaten und versuche es erneut.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    # save username to cookie
    login_user(user, remember=remember)
    if remember:
        resp = make_response(redirect(url_for('main.index')))
        resp.set_cookie( "user", email, samesite=None, expires=20)
        return resp

    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    surname = request.form.get('surname')
    password = request.form.get('password')
    is_admin = False
    bedingungen = True if request.form.get('bedingungen') else False

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('User existiert bereits, bitte anmelden')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, surname=surname, password=generate_password_hash(password, method='sha256'), is_admin=is_admin)


    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
