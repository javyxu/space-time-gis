# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-25 18:17:40
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: prediction_net.py
'''

import os
import numpy as np

from .define_net import Net
from .transform import demension_reduce, transform
from .image_folder import ImageFolder
import torch
from torch.autograd import Variable

from spacetimegis.utils.logging_mixin import logger
from spacetimegis.constants import LogLevel

def execute(path_):
    net = Net() 
    if torch.cuda.is_available():
        net.cuda()
    net.load_state_dict(torch.load(path_ + '/net_relu.pth')) # your net
    testset = ImageFolder(path_ + '/test_set/', transform) # your test set

    tys = dict() # map typhoon to its max wind
    tys_time = dict() # map typhoon-time to wind
    predictions = list()
    targets = list()

    for i in range(0, testset.__len__()):
        image, actual = testset.__getitem__(i)
        image = image.expand(1, image.size(0), image.size(1), image.size(2)) # a batch with 1 sample
        name = testset.__getitemName__(i)
        
        output = net(Variable(image))
        wind = output.data[0][0] # output is a 1*1 tensor

        name = name.split('_')
        tid = name[0]
        if tid in tys.keys() and tys[tid] < wind:
            tys[tid] = wind
        else :
            tys[tid] = wind
            
        tid_time = name[0] + '_' + name[1] + '_' + name[2] + '_' + name[3] + '_' + name[4] + '_' + name[5]
        tys_time[tid_time] = wind
        predictions.append(float(wind))
        targets.append(float(name[4]))
        
        if i % 100 == 99:
            logger.writelog(LogLevel.info, 'have processed ' + str(i + 1) + ' samples.')

    tys = sorted(tys.items(), key=lambda asd:asd[1], reverse=True)
    for ty in tys:
        logger.writelog(LogLevel.info, ty)  # show the sort of typhoons' wind

    tys_time = sorted(tys_time.items(), key=lambda asd:asd[0], reverse=False)

    res_error = np.sqrt(((np.asarray(predictions) - np.asarray(targets)) ** 2).mean())
    logger.writelog(LogLevel.info, '均方根误差是：{0}'.format(res_error))

    # where to write answer
    with open(path_ + '/result_relu.txt', 'w') as f:
        for ty in tys_time:
            f.write(str(ty) + '\n') # record all result by time