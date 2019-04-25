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

def sen2multitif(sendataname, outputpath, pixelbandindex=0, bandindexes=['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', \
                'B8', 'B8A','B9', 'B10', 'B11', 'B12']):
    """
    """
    with rasterio.open(sendataname) as ds:
        singlebandtifs = list()
        for bandindex in bandindexes:
            subdsindex = bands[bandindex]
            subdatasets = ds.subdatasets
            with rasterio.open(subdatasets[subdsindex[0]]) as subds:
                tmpdata = subds.read(subdsindex[1] + 1)
                tiff_name = os.path.join(outputpath, \
                    os.path.basename(sendataname).split('.')[0] + '_' + bandindex +'.tif')
                new_dataset = rasterio.open(tiff_name, 'w', driver='GTiff', 
                                        height=subds.height, width=subds.width, 
                                        count=1, dtype=tmpdata.dtype, 
                                        crs=subds.crs, transform=subds.transform)
                new_dataset.write(tmpdata, 1)
                del tmpdata
                new_dataset.close()
                singlebandtifs.append(tiff_name)

        multitiff_name = os.path.join(outputpath, \
            os.path.basename(sendataname).split('.')[0] +'_multi.tif')
        singlebandmerge(multitiff_name, singlebandtifs, pixelbandindex)
        # os.remove(i for i in singlebandtifs)
        for i in singlebandtifs:
            # print(i)
            os.remove(i)


def sen2singletif(sendataname, outputpath, band):
    """
    """
    with rasterio.open(sendataname) as ds:
        subdsindex = bands[band]
        subdatasets = ds.subdatasets
        with rasterio.open(subdatasets[subdsindex[0]]) as subds:
            tmpdata = subds.read(subdsindex[1] + 1)
            tiff_name = os.path.join(outputpath, os.path.basename(sendataname).split('.')[0] + '_' + band +'.tif')
            new_dataset = rasterio.open(tiff_name, 'w', driver='GTiff', 
                                    height=subds.height, width=subds.width, 
                                    count=1, dtype=tmpdata.dtype, 
                                    crs=subds.crs, transform=subds.transform)
            new_dataset.write(tmpdata, 1)
            del tmpdata
            new_dataset.close()


def sen2rgbtif(sendataname, outputpath):
    """
    """
    with rasterio.open(sendataname) as ds:
        subdatasets = ds.subdatasets
        with rasterio.open(subdatasets[3]) as subds:
            tmpdata = subds.read()
            tiff_name = os.path.join(outputpath, os.path.basename(sendataname).split('.')[0] + '_RGB' +'.tif')
            new_dataset = rasterio.open(tiff_name, 'w', driver='GTiff', 
                                    height=subds.height, width=subds.width, 
                                    count=3, dtype=tmpdata.dtype, 
                                    crs=subds.crs, transform=subds.transform)
            new_dataset.write(tmpdata)
            del tmpdata
            new_dataset.close()
    