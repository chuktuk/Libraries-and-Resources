#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The test file for the blog."""


import pytest
from flaskr.db import get_db


# tests to opening blog.index both logged in and out
def test_index(client, auth):
    # when not logged in, the Log In and Register links should be available
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data
    
    # when logged in, the Log Out link and test blog data should appear
    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2020-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data
    
    
# tests for create, update, and delete views
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'
    
    
def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()
       
    # login as user 1
    # test for 403 forbidden error
    auth.login()
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # test current user doesn't see the link to update the post
    assert b'href="/1/update"' not in client.get('/').data
    

# test that url for a post id that doesn't exist returns 404 not found
@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404
    
    
# test create view
def test_create(client, auth, app):
    
    # when logged in, the create link should work
    auth.login()
    assert client.get('/create').status_code == 200
    # create a post and add it to the db
    client.post('/create', data={'title': 'created', 'body': ''})
    
    # there should now be 2 entries, the one added initially to the test_db and the one just added
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2
        

# test the update view
def test_update(client, auth, app):
    # when logged in, the user #1 should be able to update this blog
    auth.login()
    assert client.get('/1/update').status_code == 200
    # test updating the test post
    client.post('/1/update', data={'title': 'updated', 'body': ''})
    
    # test that the update worked
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'
        

# test that title is required during create and update views
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data
    
    
# test the delete view
def test_delete(client, auth, app):
    auth.login()
    # test that the delete is successful and redirets to 'index'
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'
    
    # after deletion, the post should not exist
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None
