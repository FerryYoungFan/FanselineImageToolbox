#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sys import platform

"""
Python 3.7	                        V 3.7.4

numpy		                        V 1.19.0
opencv-python                       V 4.2.0.34
(for mac: opencv-python-headless    V 4.3.0.36)
PyQt5                               V 5.15.0
"""


def checkEnvironment(showInfo=True):
    if showInfo:
        print("Checking Python Environment...")
    try:
        import numpy
    except:
        if showInfo:
            print("Numpy not found, try to install:")
        os.system("pip3 install numpy==1.19.0")

    try:
        import cv2
    except:
        if showInfo:
            print("OpenCV not found, try to install:")
        if platform == "darwin":
            os.system("pip3 install opencv-python-headless==4.3.0.36")
        else:
            os.system("pip3 install opencv-python==4.2.0.34")

    try:
        import PyQt5
    except:
        if showInfo:
            print("PyQt5 not found, try to install:")
        os.system("pip3 install PyQt5==5.15.0")

    not_install = None
    try:
        not_install = "Numpy"
        import numpy
        not_install = "Pillow"
        import cv2
        not_install = "OpenCV"
        if showInfo:
            print("Check Environment - Done!")
    except:
        print("Error: Environment Error")
        print("{0} not installed.".format(not_install))


if __name__ == '__main__':
    checkEnvironment(True)
