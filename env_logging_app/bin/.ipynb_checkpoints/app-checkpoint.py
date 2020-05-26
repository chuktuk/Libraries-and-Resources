#!/usr/bin/env python3
'''This is a proof of concept app.py file to test logging procedures.

This app makes use of other modules to test importing and logging using functions
from multiple places.
'''

# import standard modules
import logging
from datetime import datetime as dt

# import custom modules
import module_1 as m1
import module_2 as m2
import my_logger

def main():
    '''Main function.'''
    
    
    
    # set the working directory
    # working_directory = 'C:/Users/CRTUCKER/Documents/Libraries-and-Resources/env_logging_app'
    working_directory = '/home/chucktucker/Documents/Libraries-and-Resources/env_logging_app'
    
    
    
    
    # set file_name and path for log file
    log_file = ''.join([working_directory, '/log/', dt.now().strftime('%m%d%Y'), '_app_practice_log.log'])
    
    # create a logger object
    logger = my_logger.create_file_logger(log_file, __name__, 'DEBUG')
    
    # log the start of the app
    logger.info('App initiated.')
    
    # other function calls
    m1.log_succes_message_one()
    m1.log_success_message_two()
    m1.log_error_message_one()
    m1.log_success_message_three()
    m2.log_succes_message_four()
    m2.log_success_message_five()
    m2.log_error_message_two()
    m2.log_success_message_six()
    
    # log the end of the app
    logger.info('App completed.')
    
    return
    
# call the main function if this is the primary app
if __name__ == '__main__':
    main()