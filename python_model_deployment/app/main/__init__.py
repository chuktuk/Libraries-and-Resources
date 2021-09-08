#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""Package instantiation for the main blueprint."""


from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
