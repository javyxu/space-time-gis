# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-19 11:04:03
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: pg_utils.py
'''

from spacetimegis.db_engines.constants import DatabaseType

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from geoalchemy2 import Geometry

class SQLAlchemyUtils(object):
    """
    """
    def __init__(self, host, port, username, passwd, initdb, dbtype=DatabaseType.Postgres):
        self.host = host
        self.port = port
        self.username = username
        self.passwd = passwd
        self.initdb = initdb
        self.dbtype = dbtype
        self._conn = None
        self._connect()
        # self._cursor = self._conn.cursor()

    def _connect(self):
        '''
        '''
        try:
            if self.dbtype is DatabaseType.Postgres:
                engine = create_engine( \
                    '{0}://{1}:{2}@{3}:{4}/{5}'.format(self.dbtype.description(), \
                        self.username, self.passwd, self.host, \
                        self.port, self.initdb))
            elif self.dbtype is DatabaseType.Sqlite:
                create_engine('{0}://{1}'.format(self.dbtype.description(), self.initdb))
            elif self.dbtype is DatabaseType.MySQL:
                engine = create_engine('\
                    {0}://{1}:{2}@{3}/{4}'.format(self.dbtype.description(), \
                        self.username, self.passwd, self.host, \
                        self.port, self.initdb))

            self._conn = engine.connect()
        except EOFError as e:
            pass

    def executesql(self, sql):
        '''
        Args:
        Returns:
        Raises:
        '''
        self._conn.execute(sql)
    
    def select(self, sql):
        '''
        Args:
        Returns:
        Raises:
        '''
        result = self._conn.execute(sql)
        return result.fetchall()

    def rollback(self):
        '''
        Args:
        Returns:
        Raises:
        '''
        pass

    def __del__(self):
        '''
        Args:
        Returns:
        Raises:
        '''
        try:
            # self._cursor.close()
            self._conn.close()
        except:
            pass

    def close(self):
        '''
        Args:
        Returns:
        Raises:
        '''
        self.__del__()

