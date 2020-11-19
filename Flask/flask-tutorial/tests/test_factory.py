#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This is the factory function testing file for unit testing."""


from flaskr import create_app


# test creating an app with an without testing
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
    

# tests the app.route('/hello') created in the app factory function
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
