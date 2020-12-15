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

def synthetic(sim_years,yearbeg,yearend):
    

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
    sim_years2= sim_years+3
    # read historical time series of daily wind and temperature residuals and 
    # covariance matrix
    Residuals=pd.read_csv('Historical_weather_analysis/WIND_TEMP_res_{}-{}.csv'.format(yearbeg, yearend))
    Covariance=pd.read_csv('Historical_weather_analysis/Covariance_Calculation_{}-{}.csv'.format(yearbeg, yearend))
    Solar_Residuals=pd.read_csv('Historical_weather_analysis/res_irr_{}-{}.csv'.format(yearbeg, yearend))
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
    
    
    #Add R_add to shift the entire distribution and take log
    R_temp=R; R_add=-np.floor(R.min());
    R=np.log(R+R_add)
    # pull covariance data out and convert to numerical form
    C=np.cov(np.transpose(R))
    
    # average temperature and wind speed profiles
    Ave=pd.read_csv('Historical_weather_analysis/WIND_TEMP_ave_{}-{}.csv'.format(yearbeg, yearend),header =0)
    Ave_TW = Ave.loc[0:364,'SALEM_T':].values
    
    # records of standard deviation for each calender day
    Std=pd.read_csv('Historical_weather_analysis/WIND_TEMP_std_{}-{}.csv'.format(yearbeg, yearend),header =0)
    Std_TW = Std.loc[0:364,'SALEM_T':].values
    
    #T_res=pd.read_csv('Temp_res.csv')
# =============================================================================
#     T_ave=pd.read_csv('Historical_weather_analysis/Temp_ave_{}-{}.csv'.format(yearbeg, yearend),header=0)
#     Ave_T = T_ave.loc[0:364,'SALEM_T':].values
#     T_std=pd.read_csv('Historical_weather_analysis/Temp_Std_{}-{}.csv'.format(yearbeg, yearend),header=0)
#     Std_T = T_std.loc[0:364,'SALEM_T':].values
#     T_res=pd.read_csv('Historical_weather_analysis/Temp_res_{}-{}.csv'.format(yearbeg, yearend))
# =============================================================================
    
    Solar_ave=pd.read_csv('Historical_weather_analysis/ave_irr_{}-{}.csv'.format(yearbeg, yearend))
    S_ave=Solar_ave.loc[:,'Site1':].values
    Solar_std=pd.read_csv('Historical_weather_analysis/std_irr_{}-{}.csv'.format(yearbeg, yearend))
    S_std=Solar_std.loc[:,'Site1':].values
    
    
    Clear_sky=pd.read_csv('Historical_weather_analysis/clear_sky_{}-{}.csv'.format(yearbeg, yearend),header=0,index_col=0)
    Clear_sky=Clear_sky.values
    # number of simulation days
    
    sim_days=sim_years2*365
    
    # number of fields (Temps, Wind) to calculate -- two for each station
    fields = len(C)
    
    # a row of random normal samples
    E_term=np.mean(R,axis=0)
    
    # a row of random normal samples for each day of the simulation period
    E  = np.random.multivariate_normal(E_term.tolist(),C,sim_days)
    
    E= np.exp(E)-R_add
    
    # placeholder for simulated residuals
    sim_residuals = np.zeros((sim_days,fields))
    
    # calculate residuals for each day in the simulated record
    for i in range(0,sim_days):
        
        # generate new residual
        for j in range(1,fields+1):
            name='y' + str(j)
            locals()[name] = p[0,j-1] + np.matmul(p[1:,j-1],y_seeds) + E[i,j-1]
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
    sim_weather=np.zeros((sim_days, Ave_TW.shape[1]))
      
    Std_TWs=np.tile(Std_TW, (int(sim_residuals.shape[0]/365),1))
    Ave_TWs=np.tile(Ave_TW, (int(sim_residuals.shape[0]/365),1))
    
    for j in range(0,Ave_TW.shape[1]):
        sim_weather[:,j]=(sim_residuals[:,j]*(1/np.std(sim_residuals[:,j]))*Std_TWs[:,j]) +Ave_TWs[:,j]
        if j%2==0:
            pass
        else:
            sim_weather[sim_weather[:,j]<0,j]=0  
        
    # n=0   
    # for each simulated day
    # for i in range(0,sim_days):
    #     for j in range(0,fields-7):

    #         sim_weather[i,j]=(sim_residuals[i,j]*(1/np.std(sim_residuals[:,j]))*Std_TW[n,j]) +Ave_TW[n,j]

    #         #impose logical constraints on wind speeds
    #         if j%2==0:
    #             pass
    #         else:
    #             sim_weather[i,j] = np.max((sim_weather[i,j],0))
    #     n=n+1
    #     if n >= 365:
    #         n=0
    sim_irr=np.zeros((sim_days,S_ave.shape[1]))
    
    S_stds=np.tile(S_std, (int(sim_residuals.shape[0]/365),1))
    S_aves=np.tile(S_ave, (int(sim_residuals.shape[0]/365),1))
    
    for j in range(0,S_ave.shape[1]):
        sim_irr[:,j]=(sim_residuals[:,j+Ave_TW.shape[1]]*(1/np.std(sim_residuals[:,j+Ave_TW.shape[1]]))*S_stds[:,j])+S_aves[:,j]
     
    # n=0
    # sim_irr=np.zeros((sim_days,7))
    # for i in range(0,sim_days):
    #     for j in range(0,7):
    #         sim_irr[i,j]=(sim_residuals[i,j+34]*(1/np.std(sim_residuals[:,j+34]))*S_std[n,j]) +S_ave[n,j]
    #     n=n+1
    #     if n >= 365:
    #         n=0
        
    # check for any NaN values
    
    sim_irr2=np.zeros((sim_days,S_ave.shape[1]))
    sim_irr[sim_irr<0]=0
    
    sim_irr2=np.tile(Clear_sky,(int(sim_irr.shape[0]/365),1))-sim_irr    
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
    
    df_sim2 = pd.DataFrame(sim_weather)
    df_sim2.columns = headers    
    df_sim2.to_csv('Synthetic_weather/synthetic_weather_data_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2))
    
    df_sim_irr=pd.DataFrame(sim_irr2)
    df_sim_irr.columns=headers2
    df_sim_irr.to_csv('Synthetic_weather/synthetic_irradiance_data_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2))
    

    return None


