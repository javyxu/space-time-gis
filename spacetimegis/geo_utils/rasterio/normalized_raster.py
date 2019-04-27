# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-18 17:27:31
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: normalized_raster.py
'''

import os
import rasterio

class NormalizedRaster(object):
    """
    数据标准化（Normalization），也称为归一化，
    归一化就是将你需要处理的数据在通过某种算法经过处理后，限制将其限定在你需要的一定的范围内。
    """
    def __init__(self, outputpath):
        self.outputpath = outputpath

    def linear_normalization(self, srcfilename, maxval=None, minval=None):
        """
        线性归一化：也称min-max标准化、离差标准化；是对原始数据的线性变换，使得结果值映射到[0,1]之间。转换函数如下：
        `x = (x - min(x)) / (max(x) - min(x))`
        这种归一化比较适用在数值较集中的情况。这种方法有一个缺陷，就是如果max和min不稳定的时候，
        很容易使得归一化的结果不稳定，影响后续使用效果。其实在实际应用中，我们一般用经验常量来替代max和min。
        """
        with rasterio.open(srcfilename) as ds:
            tmpdata = ds.read()
            minval = tmpdata.min() if minval is None else minval
            maxval = tmpdata.max() if maxval is None else maxval
            tmpdata = (tmpdata - [minval]) / (maxval - minval)
            
            new_filename = os.path.join(self.outputpath, os.path.basename(srcfilename).split('.')[0] + '_linear_normal.tif')
            new_dataset = rasterio.open(new_filename, 'w', driver='GTiff', 
                                        height=ds.height, width=ds.width, 
                                        count=len(tmpdata), dtype=tmpdata.dtype, crs=ds.crs, transform=ds.transform)

            if len(tmpdata) is 1:
                new_dataset.write(tmpdata, 1)
            else:
                new_dataset.write(tmpdata)
            new_dataset.close()

    def standard_deviation_normalization(self, srcfilename):
        """
        标准差归一化，也叫Z-score标准化，这种方法给予原始数据的均值（mean，μ）和标准差（standard deviation，σ）
        进行数据的标准化。经过处理后的数据符合标准正态分布，即均值为0，标准差为1，转化函数为：
        `x = (x - μ) / σ`
        """
        with rasterio.open(srcfilename) as ds:
            tmpdata = ds.read()
            tmpdata = (tmpdata - [tmpdata.mean()]) / tmpdata.std()
            
            new_filename = os.path.join(self.outputpath, os.path.basename(srcfilename).split('.')[0] + '_std_normal.tif')
            new_dataset = rasterio.open(new_filename, 'w', driver='GTiff', 
                                        height=ds.height, width=ds.width, 
                                        count=len(tmpdata), dtype=tmpdata.dtype, crs=ds.crs, transform=ds.transform)

            if len(tmpdata) is 1:
                new_dataset.write(tmpdata, 1)
            else:
                new_dataset.write(tmpdata)
            new_dataset.close()

    def nonlinear_normalization(self, srcfilename):
        """
        这种方法一般使用在数据分析比较大的场景，有些数值很大，有些很小，通过一些数学函数，
        将原始值进行映射。一般使用的函数包括log、指数、正切等，需要根据数据分布的具体情况来决定非线性函数的曲线。
        """
        pass