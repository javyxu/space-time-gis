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

import os
import imp
from .config import conf

import pendulum
import celery


version = imp.load_source(
    'spacetimegis.version', os.path.join(os.path.dirname(__file__), 'version.py')).version

cfg = conf.as_all_dict()

cfg['VERSION_STRING'] = version


TIMEZONE = pendulum.timezone('UTC')
try:
    tz = cfg.get("CELERY_TIMEZONE")
    if tz == "system":
        TIMEZONE = pendulum.local_timezone()
    else:
        TIMEZONE = pendulum.timezone(tz)
    # print(TIMEZONE)
    cfg['timezone'] = TIMEZONE
except Exception:
    pass


HEADER = '\n'.join([
    r'  ----   ------       -          --------     -------  ',
    r' \      |      |     /  \       |            |',
    r'  \     |      |    /    \      |            |',
    r'   \    |------    /      \     |            |-------  ',
    r'    \   |         / -----  \    |            |',
    r'     \  |        /          \   |            |',
    r' ----   |       /            \   --------     -------  ',
])

_celery_app = None

def get_celery_app(config):
    global _celery_app
    if _celery_app:
        return _celery_app
    _celery_app = celery.Celery(config.get('CELERY_APP_NAME'), 
                                broker=config.get('BROKER_URL'),
                                backend=config.get('BROKER_BACKEND'))
    return _celery_app