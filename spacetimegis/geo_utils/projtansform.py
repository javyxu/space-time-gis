# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-19 14:43:33
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: projtansform.py
'''

from osgeo import gdal, osr
from rasterio.transform import from_origin

def gdal_trans(src_geotrans, xsize, ysize, src_proj, tar_proj=3857):
    """
    GDAL 格式
    """
    src_srs = osr.SpatialReference()
    src_srs.ImportFromWkt(src_proj)
    dst_srs = osr.SpatialReference()
    dst_srs.ImportFromEPSG(tar_proj)
    ct = osr.CoordinateTransformation(src_srs, dst_srs)

    xmin, ymax = ct.TransformPoint(src_geotrans[0], src_geotrans[3])[:2]
    xmax , ymin = ct.TransformPoint(src_geotrans[0] + src_geotrans[1] * xsize, src_geotrans[3] + src_geotrans[5] * ysize)[:2]

    return (xmin, (xmax-xmin) / xsize , src_geotrans[2], ymax, src_geotrans[4], (ymin-ymax) / ysize)


def rasterio_trans(src_geotrans, xsize, ysize, src_proj, tar_proj=3857):
    """
    """
    out_geotrans = gdal_trans(src_geotrans, xsize, ysize, src_proj, tar_proj=3857)
    return from_origin(out_geotrans[0], out_geotrans[3], out_geotrans[1], abs(out_geotrans[5]))