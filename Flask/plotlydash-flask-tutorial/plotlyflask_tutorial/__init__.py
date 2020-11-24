#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Package initiator and app factory."""

from flask import Flask
from werkzeug.utils import import_string

import os


def init_app():
    """Construct core Flask app."""

    # create the flask app
    app = Flask(__name__, instance_relative_config=True)

    # CONFIGURATION SETTINGS
    # set by the ENV_FOR_FLASK environment variable
    # config.DevConfig for development
    # config.ProdConfig for production

    # get an instance of the config class from config.py
    cfg = import_string(os.getenv('ENV_FOR_FLASK'))()

    # set the FLASK_ENV on the OS for running the app
    os.environ['FLASK_ENV'] = cfg.FLASK_ENV

    # configure the flask app
    app.config.from_object(cfg)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        # import and register objects
        from . import routes

        # import dash app
        from .plotlydash.dashboard import init_dashboard_single_page
        app = init_dashboard_single_page(app)

        from .plotlydash.dashboard import init_multi_page_dashboard
        app = init_multi_page_dashboard(app)

        return app
