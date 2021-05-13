#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""Callbacks for all dash apps.

Each separate dashboard should have its own init_callbacks_ function.

The init_callbacks_ function is used to initialize the callbacks with a dashboard by calling it in the dashboard.py
module in the init_dashboard_ function."""

# imports
from werkzeug.utils import import_string
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import io
import flask
from flask import send_file
import pandas as pd
import pymongo
import numpy as np
import os
from copy import deepcopy
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date, time

try:
    import app.plotlydash.data as data
    import app.plotlydash.figures as figures
    import app.plotlydash.layouts as layouts
    import app.utility_scripts.dash_tools as tools
except ModuleNotFoundError:
    import data
    import figures
    import layouts
    import dashtools as tools

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


dashboard_resources_layout = layouts.create_dashboard_resources_layout()


# main dashboard callbacks
def init_callbacks(dash_app):
    """Callbacks for the main dashboard.

    Create dash callbacks as always here, just use @dash_app.callback().

    This function must be called on the dash application in the init_dashboard_ function in the dashboard.py module
    when creating the dash_app.
    """

    @dash_app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        # return dbc.Col(html.Div(pathname))

        if pathname == '/':
            return dbc.Row([
                dbc.Col([html.Div('Page 1 Content Here')])
            ], style={'margin-left': '5px'})
        elif pathname == '/page2':
            return dbc.Row([
                dbc.Col([html.Div('Page 2 Content Here')])
            ], style={'margin-left': '5px'})
        elif pathname == '/dashboard_resources':
            return dbc.Row([
                dbc.Col([dashboard_resources_layout])
            ])
        else:
            return dbc.Col('Error')

    # to setup download data link
    @dash_app.callback(
        Output('download-data', 'href'),
        [Input('filter-submit', 'n_clicks')],
        [State('filter1', 'value'),
         State('filter2', 'value')]
    )
    def update_overview_w_filters(n_clicks, filter1, filter2):
        # update the url with the filters, or use this callback to to only set value=True, then update data in a database
        # somewhere, and read that with the download callback

        url = f'/urlToDownload?value=True&filter1={filter1}&filter2={filter2}'
        
        return url

    # download overview data
    @dash_app.server.route('/urlToDownload')
    def download_csv():
        str_io = io.StringIO()

        try:
            value = flask.request.args.get('value')
            if not eval(value):
                some_df.to_csv(str_io, index=False)
            else:
                filter1_list = eval(flask.request.args.get('filter1'))
                filter2_string = flask.request.args.get('filter2')
                dff = deepcopy(some_df[some_df['Some Column'].isin(filter1_list)
                dff.to_csv(str_io, index=False)

            mem = io.BytesIO()
            mem.write(str_io.getvalue().encode('utf-8'))
            mem.seek(0)
            str_io.close()

            return send_file(
                mem,
                mimetype='text/csv',
                attachment_filename='download.csv',
                as_attachment=True
            )
        except Exception as e:
            return f'Download failed with the following error {type(e)}: {e}'


    # select/deselect all callback
    @dash_app.callback(
        Output('control1', 'value'),
        [Input('control1-select-all', 'n_clicks'),
         Input('control1-deselect-all', 'n_clicks')],
        [State('control1', 'options')]
    )
    def select_deselect_all(select_all, deselect_all, options):
        ctx = dash.callback_context
        if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == 'control1-deselect-all':
            selected = []
        else:
            selected = [i['value'] for i in options]
        return selected
