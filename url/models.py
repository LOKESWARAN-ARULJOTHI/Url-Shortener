from . import db,login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False,index=True)
    email = db.Column(db.String(120), unique=True, nullable=False,index=True)
    password = db.Column(db.String(256))

    urls = db.relationship('Urls',backref='user',lazy=True,uselist=False)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password


    def __repr__(self):
        return f'username:{self.username}, email:{self.email}'

class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shorturl = db.Column(db.String(50),unique=True,index=True)
    longurl = db.Column(db.String(250),unique=True,index=True)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    click = db.Column(db.Integer)
    user_email = db.Column(db.String(120),db.ForeignKey('user.email'),nullable=False)

    def __init__(self,longurl,shorturl,user_email,click):
        self.longurl = longurl
        self.shorturl = shorturl
        self.user_email = user_email
        self.click = click

    def __repr__(self):
        return f'shorturl:{self.shorturl},longurl:{self.longurl},date:{self.date},clicks:{self.click}'
        
    