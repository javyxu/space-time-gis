# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-25 16:24:51
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: download_api.py
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import Blueprint

from spacetimegis.utils.logging_mixin import logger
from spacetimegis.settings import get_celery_app
from spacetimegis import app

config = app.config
celery_app = get_celery_app(config)

from .utils import json_result, image_success

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def index():
    return json_result(200, msg='Hello Blueprint!')

@index_bp.route('/getimage', methods=['GET'])
def getimg():
    with open('/Users/xujavy/Documents/Work/srccode/space-time-gis/examples_data/test_00.tif','rb') as f:
        resdata = bytearray(f.read())
    return image_success(resdata)

import random
import time
@celery_app.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    print(total)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        # self.update_state(state='PROGRESS',
        #                   meta={'current': i, 'total': total,
        #                         'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}

@index_bp.route('/testcelery_tt', methods=['POST'])
def testcelery_tt():
    task_id = long_task.apply_async()
    return json_result(200, msg=str(task_id))

from flask import jsonify
@index_bp.route('/testcelery/<task_id>', methods=['GET', 'POST'])
def testcelery(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
    