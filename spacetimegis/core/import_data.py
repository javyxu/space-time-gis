# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-25 21:32:07
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: import_data.py
'''
import os

from . import pysc, uri_address

import geopyspark as gps

def importdata(tiffpath, target_crs=None):
    spatial_raster_layer = gps.geotiff.get(layer_type=gps.LayerType.SPATIAL, uri=tiffpath)
    spatial_tiled_layer = spatial_raster_layer.tile_to_layout(layout=gps.GlobalLayout())
    if not target_crs:
        spatial_raster_layer.reproject(target_crs=4326).collect_metadata().crs
    
    lyr_name = os.path.basename(tiffpath).split(',')[0]
    gps.write(uri=uri_address, 
          layer_name=lyr_name, 
          tiled_raster_layer=spatial_tiled_layer)