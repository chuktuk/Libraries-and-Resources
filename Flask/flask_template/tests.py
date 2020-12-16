#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Unit testing for the app."""

from datetime import datetime as dt
from datetime import timedelta as td
import unittest
from config import TestConfig
from app import init_app, db
from app.models import User


class UserModelCase(unittest.TestCase):
    def setUp(self):
        # use an in memory db for the unit test
        self.app = init_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='test')
        u.set_password('test')
        self.assertFalse(u.check_password('nope'))
        self.assertTrue(u.check_password('testing1!'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
