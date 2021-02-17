#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""This module contains functions for generating the dashboard figures."""


# imports
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

# custom imports
from classes import DashboardFigures


# helper functions for easily creating objects
def create_card(title, div_id, card_id, color='light', outline=False, inverse=False, content=None):
    """This function creates and returns a dbc.Card object.

    :param title: The card title
    :param div_id: The html id for the div component of the card content. Used to update card content in callbacks.
    :param card_id: The html id for the card. Used to change card color in callbacks.
    :param color: default = 'light': One of 'primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light',
                  'dark'.
    :param outline: boolean: default = False: Whether or not 'color' only applied to the card outline.
    :param inverse: boolean: default = False: Whether card text color is black (False) or white (True).
    :param content: default = None: The content to display on the card. If all card content is set by a callback, leave
                    as None.
    :return: Returns a dbc.Card object.
    """
    if content:
        body = dbc.CardBody(
            [
                html.Div(
                    children=[content],
                    id=div_id,
                    className='card-text'
                )
            ]
        )
    else:
        body = dbc.CardBody(
            [
                html.Div(
                    id=div_id,
                    className='card-text'
                )
            ]
        )

    card_layout = [
        dbc.CardHeader(title),
        dbc.CardBody(
            body
        )
    ]

    card = dbc.Card(card_layout, id=card_id, color=color, outline=outline, inverse=inverse)

    return card


# create a tabbed figure with Plot and Table tabs
def make_dash_figure(plot_content, table_content, table_id, md):
    """Assembles plot content and table content into a tabbed layout for a figure.

    :param plot_content: The 'children' value for the plot tab. Should be a dcc.Graph() object or an html.Div() object
                         containing a figure such as controls and dcc.Graph(). The html_id for the plot_content must be
                         set outside this function.
    :param table_content: The 'children' value for the table tab. Can contain an html.Div with a table or be None for
                          use with callbacks
    :param table_id: The html_id of the table to be used for callbacks
    :param md: The md value to set the width of the figure (integer 0-12)
    :return: Returns a dbc.Col object containing a tabbed layout (Plot/Table)
    """

    figure = dbc.Col(
        dbc.Tabs(
            children=[
                dbc.Tab(
                    label='Plot',
                    children=[
                        plot_content
                    ]
                ),
                dbc.Tab(
                    label='Table',
                    id=table_id,
                    children=[table_content]
                )
            ]
        ), md=md
    )

    return figure


# create figure objects below, then add them to the figure instance
figures = DashboardFigures(name='Dashboard Figures')
