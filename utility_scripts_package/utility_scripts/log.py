#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""Log module.

Functions:

    create_file_logger(log_file, module_name, level='DEBUG')

    process_log_for_errors(log_file, level='CRITICAL')

    shutdown_logging()

Uses:
    For each module of an application:

    create the logger with specifications:

        import os
        from datetime import datetime as dt

        log_name = ''.join([dt.now().strftime('%Y%d%m'), '_log.log'])

        # assuming a current module is in the 'bin' directory and the 'log' directory is beside it
        # also assuming you want the data prepended to the log

        app_dir = os.path.dirname(__file__).replace('\\', '/').replace('/bin', '')
        log_path = ''.join([app_dir, '/log/', log_name])
        logger = create_file_logger(log_path, __name__, level='INFO')

    log events:
        logger.info('Information to log.')

        try:
            statements
        except Exception as e:
            logger.exception('{type(e): e} and any additional info.')
            logger.critical('For major errors.')

    end logging:
        shutdown_logging()

"""


import logging
import re


# create file logger
def create_file_logger(log_file, module_name, level='DEBUG'):
    """This function creates a file logger to use for an app.

    Dependencies:
    import logging

    This function should be called in every module within an app that logs events.
    This function will create a file in the location specified by log_file.
    Always supply __name__ for the module_name.

    Standard format for calling this function:
    logger = create_file_logger(log_file, __name__, level)

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

    Using the logger to report exceptions:
    try:
        statements that might fail
        logger.info('Success message.')
    except Exception as e:
        logger.exception(e)
        exception statements
    """

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

    # create a formatter and add to the file handler
    # this can be modified to produce different log entry formats
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # add handler to the logger
    logger.addHandler(fh)

    # return the logger
    return logger


# process log for errors
def process_log_for_errors(log_file, level='CRITICAL'):
    """This function will process log files for errors. This function returns an email_log (boolean)
    based on whether 'level' or higher log entries are found, in addition to the highest level.

    Error hierarchy:
    CRITICAL > ERROR > WARNING > INFO > DEBUG

    :param log_file: the path and filename of the log file to check for errors.

    :param level: default='CRITICAL': the level of error to check for. The error hierarchy is specified above.
                  Supply this argument as a string

    :return: Returns True or False depending on the specified level to check and the highest level found.

    """

    # read in the contents of the file
    with open(log_file, 'r') as file:
        contents = file.read()

    # ensure file is closed
    if not file.closed:
        file.close()

    # check for the set level
    error_list = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    # check contents for any of the errors in error list, return True if any are found
    highest_level = None
    for error in error_list:
        if bool(re.search(error, contents)):
            highest_level = error

    found_idx = error_list.index(highest_level)
    check_idx = error_list.index(level)

    # compare highest index found to index of level to check and return results
    if found_idx >= check_idx:
        return True, highest_level
    else:
        return False, highest_level


# shutdown logging
def shutdown_logging():
    """Call this function to end logging once the app is complete."""

    # get the root file logger
    logger = logging.getLogger()

    fh = logger.handlers[0]

    # remove the file handler
    logger.removeHandler(fh)

    # shutdown logging
    logging.shutdown()
