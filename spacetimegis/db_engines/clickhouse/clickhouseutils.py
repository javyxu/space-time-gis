# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-26 08:39:01
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: clickhouseutils.py
'''

import sqlalchemy as sa
sa.create_engine('clickhouse://default:password@hostname:port/database')