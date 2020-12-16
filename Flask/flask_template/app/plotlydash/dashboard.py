#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The dashboard module uses objects from the data and figures modules to assemble the dashboards.
For flask applications, the dashboard code must be contained in an `init_dashboard` function. The `init_dashboard`
functions for each dashboard must be registered with the app in the application factory function in app/__init__.py.

The callbacks for each dashboard must be in a separate function, and those are registered with the appropriate
`init_dashboard` function here.
"""

# imports
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from .layouts import create_single_page_app_layout, create_multi_page_app_layout
from .callbacks import init_callbacks_single_page, init_callbacks_multi_page


# init single page dashboard
def init_dashboard_single_page(server):
    """Create a plotly dashboard."""

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp_template_single/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    sidebar, content = create_single_page_app_layout()

    # define the app layout after defining the other objects
    dash_app.layout = dbc.Row([sidebar, content], style={'padding': '30px'})

    # initialize the callbacks using function below
    init_callbacks_single_page(dash_app)

    return dash_app.server


def init_multi_page_dashboard(server):
    """Create a plotly dashboard."""

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp_template_multi/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    primary_app_content = create_multi_page_app_layout()

    # define the app layout after defining the other objects
    dash_app.layout = html.Div(primary_app_content)

    # initialize the callbacks using function below
    init_callbacks_multi_page(dash_app)

    return dash_app.server
