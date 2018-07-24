#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018-07-24
@author: Gehua Zhang
"""

import cv2
import os
import shutil

# Modify this path to the directory where you store your videos
v_directory_path = r'D:\AliothAtlas\Project\mivia_fire\mivia_fire'
# Modify this path to the desired directory where you store images
i_directory_path = r'D:\AliothAtlas\Project\mivia_fire\mivia_fire'
# Allowed video format
video_format = ['mp4','avi']
# Time span to capture images, in seconds
time_span = 1.2


files = os.listdir(v_directory_path)
list_videos = []

for video_path in files:
    if video_path[-3:] in video_format and os.path.isdir(video_path) == False: #If this file is in video_format and is not a directory
        i_directory_name = os.path.join(i_directory_path, (video_path[:-4]))
        v_directory_name = os.path.join(v_directory_path, video_path)
        print("Processing: "+str(video_path[:-4]))

        shutil.rmtree(i_directory_name)  # delete existing directory
        os.makedirs(i_directory_name)  # create directory

        vidcap = cv2.VideoCapture(v_directory_name)
        success, image = vidcap.read()
        count = 0

        while success:
            success, image = vidcap.read()
            frame_rate = round(time_span*vidcap.get(cv2.CAP_PROP_FPS),0)  # get frame rate
            frame_id = vidcap.get(cv2.CAP_PROP_POS_FRAMES)  # get frame ID, index by numbers

            if frame_id%frame_rate == 0:
                cv2.imwrite(i_directory_name + (r"\frame%d.jpg" % count), image)  # save frame as JPEG file
                count += 1