#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""App entry point for the flask app."""


# imports
import os
from werkzeug.utils import import_string


# use .env file if present in expected location
path = os.getenv('DOTENV')
if path and os.path.exists(path):
    try:
        from dotenv import load_dotenv
        load_dotenv(path)
    except Exception as e:
        pass

# create the app instance
from app import init_app
app = init_app()


if __name__ == '__main__':
    cfg = import_string(os.getenv('CONFIG_CLASS'))()

    app.run(debug=cfg.DEBUG)
