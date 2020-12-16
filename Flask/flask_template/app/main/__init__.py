#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Package initiator for main."""

from flask import Blueprint

bp = Blueprint('main', __name__)

# keeping this import at the end to avoid circular dependencies
from app.main import routes
