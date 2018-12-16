#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018-11-24
@author: Gehua Zhang
"""

import xml.dom.minidom
import os
import numpy as np
import shutil
import csv

# Extract frame's information from its name
def extractFrameInfo(frame_directory):

    frame_files = os.listdir(frame_directory)
    dict_info={}
    # Loop for each frame image - extracts its annotation information
    for frame_path in frame_files:
        if frame_path[-3:] == "jpg" and os.path.isdir(frame_path) == False:
            frame_name = frame_path[:-4]
            obj_name,height,width,frame = frame_name.split("_")
            dict_info[frame]=[frame_path,height,width,frame]
    return dict_info,obj_name


# From extracted frame information, find matched xml information.
def findXMLInfo(xml_directory, objName, objectType, objectID):

    xml_files = os.listdir(xml_directory)
    # Find corresponding XML file based on frame image name
    for xml_path in xml_files:
        xml_name="%s_annot.xml"%(objName)
        if xml_path == xml_name and os.path.isdir(xml_path) == False:
            annot_file_path = os.path.join(xml_directory, xml_name)


            # Read XML Data
            xml_doc = xml.dom.minidom.parse(annot_file_path)
            list_object = xml_doc.getElementsByTagName('object')

            # Check If Required Object Exist
            object_exist = False
            for temp_object in list_object:
                if temp_object.getElementsByTagName('name').item(0).childNodes[0].data == str(objectType) \
                        and temp_object.getElementsByTagName('id').item(0).childNodes[0].data == str(objectID):
                    objects = temp_object
                    object_exist = True
                    break
                else:
                    continue

            if not object_exist:
                print("No such object type as " + str(objectType) + ", or such ID as " + str(objectID))
                return

            # For Existed Object, Do Following
            # Looking for "polygon"
            list_polygon = objects.getElementsByTagName('polygon')

            dict_coord = {}
            if len(list_polygon) > 0:
                for polygon in list_polygon:

                    # Looking for "t", store its value as ID of each node
                    temp_id = polygon.getElementsByTagName("t").item(0).childNodes[0].data
                    dict_coord[temp_id] = []

                    # Looking for "pt", store its value as coordinate of x,y,l
                    list_points = polygon.getElementsByTagName("pt")
                    if len(list_points) > 0:
                        for points in list_points:
                            temp_x = points.getElementsByTagName('x').item(0).firstChild.data
                            temp_y = points.getElementsByTagName('y').item(0).firstChild.data
                            #temp_l = points.getElementsByTagName('l').item(0).firstChild.data
                            #dict_coord[temp_id].append([temp_x, temp_y, temp_l])
                            dict_coord[temp_id].append([temp_x, temp_y])

            #print(dict_coord["100"])
            return dict_coord


# Convert all cleaned txt file to a single csv file
def creatCSV(annot_diretory,csv_diretory,):
    if os.path.exists(csv_diretory):
        shutil.rmtree(csv_diretory)  # delete existing directory
    os.makedirs(csv_diretory)  # create directory

    list_info=[]

    # Dig into final txt file path
    list_object_directory = os.listdir(annot_diretory)
    for object_directory in list_object_directory:
        tmp_directory = os.path.join(annot_diretory,object_directory)
        if os.path.isdir(tmp_directory) == True:
            list_txt_directory = os.listdir(tmp_directory)
            for txt_path in list_txt_directory:
                tmp_tmp_directory = os.path.join(tmp_directory,txt_path)

                # Obtain txt information
                with open(tmp_tmp_directory, 'r') as txt_file:
                    list_info.append(txt_file.readlines())

    with open('%s/labels.csv'%(csv_diretory), mode='w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["filename","width","height","class","xmin","ymin","xmax","ymax"])
        for info in list_info:
            list_temp=info[0].split(",")
            csv_writer.writerow(list_temp)


# Write cleaned information into txt and create csv.
def main(frame_directory,xml_directory,annot_diretory,csv_diretory,objectType, objectID):
    # annot_diretory: Desired directory where you store cleaned annotation.
    # xml_directory: Directory where you store Vatic format xml.
    # frame_directory: Directory where you store your image frames.
    # csv_diretory: Directory where you store CSV

    dict_info, file_name_number = extractFrameInfo(frame_directory)
    dict_xml = findXMLInfo(xml_directory, file_name_number, objectType, objectID)

    # Name format: fire7_2 means this the 7th fire video and the 2nd fire objects
    file_name_path = os.path.join(annot_diretory, (str(file_name_number)+"_"+str(objectID)))

    # If the directory you want to store cleaned annotation exist, delete it and create new
    if os.path.exists(file_name_path):
        shutil.rmtree(file_name_path)  # delete existing directory
    os.makedirs(file_name_path)  # create directory


    for info in dict_info.values():
        frame_id = info[-1]
        frame_name = info[0]
        frame_height = info[1]
        frame_width = info[2]

        # Check if we have the annotation for this exact frame
        if not frame_id in dict_xml:
            continue

        arr_position=np.array(dict_xml[frame_id]).astype(np.float)
        xmax, ymax = arr_position.max(axis=0)
        xmin, ymin = arr_position.min(axis=0)

        info_write = frame_name+","+frame_width+","+frame_height+","+objectType+","+str(xmin)+","+str(ymin)+","+str(xmax)+","+str(ymax)
        # Name format: fire7_256_400_60_ID.txt
        f = open('%s/%s_%d.txt'%(file_name_path,frame_name[:-4],objectID), 'w')
        f.write(info_write)
        f.close()

    creatCSV(annot_diretory,csv_diretory)


xml_directory="/Users/gehuazhang/Desktop/data_test/vaticXML"
frame_directory="/Users/gehuazhang/Desktop/data_test/frame/fire1"
annot_diretory="/Users/gehuazhang/Desktop/data_test/cleanedXML"
csv_directory="/Users/gehuazhang/Desktop/data_test/csv"


main(frame_directory,xml_directory,annot_diretory,csv_directory,"fire",1)

