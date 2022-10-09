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

    def set_password(self):
        self.password = generate_password_hash(self.password, 'sha256')

    def check_password(self, given_password):
        given_password_hash = generate_password_hash(given_password, 'sha256')
        if check_password_hash(self.password, given_password):
            return True
        return False

class event(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    title       = db.Column(db.String(256), unique = True)
    creator     = db.Column(db.String(256), unique = False)
    image       = db.Column(db.String(256), unique = True)
    description = db.Column(db.Text, unique = True)
    date        = db.Column(db.DateTime, unique = False)
    location    = db.Column(db.String(1024), unique = False)

