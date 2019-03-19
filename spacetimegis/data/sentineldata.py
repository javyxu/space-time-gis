# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-19 14:32:25
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: sentineldata.py
'''

import os
import rasterio
from spacetimegis.geo_utils.gdal.tools import singlebandmerge

bands = {}
bands["B1"] = (2, 0) # B1
bands["B2"] = (0, 0) # B2
bands["B3"] = (0, 1) # B3
bands["B4"] = (0, 2) # B4
bands["B5"] = (1, 0) # B5
bands["B6"] = (1, 1) # B6
bands["B7"] = (1, 2) # B7
bands["B8"] = (0, 3) # B8
bands["B8A"] = (1, 3) # B8A
bands["B9"] = (2, 1) # B9
bands["B10"] = (2, 2) # B10
bands["B11"] = (1, 4) # B11
bands["B12"] = (1, 5) # B12

def sen2multitif(sendataname, outputpath, bands=['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7' \
                'B8', 'B8A','B9', 'B10', 'B11', 'B12'], pixelbandindex=0, tarproj=3857):
    """
    """
    with rasterio.open(sendataname) as ds:
        singlebandtifs = list()
        for band in bands:
            subdsindex = bands[band]
            with rasterio.open(subdatasets[subdsindex[0]]) as subds:
                tmpdata = subds.read(subdsindex[1] + 1)
                tiff_name = os.path.join(outputpath, sendataname + band +'.tif')
                new_dataset = rasterio.open(tiff_name, 'w', driver='GTiff', 
                                        height=subds.height, width=subds.width, 
                                        count=1, dtype=tmpdata.dtype, 
                                        crs=subds.crs, transform=subds.transform)
                new_dataset.write(tmpdata, 1)
                del tmpdata
                new_dataset.close()
                singlebandtifs.append(tiff_name)

        multitiff_name = os.path.join(outputpath, sendataname +'multi.tif')
        singlebandmerge(multitiff_name, singlebandtifs, pixelbandindex)
        os.remove(i for i in singlebandtifs)


def sen2singletif(sendataname, band, outputpath, tarproj=3857):
    """
    """
    with rasterio.open(sendataname) as ds:
        subdsindex = bands[band]
        with rasterio.open(subdatasets[subdsindex[0]]) as subds:
            tmpdata = subds.read(subdsindex[1] + 1)
            tiff_name = os.path.join(outputpath, sendataname + band +'.tif')
            new_dataset = rasterio.open(tiff_name, 'w', driver='GTiff', 
                                    height=subds.height, width=subds.width, 
                                    count=1, dtype=tmpdata.dtype, 
                                    crs=subds.crs, transform=subds.transform)
            new_dataset.write(tmpdata, 1)
            del tmpdata
            new_dataset.close()
    