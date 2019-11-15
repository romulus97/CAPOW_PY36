# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 12:40:20 2019

@author: YSu
"""

from __future__ import division
from statsmodels.tsa.api import VAR
import statsmodels.tsa.vector_ar.var_model as var_model
import pandas as pd
import numpy as np
import random
from copy import deepcopy

def synthetic(sim_years):
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
    sim_years = sim_years+3
    sim_years2= 2* sim_years
    # read historical time series of daily wind and temperature residuals and 
    # covariance matrix
    Residuals=pd.read_csv('Historical_weather_analysis/WIND_TEMP_res.csv')
    Covariance=pd.read_csv('Historical_weather_analysis/Covariance_Calculation.csv')
    
    Solar_Residuals=pd.read_csv('Historical_weather_analysis/res_irr.csv')
    Solar_R=Solar_Residuals.loc[:,'Site1':]
    # pull residual data and convert to numerical form
    R = Residuals.loc[:,'SALEM_T':].values
    
    R=np.column_stack((R,Solar_R))
    
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
    T_ave=pd.read_csv('Historical_weather_analysis/Temp_ave.csv',header=0)
    Ave_T = T_ave.loc[0:364,'SALEM_T':].values
    T_std=pd.read_csv('Historical_weather_analysis/Temp_Std.csv',header=0)
    Std_T = T_std.loc[0:364,'SALEM_T':].values
    T_res=pd.read_csv('Historical_weather_analysis/Temp_res.csv')
    
    Solar_ave=pd.read_csv('Historical_weather_analysis/ave_irr.csv')
    S_ave=Solar_ave.loc[:,'Site1':].values
    Solar_std=pd.read_csv('Historical_weather_analysis/std_irr.csv')
    S_std=Solar_std.loc[:,'Site1':].values
    
    
    Clear_sky=pd.read_csv('Historical_weather_analysis/clear_sky.csv',header=0,index_col=0)
    Clear_sky=Clear_sky.values
    # number of simulation days
    
    sim_days=sim_years2*365
    
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
            locals()[name] = p[0,j-1] + p[1,j-1]*y_seeds[0]+ p[2,j-1]*y_seeds[1]+ p[3,j-1]*y_seeds[2]+ p[4,j-1]*y_seeds[3]+ p[5,j-1]*y_seeds[4]+ p[6,j-1]*y_seeds[5]+ p[7,j-1]*y_seeds[6]+ p[8,j-1]*y_seeds[7]+ p[9,j-1]*y_seeds[8]+ p[10,j-1]*y_seeds[9]+ p[11,j-1]*y_seeds[10]+ p[12,j-1]*y_seeds[11]+ p[13,j-1]*y_seeds[12]+  p[14,j-1]*y_seeds[13]+ p[15,j-1]*y_seeds[14]+ p[16,j-1]*y_seeds[15]+ p[17,j-1]*y_seeds[16]+ p[18,j-1]*y_seeds[17]+ p[19,j-1]*y_seeds[18]+ p[20,j-1]*y_seeds[19]+ p[21,j-1]*y_seeds[20]+ p[22,j-1]*y_seeds[21]+ p[23,j-1]*y_seeds[22]+ p[24,j-1]*y_seeds[23]+ p[25,j-1]*y_seeds[24]+ p[26,j-1]*y_seeds[25]+ p[27,j-1]*y_seeds[26]+ p[28,j-1]*y_seeds[27]+ p[29,j-1]*y_seeds[28]+ p[30,j-1]*y_seeds[29]+ p[31,j-1]*y_seeds[30]+ p[32,j-1]*y_seeds[31]+ p[33,j-1]*y_seeds[32]+ p[34,j-1]*y_seeds[33] + p[35,j-1]*y_seeds[34]+ p[36,j-1]*y_seeds[35]+ p[37,j-1]*y_seeds[36]+ p[38,j-1]*y_seeds[37]+ p[39,j-1]*y_seeds[38]+ p[40,j-1]*y_seeds[39]+ p[41,j-1]*y_seeds[40]+ E[i,j-1]
        
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
    sim_weather=np.zeros((sim_days,fields-7))
    n=0
    
    # for each simulated day
    for i in range(0,sim_days):
        for j in range(0,fields-7):
            if j in range(1,34,2):
            # adjust simulated residuals so they're unit (=1) standard deviation, re-season, and add back 
            # mean profile
                sim_weather[i,j]=(sim_residuals[i,j]*(1/np.std(sim_residuals[:,j]))*Std_TW[n,j]) +Ave_TW[n,j]
            else:
                sim_weather[i,j]=(sim_residuals[i,j]*(1/np.std(sim_residuals[:,j]))*Std_T[n,int(j/2)]) +Ave_T[n,int(j/2)]
            
            #impose logical constraints on wind speeds
            if j%2==0:
                pass
            else:
                sim_weather[i,j] = np.max((sim_weather[i,j],0))
        n=n+1
        if n >= 365:
            n=0
    
    n=0
    sim_irr=np.zeros((sim_days,7))
    for i in range(0,sim_days):
        for j in range(0,7):
            sim_irr[i,j]=(sim_residuals[i,j+34]*(1/np.std(sim_residuals[:,j+34]))*S_std[n,j]) +S_ave[n,j]
        n=n+1
        if n >= 365:
            n=0
            
    # check for any NaN values
    ############################################################################
    #New_Temp_Model
    #################################################################################
    

    
    R = T_res.loc[:,'SALEM_T':].values
    Cov=np.cov(R,rowvar=0)
    
    # found via AIC to be 1
    model = VAR(R)
    results = model.fit(1)
    
    # coefficients of VAR model estimated via least squares regression
    p = results.params
    y_seeds = deepcopy(R[-1])
    
    C=Cov
     # number of simulation days
    sim_days=sim_years*365
    
    # number of fields (Temps, Wind) to calculate -- two for each station
    fields = len(C)
    
    # a row of random normal samples
    E_term=np.mean(R,axis=0)
    
    # a row of random normal samples for each day of the simulation period
    E  = np.random.multivariate_normal(np.zeros(17),C,sim_days)
    
    sim_residuals = np.zeros((sim_days,fields))
    
    for i in range(0,sim_days):
        
    
        # generate new residual
        for j in range(1,fields+1):
            
            y = p[0,j-1] + p[1,j-1]*y_seeds[0]+ p[2,j-1]*y_seeds[1]+ p[3,j-1]*y_seeds[2]+ p[4,j-1]*y_seeds[3] + E[i,j-1]+ p[5,j-1]*y_seeds[4]+ p[6,j-1]*y_seeds[5]+ p[7,j-1]*y_seeds[6]+ p[8,j-1]*y_seeds[7]+ p[9,j-1]*y_seeds[8]+ p[10,j-1]*y_seeds[9]+ p[11,j-1]*y_seeds[10]+ p[12,j-1]*y_seeds[11]+ p[13,j-1]*y_seeds[12]+  p[14,j-1]*y_seeds[13]+ p[15,j-1]*y_seeds[14]+ p[16,j-1]*y_seeds[15]+ p[17,j-1]* y_seeds[16] + E[i,j-1]
        
        # pass new residual to the next day as a "seed"
     
       
            y_seeds[j-1]=y
        
        # simulated residuals
    
            sim_residuals[i,j-1] = y
    
        
        
        
    sim_weather2=np.zeros((sim_days,34))
    n=0
    
    # for each simulated day
    for i in range(0,sim_days):
        for j in range(0,34):
            if j in range(1,34,2):
            # adjust simulated residuals so they're unit (=1) standard deviation, re-season, and add back 
            # mean profile
                sim_weather2[i,j]=sim_weather[i,j]
            else:
                sim_weather2[i,j]=(sim_residuals[i,int(j/2)]*(1/np.std(sim_residuals[:,int(j/2)]))*Std_T[n,int(j/2)]) +Ave_T[n,int(j/2)]
            
            #impose logical constraints on wind speeds
            if j%2==0:
                pass
            else:
                sim_weather2[i,j] = np.max((sim_weather2[i,j],0))
        n=n+1
        if n >= 365:
            n=0
            
################################################################################################################
#Find the best match between those 2 differnet synthetic sets
    New_T=sim_weather2[:,range(0,34,2)]
    Old_T=sim_weather[:,range(0,34,2)]
    
    New_T=np.reshape(New_T,(sim_years,17,365))
    Old_T=np.reshape(Old_T,(sim_years2,17,365))
    
    New_T_ave=np.mean(New_T,axis=1)
    Old_T_ave=np.mean(Old_T,axis=1)
    
    
    
    year_list=np.zeros(int(sim_years))
    Best_RMSE = np.inf
    CHECK=np.zeros((sim_years,sim_years2))
    
    for i in range(0,sim_years):
        for j in range(0,sim_years2):
            RMSE = (np.sum(np.abs(New_T_ave[i,:]-Old_T_ave[j,:])))
            CHECK[i,j]=RMSE
            if RMSE <= Best_RMSE:
                year_list[i] = j
                Best_RMSE=RMSE

            else:
                pass
        Best_RMSE = np.inf     
    K=np.argsort(CHECK)
    for i in range(0,sim_years):
        rand=random.randint(0,10)
        year_list[i]=K[i,rand]
################################################################################################################
#Orgnize data
    sim_weather3=np.zeros((sim_days,34))
    for i in range(0,sim_years):
        sim_weather3[i*365:i*365+365,range(0,34,2)]=sim_weather2[i*365:i*365+365,range(0,34,2)]
        sim_weather3[i*365:i*365+365,range(1,34,2)]=sim_weather[int(year_list[i])*365:int(year_list[i])*365+365,range(1,34,2)]
    
    
    sim_irr2=np.zeros((sim_days,7))
    sim_irr[sim_irr<0]=0
    for i in range(0,sim_years):
        sim_irr2[i*365:i*365+365,:]=Clear_sky-sim_irr[int(year_list[i])*365:int(year_list[i])*365+365,:]
    
    sim_irr2[sim_irr2<0]=0
#
    
    #convert to dataframe, send to csv        
    H = list(Residuals)
    headers = H[1:]  

    H2 = list(Solar_Residuals)
    headers2 = H2[1:]        
#    df_sim = pd.DataFrame(sim_weather)
#    df_sim.columns = headers    
#    df_sim.to_csv('Synthetic_weather/synthetic_weather_data_1.csv')
    
    df_sim2 = pd.DataFrame(sim_weather3)
    df_sim2.columns = headers    
    df_sim2.to_csv('Synthetic_weather/synthetic_weather_data.csv')
    
    df_sim_irr=pd.DataFrame(sim_irr2)
    df_sim_irr.columns=headers2
    df_sim_irr.to_csv('Synthetic_weather/synthetic_irradiance_data.csv')
    

    return None
    
    
