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

from spacetimegis.data.download.download_agora import * 
from .utils import json_result, task_progress

download_bp = Blueprint('download', __name__)

@download_bp.route('/download_agora', methods=['GET', 'POST'])
def download_agora():
    try:
        if request.method == 'POST':
            path = request.args.get('savepath')
            task_id = download.delay(path)
            return json_result(200, msg={'task_id': str(task_id)})
        else:
            task_id = request.args.get('task_id')
            task = download.AsyncResult(task_id)
            return task_progress(task)
    except Exception as e:
        logger.writeerrorlog(e)
        return json_result(500, msg='download failure!')