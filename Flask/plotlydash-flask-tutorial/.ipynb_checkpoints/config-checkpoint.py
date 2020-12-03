#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Flask config.

If you want to retrieve any of these values in the app, you must
define it as a property using the @property decorator.
You must also create an instance of the class before calling
.from_object() in the app factory function.
"""

import os


# base config
class Config:
    """Set base Flask config variables."""

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


# production config
class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    @property
    def FLASK_ENV(self):
        return 'production'


# development config
class DevConfig(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'dev'

    @property
    def FLASK_ENV(self):
        return 'development'
