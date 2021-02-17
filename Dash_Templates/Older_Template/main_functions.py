#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''This is a template that contains basic functions that are resuable.
This file should hold all functions needed to run a Dash app, then import to the app.'''

import pandas as pd

import dash
import dash_table

# must pip install dash_bootstrap_components==0.10.7 or include in requirements.txt
import dash_bootstrap_components as dbc

import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_dash_datatable(df, html_id, cell_width='150px', page_size=10):
    table = dash_table.DataTable(
                id=html_id,
                columns = [{'name': i, 'id': i} for i in df.columns],
                data=df.to_dict('records'),
                        
                style_table={'overflowX': 'auto'},
                style_cell={'minWidth': cell_width, 'width': cell_width, 'maxWidth': cell_width},
                page_size=page_size)
                
    return table