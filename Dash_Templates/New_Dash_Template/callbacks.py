#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""This module contains the callbacks for the dash application. You must register the callbacks in app.py
by calling `init_callbacks(app)` on the app=dash.Dash() object."""


from dash.dependencies import Input, Output, State
import dash_html_components as html


def init_callbacks(dash_app):
    """This is the initialization function for the callbacks.

    # add callbacks using the following generic syntax:
    @dash_app.callback(
        Output(),
        [Input()])
    def callback(value):
        return value
    """
