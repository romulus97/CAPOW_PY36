# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:29:16 2018

@author: jdkern
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def exchange(year):

    df_data = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/Load_Path_Sim.csv',header=0)
    c = ['Path66_sim','Path46_sim','Path61_sim','Path42_sim','Path24_sim','Path45_sim']
    df_data = df_data[c]
    paths = ['Path66','Path46','Path61','Path42','Path24','Path45']
    df_data.columns = paths
    df_data = df_data.loc[year*365:year*365+364,:]
    
    # select dispatchable imports (positve flow days)
    imports = df_data
    imports = imports.reset_index()
    
    for p in paths:
        for i in range(0,len(imports)):     
            
            if p == 'Path42':
                if imports.loc[i,p] >= 0:
                    imports.loc[i,p] = 0
                else:
                    imports.loc[i,p] = -imports.loc[i,p]
            
            elif p == 'Path46':
                if imports.loc[i,p] < 0:
                    imports.loc[i,p] = 0
                else:
                    imports.loc[i,p] = imports.loc[i,p]*.404 + 424
            
            else:
                if imports.loc[i,p] < 0:
                    imports.loc[i,p] = 0
                    
                    
    imports.rename(columns={'Path46':'Path46_SCE'}, inplace=True)
    imports.to_csv('Path_setup/CA_imports.csv')
    
    # convert to minimum flow time series and dispatchable (daily)
    df_mins = pd.read_excel('Path_setup/CA_imports_minflow_profiles.xlsx',header=0)
    lines = ['Path66','Path46_SCE','Path61','Path42']
    
    for i in range(0,len(df_data)):
        for L in lines:
            
            if df_mins.loc[i,L] >= imports.loc[i,L]:
                df_mins.loc[i,L] = imports.loc[i,L]
                imports.loc[i,L] = 0
            
            else:
                imports.loc[i,L] = np.max((0,imports.loc[i,L]-df_mins.loc[i,L]))
    
    dispatchable_imports = imports*24
    dispatchable_imports.to_csv('Path_setup/CA_dispatchable_imports.csv')
    
    df_data = pd.read_csv('Path_setup/CA_imports.csv',header=0)
    
    # hourly minimum flow for paths
    hourly = np.zeros((8760,len(lines)))
    
    for i in range(0,365):
        for L in lines:
            index = lines.index(L)
            
            hourly[i*24:i*24+24,index] = np.min((df_mins.loc[i,L], df_data.loc[i,L]))
            
    H = pd.DataFrame(hourly)
    H.columns = ['Path66','Path46_SCE','Path61','Path42']
    H.to_csv('Path_setup/CA_path_mins.csv')
    
    # hourly exports
    df_data = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/Load_Path_Sim.csv',header=0)
    c = ['Path66_sim','Path46_sim','Path61_sim','Path42_sim','Path24_sim','Path45_sim']
    df_data = df_data[c]
    df_data.columns = [paths]
    
    df_data = df_data.loc[year*365:year*365+364,:]
    df_data = df_data.reset_index()
    
    e = np.zeros((8760,4))
    
    #Path 42
    path_profiles = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path42',header=None)
    pp = path_profiles.values
    
    for i in range(0,len(df_data)):
        if df_data.loc[i,'Path42'].values > 0:
            e[i*24:i*24+24,0] = pp[i,:]*df_data.loc[i,'Path42'].values
    
    #Path 24
    path_profiles = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path24',header=None)
    pp = path_profiles.values
    
    for i in range(0,len(df_data)):
        if df_data.loc[i,'Path24'].values < 0:
            e[i*24:i*24+24,1] = pp[i,:]*df_data.loc[i,'Path24'].values*-1
    
    #Path 45
    path_profiles = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path45',header=None)
    pp = path_profiles.values
    
    for i in range(0,len(df_data)):
        if df_data.loc[i,'Path45'].values < 0:
            e[i*24:i*24+24,2] = pp[i,:]*df_data.loc[i,'Path45'].values*-1  
            
    #Path 66
    path_profiles = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path66',header=None)
    pp = path_profiles.values
    
    for i in range(0,len(df_data)):
        if df_data.loc[i,'Path66'].values < 0:
            e[i*24:i*24+24,2] = pp[i,:]*df_data.loc[i,'Path66'].values*-1  
    
    e = e*24
    
    exports = pd.DataFrame(e) 
    exports.columns = ['Path42','Path24','Path45','Path66']
    exports.to_csv('Path_setup/CA_exports.csv')
    
    
    
    ##########################3
    ##########################
    
    # HYDRO
    
    # convert to minimum flow time series and dispatchable (daily)
    
    df_data = pd.read_excel('../Stochastic_engine/CA_hydropower/CA_hydro_daily.xlsx',header=0)
    hydro = df_data.loc[year*365:year*365+364,:]
    hydro = hydro.reset_index()
    hydro=hydro.values
    PGE_ALL=hydro[:,1]/0.837
    SCE_all=hydro[:,2]/0.8016
    hydro=pd.DataFrame()
    hydro['PGE_valley']=PGE_ALL
    hydro['SCE']=SCE_all
    zones = ['PGE_valley','SCE']
    df_mins = pd.read_excel('Hydro_setup/Minimum_hydro_profiles.xlsx',header=0)
    
    for i in range(0,len(hydro)):
        for z in zones:
            
            if df_mins.loc[i,z]*24 >= hydro.loc[i,z]:
                df_mins.loc[i,z] = hydro.loc[i,z]/24
                hydro.loc[i,z] = 0
            
            else:
                hydro.loc[i,z] = np.max((0,hydro.loc[i,z]-df_mins.loc[i,z]*24))
    
    dispatchable_hydro = hydro
    dispatchable_hydro.to_csv('Hydro_setup/CA_dispatchable_hydro.csv')
    
    # hourly minimum flow for hydro
    hourly = np.zeros((8760,len(zones)))
    
    df_data = pd.read_excel('../Stochastic_engine/CA_hydropower/CA_hydro_daily.xlsx',header=0)
    hydro = df_data.loc[year*365:year*365+364,:]
    hydro = hydro.reset_index()
    PGE_ALL=hydro[:,1]/0.837
    SCE_all=hydro[:,2]/0.8016
    hydro=pd.DataFrame()
    hydro['PGE_valley']=PGE_ALL
    hydro['SCE']=SCE_all
    zones = ['PGE_valley','SCE']
    
    for i in range(0,365):
        for z in zones:
            index = zones.index(z)
            
            hourly[i*24:i*24+24,index] = np.min((df_mins.loc[i,z],hydro.loc[i,z]))
            
    H = pd.DataFrame(hourly)
    H.columns = zones
    H.to_csv('Hydro_setup/CA_hydro_mins.csv')

    return None
