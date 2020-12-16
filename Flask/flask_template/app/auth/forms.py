#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A module to store classes for forms needed for the app.
This template includes a simple login form."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, ValidationError, Email, EqualTo, Length, Regexp
from app.models import User
from flask_babel import _, lazy_gettext as _l
import re


# registration form
class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[InputRequired()])
    email = StringField(_l('Email'), validators=[InputRequired(), Email()])
    password = PasswordField(_l('Password'),
                             validators=[
                                 InputRequired(),
                                 Length(min=8),
                                 Regexp('[0-9]', message=_l('Password must contain at least one number.')),
                                 Regexp('[a-zA-Z]', message=_l('Password must contain at least one letter.')),
                                 Regexp('[!@#$&?]', message=_l('Password must contain at least one of !@#$&?'))
                             ])
    password2 = PasswordField(_l('Confirm Password'), validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    # any validate_<fieldname> methods are taken by wtforms as custom and they are invoked automatically
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Username in use, please enter a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Email address in use, please enter a different email.'))


# login form
class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[InputRequired()])
    password = PasswordField(_l('Password'), validators=[InputRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


# reset password request form
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[InputRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


# reset password form
class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'),
                             validators=[
                                 InputRequired(),
                                 Length(min=8)])

    def validate_password(self, password):
        numbers = re.compile('\d')
        letters = re.compile('[a-zA-Z]')
        spec_chars = re.compile('[!@#$%&?]')
        if not numbers.search(password.data):
            raise ValidationError(_('Password must contain at least one number.'))
        if not letters.search(password.data):
            raise ValidationError(_('Password must contain at least one letter.'))
        if not spec_chars.search(password.data):
            raise ValidationError(_('Password must contain at least one of !@#$%&?'))

    password2 = PasswordField(_l('Confirm Password'), validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField(_l('Submit Changes'))
