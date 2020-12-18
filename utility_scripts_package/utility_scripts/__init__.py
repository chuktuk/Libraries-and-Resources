#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""Utility scripts package. This package contains useful utility scripts separated into modules by functionality.

Modules:

    dbase.py
        - Objects associated with database connections.

    email.py
        - Objects associated with email functionality.

    fsconn.py
        - Objects associated with fileserver connections.

    log.py
        - Objects associated with application logging.
"""

# import all needed objects
# usage: import utility_scripts as us
# then call objects as us.Mail() etc.

# import all dbase, fsconn, and log
from .dbase import *
from .fsconn import *
from .log import *

# only import the Mail class from email
from .email import Mail


# also allow each module to be import explicitly
# usage: from utility_scripts import email
import utility_scripts.dbase
import utility_scripts.email
import utility_scripts.fsconn
import utility_scripts.log
