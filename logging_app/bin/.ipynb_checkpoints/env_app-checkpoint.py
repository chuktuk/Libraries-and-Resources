#!/usr/bin/env python3
'''This is a proof of concept to run app.py file using a virtual environment.

Running this script should product the same results as running app.py with two
additional log entries.
'''

import os
import logging
from datetime import datetime as dt

import my_logger



def main():
    '''Main function that creates and executes app.py in a virtual environment.'''
    
    
    
    
    # set the working directory
    # also set this in app.py, module_1.py, and module_2.py
    working_directory = 'C:/Users/CRTUCKER/Documents/Libraries-and-Resources/logging_app'
    
    
    
    
    
    log_file = ''.join([working_directory, '/log/', dt.now().strftime('%m%d%Y'), '_app_practice_log.log'])
    
    # intiate logging
    level = 'DEBUG'
    logger = my_logger.create_file_logger(log_file, __name__, level)
    logger.info('---------------------------BEGIN---------------------------')
    logger.info('Initiated env_app.py')
    
    # environment setup and script execution
    try:
        os.chdir(working_directory)
    except Exception as e:
        message = ' '.join(['FATAL ERROR:', e])
        logger.exception(message)
        
    # set commands
    venv = ''.join(['py -m venv ', working_directory, '/env'])
    activ = ''.join([working_directory, '/env/Scripts/activate'])
    pip_install = 'py -m pip install --upgrade pip'
    req = 'pip install -r env/requirements.txt'
    script = ''.join(['python ', working_directory, '/bin/app.py'])
    
    commands = ' & '.join([venv, activ, pip_install, req, script])
    
    # run the commands
    try:
        os.system(commands)
    except Exception as e:
        message = ' '.join(['FATAL ERROR:', e])
        logger.exception(message)
    
    # log completion
    logger.info('env_app.py script complete.')
    logger.info('----------------------------END----------------------------')
    
if __name__ == '__main__':
    main()