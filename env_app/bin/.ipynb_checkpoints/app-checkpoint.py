#!/usr/bin/env python3
'''This is a proof of concept to setup an environment for an app.

prior to the first execution of this app, pyglet was not installed.'''

import os


def main():
    '''This is the main function that will execute the code for this
    proof of concept.'''
    
    # linux env
    pip_install = 'python3 -m pip install --upgrade pip'
    
    # windows env
    # pip_install = 'py -m pip install --upgrade pip'
    
    # all envs
    req = 'pip install -r ../env/requirements.txt'
    
    # execute commands
    os.system(pip_install)
    os.system(req)
    
    import pyglet
    
    return

if __name__ == '__main__':
    main()