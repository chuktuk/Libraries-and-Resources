#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""The controls module contains objects needed to generate the controls or user inputs for all dashboards."""

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


from classes import DashboardControls


def create_controls():
    """This is a factory function to create a DashboardControls object and add controls or form groups."""

    controls = DashboardControls(name='Name for Controls')

    return controls
