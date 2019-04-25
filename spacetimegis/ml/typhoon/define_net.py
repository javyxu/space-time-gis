# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-25 17:18:43
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: define_net.py
'''

from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(2, 20, 3)
        self.pool1 = nn.MaxPool2d(5, 5)
        self.conv2 = nn.Conv2d(20, 40, 3)
        self.pool2 = nn.MaxPool2d(4, 4)
        self.conv3 = nn.Conv2d(40, 60, 3)
        self.pool3 = nn.MaxPool2d(3, 3)
        self.fc1 = nn.Linear(60 * 3 * 3, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.fc4 = nn.Linear(10, 1)

        
    def forward(self, x):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        x = x.to(device)
        x = self.pool1(F.relu(self.conv1(x))) # better than sigmoid/tanh
        x = self.pool2(F.relu(self.conv2(x))) # better than sigmoid/tanh
        x = self.pool3(F.relu(self.conv3(x))) # better than sigmoid/tanh
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features