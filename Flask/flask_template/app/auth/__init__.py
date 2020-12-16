#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The authorizations package."""


from flask import Blueprint

bp = Blueprint('auth', __name__)

# keeping this import at the end to avoid circular dependencies
from app.auth import routes
