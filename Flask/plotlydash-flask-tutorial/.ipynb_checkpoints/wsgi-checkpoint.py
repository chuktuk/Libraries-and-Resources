#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""App entrypoint for the plotly dash flask tutorial."""

from plotlyflask_tutorial import init_app
from werkzeug.utils import import_string

import os


# create the app instance
app = init_app()


if __name__ == '__main__':
    
    # get an instance of the config class to set the debug state for the app
    cfg = import_string(os.getenv('ENV_FOR_FLASK'))()

    app.run(debug=cfg.DEBUG)
