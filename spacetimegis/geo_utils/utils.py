# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-21 13:07:23
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: utils.py
'''

import os
import rasterio
import numpy as np

def single2rgb(filepath, colormap, outpath):
    '''
    Args:
        filepath: 
        
        colormap:
            colormap = {1: (89, 105, 120),
                        2: (51, 160, 44),
                        3: (31, 120, 180),
                        4: (215, 25, 28),
                        5: (73, 75, 230),
                        6: (230, 22, 89),
                        7: (88, 99, 110),
                        8: (186, 146, 18)}

        outpath:

    Raises:
    '''
    
    with rasterio.open(filepath) as ds:
        data = ds.read(1)

        rbands = np.zeros((ds.height, ds.width))
        gbands = np.zeros((ds.height, ds.width))
        bbands = np.zeros((ds.height, ds.width))

        for i in range(ds.height):
            for j in range(ds.width):
                colortmp = colormap[data[i][j]]
                rbands[i][j] = colortmp[0]
                gbands[i][j] = colortmp[1]
                bbands[i][j] = colortmp[2]
        
        multibands = (np.asarray([rbands, gbands, bbands])).astype(data.dtype)
        full_name = os.path.join(outpath, os.path.basename(filepath).split('.')[0] + '_rgb.tiff')
        new_dataset = rasterio.open(full_name, 'w', driver='GTiff', \
                                    height=ds.height, width=ds.width, \
                                    count=len(multibands), dtype=multibands.dtype, \
                                    crs=ds.crs, transform=ds.transform)

        new_dataset.write(multibands)
        new_dataset.close()