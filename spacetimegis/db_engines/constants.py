# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-22 10:32:23
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: constants.py
'''

from enum import Enum

class DatabaseType(Enum):
    """
    """
    Sqlite = (0,'sqlite')
    MySQL = (1, 'mysql')
    Postgres = (2, 'postgresql')

    def __init__(self, dbtypeindex, dbtypedes):
        self.dbtypeindex = dbtypeindex
        self.dbtypedes = dbtypedes
        
    def description(self):
        return(self.value[1])
