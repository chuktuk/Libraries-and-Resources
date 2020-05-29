#!/usr/bin/env python3
'''This is a proof of concept my_logger.py file to test logging procedures.

This is a sample module that sets up a primary logger and a module level logger.
This proof of concept works. It is important to pass the module name when creating
a logger within a module. Standard format is below

`logger = my_logger.create_module_logger(log_file, __name__)`

Could modify this module to accept different args to produce different loggers.
e.g. could to file vs console logger and set different levels. Can use if/switch
statements or just create different functions for each type.
'''

# import standard packages
import logging
# from datetime import datetime as dt
    

# create a module level file logger
# this works in the app.py file or any associated custom modules
# create the logger in each module using the standard format
# nest logging statements within functions of modules
# see app.py, module_1.py, and module_2.py for examples
def create_file_logger(log_file, module_name, level='DEGUB'):
    '''This function creates a file logger to use for an app. 
    
    Dependencies:
    import logger
    
    This function should be called in every module within an app that logs events. 
    This function will create a file in the location specified by log_file. 
    Always supply __name__ for the module_name.
    
    Standard format for calling this function:
    logger = us.create_file_logger(log_file, __name__, level)
    
    Accepted values for level:
    'CRITICAL'
    'ERROR'
    'WARNING'
    'INFO'
    'DEBUG'
    
    Whichever level is supplied, every level above selection will also be logged.
    e.g. if level == 'WARNING' then 'WARNING', 'ERROR', and 'CRITICAL' are logged.
    
    
    Using the logger to log information about events with a custom message:
    logger.info('Message to log.')
    logger.info('%s a log message using %s', 'Writing', 'variables')
    
    Using the logger to report exceptions:
    try:
        statements that might fail
        logger.info('Success message.')
    except Exception as e:
        logger.exception(e)
        exception statements
    '''
    
    # create a logger
    logger = logging.getLogger(module_name)
    
    # create a filehandler
    fh = logging.FileHandler(log_file)
    
    # set the logger level and handler level
    if level == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)
        fh.setLevel(logging.CRITICAL)
    elif level == 'ERROR':
        logger.setLevel(logging.ERROR)
        fh.setLevel(logging.ERROR)
    elif level == 'WARNING':
        logger.setLevel(logging.WARNING)
        fh.setLevel(logging.WARNING)
    elif level == 'INFO':
        logger.setLevel(logging.INFO)
        fh.setLevel(logging.INFO)
    elif level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
    else:
        raise ValueError(''.join(['level must be one of the following: \'CRITICAL\', \'ERROR\', ',
                                 '\'WARNING\', \'INFO\', or \'DEBUG\'. ',
                                 'You entered ', '\'', level, '\'.']))
            #'''level must be one of the following: \'CRITICAL\', \'ERROR\', \'WARNING\', \'INFO\', or \'DEBUG\'. You entered '''level)
    
    # create a formatter and add to the file handler
    # this can be modified to produce different log entry formats
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    # add handler to the logger
    logger.addHandler(fh)
    
    # return the logger
    return logger

def shutdown_logging():
    '''This function closes the logger and ends logging.'''
    
    logger = logging.getLogger()
    
    # shut it down
    logger.removeHandler('fh')
    logging.shutdown()