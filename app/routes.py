# file responsible for routing and operations related to User actions
# coders responsible for file : Michal Koren, Stanislaw Kawulok

from app import app, load_user
from flask import render_template, request, flash
from flask_login import login_user
from app.models import Login, GetUserByUserName, GetAllEvents
import jinja2
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

#main webpage


@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form = form) 
    else:
        user = request.form.get('username')
        password = request.form.get('password')
        if Login(user, password):
            login_user(GetUserByUserName(user))
            return render_template('index.html')
        else:
            flash('Zły login lub hasło')
            return render_template('login.html', form = form)         
@app.route('/signup')
def signup():
    form = LoginForm()
    return render_template('login.html', form = form)

@app.route('/events')
def all_events():
    return render_template('events.html', events= GetAllEvents())

