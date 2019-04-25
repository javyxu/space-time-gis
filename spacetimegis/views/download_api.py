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

from spacetimegis.data.download.download_agora import * 


def json_result(code=0, result=None, msg='success'):
    return jsonify({"code":code, "result": result, "msg":msg})

@app.route('/download_agora', methods=['GET'])
def download_agora():
    try:
        path = request.args.get('savepath')
        ts, links = get_ty_links()
        logger.writelog(LogLevel.info, (ts, links))
        download_imgs(path, ts, links)
    except Exception as e:
        logger.writelog(LogLevel.error, e)
        return json_result(500, msg='download failure!')
    return json_result(200, msg='download sucess!')