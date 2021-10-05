#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, flash, g
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from datetime import datetime

import models
import forms

app = Flask(__name__)
host = '0.0.0.0'
port = 8000
debug = True

app.secret_key = "SUPERSECRETKEYDON'TSHARE"
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.db
    g.db.connect()
    g.current_user = current_user

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
@login_required
def index():
    checked_in = g.current_user._get_current_object().checked_in
    return render_template('index.html',checked_in=checked_in)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.UserRegistration()
    if form.validate_on_submit():
        models.User.create_user(
            username = form.username.data,
            password = form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("User does not exist!")
            pass
        else:
            if(check_password_hash(user.password, form.password.data)):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Username or password incorrect")
                pass
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/test')
@login_required
def testView():
    return "Sweet you're logged in!"

@app.route("/checkin", methods=['POST'])
@login_required
def checkIn():
    user = g.current_user._get_current_object()
    if not user.checked_in:
        user.checked_in = True
        user.save()
        models.CheckIn.create(
            user = user
        )
    else:
        flash("You're currently checked in!")
    return redirect(url_for('index'))

@app.route('/checkins', methods=['GET'])
@login_required
def checkIns():
    checkins = models.CheckIn.select().where(models.CheckIn.user == g.current_user._get_current_object())
    for checkIn in checkins:
        print(checkIn.timeIn)
    return redirect(url_for('index'))

@app.route('/checkOut', methods=['POST'])
@login_required
def checkOut():
    user = g.current_user._get_current_object()
    if user.checked_in:
        user.checked_in = False
        user.save()
        checkIn = models.CheckIn.select().where(models.CheckIn.user == user)[0]
        checkIn.timeOut = datetime.now()
        checkIn.save()
    else:
        flash("You're not checked in!")
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return "About"

if __name__ == '__main__':
    models.initialize()
    app.run(host=host,port=port,debug=debug)
