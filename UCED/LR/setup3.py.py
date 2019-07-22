
"""
Created on Tue Dec  4 14:20:33 2018

@author: YSu
"""

import os
from shutil import copy

for run in range(0,1200):

    path=os.getcwd()+'\\PNW' + str(run)
    os.makedirs(path,exist_ok=True)
    update='PNW_wrapper.py'
    update_2='CA_wrapper.py'
    path=os.getcwd()+'\\PNW' + str(run)+'\\'+'UCED'
    copy(update,path)
    copy(update_2,path)