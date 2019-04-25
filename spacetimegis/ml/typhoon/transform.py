# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-25 17:37:14
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: transform.py
'''

import torch
import torchvision.transforms as transforms

class demension_reduce(object):
    def __call__(self, tensor):
        return tensor # only need Red and Green channel

transform = transforms.Compose([transforms.ToTensor(),
                                demension_reduce(),
                                transforms.Normalize((0.5, 0.5, 0.5),(0.5, 0.5, 0.5))])