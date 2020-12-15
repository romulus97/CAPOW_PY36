# -*- coding: utf-8 -*-
"""
Created on Mon Oct 08 15:08:33 2018

@author: Joy Hill
"""

import matplotlib.pyplot as plt
import pandas as pd 
from pandas.plotting import autocorrelation_plot
from pandas import ExcelWriter
import numpy as np
import scipy.stats as stats


def PNW_demand(BPA_demand):

    #read in 2024 projections
    df_area = pd.read_excel('Synthetic_demand_pathflows/PNWAreaLoadShapes.xlsx', usecols=[1,5,7,12,14,22,26,29,30,35])
    area_load = df_area.values
    BPA2024_demand = area_load[:,1]
    AVA2024_demand = area_load[:,0]
    CHPD2024_demand = area_load[:,2]
    DOPD2024_demand = area_load[:,3]
    GCPD2024_demand = area_load[:,4]
    PACW2024_demand = area_load[:,5]
    PGE2024_demand = area_load[:,6]
    PSEI2024_demand = area_load[:,7]
    SCL2024_demand = area_load[:,8]
    TPWR2024_demand = area_load[:,9]
    
    BPA_std_change = np.std(BPA_demand)/np.std(BPA2024_demand)
    BPA_mean_change = np.mean(BPA_demand)/np.mean(BPA2024_demand)
       
    AVA_error = 100000
    AVA_hist_peak = 1700
    AVA2024_mean = np.nanmean(AVA2024_demand)
    AVA2024_std = np.nanstd(AVA2024_demand)
    AVA_whitened = (AVA2024_demand-AVA2024_mean)/AVA2024_std
    
    for pct in np.arange(0,1.01,.01):
        AVA_new = (AVA_whitened*AVA2024_std*BPA_std_change)+(pct*AVA2024_mean)
        AVA_new_peak = np.max(AVA_new)
    
        if np.abs(AVA_new_peak - AVA_hist_peak) < AVA_error:
            AVA_best = pct
        
            AVA_error = np.abs(AVA_new_peak - AVA_hist_peak)
    AVA_demand = (AVA_whitened*AVA2024_std*BPA_std_change)+(AVA_best*AVA2024_mean)
    
    
    #    CHPD_error = 100000
    #    CHPD_error2 = 100000
    #    CHPD_hist_avg = 200
    #    CHPD_hist_peak = 500
    CHPD2024_mean = np.nanmean(CHPD2024_demand)
    CHPD2024_std = np.nanstd(CHPD2024_demand)
    CHPD_whitened = (CHPD2024_demand-CHPD2024_mean)/CHPD2024_std
    CHPD_demand = (CHPD_whitened*CHPD2024_std*0.8)+(0.5*CHPD2024_mean) #I manually chose these values in order to obtain a peak and avg load close to reported values
    CHPD_demand[6004] = np.mean((CHPD_demand[6003],CHPD_demand[6005]))
    
    
    
    DOPD_error = 100000
    DOPD_hist_avg = 100
    DOPD2024_mean = np.nanmean(DOPD2024_demand)
    DOPD2024_std = np.nanstd(DOPD2024_demand)
    DOPD_whitened = (DOPD2024_demand-DOPD2024_mean)/DOPD2024_std
    
    for pct in np.arange(0,1.01,.01):
        DOPD_new = (DOPD_whitened*DOPD2024_std*BPA_std_change)+(pct*DOPD2024_mean)
        DOPD_new_avg = np.nanmean(DOPD_new)
        
        if np.abs(DOPD_new_avg - DOPD_hist_avg) < DOPD_error:
            DOPD_best = pct
            
            DOPD_error = np.abs(DOPD_new_avg - DOPD_hist_avg)
    DOPD_demand = (DOPD_whitened*DOPD2024_std*BPA_std_change)+(DOPD_best*DOPD2024_mean)
    
    GCPD_error = 100000
    GCPD_hist_avg = 500
    GCPD2024_mean = np.nanmean(GCPD2024_demand)
    GCPD2024_std = np.nanstd(GCPD2024_demand)
    GCPD_whitened = (GCPD2024_demand-GCPD2024_mean)/GCPD2024_std
    
    for pct in np.arange(0,1.01,.01):
        GCPD_new = (GCPD_whitened*GCPD2024_std*BPA_std_change)+(pct*GCPD2024_mean)
        GCPD_new_avg = np.nanmean(GCPD_new)
        
        if np.abs(GCPD_new_avg - GCPD_hist_avg) < GCPD_error:
            GCPD_best = pct
            
            GCPD_error = np.abs(GCPD_new_avg - GCPD_hist_avg)
    GCPD_demand = (GCPD_whitened*GCPD2024_std*BPA_std_change)+(GCPD_best*GCPD2024_mean)
    
    PACW_error = 100000
    PACW_hist_peak = 3174
    PACW2024_mean = np.nanmean(PACW2024_demand)
    PACW2024_std = np.nanstd(PACW2024_demand)
    PACW_whitened = (PACW2024_demand-PACW2024_mean)/PACW2024_std
    
    for pct in np.arange(0,2.01,.01):
        PACW_new = (PACW_whitened*PACW2024_std*BPA_std_change)+(pct*PACW2024_mean)
        PACW_new_peak = np.max(PACW_new)
        
        if np.abs(PACW_new_peak - PACW_hist_peak) < PACW_error:
            PACW_best = pct
            
            PACW_error = np.abs(PACW_new_peak - PACW_hist_peak)
    PACW_demand = (PACW_whitened*PACW2024_std*BPA_std_change)+(PACW_best*PACW2024_mean)
    
    PGE_error = 100000
    PGE_hist_peak = 3620
    PGE_hist_avg = 2335
    PGE2024_mean = np.nanmean(PGE2024_demand)
    PGE2024_std = np.nanstd(PGE2024_demand)
    PGE_whitened = (PGE2024_demand-PGE2024_mean)/PGE2024_std
    
    #changing std dev
    for pct in np.arange(0,1.01,.01):
        PGE_new = (PGE_whitened*PGE2024_std*pct)+(BPA_mean_change*PGE2024_mean)
        PGE_new_peak = np.max(PGE_new)
        PGE_new_avg = np.mean(PGE_new)
        
        if np.abs(PGE_new_peak - PGE_hist_peak) < PGE_error and np.abs(PGE_new_avg - PGE_hist_avg) < PGE_error:
            PGE_best = pct
            
            PGE_error = np.abs(PGE_new_peak - PGE_hist_peak)
    PGE_demand = (PGE_whitened*PGE2024_std*PGE_best)+(BPA_mean_change*PGE2024_mean)
    
    PSEI_error = 100000
    PSEI_hist_peak = 4929
    PSEI_hist_avg = 2600
    PSEI2024_mean = np.nanmean(PSEI2024_demand)
    PSEI2024_std = np.nanstd(PSEI2024_demand)
    PSEI_whitened = (PSEI2024_demand-PSEI2024_mean)/PSEI2024_std
    
    for pct in np.arange(0,2.01,.01):
        PSEI_new = (PSEI_whitened*PSEI2024_std*pct)+(BPA_mean_change*PSEI2024_mean)
        PSEI_new_peak = np.max(PSEI_new)
        PSEI_new_avg = np.mean(PSEI_new)
        
        if np.abs(PSEI_new_peak - PSEI_hist_peak) < PSEI_error and np.abs(PSEI_new_avg - PSEI_hist_avg) < PSEI_error:
            PSEI_best = pct
            
            PSEI_error = np.abs(PSEI_new_peak - PSEI_hist_peak)
    PSEI_demand = (PSEI_whitened*PSEI2024_std*PSEI_best)+(BPA_mean_change*PSEI2024_mean)
    
    SCL_error = 100000
    SCL_hist_peak = 1650
    SCL2024_mean = np.nanmean(SCL2024_demand)
    SCL2024_std = np.nanstd(SCL2024_demand)
    SCL_whitened = (SCL2024_demand-SCL2024_mean)/SCL2024_std
    
    for pct in np.arange(0,2.01,.01):
        SCL_new = (SCL_whitened*SCL2024_std*BPA_std_change)+(pct*SCL2024_mean)
        SCL_new_peak = np.max(SCL_new)
        
        if np.abs(SCL_new_peak - SCL_hist_peak) < SCL_error:
            SCL_best = pct
            
            SCL_error = np.abs(SCL_new_peak - SCL_hist_peak)
    SCL_demand = (SCL_whitened*SCL2024_std*BPA_std_change)+(SCL_best*SCL2024_mean)
    
    TPWR_error = 100000
    TPWR_hist_avg = 550
    TPWR2024_mean = np.nanmean(TPWR2024_demand)
    TPWR2024_std = np.nanstd(TPWR2024_demand)
    TPWR_whitened = (TPWR2024_demand-TPWR2024_mean)/TPWR2024_std
    
    for pct in np.arange(0,1.01,.01):
        TPWR_new = (TPWR_whitened*TPWR2024_std*BPA_std_change)+(pct*TPWR2024_mean)
        TPWR_new_avg = np.nanmean(TPWR_new)
        
        if np.abs(TPWR_new_avg - TPWR_hist_avg) < TPWR_error:
            TPWR_best = pct
            
            TPWR_error = np.abs(TPWR_new_avg - TPWR_hist_avg)
    TPWR_demand = (TPWR_whitened*TPWR2024_std*BPA_std_change)+(TPWR_best*TPWR2024_mean)
    
    Total_PNW_load = np.sum((AVA_demand,BPA_demand,CHPD_demand,DOPD_demand,GCPD_demand,PACW_demand,PGE_demand,PSEI_demand,SCL_demand,TPWR_demand),axis=0)
        
    return(Total_PNW_load)

    

