#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""App entry point for the this template and Flask apps."""

from app import init_app, db, cli
from app.models import User

from werkzeug.utils import import_string

import os

# use .env file if present
if os.path.exists('.env'):
    try:
        from dotenv import load_dotenv
        # not setting override=True means you can overwrite .env variables at the system env var level
        # useful for deployment to RStudio Connect, setting env vars after deployment
        load_dotenv()
    except Exception as e:
        pass

# create the app instance
app = init_app()
cli.register(app)


# create a shell context processor
# running `flask shell` in the terminal allows you to work with objects in the flask app context in the terminal
# an example is running commands on the db
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == '__main__':
    # get an instance of the config class to set the debug state for the app
    cfg = import_string(os.getenv('CONFIG_CLASS'))()

    app.run(debug=cfg.DEBUG)
