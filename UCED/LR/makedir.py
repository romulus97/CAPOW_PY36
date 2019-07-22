# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:17:59 2018

@author: YSu
"""

import os
from shutil import copy

Num_dir=10

for i in range(0,Num_dir):
    path=os.getcwd()+'\\' + str(i)
    copy('myscript.py',path)
    os.makedirs(path,exist_ok=True)