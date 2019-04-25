# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-25 11:40:36
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: constants.py
'''

from enum import Enum

class LogLevel(Enum):
    """Log Level"""
    debug = 0
    info = 1
    warning = 2
    error = 3
    crit = 4