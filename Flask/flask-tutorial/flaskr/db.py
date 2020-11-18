#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains functions to work with a sqlite database for the flask app.
"""

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    
    # g is an object for each request that can store data used by multiple function during the request
    # sort of mini request globals
    if 'db' not in g:
        
        # establish a connection to sqlite using the DATABASE config key
        # the DATABASE config key file doesn't have to exist yet, and won't until the database is initialized
        g.db = sqlite3.connect(
            
            # current_app is useful when using an application factory (like I am in _init__.py)
            # there is no application object in the rest of my code, so current_app is used
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # this tells the connection to return rows that behave like dicts
        # this way you can access cols by name
        g.db.row_factory = sqlite3.Row
    
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

        
def init_db():
    
    # get the database
    db = get_db()
    
    # .open_resource() opens a file relative to the flaskr package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        

# click.command() defines a line command called 'init-db' that calls the init_db function
# more info on flask CLI in Flask_Notes.ipynb about this tutorial
# click.echo() displays a message if everything is successful to that point in the function
# this (once the command is added to the app.cli) allows you to run 'flask init-db' from the cli in flask-tutorial dir
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

    
# the close_db() and init_db_command functions need to be registered with the app
# since I'm using a factory function, that instance isn't available here
# so I need this function to do that
# this function must be imported and called from the app factory in __init__.py
def init_app(app):
    
    # app.teardown_appcontext tells Flask to call that function when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    
    # adds a new command that can be called with the flask command
    # run flask init-db (from the command line in the flask-tutorial dir)
    app.cli.add_command(init_db_command)
