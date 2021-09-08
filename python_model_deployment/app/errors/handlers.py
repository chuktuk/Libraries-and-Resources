#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Error handling for the app."""

from flask import render_template
from app.errors import bp


@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404
