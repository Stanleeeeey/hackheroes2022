from app import app
from flask import render_template
import jinja2
#KOREN ty tutaj robisz sciezki te takie @app.route('/')

#main webpage

@app.route('/')
def home_page():
    #zwroc plik index.html tak jakby co
    return render_template('index.html')