import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer,primary_key = True)
    profile_image = db.Column(db.String(64),nullable = False,default = 'static/profile_pics/default.png')
    email = db.Column(db.String(64),unique = True,index = True)
    name = db.Column(db.String(64),unique = True,index = True)
    phno = db.Column(db.String(128),unique = True,index = True)
    password_hash = db.Column(db.String(128))

    def __init__(self,email,name,phno,password):
        self.email = email
        self.name = name
        self.phno = phno
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Messages(db.Model):
    __tablename__ = 'Messages'

    id = db.Column(db.Integer,primary_key = True)
    message = db.Column(db.Text)
    sender = db.Column(db.String(64))
    receiver = db.Column(db.String(64))

    def __init__(self,message,sender,receiver):
        self.message = message
        self.sender = sender
        self.receiver = receiver

def update_users():
    users = []
    for i in User.query.all():
        users.append((i.name,i.name))
    return users
