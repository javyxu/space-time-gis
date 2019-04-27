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

from flask import jsonify

from sqlalchemy import and_, or_, UniqueConstraint

from spacetimegis.utils.logging_mixin import logger


def json_result(code=0, result=None, msg='success'):
    # res = Response(json_msg, status=status, mimetype='application/json')
    return jsonify({"code":code, "result": result, "msg":msg})