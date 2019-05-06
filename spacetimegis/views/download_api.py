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

from flask import request, Blueprint, jsonify

from spacetimegis.utils.logging_mixin import logger

from spacetimegis.data.download.download_agora import * 
from .utils import json_result

download_bp = Blueprint('download', __name__)

@download_bp.route('/download_agora', methods=['GET', 'POST'])
def download_agora():
    try:
        if request.method == 'POST':
            path = request.args.get('savepath')
            task_id = download.delay(path)
            return json_result(200, msg='task id is : {0}'.format(str(task_id)))
        else:
            task_id = request.args.get('task_id')
            task = download.AsyncResult(task_id)
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
    except Exception as e:
        logger.writeerrorlog(e)
        return json_result(500, msg='download failure!')