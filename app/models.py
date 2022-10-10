# File responsible for database managment contains rows definitions, function to make using it simpler 
# coders responsible for db operations: Stanislaw Kawulok

from app import db
from werkzeug.security import generate_password_hash, check_password_hash

#User definition
class User(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(256), unique=True)
    mail        = db.Column(db.String(256), unique=True)
    password    = db.Column(db.String(256), unique=False)
    city        = db.Column(db.String(1024), unique=False)
    description = db.Column(db.String(4096), unique = False)
    role        = db.Column(db.String(256), unique=False)

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

def AddUser(name, mail,password, city, description, role):
    try:
        newUser = User(name = name, mail = mail, password = password, city = city, description = description, role = role)
        newUser.set_password()

        db.session.add(newUser)
        db.session.commit()

        return True
    except Exception as e:
        print(f'AddUser failed due to the error {e}')
        return False

# event related functions

def AddEvent(title, creator, image, descriprion, date, location):
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