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

from flask import request, Blueprint

from spacetimegis.utils.logging_mixin import logger

from spacetimegis.ml.typhoon import train_net, prediction_net, create_samples
from .utils import json_result, task_progress

ml_bp = Blueprint('ml', __name__)

@ml_bp.route('/create_samples', methods=['GET', 'POST'])
def create():
    try:
        if request.method == 'POST':
            path = request.args.get('savepath')
            task_id = create_samples.execute.delay(path)
            return json_result(200, msg={'task_id': str(task_id)})
        else:
            task_id = request.args.get('task_id')
            task = create_samples.execute.AsyncResult(task_id)
            return task_progress(task)
    except Exception as e:
        logger.writeerrorlog(e)
        return json_result(500, msg='create samples failure!')

@ml_bp.route('/tarin_net', methods=['GET', 'POST'])
def train():
    try:
        if request.method == 'POST':
            path = request.args.get('savepath')
            task_id = train_net.execute.delay(path)
            return json_result(200, msg={'task_id': str(task_id)})
        else:
            task_id = request.args.get('task_id')
            task = train_net.execute.AsyncResult(task_id)
            return task_progress(task)
    except Exception as e:
        logger.writeerrorlog(e)
        return json_result(500, msg='train failure!')


@ml_bp.route('/prediction_net', methods=['GET', 'POST'])
def prediction():
    try:
        if request.method == 'POST':
            path = request.args.get('savepath')
            task_id = prediction_net.execute.delay(path)
            return json_result(200, msg={'task_id': str(task_id)})
        else:
            task_id = request.args.get('task_id')
            task = prediction_net.execute.AsyncResult(task_id)
            return task_progress(task)
    except Exception as e:
        logger.writeerrorlog(e)
        return json_result(500, msg='prediction failure!')