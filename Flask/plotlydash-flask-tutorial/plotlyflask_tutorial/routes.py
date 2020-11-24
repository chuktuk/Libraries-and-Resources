#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The routes for the app."""


# imports
from flask import render_template
from flask import current_app as app


@app.route('/')
def home():
    """Landing Page."""
    return render_template('prim/index.html')
