# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 12:40:20 2019

@author: YSu
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 21:23:20 2018

@author: jdkern
"""

from __future__ import division
from statsmodels.tsa.api import VAR
import statsmodels.tsa.vector_ar.var_model as var_model
import pandas as pd
import numpy as np
from copy import deepcopy

#def synthetic(sim_years):
#########################################################################
# This purpose of this script is to use daily temperature and wind profiles, and 
# a covariance matrix that describes statistical dependencies
# in daily temperature and wind speeds across the 17 National 
# Climatic Data Center GHN monitoring stations, to creat synthetic records of
# temperature and wind speed at each station.

# a vector autoregressive model is used to produce cross-correlated residuals 
# and these are layered on top of average daily profiles to arrive at new
# synthetic records
#########################################################################

# need to generate 2 additional years of data (FCRPS model will cut first 
# and last)
sim_years = 50

# read historical time series of daily wind and temperature residuals and 
# covariance matrix
Residuals=pd.read_csv('Historical_weather_analysis/WIND_TEMP_res.csv')
Covariance=pd.read_csv('Historical_weather_analysis/Covariance_Calculation.csv')

# pull residual data and convert to numerical form
R = Residuals.loc[:,'SALEM_T':].values

# there are a few remaining NaNs. We just set those to zero.
for i in np.argwhere(np.isnan(R)):
    R[i]=0
    
# establish vector-autoregressive (VAR) model for residuals. Optimal lag was
# found via AIC to be 1
model = VAR(R)
results = model.fit(1)

# coefficients of VAR model estimated via least squares regression
p = results.params

# use the last values recorded from the historical record as
# "seeds" (first values) for the VAR model
y_seeds = R[-1]


#Add 5 to shift the entire distribution and take log
R=np.log(R+5)
# pull covariance data out and convert to numerical form
C=np.cov(np.transpose(R))

# average temperature and wind speed profiles
Ave=pd.read_csv('Historical_weather_analysis/WIND_TEMP_ave.csv',header =0)
Ave_TW = Ave.loc[0:364,'SALEM_T':].values

# records of standard deviation for each calender day
Std=pd.read_csv('Historical_weather_analysis/WIND_TEMP_std.csv',header =0)
Std_TW = Std.loc[0:364,'SALEM_T':].values

#T_res=pd.read_csv('Temp_res.csv')
T_ave=pd.read_csv('Temp_ave.csv',header=0)
Ave_T = T_ave.loc[0:364,'SALEM_T':].values
T_std=pd.read_csv('Temp_Std.csv',header=0)
Std_T = T_std.loc[0:364,'SALEM_T':].values


# number of simulation days
sim_days=sim_years*365

# number of fields (Temps, Wind) to calculate -- two for each station
fields = len(C)

# a row of random normal samples
E_term=np.mean(R,axis=0)

# a row of random normal samples for each day of the simulation period
E  = np.random.multivariate_normal(E_term.tolist(),C,sim_days)

E= np.exp(E)-5

# placeholder for simulated residuals
sim_residuals = np.zeros((sim_days,fields))

# calculate residuals for each day in the simulated record
for i in range(0,sim_days):
    
    # generate new residual
    for j in range(1,fields+1):
        name='y' + str(j)
        locals()[name] = p[0,j-1] + p[1,j-1]*y_seeds[0]+ p[2,j-1]*y_seeds[1]+ p[3,j-1]*y_seeds[2]+ p[4,j-1]*y_seeds[3]+ p[5,j-1]*y_seeds[4]+ p[6,j-1]*y_seeds[5]+ p[7,j-1]*y_seeds[6]+ p[8,j-1]*y_seeds[7]+ p[9,j-1]*y_seeds[8]+ p[10,j-1]*y_seeds[9]+ p[11,j-1]*y_seeds[10]+ p[12,j-1]*y_seeds[11]+ p[13,j-1]*y_seeds[12]+  p[14,j-1]*y_seeds[13]+ p[15,j-1]*y_seeds[14]+ p[16,j-1]*y_seeds[15]+ p[17,j-1]*y_seeds[16]+ p[18,j-1]*y_seeds[17]+ p[19,j-1]*y_seeds[18]+ p[20,j-1]*y_seeds[19]+ p[21,j-1]*y_seeds[20]+ p[22,j-1]*y_seeds[21]+ p[23,j-1]*y_seeds[22]+ p[24,j-1]*y_seeds[23]+ p[25,j-1]*y_seeds[24]+ p[26,j-1]*y_seeds[25]+ p[27,j-1]*y_seeds[26]+ p[28,j-1]*y_seeds[27]+ p[29,j-1]*y_seeds[28]+ p[30,j-1]*y_seeds[29]+ p[31,j-1]*y_seeds[30]+ p[32,j-1]*y_seeds[31]+ p[33,j-1]*y_seeds[32]+ p[34,j-1]*y_seeds[33] +E[i,j-1]
    
    # pass new residual to the next day as a "seed"
    for j in range(1,fields+1):
        name='y' + str(j)
        y_seeds[j-1]=locals()[name]
    
    # simulated residuals
    for j in range(1,fields+1):
        name='y' + str(j)
        sim_residuals[i,j-1] = locals()[name]
        
################################################
# The next step is to simulate each field using the residuals simulated above
# and average profiles

# synthetic weather as sum of residuals and average profiles, re-seasoned
sim_weather=np.zeros((sim_days,fields))
n=0

# for each simulated day
for i in range(0,sim_days):
    for j in range(0,fields):
        if j in range(1,34,2):
        # adjust simulated residuals so they're unit (=1) standard deviation, re-season, and add back 
        # mean profile
            sim_weather[i,j]=(sim_residuals[i,j]*(1/np.std(sim_residuals[:,j]))*Std_TW[n,j]) +Ave_TW[n,j]
        else:
            sim_weather[i,j]=(sim_residuals[i,j]*(1/np.std(sim_residuals[:,j]))*Std_T[n,j]) +Ave_T[n,j]
        
        #impose logical constraints on wind speeds
        if j%2==0:
            pass
        else:
            sim_weather[i,j] = np.max((sim_weather[i,j],0))
    n=n+1
    if n >= 365:
        n=0
        
        
# check for any NaN values
############################################################################
#New_Temp_Model
#################################################################################
#    T_res=pd.read_csv('Temp_res.csv')
#    T_ave=pd.read_csv('Temp_ave.csv')
#    T_std=pd.read_csv('Temp_Std.csv')
#    
#    R = T_res.loc[:,'SALEM_T':].values
#    Cov=np.cov(R,rowvar=0)
#    
#    # found via AIC to be 1
#    model = VAR(R)
#    results = model.fit(1)
#    
#    # coefficients of VAR model estimated via least squares regression
#    p = results.params
#    y_seeds = deepcopy(R[-1])
#    
#    C=Cov
#     # number of simulation days
#    sim_days=sim_years*365
#    
#    # number of fields (Temps, Wind) to calculate -- two for each station
#    fields = len(C)
#    
#    # a row of random normal samples
#    E_term=np.mean(R,axis=0)
#    
#    # a row of random normal samples for each day of the simulation period
#    E  = np.random.multivariate_normal(np.zeros(17),C,sim_days)
#    
#    sim_residuals = np.zeros((sim_days,fields))
#
#    for i in range(0,sim_days):
#        
#
#        # generate new residual
#        for j in range(1,fields+1):
#            
#            y = p[0,j-1] + p[1,j-1]*y_seeds[0]+ p[2,j-1]*y_seeds[1]+ p[3,j-1]*y_seeds[2]+ p[4,j-1]*y_seeds[3] + E[i,j-1]+ p[5,j-1]*y_seeds[4]+ p[6,j-1]*y_seeds[5]+ p[7,j-1]*y_seeds[6]+ p[8,j-1]*y_seeds[7]+ p[9,j-1]*y_seeds[8]+ p[10,j-1]*y_seeds[9]+ p[11,j-1]*y_seeds[10]+ p[12,j-1]*y_seeds[11]+ p[13,j-1]*y_seeds[12]+  p[14,j-1]*y_seeds[13]+ p[15,j-1]*y_seeds[14]+ p[16,j-1]*y_seeds[15]+ p[17,j-1]* y_seeds[16] + E[i,j-1]
#        
#        # pass new residual to the next day as a "seed"
#     
#       
#            y_seeds[j-1]=y
#        
#        # simulated residuals
#
#            sim_residuals[i,j-1] = y
#    
#    
#    
#    
#    
#    





#convert to dataframe, send to csv        
H = list(Residuals)
headers = H[1:]        
df_sim = pd.DataFrame(sim_weather)
df_sim.columns = headers    
df_sim.to_csv('Synthetic_weather/synthetic_weather_data.csv')

#    return None


