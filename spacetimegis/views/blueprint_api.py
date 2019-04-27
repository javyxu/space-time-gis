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

from .utils import json_result

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def index():
    return json_result(200, msg='Hello Blueprint!')