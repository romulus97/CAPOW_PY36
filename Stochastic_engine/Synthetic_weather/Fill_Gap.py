# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:34:54 2019

@author: YSu
"""
import numpy as np
import math

def fillgap(Q,d):
    #The first step is to check where the gaps are
    gaps_location=np.argwhere(np.isnan(Q))
    if len(gaps_location)==0:
        print('There is no gap')
    else:
        gaps=Q.isnull().astype(int).groupby(Q.notnull().astype(int).cumsum()).sum()
        list_of_gaps = gaps.loc[~(gaps==0)]
        largest_gap=np.max(gaps)
        if largest_gap>=d:
            print('More cleaning up')
        else:
            Index_correction=0
            for i in range(0,len(list_of_gaps)):
                Num_NaNs=list_of_gaps.values[i]
                Num_previous_point=math.ceil(Num_NaNs/2)
                
                for j in range(0,Num_NaNs):
                    gap_location=list_of_gaps.index.values[i]+Index_correction
                    if j <=Num_previous_point:
                        Q.iloc[gap_location]=Q.iloc[gap_location-1]
                        Index_correction=Index_correction+1
                    else:
                        Q.iloc[gap_location]=Q.iloc[gap_location+Num_NaNs+1]
                        Index_correction=Index_correction+1
    gaps_location_2=np.argwhere(np.isnan(Q))
    if len(gaps_location)==0:
        pass
    elif len(gaps_location_2)==0:
        print('gaps are filled')
    else:
        print("there are still gaps")
        print(gaps_location_2)
    
    return Q