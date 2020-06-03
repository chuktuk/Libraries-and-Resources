#!/usr/bin/env python3

'''Docstrings. Update working_directory.

This file has now become redundant.

'''

import os

   
def main():

    working_directory = '/home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app'
    
    
    venv_path = ''.join([working_directory, '/env'])
    req_path = ''.join([working_directory, '/env/requirements.txt'])
   
    # set windows commands
    venv = ' '.join(['py -m venv', venv_path])
    activ = ''.join([working_directory, '/env/Scripts/activate'])
    pip_install = 'py -m pip install --upgrade pip'
    req = ' '.join(['pip install -r', req_path])
    
    # set linux commands
    lvenv = ' '.join(['python3 -m venv', venv_path])
    lactiv = ' '.join(['.', working_directory, '/env/bin/activate'])
    lpip_install = 'python3 -m pip install --upgrade pip'
   
    # run windows commands
    # commands = ' & '.join([venv, activ, pip_install, req])
    
    # run linux commands
    commands = ' && '.join([lvenv, lactiv, lpip_install, req])
    
    os.system(commands)

if __name__ == '__main__':
    main()