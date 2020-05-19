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
def create_module_logger(log_file, module_name):
    '''Maybe should do as a class rather than function?'''

    # set a module level logger
    # use this object for logging calls
    # logger = logging.getLogger(__name__)
    logger = logging.getLogger(module_name)

    # set the logger level
    # could alter this function to accept different levels as an arg
    # could use a switch statement to set the different levels
    logger.setLevel(logging.DEBUG)

    # create a file handler and set level
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # create a formatter and add to filehandler
    # includes the datetime, name, level name, and the message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # add handler to the logger
    logger.addHandler(fh)
    
    # return the logger
    return logger