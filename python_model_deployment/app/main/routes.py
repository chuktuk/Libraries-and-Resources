#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os
from flask import (
    render_template, flash, redirect, url_for, request, send_from_directory, current_app as app
)
# from app import cfg
from app.main import bp


# favicon, sets the icon in the tab
@bp.route('/favicon.ico')
def favicon():
    # return url_for('static', filename='/images/sclogo_no_background.png')
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'RStudio-Logo-Flat-icon.png', mimetype='image/png')


# index page
@bp.route('/')
@bp.route('/index')
def index():
    """Landing/home page."""
    return render_template('index.html', title=' '.join([app.config['APPLICATION_NAME'], 'Home']))
