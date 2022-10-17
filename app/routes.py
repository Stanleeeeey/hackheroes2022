# file responsible for routing and operations related to User actions
# coders responsible for file : Michal Koren, Stanislaw Kawulok

from app import app
from flask import render_template
import jinja2
#KOREN ty tutaj robisz sciezki te takie @app.route('/')

#main webpage

@app.route('/')
def home_page():
    #zwroc plik index.html tak jakby co
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/events')
def all_events():
    return render_template('events.html')