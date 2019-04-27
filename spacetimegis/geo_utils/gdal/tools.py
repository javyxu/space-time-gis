# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-18 17:59:27
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: retile_raster.py
'''

import os
import subprocess
from osgeo import gdal

def singlebandmerge(mergedtif, singlebandtifs, pixelbandindex=1):
    """
    """
    # if pixelx is None or pixely is None:
    ds = gdal.Open(singlebandtifs[pixelbandindex - 1])
    pixelx = ds.GetGeoTransform()[1]
    pixely = ds.GetGeoTransform()[5]
    print(pixelx, pixely)
    del ds

    cmd = 'gdal_merge.py -ps {0} {1} -separate -of GTiff -o {2} {3}'.format(abs(pixelx), abs(pixelx), \
        mergedtif, ' '.join(singlebandtifs))
    subprocess.call(cmd, shell=True)


def set_nodata(srcfilename, targetfilename, nodataval=-999999999.0):
    """
    """
    cmd = 'gdal_translate -a_nodata {0} -of GTiff {1} {2}'.format(nodataval, targetfilename, srcfilename)
    subprocess.call(cmd, shell=True)


def nearblack(srcfilename, targetfilename):
    """
    """
    cmd = 'nearblack -of GTiff -o {0} -setalpha {1}'.format(targetfilename, srcfilename)
    subprocess.call(cmd, shell=True)


def clipraster(height, width, targetdir, srcfilename):
    """
    """
    if os.path.exists(targetdir) is False:
        os.mkdir(targetdir)
    
    cmd = 'gdal_retile.py -ps {0} {1} -targetDir {2} {3}'.format(height, width, targetdir, srcfilename)
    subprocess.call(cmd, shell=True)


def vector2raster(height, width, shpfilename, targetfilename, attributename):
    """
    """    
    cmd = 'gdal_rasterize -ot Int16 -ts {0} {1} -a {2} {3} target_raster.tiff'.format(\
        height, width, attributename, shpfilename, targetfilename)
    subprocess.call(cmd, shell=True)


def sieve_raster(threshold, srcfilename, targetfilename):
    '''
    Args:
    Returns:
    Raises:
    '''
    cmd = 'gdal_sieve.py -st {0} -4 -of {1} {2}'.format(threshold, srcfilename, targetfilename)
    subprocess.call(cmd, shell=True)

def test():
    '''
    Args:
    Returns:
    Raises:
    '''
    gdal.Open()