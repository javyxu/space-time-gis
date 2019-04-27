# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-03 13:53:12
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: log_utils.py
'''

import logging
import logging.config
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import os

from spacetimegis.constants import LogLevel

from spacetimegis.config import cfg

path = os.path.dirname(os.path.realpath(__file__))
logconfig = os.path.join(path, "../../logconfig.yml")

logdir = cfg.get('core')['BASE_LOG_FOLDER']
if not os.path.exists(logdir):
    os.mkdir(logdir)

class LoggingMixin(object):
    def __init__(self):
        with open(logconfig, 'r', encoding='utf-8') as f:
            config = load(f, Loader=Loader)
            config['handlers']['file']['filename'] = os.path.join(logdir, config['handlers']['file']['filename'])
            config['handlers']['error']['filename'] = os.path.join(logdir, config['handlers']['error']['filename'])
            logging.config.dictConfig(config)
        self.logger = logging.getLogger(name='main')

    def writelog(self, logLevel, msg):
        if logLevel is LogLevel.debug:
            self.logger.debug(msg)
        elif logLevel is LogLevel.info:
            self.logger.info(msg)
        elif logLevel is LogLevel.warning:
            self.logger.warning(msg)
        elif logLevel is LogLevel.error:
            self.logger.error(msg)
        elif logLevel is LogLevel.crit:
            self.logger.critical(msg)
    
    def writedebuglog(self, msg):
        self.writelog(LogLevel.debug, msg)
    
    def writeinfolog(self, msg):
        self.writelog(LogLevel.info, msg)

    def writewarninglog(self, msg):
        self.writelog(LogLevel.warning, msg)

    def writeerrorlog(self, msg):
        self.writelog(LogLevel.error, msg)
    
    def writecritlog(self, msg):
        self.writelog(LogLevel.crit, msg)

logger = LoggingMixin()