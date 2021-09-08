#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


# api error response
def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


# code 400 is bad request, a request with invalid data
def bad_request(message):
    return error_response(400, message)
