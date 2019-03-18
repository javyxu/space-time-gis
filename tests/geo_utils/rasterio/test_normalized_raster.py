# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-18 18:29:45
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: test_normalized_raster.py
'''

import unittest
import os

from spacetimegis.geo_utils.rasterio.normalized_raster import NormalizedRaster

class Test_NormalizedRaster(unittest.TestCase):
    # '/Users/xujavy/Documents/Work/srccode/space-time-gis/tests/geo_utils/rasterio/'
    folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../examples_data')
    norm_raster = NormalizedRaster(folder_path)
    srcfilename = folder_path + '/test_01.tif'

    def test_linear_normalization(self):
        self.norm_raster.linear_normalization(self.srcfilename)
    
    def test_standard_deviation_normalization(self):
        self.norm_raster.standard_deviation_normalization(self.srcfilename)

    
if __name__ == "__main__":
    unittest.main()