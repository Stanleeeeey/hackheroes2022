# File responsible for database managment contains rows definitions, function to make using it simpler 
# coders responsible for db operations: Stanislaw Kawulok

from cmd import IDENTCHARS
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

#User definition
class User(db.Model):
    id                  = db.Column(db.Integer, primary_key = True)
    name                = db.Column(db.String(256), unique=True)
    mail                = db.Column(db.String(256), unique=True)
    password            = db.Column(db.String(256), unique=False)
    city                = db.Column(db.String(1024), unique=False)
    description         = db.Column(db.String(4096), unique = False)
    role                = db.Column(db.String(256), unique=False)
    is_authenticated    = True
    is_active           = True
    is_anonymous        = False

    def get_id(self):
        return self.id

    def set_password(self):
        self.password = generate_password_hash(self.password, 'sha256')

    def check_password(self, given_password):
        given_password_hash = generate_password_hash(given_password, 'sha256')
        if check_password_hash(self.password, given_password):
            return True
        return False

#event definition
class Event(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    title       = db.Column(db.String(256), unique = True)
    creator     = db.Column(db.String(256), unique = False)
    image       = db.Column(db.String(256), unique = True)
    description = db.Column(db.Text, unique = True)
    date        = db.Column(db.DateTime, unique = False)
    location    = db.Column(db.String(1024), unique = False)

#user related functions

def AddUser(name:str, mail:str,password:str, city:str, description:str, role:str):
    try:
        newUser = User(name = name, mail = mail, password = password, city = city, description = description, role = role)
        newUser.set_password()

        db.session.add(newUser)
        db.session.commit()

        return True
    except Exception as e:
        print(f'AddUser failed due to the error {e}')
        return False

def GetAllUsers():
    return User.query.all()

def GetUserById(id):
    return User.query.filter_by(id = id).first()

def GetUserByUserName(username:str):
    return User.query.filter_by(name=username).first()

# True if user iwth given password exists else false
def Login(username:str, password:str):
    user = User.query.filter_by(name=username).first()

    if user is None:
        return False
    elif user.check_password(password):
        return True
    else:
        return False

def EditUserPassword(id,  password):
    user = User.query.filter_by(id = id).first()

    user.password = password
    user.set_password()

    db.session.commit()


def EditUser(id, name, city, description, mail):
    user = User.query.filter_by(id = id).first()

    user.name = name
    user.city = city
    user.description = description
    user.mail = mail

    db.session.commit()
    
# event related functions

def AddEvent(title:str, creator:str, image:str, descriprion:str, date:datetime, location:str):
    try:
        newEvent = Event(title = title, creator = creator, image = image, description =descriprion,date = date, location = location )

        db.session.add(newEvent)
        db.session.commit()

        return True
    except Exception as e:
        print(f'AddEvent failed due to {e}')
        return False

def GetAllEvents():
    return Event.query.all()

def GetEventById(id : int):
    
    return Event.query.filter_by(id = id).first()

def GetEventByTitle(title : str):
    return Event.query.filter_by(title = title).first()