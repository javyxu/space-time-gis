# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-04-25 17:17:24
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: train_net.py
'''
import os

from spacetimegis.utils.logging_mixin import logger
from spacetimegis.constants import LogLevel
from spacetimegis.settings import get_celery_app
from spacetimegis import app

from .define_net import Net
from .transform import transform
from .image_folder import ImageFolder
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.init as init
import torch.optim as optim
import torch
import torchvision

celery_app = get_celery_app(app.config)

def testset_loss(dataset, network):
    loader = torch.utils.data.DataLoader(dataset)

    all_loss = 0.0
    for i, data in enumerate(loader, 0):
        inputs, labels = data
        inputs = Variable(inputs)

        outputs = network(inputs)   
        all_loss = all_loss + abs(labels[0] - outputs.data[0][0])

    return all_loss / i

@celery_app.task(bind=True)
def execute(self, path_):
    # path_ = os.path.abspath('.')
    trainset = ImageFolder(path_ + '/train_set/', transform)
    trainloader = torch.utils.data.DataLoader(trainset)
    testset = ImageFolder(path_ + '/test_set/', transform)

    net = Net()
    if torch.cuda.is_available():
        net.cuda()
    init.xavier_uniform_(net.conv1.weight.data, gain=1)
    init.constant_(net.conv1.bias.data, 0.1)
    init.xavier_uniform_(net.conv2.weight.data, gain=1)
    init.constant_(net.conv2.bias.data, 0.1)

    criterion = nn.L1Loss()

    optimizer = optim.Adam(net.parameters(), lr=0.001)

    for epoch in range(10): #
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            inputs, labels = Variable(inputs), Variable(labels)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = net(inputs)
            loss = criterion(outputs, labels.float())
            loss.backward()
            optimizer.step()

            running_loss += loss.data
            if i % 200 == 199:
                logger.writelog(LogLevel.info, '[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 200))
                running_loss = 0.0
        
        test_loss = testset_loss(testset, net)
        logger.writelog(LogLevel.info, '[%d ] test loss: %.3f' % (epoch + 1, test_loss))

    logger.writelog(LogLevel.info, 'Finished Training')
    torch.save(net.state_dict(), path_ + '/net_relu.pth')
    
    return {'current': 100, 'total': 100, 'status': 'Task completed!'}