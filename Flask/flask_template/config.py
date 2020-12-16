#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Flask config.

If you want to retrieve any of these values in the app, you must
define it as a property using the @property decorator.
You must also create an instance of the class before calling
.from_object() in the app factory function.
"""


import os


# base config class
class Config:
    """Set base Flask config attributes."""

    # application name
    APPLICATION_NAME = os.getenv('APPLICATION_NAME')

    # application home full directory
    APPLICATION_HOME = os.path.dirname(__file__).replace('\\', '/')

    # language support
    LANGUAGES = ['en', 'es']

    # static folder path
    STATIC_FOLDER = 'static'

    # templates folder path
    TEMPLATES_FOLDER = 'templates'

    # database connections
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # logging and email log settings
    LOGGING = os.getenv('LOGGING')
    EMAIL_LOGS = os.getenv('EMAIL_LOGS')

    # emailing
    # may need to turn these into @property values to make them accessible
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT', 25)
    MAIL_SENDER = os.getenv('MAIL_SENDER')
    MAIL_RECIPIENT = os.getenv('MAIL_RECIPIENT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', False)
    MAIL_SUBJECT = os.getenv('MAIL_SUBJECT')


# production config
class ProdConfig(Config):
    """Set production environment attributes."""

    # set debug/testing to false for production
    DEBUG = False
    TESTING = False

    # set the secret key
    # for RStudio Connect deployments, set this after deployment
    SECRET_KEY = os.getenv('SECRET_KEY')

    # database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    @property
    def FLASK_ENV(self):
        return 'production'


# development config
class DevConfig(Config):
    """Set development environment attributes."""

    # set debug to true
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'dev'

    # database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    @property
    def FLASK_ENV(self):
        return 'development'


# testing config
class TestConfig(Config):
    """Set testing environment attributes."""

    # set debug/testing to true
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'testing'

    # database
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    @property
    def FLASK_ENV(self):
        return 'testing'
