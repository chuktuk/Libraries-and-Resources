#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the application factory.

It also tells Python that flaskr should be treated like a package.
"""

import os

from flask import Flask

def create_app(test_config=None):
    
    # create and configure the flask instance for the app
    # uses the current python module name to set up paths
    # instance_relative_config=True tells the app config files are relative to instance folder
    # instance folder is outside flaskr and has some .gitignore files
    app = Flask(__name__, instance_relative_config=True)
    
    # sets some default configurations
    app.config.from_mapping(
        
        # SECRET_KEY is used by Flask and its extensions to keep data safe
        # ok to use 'dev' in development, but set to a random value for production
        SECRET_KEY='dev',
        
        # DATABASE is the path where the SQLite database is saved
        # app.instance_path is the path to the instance folder
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    # check if using a testing configuration (test_config)
    # if not, set the config from config.py
    # otherwise, set the config from the test_config mapping supplied
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello World!'
    
    # import and call the init_app function from db.py
    from . import db
    db.init_app(app)
    
    # import and register the blueprint
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app
