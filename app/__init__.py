# File responsible fot initializing app


from datetime import datetime
from flask import Flask
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate, Migrate
import os
from flask_login import LoginManager


MYDIR = os.path.dirname(__file__)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + MYDIR + '/database.db'
app.config['UPLOAD_FOLDER'] = os.path.join(MYDIR+'/'+ "static/images")
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
app.config['STATIC_URL_PATH'] = os.path.join(MYDIR+'/'+ "static")

db       = SQLAlchemy(app)
migation = Migrate(app, db)




from app import models

app.jinja_env.globals.update(GetUserById=models.GetUserById)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return models.GetUserById(user_id)
with app.app_context():
    db.create_all()

from app import routes

app.run()