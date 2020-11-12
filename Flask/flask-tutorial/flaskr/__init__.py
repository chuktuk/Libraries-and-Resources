#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the application factory.

It also tells Python that flaskr should be treated like a package.
"""

import os

from flask import Flask

def create_app(test_config=None):
    
    # create and configure the app
    # uses the current python module name
    # instance_relative_config=True tells the app config files are relative to instance folder
    # instance folder is outside flaskr and has some .gitignore files
    app = Flask(__name__, instance_relative_config=True)
    
    # sets some default configurations
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
    # ensure the instace folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello World!'
    
    return app
