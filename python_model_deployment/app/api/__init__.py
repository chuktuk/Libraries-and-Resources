#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import model
