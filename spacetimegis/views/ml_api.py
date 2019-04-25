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

from flask import Flask, jsonify, Response, request

from spacetimegis import app
from spacetimegis.constants import LogLevel
from spacetimegis.utils.logging_mixin import logger

from spacetimegis.ml.typhoon import train_net, prediction_net


def json_result(code=0, result=None, msg='success'):
    return jsonify({"code":code, "result": result, "msg":msg})

@app.route('/tarin_net', methods=['GET'])
def train():
    try:
        path = request.args.get('savepath')
        train_net.execute(path)
    except Exception as e:
        logger.writelog(LogLevel.error, e)
        return json_result(500, msg='train failure!')
    return json_result(200, msg='train sucess!')


@app.route('/prediction_net', methods=['GET'])
def prediction():
    try:
        path = request.args.get('savepath')
        prediction_net.execute(path)
    except Exception as e:
        logger.writelog(LogLevel.error, e)
        return json_result(500, msg='prediction failure!')
    return json_result(200, msg='prediction sucess!')