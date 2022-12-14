# File responsible for database managment contains rows definitions, function to make using it simpler 


from cmd import IDENTCHARS
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

#User definition
class User(db.Model):
    id                  = db.Column(db.Integer, primary_key = True)
    name                = db.Column(db.String(256), unique=True)
    mail                = db.Column(db.String(256), unique=True)
    password            = db.Column(db.String(256), unique=False)
    city                = db.Column(db.String(1024), unique=False)
    description         = db.Column(db.String(4096), unique = False)
    role                = db.Column(db.String(256), unique=False)
    like                = db.Column(db.Text, unique = False)
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
    like_count  = db.Column(db.Integer)

#user related functions

def AddUser(name:str, mail:str,password:str, city:str, description:str, role:str):
    try:
        newUser = User(name = name, mail = mail, password = password, city = city, description = description, role = role, like = '')
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

def DoesUserLike(title, user):
    try:
        user_list  = user.like.split(' ')
        event_id   = GetEventByTitle(title).id


        
        if str(event_id) in user_list:
            return False
        return True
    except:
        return False

def GetAllLikedEvents(user):
    user_liked = user.like.split(' ')

    ans        = []
    for id in user_liked:
        
        try:
            ans.append(Event.query.filter_by(id = int(id)).first())
        except:
            pass
    return ans

def GetAllCreatedEvents(user):


    return Event.query.filter_by(creator = user.id).all()


# event related functions

def AddEvent(title:str, creator:str, image:str, descriprion:str, date:datetime, location:str):
    try:
        newEvent = Event(title = title, creator = creator, image = image, description =descriprion,date = date, location = location, like_count = 0 )

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

def LikeEvent(user, event_name):
    event = GetEventByTitle(event_name)

    user.like = user.like + " " + str(event.id)
    event.like_count += 1;
    db.session.commit()

def UnlikeEvent(user, event_name):
    event = GetEventByTitle(event_name)
    user_list = user.like.split(' ')
    if str(event.id) in user_list:

        event.like_count -= 1;

        user_list.remove(str(event.id))
        user.like = " ".join(user_list)
        db.session.commit()

def GetNextEventId():
    result = Event.query.all()
    

    return str(len(result) +1)
