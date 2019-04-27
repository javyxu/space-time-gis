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
# app.config.from_object(config)
app.config.update(cfg.get('core'))
app.config.update(cfg.get('webserver'))

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

from spacetimegis.views.blueprint_api import index_bp
app.register_blueprint(index_bp, url_prefix='/api/v1')

from spacetimegis import views  # noqa