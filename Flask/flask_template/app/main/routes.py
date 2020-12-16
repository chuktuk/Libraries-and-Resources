#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main package routes."""

from flask import (
    render_template, flash, redirect, url_for, request, g, current_app as app
)
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm, SearchForm
from app.models import User
from app.main import bp

from datetime import datetime as dt


# execute commands before view functions
@bp.before_app_request
def before_request():
    # add last login info to the database
    if current_user.is_authenticated:
        current_user.last_login = dt.utcnow()
        db.session.commit()
        g.search_form = SearchForm()

    # get the users locale for pybabel datetime translations
    g.locale = str(get_locale())


# index (home) landing page
@bp.route('/')
@bp.route('/index')
def index():
    """Landing Page."""
    return render_template('index.html', title=' '.join([app.config['APPLICATION_NAME'], _('Home')]))


@bp.route('/dashboards')
def dashboards():
    return render_template('dashboards.html', title='Dashboards')


# about page
@bp.route('/about')
def about():
    return render_template('about.html', title=' '.join([app.config['APPLICATION_NAME'], _('About Page')]))


# any login required pages
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title='Profile Page', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/privileged')
@login_required
def privileged():
    return render_template('login_required/privileged.html', title='Privileged: Login Required')
