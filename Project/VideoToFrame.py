#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018-11-24
@author: Gehua Zhang
"""

import cv2
import os
import shutil


def videoToFrame(v_directory_path, i_directory_path, use_frame = True, use_vatic=True, span=1):
    # v_directory_path = path to the directory where you store videos
    # i_directory_path = path to the desired directory where you store images
    # use_frame=True: the output is per frame. No span.
    # use_vatic=True: Vatic format annotation generates annotation for each 0.5 frames, to match Vatic XML our image name would * 2.

    # Allowed video format
    video_format = ['mp4','avi']

    # Time span to capture images, in seconds
    if use_frame:
        print("You are generating each image per frame, time span is not using here.")
        time_span = 1
    else:
        print("Using time span = %d"%(span))
        if span == 1:
            print("Span == 1 equals use frame")
        time_span = span

    if use_vatic:
        name_span = 2
    else:
        name_span = 1

    files = os.listdir(v_directory_path)

    for video_path in files:
        print("")
        if video_path[-3:] in video_format and os.path.isdir(video_path) == False:  # If this file is in video_format and is not a directory
            i_directory_name = os.path.join(i_directory_path, (video_path[:-4]))
            v_directory_name = os.path.join(v_directory_path, video_path)
            file_name = video_path[:-4]

            print("Processing: "+str(file_name))
            print("Store frames in "+str(i_directory_name))

            if os.path.exists(i_directory_name):
                shutil.rmtree(i_directory_name)  # delete existing directory
            os.makedirs(i_directory_name)  # create directory

            vidcap = cv2.VideoCapture(v_directory_name)
            success, image = vidcap.read()
            count = 0

            print("Total Frames: "+str(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))
            print("FPS: "+str(vidcap.get(cv2.CAP_PROP_FPS)))

            # Store video frame
            while success:
                success, image = vidcap.read()
                #frame_rate = round(time_span*vidcap.get(cv2.CAP_PROP_FPS), 0)  # get frame rate
                frame_rate=time_span
                #frame_rate = time_span * vidcap.get(cv2.CAP_PROP_FPS)
                if frame_rate == 0:
                    print("Frame Increment Below Zero, Consider Using Larger Time Span")
                    break
                if not success:
                    if not count ==0:
                        print("%d frames generated"%(count))
                    break

                frame_id = vidcap.get(cv2.CAP_PROP_POS_FRAMES)  # get frame ID, index by numbers
                height, width = image.shape[:2]

                if use_frame:
                    cv2.imwrite(os.path.join(i_directory_name, (r"%s_%d_%d_%d.jpg" % (file_name,height,width,name_span*frame_id))), image)
                    count += 1
                else:
                    if frame_id%frame_rate == 0:  # frame rate can be divided by frame_id
                        cv2.imwrite(os.path.join(i_directory_name, (r"%s_%d_%d_%d.jpg" % (file_name,height,width,name_span*frame_id))), image)  # save frame as JPEG file
                        count += 1


# Output name format: firenumber_height_width_framenumber.jpg

v_directory_path = r'/Users/gehuazhang/Desktop/data_test/video/'
i_directory_path = r'/Users/gehuazhang/Desktop/data_test/frame/'

videoToFrame(v_directory_path, i_directory_path,False,True,span=10)