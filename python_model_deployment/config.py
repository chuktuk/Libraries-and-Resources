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
    APPLICATION_NAME = "Model Deployment POC"
    APP_PACKAGE_HOME = 'app'

    # databases and collections
    DATABASE = 'pocMLModelMonitoring'
    API_COLLECTION = 'apis'
    PREDICTION_COLLECTION = 'iris_knn'

    # application home full directory
    APPLICATION_HOME = os.path.dirname(__file__).replace('\\', '/')

    # static folder path
    STATIC_FOLDER = 'static'

    # templates folder path
    TEMPLATES_FOLDER = 'templates'

    # logging and email log settings
    LOGGING = os.getenv('LOGGING')
    EMAIL_LOGS = os.getenv('EMAIL_LOGS')


# production config
class ProdConfig(Config):
    """Set production environment attributes."""

    # set debug/testing to false for production
    DEBUG = False
    TESTING = False

    # set the secret key
    # for RStudio Connect deployments, set this after deployment
    SECRET_KEY = os.getenv('SECRET_KEY')

    # email subject
    MAIL_SUBJECT = "POC: Model Deployment"

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

    # email subject
    MAIL_SUBJECT = "POC: Model Deployment"

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

    # email subject
    MAIL_SUBJECT = "Testing Error: Model Deployment"

    @property
    def FLASK_ENV(self):
        return 'testing'
