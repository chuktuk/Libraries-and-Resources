#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This is the test authorization file."""


import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    # client.get makes a get request
    assert client.get('/auth/register').status_code == 200
    # client.post makes a post request, sending the data
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']
    
    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None
        

# mark.parameterize runs the same func multiple times with diff args
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
    
    
# test session info for tracking logins
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'
    
    # allows you to get session variables after the response is returned
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'
        
        
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
    
    
# test logout
def test_logout(client, auth):
    auth.login()
    
    with client:
        auth.logout()
        # custom user_id session variable should be cleared upon logout
        assert 'user_id' not in session
