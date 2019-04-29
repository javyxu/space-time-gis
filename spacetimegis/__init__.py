# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-22 15:06:18
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: __init__.py
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from spacetimegis.config import cfg

APP_DIR = os.path.dirname(__file__)

app = Flask(__name__)
app.config.update(cfg)

db = SQLAlchemy(app)

migrate = Migrate(app, db, directory=APP_DIR + '/migrations')

# Flask-Cors
if app.config.get('ENABLE_CORS') is True:
    from flask_cors import CORS
    CORS(app, supports_credentials=True)

# Flask-Compress
if app.config.get('ENABLE_FLASK_COMPRESS') is True:
    from flask_compress import Compress
    Compress(app)

# Flask-Blueprint
from spacetimegis.views import blueprint_api, core_api, download_api, ml_api
app.register_blueprint(blueprint_api.index_bp, url_prefix='/api/v1')
app.register_blueprint(core_api.core_bp, url_prefix='/api/v1/core')
app.register_blueprint(download_api.download_bp, url_prefix='/api/v1/download')
app.register_blueprint(ml_api.ml_bp, url_prefix='/api/v1/machinelearning')