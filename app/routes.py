# file responsible for routing and operations related to User actions

import os
import re
from timeit import repeat
from app import app, load_user
from flask import render_template, request, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from app.models import *
import jinja2
from flask_wtf import FlaskForm
from wtforms import StringField,DateTimeField,PasswordField,EmailField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import InputRequired
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

class SingUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    repeat_password = PasswordField('RepeatPassword', validators=[InputRequired()])
    city = StringField('city', validators=[InputRequired()])
    description = TextAreaField('description', validators=[InputRequired()])
    mail = EmailField('mail', validators=[InputRequired()])
    submit = SubmitField('Submit')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password')
    repeat_password = PasswordField('RepeatPassword')
    city = StringField('city', validators=[InputRequired()])
    description = TextAreaField('description', validators=[InputRequired()])
    mail = EmailField('mail', validators=[InputRequired()])
    submit = SubmitField('Submit')

class AddEventForm(FlaskForm):
    title = StringField('title', validators=[InputRequired()])
    image = FileField(validators=[FileRequired()])
    location = StringField('location', validators=[InputRequired()])
    description = TextAreaField('description', validators=[InputRequired()])
    date = DateTimeField('date', validators=[InputRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Submit')

#main webpage
def IsLoged():
  return current_user.is_authenticated 

@app.route('/about')
def about():
    return render_template('about.html', loged = IsLoged() )

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
    form = SingUpForm()
    if request.method == 'GET':
        return render_template('signup.html', form = form, loged = IsLoged())
    else:
        user            = request.form.get('username')
        password        = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        city            = request.form.get('city')
        description     = request.form.get('description')
        mail            = request.form.get('mail')


        if password == repeat_password:
            if AddUser(user, mail, password, city, description, 'user'):
                return redirect('/login')
            else:
                flash('Istnieje taki uzytkownik')
                return render_template('signup.html', form = form, loged = IsLoged())
                
        else:
            flash('hasła nie są takie same')
            return render_template('signup.html', form = form, loged = IsLoged())


@app.route('/logout')
@login_required
def logout():
    
    logout_user()
    
    return redirect('/')

@app.route('/events')
def all_events():
    
    return render_template('events.html', events= GetAllEvents(), loged = IsLoged())

@app.route('/event/<title>')
def event(title):
    event = GetEventByTitle(title)
    if event is None:
        return render_template('event.html', loged = IsLoged(), event = "None")
    else:
        return render_template('event.html', loged = IsLoged(), event = event, like = DoesUserLike(title, current_user))

@app.route('/account', methods = ['POST', 'GET'])
@login_required
def UserAccount():
    form = EditUserForm()
    if request.method == "GET":

        return render_template('account.html', user = current_user, form = form, loged = IsLoged())
    else:
        user            = request.form.get('username')
        password        = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        city            = request.form.get('city')
        description     = request.form.get('description')
        mail            = request.form.get('mail')
        if password !='' and repeat_password != '':
            if password == repeat_password:
                EditUserPassword(current_user.id,  password)
                flash('zmieniono hasło')
            else:
                flash('hasła nie pokrywają się')
            
        EditUser(current_user.id, user, city, description, mail)
        return render_template('account.html', user = current_user, form = form, loged = IsLoged())

@app.route('/add-event', methods = ['POST', 'GET'])
@login_required
def addevent():
    form = AddEventForm()
    if request.method == "GET":
        return render_template('add-event.html', form = form)

    if form.validate_on_submit():
        title           = form.title.data
        location        = request.form.get('location')
        description     = request.form.get('description')
        date            = request.form.get('date')

        date            = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


    
        image_filename  = "image" + GetNextEventId() + '.jpg'

        if AddEvent(title, current_user.id, image_filename, description, date, location):
            form.image.data.save(os.path.join(
                app.config['UPLOAD_FOLDER'], image_filename
            ))
            flash('dodano nowe wydarzenie')
        else:
            flash('tytuł lub opis powtarzają się lub data jest nie poprawana')

    else:
        flash('zle dane')
    return render_template('add-event.html', form = form,  loged = IsLoged())

@app.route('/like/<event>')
@login_required
def likeevent(event):
    LikeEvent(current_user, event)
    return redirect('/event/' + event)

@app.route('/unlike/<event>')
@login_required
def unlikeevent(event):
    UnlikeEvent(current_user, event)
    return redirect('/event/' + event)

@app.route('/user-events')
@login_required
def user_event():

    return render_template('user-events.html', liked_events = GetAllLikedEvents(current_user), created_events = GetAllCreatedEvents(current_user), loged = IsLoged() )


@app.errorhandler(HTTPException)
def handle_bad_request(e):
    return render_template('error.html', name = e.code, desc = e.description,  loged = IsLoged() )

#PODSUMOWANIE
# TO DO
# /account
# /add
