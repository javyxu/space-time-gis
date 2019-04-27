# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-21 13:13:46
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: test_utils.py
'''

import unittest
from spacetimegis.geo_utils.utils import *

class test_utils(unittest.TestCase):

    def test_single2rgb(self):
        colormap = {1: (89, 105, 120),
                    2: (51, 160, 44),
                    3: (31, 120, 180),
                    4: (215, 25, 28),
                    5: (73, 75, 230),
                    6: (230, 22, 89),
                    7: (88, 99, 110),
                    8: (186, 146, 18)}
        tiff_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../examples_data/train_demo.tiff')
        single2rgb(tiff_path, colormap, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../examples_data'))

if __name__ == "__main__":
    unittest.main()