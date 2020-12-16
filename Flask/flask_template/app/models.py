#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The database models for the app."""

# from flask_template_main import db
from app import db, login
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime as dt
from time import time
import jwt


# the user database model
# including UserMixin from flask login provides the four required items for Flask-Login
# those four reqs are is_authenticated, is_active, is_anonymous, get_id()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_login = db.Column(db.DateTime, default=dt.utcnow())

    # define output representation for viewing user
    def __repr__(self):
        return f'<User {self.username}>'

    # setting password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # checking password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # add an avatar or profile image
    # this is not yet active, and no path to images is set
    # need way to choose an avatar or upload an image to utilize
    # uncomment section of user.html to use
    # def avatar(self):
    #     return f'path/to/images/{self.username}'

    # generate password token method
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(int(user_id))


# the user loader function, needed for Flask-Login to access the database and query user information
@login.user_loader
def load_user(user_id):
    # user_id will passed as a string, converting to int for the database query
    return User.query.get(int(user_id))
