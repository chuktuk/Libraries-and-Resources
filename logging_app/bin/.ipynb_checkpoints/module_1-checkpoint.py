#!/usr/bin/env python3
'''This is a proof of concept module_1.py file to test logging procedures.

This is a sample module that will include logging to test outputs.
'''

# import logging
import logging
from datetime import datetime as dt

# import logging module
import my_logger





# set the working directory
working_directory = 'C:/Users/CRTUCKER/Documents/Libraries-and-Resources/logging_app'

    
    
    
    
# set file_name and path for log file
log_file = ''.join([working_directory, '/log/', dt.now().strftime('%m%d%Y'), '_app_practice_log.log'])

# create your logger to use with this module
logger = my_logger.create_file_logger(log_file, __name__, 'DEBUG')

# define any module functions that use the logger
def log_succes_message_one():
    '''All this function does is log a successful message.'''
    
    try:
        logger.info('Message one logged successfully.')
    except Exception as e:
        logger.exception(e)
        pass
    
def log_success_message_two():
    '''All this function does is log a successful message.'''
    
    try:
        logger.info('Message two logged successfully.')
    except Exception as e:
        logger.exception(e)
        pass
    
def log_error_message_one():
    '''All this function does is log an error message.'''
    
    try:
        pd.read_csv('no_module_named_pd.csv')
    except Exception as e:
        logger.exception(e)
        pass

def log_success_message_three():
    '''All this function does is log a successful message.'''
    
    try:
        logger.info('Message three logged successfully.')
    except Exception as e:
        logger.exception(e)
        pass

def main():
    '''Main function that lists the module's name.'''
    
    print(__name__)
    
if __name__ == '__main__':
    main()