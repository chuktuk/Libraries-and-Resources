#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The views/routes for the app."""

# imports
from app import db
from app.auth import bp
from app.models import User
from app.mail import send_password_reset_email
from app.auth.forms import (
    LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
)

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


# login form view
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # send back to landing page if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # get the login form
    form = LoginForm()

    # returns true if POST request is received and all wtform validators are satisfied
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # probably want to add way to reset password
        # maybe add security question(s) and hash/store those to help with this
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('auth.login'))

        # only occurs if above evaluates False
        # login_user is a special function from flask-login
        login_user(user, remember=form.remember_me.data)

        # when @login_required intercepts a request, the url is modified to /login?next=url_clicked
        # where url_clicked is the protected view
        next_page = request.args.get('next')

        # the url_parse section below protects the app from redirecting to an absolute url
        # this could allow the app to redirect to an outside web page
        # this arg only allows relative redirects (within this app)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')

        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)


# logout view
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# register view
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


# request password reset view
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instructions to reset your password.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


# reset password form
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first_or_404()
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return render_template('user.html', user=user)
    return render_template('auth/reset_password.html', form=form)
