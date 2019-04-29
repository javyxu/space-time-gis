# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-27 10:49:42
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: core.py
'''

from spacetimegis import db
from sqlalchemy import (
    Boolean, Column, create_engine, DateTime, ForeignKey, Integer,
    MetaData, String, Table, Text,
)
from sqlalchemy.schema import UniqueConstraint

from .helpers import ImportMixin


class Database(db.Model, ImportMixin):

    """An ORM object that stores Database related information"""

    __tablename__ = 'dbs'
    type = 'table'
    __table_args__ = (UniqueConstraint('database_name'),)

    id = Column(Integer, primary_key=True)
    database_name = Column(String(250), unique=True)
    sqlalchemy_uri = Column(String(1024))