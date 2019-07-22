# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 12:04:22 2019

@author: sdenaro
"""

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
    

for i in range(0,200):
    file_path='LR/PNW'+str(i)+'/PNW_price_calculation_LR.py'
    pattern='../Model_setup/PNW_data_file/generators.csv'
    subst='generators.csv' 
    replace(file_path, pattern, subst)