#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""The layouts module assembles the layout for each dash app and returns a dash.layout object.
These objects are organized into dashboards in the dashboard module."""


# imports
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

# custom imports
from classes import Styles
from controls import create_controls
from figures import figures

# create class instances
styles = Styles()


# application layout function
def create_single_page_app_layout():
    """This function creates the layout for the Time to Fill Dash Application.

    Dependencies:
        This module depends on other modules in the same directory:
            - classes.py

    Usage:
        This function is called in app.py to generate the sidebar and content used for the application.

    :return: sidebar, content
        sidebar: the html.Div component containing the sidebar for the app
        content: the primary content for the application (figures, tables, and additional controls)
    """

    # create the sidebar
    sidebar = dbc.Col(
        [
            html.Div(
                [
                    html.H2('Parameters', style=styles.dash_text),
                    html.Hr(),
                    create_controls()
                ],
                style=styles.sidebar_single_page,
            )
        ],
        style={'position': 'fixed'}
    )

    # organize the content
    content = dbc.Col(
        [
            html.H2('Dashboard Title', style=styles.dash_text),
            html.Hr(),

            # put content rows here
        ],
        style=styles.dash_content
    )

    return sidebar, content
