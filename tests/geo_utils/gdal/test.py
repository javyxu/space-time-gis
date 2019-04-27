# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-08 17:54:46
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: test.py
'''

from osgeo import gdal

if if __name__ == "__main__":
    filename = '/Users/xujavy/Documents/Work/data/nc_data/air.1949.nc'
    dataset =  gdal.Open(filename)
    dataset.ReadAsArray()