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

from spacetimegis import config

app = Flask(__name__)
# app.config.from_object(config)
app.config.update(dict(config.cfg.get('core')))
app.config.update(dict(config.cfg.get('webserver')))

db = SQLAlchemy(app)

APP_DIR = os.path.dirname(__file__)
migrate = Migrate(app, db, directory=APP_DIR + '/migrations')


from spacetimegis import views  # noqa