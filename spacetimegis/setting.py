# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-29 14:53:54
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: utils.py
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import celery


_celery_app = None


def get_celery_app(config):
    global _celery_app
    if _celery_app:
        return _celery_app
    _celery_app = celery.Celery(config.get('CELERY_APP_NAME'), 
                                broker=config.get('BROKER_URL'),
                                backend=config.get('BROKER_BACKEND'))
    return _celery_app