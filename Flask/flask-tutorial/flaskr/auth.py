#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the authentication blueprint.
"""

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# create authentication blueprint named 'auth'
# it needs to know where it's created, so __name__ is passed
# the url_prefix will be prepended to all URLs assoc. with this blueprint
# the blueprint must be registered in the app factory in __init__.py
bp = Blueprint('auth', __name__, url_prefix='/auth')


# the register view
# bp.route('/register') associates the /register url with the register view function
# when /auth/register is visited, it will call register() and the return value is the response
@bp.route('/register', methods=('GET', 'POST'))
def register():
    
    # when a user submits an html form, POST is the request.method
    if request.method == 'POST':
        
        # request.form is a dict of form submissions, and we are accessing two keys to get their values
        username = request.form['username']
        password = request.from['password']
        db = get_db()
        error = None
        
        # data validation, non-empty username and password
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # data validation, username not already stored in the user table
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'
        
        # generate and store the password hash, instead of the raw password
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            
            # commit changes to the database
            db.commit()
            
            # if all of this is successful, the user is redirected to the login page
            return redirect(url_for('auth.login'))
        
        # if the validation fails, store the error for retrieval when rendering the template
        flash(error)
        
    # render the register form page if validation fails or request.method is GET
    return render_template('auth/register.html')


# the login view
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        
        # get the submitted username and password from the login
        username = request.form['username']
        password = request.form['password']
        
        # get the db for authentication
        db = get_db()
        error=None
        
        # search for the user in the database
        # returns a dict called user
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        # validate that something was returned
        if user is None:
            error = 'Incorrect username.'
        # check the hashed password from the db user['password'] against the submitted password
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            
        # create a new session for the user id if login is valid
        # and redirect to the url for the index
        # flask securely signs the session/cookie data so it can't be tampered with
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)
        
    return render_template('auth/login.html')


# register a function that runs before the view function no matter what url is requested
# this checks if a user id is stored in the session and store as g.user which lasts for the length of the request
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        

# logout a user and remove session info, then redirect to the index
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# require a user to be logged in (use on any views you want to require a user to be logged in)
# the decorator function (login_required) wraps a view function
# it checks if a user has a session user id loaded in g.user
# if not, it redirects users to the login view
# if a user has info loaded in g.user, the requested view is returned
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
