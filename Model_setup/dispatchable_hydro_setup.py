# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:29:16 2018

@author: jdkern
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


years = ['2001','2005','2010','2011']
num_years = int(len(years))
days = 365
hours = 8760
regions = ['PGE_V','SCE','PNW']
num_regions = int(len(regions))
upramps = np.zeros((days,num_regions,num_years))
downramps = np.zeros((days,num_regions,num_years))
min_flow = np.zeros((days,num_regions,num_years))
max_flow = np.zeros((days,num_regions,num_years))

for y in years:
    
    y_index = years.index(y)
    
    for r in regions:
        r_index = regions.index(r)
        
        #load data 
        filename = 'Hydro_setup/' + r + '_hydro_' + y + '.xlsx'
        M = pd.read_excel(filename,header=None)
        m = M.values
            
        v = np.sum(m,axis=1)
            
        for d in range(0,days):
            
                        
            sample = v[d*24:d*24+24]
            min_flow[d,r_index,y_index] = np.min(sample)
            max_flow[d,r_index,y_index] = np.max(sample)
            
            ramp = 0
            
            for h in range(0,23):
                if ramp < sample[h+1] - sample[h]:
                    ramp = sample[h+1] - sample[h]
            
            upramps[d,r_index,y_index] = ramp
                
            ramp = 0
            
            for h in range(0,23):
                if ramp < sample[h] - sample[h+1]:
                    ramp = sample[h] - sample[h+1]
            
            downramps[d,r_index,y_index] = ramp
                

# select ramping rates across years
#for r in regions:
#    
#    r_index = regions.index(r)
    
#    plt.figure()
#    
#    for y in years:
#            
#        y_index = years.index(y)
#            
#        plt.plot(upramps[:,r_index,y_index])
#        plt.title(r + '_Upramps')
# 
#    plt.figure()
#    
#    for y in years:
#            
#        y_index = years.index(y)
#        plt.plot(downramps[:,r_index,y_index])
#        plt.title(r + '_Downramps')           
#
#    plt.figure()
#    
#    for y in years:
#            
#        y_index = years.index(y)
#        plt.plot(min_flow[:,r_index,y_index])
#        plt.title(r + '_Minflow')      
#    
#    plt.figure()
#    
#    for y in years:
#            
#        y_index = years.index(y)
#        plt.plot(max_flow[:,r_index,y_index])
#        plt.title(r + '_Maxflow')  
        
#min flows for each zone       
f = min_flow[:,0,:]
PGE_V_min = np.min(f,axis=1)

f = min_flow[:,1,:]
SCE_min = np.min(f,axis=1)

f = min_flow[:,2,:]
PNW_min = np.min(f,axis=1)

#max flows for each zone       
f = max_flow[:,0,:]
PGE_V_max = np.max(f,axis=1)

f = max_flow[:,1,:]
SCE_max = np.max(f,axis=1)

f = max_flow[:,2,:]
PNW_max = np.max(f,axis=1)

#add low pass filter
SCE_min_filtered = np.zeros((365,1))
PGE_V_min_filtered = np.zeros((365,1))
PNW_min_filtered = np.zeros((365,1))

for i in range(15,350):
    SCE_min_filtered[i] = np.mean(SCE_min[i-15:i+15])
    PGE_V_min_filtered[i] = np.mean(PGE_V_min[i-15:i+15])
    PNW_min_filtered[i] = np.mean(PNW_min[i-15:i+15])

SCE_min_filtered[0:15] = SCE_min_filtered[15]
SCE_min_filtered[350:] = SCE_min_filtered[349]
PGE_V_min_filtered[0:15] = PGE_V_min_filtered[15]
PGE_V_min_filtered[350:] = PGE_V_min_filtered[349]
PNW_min_filtered[0:15] = PNW_min_filtered[15]
PNW_min_filtered[350:] = PNW_min_filtered[349]

combined = np.column_stack((PGE_V_min_filtered,SCE_min_filtered,PNW_min_filtered))
df_C = pd.DataFrame(combined)
df_C.columns = ['PGE_valley','SCE','PNW']
df_C.to_excel('Hydro_setup/Minimum_hydro_profiles.xlsx')


