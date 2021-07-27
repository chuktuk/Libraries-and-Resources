#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


# imports
import os
from werkzeug.utils import import_string
import pandas as pd
from copy import deepcopy
from datetime import datetime as dt

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
try:
    import app.utility_scripts.dash_tools as tools
    # import app.plotlydash.data as data
except ModuleNotFoundError:
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

styles = tools.DashStyles()


# checkbox with select/deselect all
control1_label = dbc.FormGroup(
    [
        dbc.Label('Conrol 1'),
        dbc.Button(
            'Select All',
            id='control1-select-all',
            color='success',
            style={
                'height': '30px',
                'padding': '0px 5px 0px 5px',
                'margin-right': '5px',
                'position': 'absolute',
                'right': '40px'
            }
        ),
        dbc.Button(
            'X',
            id='control1-deselect-all',
            color='danger',
            style={
                'height': '30px',
                'width': '25px',
                'padding': '0px 5px 0px 5px',
                'position': 'absolute',
                'right': '15px'
            }
        )
    ], style={'margin-bottom': '0px'}
)
control1 = dbc.Card(
    dbc.Checklist(
        id='control1',
        options=[
            {'label': i, 'value': i} for i in [1, 2, 3, 4]
        ],
        value=[1, 2, 3, 4]
    ), style={'padding': '5px', 'max-height': '350px', 'overflow': 'scroll'}
)

# assemble the sidebar
sidebar = dbc.Col(
    [
        html.H3(
            'Sidebar Title',
            style=styles.sidebar_title
        ),
        html.Hr(),

        dbc.FormGroup([control1_label, control1_label])
    ],
    style=styles.sidebar_column,
    width=3
)
