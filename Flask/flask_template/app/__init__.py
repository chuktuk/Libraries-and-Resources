#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""In this flask application template, app/ serves as the main package.

Package Contents:
1. __init__.py
    The package initiator and application factory

2. auth/
    authorization related package

3. errors/
    error related package

4. main/
    main package with generic forms/routes

5. plotlydash/
    Directory where all dash applications are stored

6. static/
    Directory for static app files like css and js files

7. templates/
    Directory for application html templates

8. translations/
    Translation related directory for spanish support

9. cli.py
    Command line utility to create `flask` functions for translations

10. mail.py
    mail module for email functionality

11. models.py
    models module for database models

12. data/
    data folder for the dashboards

13. migrations/
    Files related to sqlite database changes

14. babel.cfg
    Babel config file

15. config.py
    Configuration file for the app

16. flask_template.db
    Development database

17. README.md
    Read me markdown file

18. requirements.txt
    Application pip requirements

19. tests.py
    Unit tests

20. wsgi.py
    Application entry point
"""

import os

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask, request, current_app
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from app.mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string

# get the db
# add it to the app inside the factory function
# must create it here first though to import in other modules and accessing must occur in flask app context
db = SQLAlchemy()
migrate = Migrate()

# create the bootstrap object
bootstrap = Bootstrap()

# create the flask moment object
moment = Moment()

# create the babel instance
babel = Babel()

# login manager
login = LoginManager()
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')

# CONFIGURATION SETTINGS
# set by the ENV_FOR_FLASK environment variable
# use config.DevConfig for development
# use config.ProdConfig for production
# get an instance of the config class from config.py
cfg = import_string(os.getenv('CONFIG_CLASS'))()


# init_app function
def init_app(config=cfg):
    """Construct the core flask app (application factory)."""

    # create the flask app
    app = Flask(__name__)

    # configure the flask app using configuration settings in config.py
    app.config.from_object(config)

    # app initializations
    # the remainder of init_app was within app_context, but this wasn't working
    # was getting circular import errors on db
    # with app.app_context():

    # add the db to the app
    db.init_app(app)
    migrate.init_app(db)

    # add the login manager to the app
    # register the 'login' view from routes.py
    # add language support to login message
    login.init_app(app)

    # import any dash apps to register
    # if using multiple dash apps, init all of them
    from .plotlydash.dashboard import init_dashboard_single_page, init_multi_page_dashboard
    app = init_dashboard_single_page(app)
    app = init_multi_page_dashboard(app)

    # initialize bootstrap with the app
    bootstrap.init_app(app)

    # initialize flask moment
    moment.init_app(app)

    # initialize babel
    babel.init_app(app)

    # register blueprints
    from app.auth import bp as auth_bp
    from app.errors import bp as errors_bp
    from app.main import bp as main_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    # logging and mail handler
    if not app.debug and not app.testing:
        if app.config['LOGGING']:
            # file logger
            if not os.path.exists('logs'):
                os.mkdir('logs')
            log_name = ''.join(['logs/', app.config['APPLICATION_NAME'], '.log'])
            file_handler = RotatingFileHandler(log_name, maxBytes=10240, backupCount=10)
            file_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info(' '.join([app.config['APPLICATION_NAME'], 'Startup']))

        # good chance the email functionality won't work
        # need to test
        if app.config['EMAIL_LOGS'] and app.config['MAIL_SERVER']:
            # email logger
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_SENDER'],
                toaddrs=app.config['MAIL_RECIPIENT'],
                subject=app.config['MAIL_SUBJECT'],
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app


@babel.localeselector
def get_locale():
    """Change return value to 'es' to test spanish language."""
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    # return 'es'


from app import models
