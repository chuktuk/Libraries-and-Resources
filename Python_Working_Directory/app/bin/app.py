#!/usr/bin/env python3
'''Proof of concept for getting the app working directory regardless of where the command is executed.

Only works in python 3 or higher. Does not work with python 2.7 for virtual environments.'''

import os
import pyglet

# this command gets the location of app.py, and sets a variable to the app folder
app_dir = os.path.dirname(__file__).replace('\\', '/').replace('/bin', '')

print('App Location: ', app_dir)
print('Virtual Environment setup. Pyglet imported successfully.')
