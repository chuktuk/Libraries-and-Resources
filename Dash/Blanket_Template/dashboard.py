#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""The dashboard module contains all of the init_dashboard_ functions.

Every dashboard in this application must have an init_dashboard_ function here and have that function
registered in the app/__init__.py application factory function.

Layouts are created in the layouts.py module, and those must be passed to the init_dashboard function.
All callbacks are stored in the callbacks.py module, and those must be passed to the init_dashboard function."""


# imports
import os

# use .env file if present in expected location
if not os.getenv('SOME_ENV_VAR'):
    path = os.getenv('DOTENV')
    if path and os.path.exists(path):
        try:
            from dotenv import load_dotenv
            load_dotenv(path)
        except Exception as e:
            pass

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc


# init dashboard function
def init_dashboard(server, route_prefix, dashboard_layout, init_callbacks):
    """This function initializes a dash application with the Flask host.

    :param server: the Flask app object
    :param route_prefix: the route for the current dash app being initialized (format: '/dashboard_route/')
    :param dashboard_layout: the layout object created by the dash_tools.create_layout function
    :param init_callbacks: the init_callbacks function from callbacks.py for the specific dash app
    :return: returns the Flask app server
    """

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix=route_prefix,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        title='Dashboard Title'
    )

    # add the layout/content to the dashboard
    dash_app.layout = html.Div(dashboard_layout)

    # initialize callbacks
    init_callbacks(dash_app)

    return dash_app.server


# for standalone dash app
# create the config instance
from werkzeug.utils import import_string
try:
    cfg = import_string(os.getenv('CONFIG_CLASS'))()
except:
    import fallback_config as fc
    config = os.getenv('CONFIG_CLASS')
    if config == 'config.ProdConfig':
        cfg = fc.ProdConfig()
    elif config == 'config.TestConfig':
        cfg = fc.TestConfig()
    else:
        cfg = fc.DevConfig()

# import the layout and callbacks (with continencies if embedded in a Flask app)
try:
    from app.plotlydash.layouts import create_layout
    from app.plotlydash.callbacks import init_callbacks
except ModuleNotFoundError:
    from layouts import create_layout
    from callbacks import init_callbacks_blanket_tracking

# create the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True,
                title='Dashboard Title')
app.layout = html.Div(create_layout())

# initialize callbacks
init_callbacks(app)


# main function for the standalone dashboard
if __name__ == '__main__':

    # run the app
    app.run_server(debug=cfg.DEBUG)
