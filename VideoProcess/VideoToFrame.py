#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018-07-24
@author: Gehua Zhang
"""

import cv2
import os
import shutil


def videoToFrame(v_directory_path, i_directory_path, s_directory_path):
    # v_directory_path = path to the directory where you store videos
    # i_directory_path = path to the desired directory where you store images
    # s_directory_path = path to the directory for storing image/video frame size

    # Allowed video format
    video_format = ['mp4','avi']
    # Time span to capture images, in seconds
    time_span = 1.5

    files = os.listdir(v_directory_path)

    for video_path in files:
        if video_path[-3:] in video_format and os.path.isdir(video_path) == False:  # If this file is in video_format and is not a directory
            i_directory_name = os.path.join(i_directory_path, (video_path[:-4]))
            v_directory_name = os.path.join(v_directory_path, video_path)
            s_directory_name = os.path.join(s_directory_path, video_path[:-4])
            print("Processing: "+str(video_path[:-4]))

            if os.path.exists(i_directory_name):
                shutil.rmtree(i_directory_name)  # delete existing directory
            os.makedirs(i_directory_name)  # create directory

            vidcap = cv2.VideoCapture(v_directory_name)
            success, image = vidcap.read()
            count = 0

            # Store image size
            f = open(s_directory_name+".txt", "w")
            content = ' '.join(map(str, image.shape[:-1]))  # obtain image size then convert to string
            f.write(content)
            f.close()

            # Store video frame
            while success:
                success, image = vidcap.read()
                frame_rate = round(time_span*vidcap.get(cv2.CAP_PROP_FPS), 0)  # get frame rate
                if frame_rate == 0:
                    print("Frame Increment Below Zero, Consider Using Larger Time Span")
                    break

                frame_id = vidcap.get(cv2.CAP_PROP_POS_FRAMES)  # get frame ID, index by numbers
                if frame_id%frame_rate == 0:  # frame rate can be divided by frame_id
                    cv2.imwrite(i_directory_name + (r"\frame%d.jpg" % count), image)  # save frame as JPEG file
                    count += 1



v_directory_path = r'D:\AliothAtlas\Project\FireTrain\Mivis_Fire\Video\mp4'
i_directory_path = r'D:\AliothAtlas\Project\FireTrain\Mivis_Fire\Frame'
s_directory_path = r'D:\AliothAtlas\Project\FireTrain\Mivis_Fire\Size'
videoToFrame(v_directory_path, i_directory_path, s_directory_path)