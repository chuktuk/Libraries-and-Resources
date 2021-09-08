#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""Errors blueprint creation."""

from flask import Blueprint

bp = Blueprint('errors', __name__)

# include this import at the bottom to avoid circular dependencies
from app.errors import handlers
