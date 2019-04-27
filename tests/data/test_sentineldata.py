# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-19 17:16:22
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: test_sentineldata.py
'''

import unittest
from spacetimegis.data.sentineldata import *

class test_sentineldata(unittest.TestCase):
    datapath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../examples_data/sentinel_data/S2A_MSIL1C_20180313T033531_N0206_R061_T49TDE_20180313T080228.zip')
    output = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../examples_data/sentinel_data/results')
    def test_sen2multitif(self):
        sen2multitif(datapath, output, 2)

    def test_sen2singletif(self):
        sen2singletif(datapath, output, 'B2')

if __name__ == "__main__":
    unittest.main()