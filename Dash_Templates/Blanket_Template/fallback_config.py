#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os


# base config class
class Config:
    def __init__(self):
        """Set base Flask config attributes."""

        # application name
        self.APPLICATION_NAME = "Application Name"
        self.APP_PACKAGE_HOME = 'app'

        # application home full directory
        self.APPLICATION_HOME = os.path.dirname(__file__).replace('\\', '/')

        # static folder path
        self.STATIC_FOLDER = 'static'

        # templates folder path
        self.TEMPLATES_FOLDER = 'templates'

        # logging and email log settings
        self.LOGGING = os.getenv('LOGGING')
        self.EMAIL_LOGS = os.getenv('EMAIL_LOGS')


# production config
class ProdConfig(Config):
    def __init__(self):
        """Set production environment attributes."""

        # set debug/testing to false for production
        super().__init__()
        self.DEBUG = False
        self.TESTING = False

        # set the secret key
        # for RStudio Connect deployments, set this after deployment
        self.SECRET_KEY = os.getenv('SECRET_KEY')

        # email subject
        self.MAIL_SUBJECT = "Production Error: "

        # generation database
        self.DATABASE = 'production'

        self.FLASK_ENV = 'production'


# development config
class DevConfig(Config):
    def __init__(self):
        """Set development environment attributes."""

        # set debug to true
        super().__init__()
        self.DEBUG = True
        self.TESTING = False
        self.SECRET_KEY = 'dev'

        # email subject
        self.MAIL_SUBJECT = "Dev Error: "

        # generation database
        self.DATABASE = 'development'

        self.FLASK_ENV = 'development'


# testing config
class TestConfig(Config):
    def __init__(self):
        """Set testing environment attributes."""

        # set debug/testing to true
        super().__init__()
        self.DEBUG = True
        self.TESTING = True
        self.SECRET_KEY = 'testing'

        # email subject
        self.MAIL_SUBJECT = "Testing Error: "

        # generation database
        self.DATABASE = 'development'

        self.FLASK_ENV = 'testing'
