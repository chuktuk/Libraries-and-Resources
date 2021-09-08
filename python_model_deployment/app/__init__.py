#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

# imports
import os

from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from werkzeug.utils import import_string


# create the bootstrap object
bootstrap = Bootstrap()

# configuration settings
cfg = import_string(os.getenv('CONFIG_CLASS'))()


# application factory init_app function
def init_app(config=cfg):
    """The application factory function."""

    # create the flask app
    app = Flask(__name__)

    # configure the flask app using setting from the CONFIG class
    app.config.from_object(config)

    # import and register the dash apps

    # initialize bootstrap with the app
    bootstrap.init_app(app)

    # register blueprints
    from app.errors import bp as errors_bp
    from app.main import bp as main_bp
    from app.api import bp as api_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
