#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main package forms."""

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Email
from flask_babel import _, lazy_gettext as _l
from app.models import User


# edit profile form
class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[InputRequired()])
    email = StringField(_l('Email'), validators=[InputRequired(), Email()])
    submit = SubmitField(_l('Submit Changes'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    # only validate that the username isn't in the db if it's different than the current username
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Username in use, please enter a different username.'))


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
