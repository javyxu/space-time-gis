# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-27 11:07:14
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: helpers.py
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from sqlalchemy import and_, or_, UniqueConstraint
from sqlalchemy.orm.exc import MultipleResultsFound

from spacetimegis.utils.logging_mixin import logger


class ImportMixin(object):

    @classmethod
    def _unique_constrains(cls):
        """Get all (single column and multi column) unique constraints"""
        unique = [{c.name for c in u.columns} for u in cls.__table_args__
                  if isinstance(u, UniqueConstraint)]
        unique.extend({c.name} for c in cls.__table__.columns if c.unique)
        return unique
    
    @classmethod
    def import_from_dict(cls, session, dict_rep):
        """Import obj from a dictionary"""
        unique_constrains = cls._unique_constrains()

        filters = []  # Using these filters to check if obj already exists
        # Add filter for unique constraints
        ucs = [and_(*[getattr(cls, k) == dict_rep.get(k)
               for k in cs if dict_rep.get(k) is not None])
               for cs in unique_constrains]
        filters.append(or_(*ucs))

        # Check if object already exists in DB, break if more than one is found
        try:
            obj_query = session.query(cls).filter(and_(*filters))
            obj = obj_query.one_or_none()
        except MultipleResultsFound as e:
            logger.writeerrorlog(
                'Error importing {0} \n {1} \n {2}'.format(cls.__name__, str(obj_query), dict_rep))
            raise e

        if not obj:
            is_new_obj = True
            # Create new DB object
            obj = cls(**dict_rep)
            logger.writeinfolog('Importing new {0} {1}'.format(obj.__tablename__, str(obj)))
            session.add(obj)
        else:
            is_new_obj = False
            logger.writeinfolog('Updating {0} {1}'.format(obj.__tablename__, str(obj)))
            # Update columns
            for k, v in dict_rep.items():
                setattr(obj, k, v)