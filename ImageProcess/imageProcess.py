#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018-07-13
@author: Gehua Zhang
"""
import os
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np


# For image augmentation, parameters are randomly picked.
def image_augmentation(train_path, test_path, size=(224,224)):

    # Using augmented pictures as rules specified
    augment_rule = image.ImageDataGenerator(featurewise_center=True, featurewise_std_normalization=True,
                                            rotation_range=20, width_shift_range=0.2, height_shift_range=0.2,
                                            rescale=1. / 255)
    train_generator = augment_rule.flow_from_directory(train_path, target_size=size, batch_size=32,
                                                               class_mode='binary')
    validation_generator = image.ImageDataGenerator(rescale=1./255).flow_from_directory(test_path, target_size=size, batch_size=32,
                                                                   class_mode='binary')
    return train_generator, validation_generator


def load_batch(directory_path, size=(224, 224)):
    files = os.listdir(directory_path)
    list_img = []
    for img_path in files:
        if not os.path.isdir(img_path):

            img = image.load_img(os.path.join(directory_path,img_path), target_size=size)
            imgInput = image.img_to_array(img)
            imgInput = np.expand_dims(imgInput, axis=0)
            imgInput = preprocess_input(imgInput)
            list_img.append(imgInput)
    return list_img


def load_single(img_path, size=(224, 224)):
    img = image.load_img(img_path, target_size=size)
    imgInput = image.img_to_array(img)
    imgInput = np.expand_dims(imgInput, axis=0)
    imgInput = preprocess_input(imgInput)  # Convert Img Array to VGG16 Recognizable File

    return imgInput
