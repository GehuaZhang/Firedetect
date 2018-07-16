#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018-07-13
@author: Gehua Zhang
"""

# Ignore Hardware Acceleration Warning
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from keras.applications.vgg16 import VGG16, decode_predictions
from keras.preprocessing import image
import numpy as np


# Pre-trained VGG16 model
def pretrain_vgg16(train_data):
    model = VGG16(weights="imagenet", include_top=True)

    for tain_img in train_data:
        features = model.predict(tain_img)
        #print(model.summary())
        print(decode_predictions(features, top=3))
