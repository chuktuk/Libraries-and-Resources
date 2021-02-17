#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


# imports
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

# custom imports
from callbacks import init_callbacks
from layout import create_single_page_app_layout


# Initialize App and Set the layout Attribute

# create the layout objects using the factory function from layout.py
sidebar, content = create_single_page_app_layout()

# initialize the app and define the layout
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])

# initialize the callbacks
init_callbacks(app)


# main function
if __name__ == '__main__':
    app.run_server(debug=True)
