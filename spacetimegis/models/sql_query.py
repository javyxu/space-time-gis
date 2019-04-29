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
                   'query_result': [resdata[0] for resdata in res.fetchall()]}
            return tmp
        except Exception as e:
            logger.writeerrorlog(e)
            return None

    