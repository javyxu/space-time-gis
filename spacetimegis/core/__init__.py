# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-25 20:51:04
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: __init__.py
'''
import os

from pyspark.sql import *
from pkg_resources import resource_filename
from geopyspark.geopyspark_constants import JAR

from spacetimegis.config import cfg
from spacetimegis.utils.logging_mixin import logger

module_jars = [
        os.path.abspath(resource_filename('geopyspark.jars', JAR))
    ]
jar_dirs = [(jar, os.path.dirname(jar)) for jar in module_jars]
jars = [jar_dirs[0][0]]
jar_string= ",".join(set(jars))

spark_home = cfg.get('spark')['SPARK_HOME')
if not spark_home:
    logger.writedebuglog('please set SPARK_HOME in spacetimegis.cfg')
    logger.writeinfolog('please set SPARK_HOME in spacetimegis.cfg')
    
if not os.environ.get('SPARK_HOME'):
    os.environ["SPARK_HOME"] = spark_home

pysc = SparkSession.builder
        .master(cfg.get('spark')['master'))
        .appName(cfg.get('spark')['APPNAME'))
        .config("spark.ui.enabled", cfg.get('spark')['UI_ENABLED'))
        .config("spark.serializer","org.apache.spark.serializer.KryoSerializer")
        .config("spark.kryo.registrator","geopyspark.geotools.kryo.ExpandedKryoRegistrator")
        .config('spark.driver.memory','8G')
        .config('spark.executor.memory','8G')
        .config('spark.jars',  jar_string)
        .getOrCreate()

uri_address = cfg.get('spark')['URI_ADDRESS')