#!/usr/bin/env python3
'''This is a proof of concept module_2.py file to test logging procedures.

This is a sample module that will include logging to test outputs.
'''

# import logging
import logging
from datetime import datetime as dt

# import logging module
import my_logger





# set the working directory
# working_directory = 'C:/Users/CRTUCKER/Documents/Libraries-and-Resources/logging_app'
working_directory = '/home/chucktucker/Documents/Libraries-and-Resources/env_logging_app'

    
    
    
    
# set file_name and path for log file
log_file = ''.join([working_directory, '/log/', dt.now().strftime('%m%d%Y'), '_app_practice_log.log'])

# create your logger to use with this module
logger = my_logger.create_file_logger(log_file, __name__, 'DEBUG')

# define any module functions that use the logger
def log_succes_message_four():
    '''All this function does is log a successful message.'''
    
    try:
        logger.info('Message four logged successfully.')
    except Exception as e:
        logger.exception(e)
        pass
    
def log_success_message_five():
    '''All this function does is log a successful message.'''
    
    try:
        logger.info('Message five logged successfully.')
    except Exception as e:
        logger.exception(e)
        pass
    
def log_error_message_two():
    '''All this function does is log an error message.'''
    
    try:
        r = c
        logger.info('This message won\'t print.')
    except Exception as e:
        logger.exception(e)
        pass

def log_success_message_six():
    '''All this function does is log a successful message.'''
    
    try:
        logger.info('Message six logged successfully.')
    except Exception as e:
        logger.exception(e)
        pass

def main():
    '''Main function that lists the module's name.'''
    
    print(__name__)
    
if __name__ == '__main__':
    main()