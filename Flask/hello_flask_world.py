#!/usr/bin/env python

# import the Flask class
from flask import Flask

# create an instance of this class
# use __name__ if using a single module for the app
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'