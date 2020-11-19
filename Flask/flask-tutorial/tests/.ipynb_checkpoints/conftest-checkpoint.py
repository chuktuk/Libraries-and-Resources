#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This is the test configuration file for unit testing."""


import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')
    

@pytest.fixture
def app():
    # create an return a temp file to use as the database for the app
    db_fd, db_path = tempfile.mkstemp()
    
    # create the app using the temp file for the database
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    
    # create the db and insert the data (using data.sql) in the temp db file
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
        
    yield app
    
    # after the test is complete, close and remove the temp file
    os.close(db_fd)
    os.unlink(db_path)
    

# tests can be run on the app created by the app fixture without running the server
@pytest.fixture
def client(app):
    return app.test_client()


# this creates a runner that can call click commands registered with the app
@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# test authentication class
class AuthActions(object):
    def __init__(self, client):
        self._client = client
        
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')
    

# allows repeated use of AuthActions class in testing
@pytest.fixture
def auth(client):
    return AuthActions(client)
