# file responsible for routing and operations related to User actions
# coders responsible for file : Michal Koren, Stanislaw Kawulok

import re
from app import app, load_user
from flask import render_template, request, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from app.models import Login, GetUserByUserName, AddUser, GetAllEvents, GetEventByTitle
import jinja2
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from werkzeug.exceptions import HTTPException
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

#main webpage
def IsLoged():
  return current_user.is_authenticated 

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
def home_page():
    return render_template('index.html', loged = IsLoged())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form = form, loged = IsLoged()) 
    else:
        user = request.form.get('username')
        password = request.form.get('password')
        if Login(user, password):
            login_user(GetUserByUserName(user))
            return redirect('/')
        else:
            flash('Zły login lub hasło')
            return render_template('login.html', form = form, loged = IsLoged())   

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('signup.html', form = form, loged = IsLoged())
    else:
        user = request.form.get('username')
        password = request.form.get('password')
        if AddUser(user, '', password, '', '', 'user'):
            return redirect('/login')
        else:
            flash('Zły login lub hasło')
            return render_template('signup.html', form = form, loged = IsLoged())


@app.route('/logout')
#@login_required
def logout():
    print('login out')
    logout_user()
    print(IsLoged())
    return redirect('/')

@app.route('/events')
def all_events():
    print(GetAllEvents())
    return render_template('events.html', events= GetAllEvents(), loged = IsLoged())

@app.route('/event/<title>')
def event(title):
    event = GetEventByTitle(title)
    if event is None:
        return render_template('event.html', event = "None" )
    else:
        return render_template('event.html', event = event )

@app.errorhandler(HTTPException)
def handle_bad_request(e):
    return render_template('error.html', name = e.code, desc = e.description)

#PODSUMOWANIE
# TO DO
# /account
# /add
