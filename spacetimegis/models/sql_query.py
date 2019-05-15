# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-28 17:44:47
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: sql_query.py
'''
from datetime import datetime
from spacetimegis.utils.logging_mixin import logger

from sqlalchemy import create_engine


class SQLQuery(object):
    def __init__(self, uri):
        self.uri = uri
        engine = create_engine(uri)
        try:
            self.conn = engine.connect()
        except Exception as e:
            self.conn = None
            logger.writeerrorlog(e)

    def executesql(self, sql):
        try:
            starttime = datetime.now()
            res = self.conn.execute(sql)
            endtime = datetime.now()
            tmp = {'execute_time': (endtime - starttime).total_seconds(),
                   'query_result': [dict(r) for r in res.fetchall()]}
                #    'query_result': [list(resdata) for resdata in res.fetchall()]}
            return tmp
        except Exception as e:
            logger.writeerrorlog(e)
            return None

    def insert(self, sql):
        from sqlalchemy_clickhouse import connector
        conn1 = connector.connect(db_name='test', db_url='http://10.0.3.218:8123/', username='default', password=123)
        cursor = conn1.cursor()
        cursor.execute(sql, is_response=False)
    