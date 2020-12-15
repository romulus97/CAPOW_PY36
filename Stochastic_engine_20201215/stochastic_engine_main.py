# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 18:24:48 2020

@author: 11487
"""

import time

# Function: Copying all the files in directory src to dst;
import os, shutil
def CopyFiles(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
            
# Function: Deleting all the files in directory mypath;            
import os, re, os.path
def DeleteFiles(mypath):
    # mypath = "my_folder"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))


# %% initilization
# define the number of standard years of simulations, begin and end year of historical data
            
# stoch_years=1000;yearbeg=2005;yearend=2034;   #2005/01/01-2034/12/31        
stoch_years=1000;yearbeg=2035;yearend=2064;     #2035/01/01-2064/12/31



# =============================================================================
# # delete all the files for initialization
# DeleteFiles('Synthetic_streamflows')
# DeleteFiles('Synthetic_weather')
# DeleteFiles('Historical_weather_analysis')
# =============================================================================

# copy all the files required for synthetic simulation
CopyFiles('Copy to Synthetic_streamflows', 'Synthetic_streamflows')
CopyFiles('Copy to Historical_weather_analysis', 'Historical_weather_analysis')


# Run data_extract.py to extract data within a given range of time period
import data_extract
data_extract.data_extracts(yearbeg,yearend)

# Run cal_cov.py to calculate the covariance and residuals of temperature and windspeed.
import cal_cov
cal_cov.cal_covs(yearbeg, yearend)

# %% Generate synthetic weather (wind speed and temperature) records. 
import synthetic_temp_wind
starttime = time.time()
print('synth weather: will be running for about {} seconds'.format(185/1000*stoch_years))
synthetic_temp_wind.synthetic(stoch_years,yearbeg,yearend)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed))

# %% Generate synthetic streamflow records 
import synthetic_streamflow
starttime = time.time()
print('streamflows: will be running for about {} seconds'.format(213/1000*stoch_years))
synthetic_streamflow.synthetic(stoch_years,1901,yearbeg,yearend)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed))

# %% caculating correlation matrix
import cal_cor_mat
cor_mat=cal_cor_mat.cal_cor_mats(stoch_years, yearbeg, yearend)

# %% save matrix into files
# creating directory
import os
# define the name of the directory to be created
Cpath = "Correlation matrix/"
if not os.path.exists(Cpath):
    os.makedirs(Cpath) 
    
# save data
import pickle
sim_years2=stoch_years+3; # three more years of data are required
filename=Cpath+"cor_mat_{}-{}_{}.pkl".format(yearbeg, yearend, sim_years2)
with open(filename, 'wb') as output:
    pickle.dump(cor_mat, output, pickle.HIGHEST_PROTOCOL)

# copy the module cal_cor_mat into the same folder of matrix files
    # this module or file is required to load the pkl files.
import shutil  
dest = shutil.copyfile('cal_cor_mat.py', Cpath+'cal_cor_mat.py')

# %% visualization
stoch_years=1000;yearbeg=2005;yearend=2034;   #2005/01/01-2034/12/31        
# stoch_years=1000;yearbeg=2035;yearend=2064;     #2035/01/01-2064/12/31
sim_years2=stoch_years+3; # three more years of data are required

Cpath = "Correlation matrix/"
Cpath_fig=Cpath+'{}-{}_{}/'.format(yearbeg, yearend, sim_years2)
import os
if not os.path.exists(Cpath_fig):
    os.makedirs(Cpath_fig)    

import pandas as pd
# 
cor_mat1=pd.read_pickle(Cpath+"cor_mat_{}-{}_{}.pkl".format(yearbeg, yearend, sim_years2))
cor_mat2=pd.read_pickle(Cpath+"cor_mat_{}-{}_{}.pkl".format(2035, 2064, sim_years2))

import visualization as visu
plt1=visu.sub_fig1(cor_mat1.C_wea_irr_obs,cor_mat1.C_wea_irr_sim,'{}-{} (wea_irr)'.format(yearbeg, yearend))

plt1.savefig(Cpath_fig+'C_wea_irr_{}.png'.format(cor_mat1.C_wea_irr_obs.shape[1]),dpi=1000,bbox_inches='tight')
plt1.show()

plt1=visu.sub_fig2(cor_mat1.C_wea_irr_obs,cor_mat1.C_wea_irr_sim,'Sim-Obs (wea_irr): {}-{}'.format(yearbeg, yearend))
plt1.savefig(Cpath_fig+'dC_wea_irr_{}.png'.format(cor_mat1.C_wea_irr_obs.shape[1]),dpi=1000,bbox_inches='tight')
plt1.show()

plt2=visu.sub_fig1(cor_mat1.C_strs_obs,cor_mat1.C_strs_sim,'{}-{} (str)'.format(yearbeg, yearend))
plt2.savefig(Cpath_fig+'C_strs_{}.png'.format(cor_mat1.C_strs_obs.shape[1]),dpi=1000,bbox_inches='tight')
plt2.show()

plt2=visu.sub_fig2(cor_mat1.C_strs_obs,cor_mat1.C_strs_sim,'Sim-Obs (str): {}-{}'.format(yearbeg, yearend))
plt2.savefig(Cpath_fig+'dC_strs_{}.png'.format(cor_mat1.C_strs_obs.shape[1]),dpi=1000,bbox_inches='tight')
plt2.show()

# % comparison between cor_mat in current and future stage
plt3=visu.sub_fig1(cor_mat2.C_wea_irr_obs-cor_mat1.C_wea_irr_obs,cor_mat2.C_wea_irr_sim-cor_mat1.C_wea_irr_sim,'Difference (wea_irr): 2035-2064 ~ {}-{}'.format(yearbeg, yearend))
plt3.savefig(Cpath_fig+'period_dc_wea_irr_{}.png'.format(cor_mat2.C_wea_irr_obs.shape[1]),dpi=1000,bbox_inches='tight')
plt3.show()

plt3=visu.sub_fig1(cor_mat2.C_strs_obs-cor_mat1.C_strs_obs,cor_mat2.C_strs_sim-cor_mat1.C_strs_sim,'Difference (str): 2035-2064 ~ {}-{}'.format(yearbeg, yearend))
plt3.savefig(Cpath_fig+'period_dc_strs_{}.png'.format(cor_mat2.C_wea_irr_obs.shape[1]),dpi=1000,bbox_inches='tight')
plt3.show()


# %% 
a=0;
