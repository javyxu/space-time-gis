# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-25 20:51:04
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: __init__.py
'''
from spacetimegis.config import cfg

import os
if not os.environ.get('SPARK_HOME'):
    os.environ["SPARK_HOME"] = cfg.get('spark')['SPARK_HOME')

from pyspark.sql import *
from pkg_resources import resource_filename
from geopyspark.geopyspark_constants import JAR
module_jars = [
        os.path.abspath(resource_filename('geopyspark.jars', JAR))
    ]
jar_dirs = [(jar, os.path.dirname(jar)) for jar in module_jars]
jars = [jar_dirs[0][0]]
jar_string= ",".join(set(jars))

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