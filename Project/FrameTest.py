#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-10
@author: Gehua Zhang
"""


# Test your image annotation matches with Vatic XML

from PIL import Image, ImageDraw


def insertHighlight(image_path,position):

    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    draw.text(position,"*",fill=(255,0,0,255))
    img.show()

insertHighlight("/Users/gehuazhang/Desktop/fire13_240_320_860.jpg",(167,151))