from flask import Flask
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate, Migrate
import os


MYDIR = os.path.dirname(__file__)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + MYDIR + '/database.sql'
app.config['UPLOAD_FOLDER'] = os.path.join(MYDIR+'/'+ "static/images")
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
app.config['STATIC_URL_PATH'] = os.path.join(MYDIR+'/'+ "static")

db       = SQLAlchemy(app)
migation = Migrate(app, db)




from app import models, routes

with app.app_context():
    db.create_all()

app.run()