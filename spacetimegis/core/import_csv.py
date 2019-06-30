# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-05-09 21:19:15
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: import_csv.py
'''

import pandas as pd


df = pd.read_csv(csvfile.as_posix(), encoding="gbk", header=0)

nu = df.values