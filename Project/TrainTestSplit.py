#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-10
@author: Gehua Zhang
"""

import os
import csv
import random
import shutil


def trainTestSplit(train_ratio,csv_diretory,frame_directory,desired_directory):

    if os.path.exists(desired_directory):
        shutil.rmtree(desired_directory)  # delete existing directory
    os.makedirs(desired_directory)  # create directory

    data_set = []
    train_set = []
    test_set = []

    with open('%s/labels.csv' % (csv_diretory)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if not line_count == 0:
                data_set.append(row)
                line_count+=1
            else:
                line_count+=1
                continue

    num_data = len(data_set)
    num_train = round(num_data*train_ratio)
    num_test = num_data-num_train

    # Random select train data and the rest is for test data
    list_train_index=random.sample(range(0, num_data), num_train)
    list_test_index=[i for j, i in enumerate(range(num_data)) if j not in list_train_index]

    for index in list_train_index:
        train_set.append(data_set[index])
    for index in list_test_index:
        test_set.append(data_set[index])


    # Define storage path
    train_path = os.path.join(desired_directory,"train")
    test_path = os.path.join(desired_directory,"test")
    os.makedirs(train_path)
    os.makedirs(test_path)


    with open('%s/train_labels.csv'%(desired_directory), mode='w') as train_csv:
        train_writer = csv.writer(train_csv)
        train_writer.writerow(["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"])

        for train_info in train_set:
            # Find corresponding image and move to desired directory
            frame_name = train_info[0]
            obj_name = frame_name.split("_")[0]
            obj_path = os.path.join(*[frame_directory,obj_name,frame_name])
            if os.path.exists(obj_path):
                shutil.copy2(obj_path, train_path)

            # Generate train label csv
            train_writer.writerow(train_info)

    with open('%s/test_labels.csv'%(desired_directory), mode='w') as test_csv:
        test_writer = csv.writer(test_csv)
        test_writer.writerow(["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"])

        for test_info in test_set:
            # Find corresponding image and move to desired directory
            frame_name = test_info[0]
            obj_name = frame_name.split("_")[0]
            obj_path = os.path.join(*[frame_directory,obj_name,frame_name])
            if os.path.exists(obj_path):
                shutil.copy2(obj_path, test_path)

            # Generate test label csv
            test_writer.writerow(test_info)


csv_directory="/Users/gehuazhang/Desktop/data_test/csv"
frame_directory="/Users/gehuazhang/Desktop/data_test/frame"
desired_directory="/Users/gehuazhang/Desktop/data_test/ready"
trainTestSplit(0.8,csv_directory,frame_directory,desired_directory)