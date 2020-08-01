#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
If you want to use pyinstaller for this project,
simply run:
"
    python3 _Installer.py
                            "
in terminal
"""

import os

try:
    from _CheckEnvironment import checkEnvironment

    checkEnvironment(True)
except:
    pass

try:
    import PyInstaller.__main__
except:
    print("check pyinstaller: not installed. Now install pyinstaller:")
    os.system('pip3 install pyinstaller')
    import PyInstaller.__main__

from sys import platform

app_name = "FanselineToolbox"
main_file = "FanselineToolbox.py"

if platform == "darwin":
    icon_path = "./GUI/Image/icon-mac.icns"
    output_list = ["--name=%s" % app_name, "--windowed"]
    if os.path.exists("./GUI"):
        output_list.append("--add-data=%s" % "./GUI:GUI/")
    if os.path.exists("./Source_/MacOS_Support"):
        pass
    if os.path.exists(icon_path):
        output_list.append("--icon=%s" % icon_path)
    output_list.append(main_file)
else:
    icon_path = "./GUI/Image/Logo_Desktop_256x256.ico"
    output_list = ["--noconfirm", "--name=%s" % app_name]
    if os.path.exists("./GUI"):
        if os.name == "nt":
            output_list.append("--add-data=%s" % "./GUI;GUI/")
        else:
            output_list.append("--add-data=%s" % "./GUI:GUI/")
    output_list.append("--onedir")
    output_list.append("--windowed")
    if os.path.exists(icon_path):
        output_list.append("--icon=%s" % icon_path)
    output_list.append(main_file)

PyInstaller.__main__.run(output_list)
