import os
from flask import Flask,render_template,flash,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required,current_user,login_user,logout_user
from werkzeug.security import check_password_hash,generate_password_hash
from .base62 import url_shortener
from flask_mail import Mail, Message

app=Flask(__name__)
app.config['SECRET_KEY'] = '11Lokeswaran.'

# Database ########################################################################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
app.config.update(dict(
    DEBUG = False,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'example@gmail.com',
    MAIL_PASSWORD = 'password'
))
mail = Mail(app)

# Login manager ##################################################################################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# routes ########################################################################################
from .models import User, Urls

# index page
@app.route('/', methods=['GET', 'POST'])
def index():
    all_urls = request.args.get('all_urls')
    if current_user.is_authenticated:
        print('authenticated\n',current_user.email)
        all_urls=Urls.query.filter_by(user_email=current_user.email).all()
             
    if request.method == 'POST':
        if current_user.is_authenticated:
            longurl = request.form.get('longurl')
            user_email = request.form.get('user_email')
            user_message = request.form.get('user_message')
            if user_message and user_message:
                full_message = 'mail id: ' + user_email +'\nmessage: '+user_message
                msg = Message(subject='Feedback from URL Shortener user',body=full_message,
                    sender="11lokeshmc@gmail.com",
                    recipients=["11lokeswaran@gmail.com"])
                msg.body = full_message
                mail.send(msg)
            if longurl and longurl.find('https://shrtyurl.herokuapp.com/')!= -1:
                print('its a shorturl')
                if Urls.query.filter_by(shorturl=longurl).first():
                    link = Urls.query.filter_by(shorturl=longurl).first()
                    shorturl = link.shorturl
                    print(shorturl)
                    return redirect(url_for(".index",shorturl=shorturl,all_urls=all_urls))
            elif longurl and Urls.query.filter_by(longurl=longurl).first():
                print('longurl exists')
                link = Urls.query.filter_by(longurl=longurl).first()
                print('link:',link.longurl)
                print('done')
                shorturl = link.shorturl
                print(shorturl)
                return redirect(url_for(".index",shorturl=shorturl,all_urls=all_urls))
            elif longurl:
                print('new url')
                link = Urls(longurl=longurl,shorturl=None,user_email=current_user.email,click=0)
                db.session.add(link)
                db.session.commit()
                link.shorturl = url_shortener(longurl,link.id)
                print(link.shorturl)
                db.session.commit()
                shorturl = link.shorturl
                return redirect(url_for(".index",shorturl=shorturl,all_urls=all_urls))
        else:
            flash("You need to log in to use our service", category='error')

        
    shorturl=request.args.get('shorturl')
    return render_template("index.html",user=current_user,shorturl=shorturl,all_urls=all_urls)

# Redirect shorturl to longurl
@app.route('/<shorturl>')
def shorturl(shorturl):
    print(shorturl)
    shorturl = "https://shrtyurl.herokuapp.com/"+shorturl
    link = Urls.query.filter_by(shorturl=shorturl).first_or_404()
    original_url = link.longurl
    link.click+=1
    db.session.commit()
    return redirect(original_url)

# Login page     
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            if check_password_hash(user.password,password):
                login_user(user, remember=True)
                flash('Logged in successfully')

                return redirect(url_for('index',username = user.username))   
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exists.', category='error')
    return render_template("login.html",user = current_user)

# Register page
@app.route('/signin', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').capitalize()
        email = request.form.get('email')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email Id already exists.', category='error')
        elif password!=confirmpassword:
            flash('Passwords does not match.', category='error')
        else:
            password=generate_password_hash(password)
            new_user = User(username=username,email=email,password=password)
            print('User:',new_user)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created successfully', category='success')
            return redirect(url_for('index',username=new_user.username))


    return render_template("register.html",user = current_user)

# Log out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out succesfully',category='success')
    return redirect(url_for('login'))