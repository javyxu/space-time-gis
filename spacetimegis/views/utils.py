# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-27 11:07:14
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: utils.py
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import jsonify, Response


def json_result(code=200, result=None, msg='success'):
    return jsonify({"code":code, "result": result, "msg":msg})

def json_success(json_msg, status=200):
    return Response(json_msg, status=status, mimetype='application/json')

def image_success(obj_msg, status=200):
    return Response(obj_msg, status=status, mimetype='application/tiff')

def task_progress(task):
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