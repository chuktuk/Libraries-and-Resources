#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Testing functions for the database."""


import sqlite3

import pytest
from flaskr.db import get_db


# check the the db is closed after the context
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
        
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
        
    assert 'closed' in str(e.value)
    

# use pytest's monkeypatch to replace init_db func with one that records it's been called
# uses the runner fixture created in conftest.py
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False
        
    def fake_init_db():
        Recorder.called = True
        
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
