#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018-07-16
@author:
"""

import os
# Import our functions
from ImageProcess import imageProcess
from Model.VGG16.PreTrained import pretrainVGG16


# Modify to your own system path
os.chdir(r"D:\CodeProjects\AliothAtlas\FireDetect")
train_path = r"DataSet\Train"

train_data = imageProcess.load_batch(train_path) # Load batch of pictures
#train_data = imageProcess.load_single(train_path) # Load a single picture

pretrainVGG16.pretrain_vgg16(train_data)