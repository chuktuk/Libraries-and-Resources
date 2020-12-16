#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Enhanced cli commands for the app."""

import os
import click


# create the register function
def register(app):
    """Provides cli commands to register new languages, updates translations when _() and _l() are used,
    and to compile .mo files. You still need to add translations to the .po file prior to compiling the .mo file.

    Commands:

    Register a new language:
    flask translate init <language-code>

    Update all languages after editing _() and _l() in the app:
    flask translate update

    Compile all languages after running update:
    flask translate compile
    """
    # create cli commands
    # this defines the group 'translate'
    # all this does is define the group, so this doesn't do anything
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    # define the update command
    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(f'pybabel update -i messages.pot -d {app.config.get("APP_PACKAGE_HOME", "app")}/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    # define the compile command
    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system(f'pybabel compile -d {app.config.get("APP_PACKAGE_HOME", "app")}/translations'):
            raise RuntimeError('compile command failed')

    # the init LANG command
    # this functions needs an argument, so using click
    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                f'pybabel init -i messages.pot -d {app.config.get("APP_PACKAGE_HOME", "app")}/translations -l {lang}'
        ):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')
