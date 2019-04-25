# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import Flask, jsonify, Response, request
from flask_cors import CORS

from spacetimegis import app
from spacetimegis.constants import LogLevel
from spacetimegis.utils.logging_mixin import logger

import simplejson as json

CORS(app, supports_credentials=True)
CORS(app, resources=r'/api')

def json_result(code=0, result=None, msg='success'):
    return jsonify({"code":code, "result": result, "msg":msg})

@app.route('/', methods=['GET'])
def index():
    return json_result(200, 'Hello Space Time GIS!')

@app.route('/helloworld')
def helloworld():
    return json_result(200, 'Hello World!')

@app.route('/testlog', methods=['GET'])
def testlog():
    logger.writelog(LogLevel.info, 'This is info log!')
    logger.writelog(LogLevel.debug, 'This is debug log!')
    logger.writelog(LogLevel.warning, 'This is warning log!')
    logger.writelog(LogLevel.crit, 'This is crit log!')
    return json_result(200, 'Log is Success!')
# @app.route("/getimage")
# def getimage():
#     img =     
#     resp = Response(res, mimetype="image/tiff")
#     return resp