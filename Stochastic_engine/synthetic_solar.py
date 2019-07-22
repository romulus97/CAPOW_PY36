# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 11:30:56 2018

@author: jdkern
"""

from __future__ import division
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import scipy.stats as st
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

########################################################
# This script uses historical records of hourly solar power
# production to create new synthetic records of hourly solar power 
# production in each zone. CAISO solar power production is disaggregated 
# into values for each sub-zone (PG&E, SCE, SDGE in a separate script)
########################################################

def solar_sim(sim_years,cap):
    
    sim_years = sim_years+3
    
    # load historical solar power production
    df_CAISO = pd.read_excel('Synthetic_wind_power/renewables_2011_2017.xlsx',sheetname='CAISO',header=0)
    df_cap = pd.read_excel('Synthetic_wind_power/cap_by_month.xlsx',sheetname = 'solar',header=0)
    
    years = range(2011,2018)
    
    ## first standardize solar by installed capacity, yielding hourly capacity factors
    hours = len(df_CAISO)
    num_years = int(len(years))
    st_solar = np.zeros((hours,1))
    
    
    for i in years:
        
        year_index = years.index(i)
    
        for j in range(0,31):
            for k in range(0,24):
                
                st_solar[year_index*8760 +j*24+k] = df_CAISO.loc[year_index*8760 + j*24+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==1),'CAISO']
                st_solar[year_index*8760 +j*24+1416+k] = df_CAISO.loc[year_index*8760 + j*24+1416+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==3),'CAISO']
                st_solar[year_index*8760 +j*24+2880+k] = df_CAISO.loc[year_index*8760 + j*24+2880+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==5),'CAISO']
                st_solar[year_index*8760 +j*24+4344+k] = df_CAISO.loc[year_index*8760 + j*24+4344+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==7),'CAISO']
                st_solar[year_index*8760 +j*24+5088+k] = df_CAISO.loc[year_index*8760 + j*24+5088+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==8),'CAISO']
                st_solar[year_index*8760 +j*24+6552+k] = df_CAISO.loc[year_index*8760 + j*24+6552+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==10),'CAISO']
                st_solar[year_index*8760 +j*24+8016+k] = df_CAISO.loc[year_index*8760 + j*24+8016+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==12),'CAISO']
    
        for j in range(0,30):
            for k in range(0,24):
    
                st_solar[year_index*8760 +j*24+2160+k] = df_CAISO.loc[year_index*8760 + j*24+2160+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==4),'CAISO']
                st_solar[year_index*8760 +j*24+3624+k] = df_CAISO.loc[year_index*8760 + j*24+3624+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==6),'CAISO']
                st_solar[year_index*8760 +j*24+5832+k] = df_CAISO.loc[year_index*8760 + j*24+5832+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==9),'CAISO']
                st_solar[year_index*8760 +j*24+7296+k] = df_CAISO.loc[year_index*8760 + j*24+7296+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==11),'CAISO']
                
        for j in range(0,28):
            for k in range(0,24):
    
                st_solar[year_index*8760 +j*24+744+k] = df_CAISO.loc[year_index*8760 + j*24+744+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==2),'CAISO']
    
    #only take the last three years (2015-2017)
    st_recent = st_solar[35040:]
    
    #calculate daily summed capacity factors
    days = int(len(st_recent)/24)
    daily_sum = np.zeros((days,1))
    
    for i in range(0,days):
        daily_sum[i] = np.sum(st_recent[i*24:i*24+24])
    
    #find maximum daily summed capacity factor for each calender day across 3 years
    daily_max = np.zeros((365,1))
    
    for j in range(0,3):
        for i in range(0,365):
            daily_max[i] = np.max([daily_sum[j*365+i],daily_max[i]])
    
    #smooth (30-day moving average) the maximum daily summed capacity factor
    smoothed = np.zeros((365,1))
    lag =30
    max_extended = np.vstack((daily_max[-lag:],daily_max,daily_max[0:lag]))
    
    for i in range(0,365):
        smoothed[i] = np.mean(max_extended[i:i+lag*2])
    
    # adjust smoother daily maximum values to represent "clear sky" solar power production
    # for each calender day
    no_clouds = smoothed + .6
    no_clouds[0:145] = no_clouds[0:145] + .1
    no_clouds[75:150] = no_clouds[75:150] + .1
    no_clouds[270:290] = no_clouds[270:290] - .10
    no_clouds[290:] = no_clouds[290:] - .30
    
    
    # now create a time series of daily "losses" due to cloud effects
    num_years = 3
    daily_losses = np.zeros((days,1))
    for i in range(0,3):
        daily_losses[i*365:i*365+365] = no_clouds - daily_sum[i*365:i*365+365]
        
    for i in range(0,len(daily_losses)):
        if daily_losses[i]<0:
            daily_losses[i]=0
    
    # characterize daily losses by month
    jan = np.zeros((num_years*31,1))
    feb = np.zeros((num_years*28,1))
    mar = np.zeros((num_years*31,1))
    apr = np.zeros((num_years*30,1))
    may = np.zeros((num_years*31,1))
    jun = np.zeros((num_years*30,1))
    jul = np.zeros((num_years*31,1))
    aug = np.zeros((num_years*31,1))
    sep = np.zeros((num_years*30,1))
    oct = np.zeros((num_years*31,1))
    nov = np.zeros((num_years*30,1))
    dec = np.zeros((num_years*31,1))
    
    for y in range(0,3):
        jan[y*31:y*31+31] = daily_losses[y*365:y*365+31]
        feb[y*28:y*28+28] = daily_losses[y*365+31:y*365+59]
        mar[y*31:y*31+31] = daily_losses[y*365+59:y*365+90]
        apr[y*30:y*30+30] = daily_losses[y*365+90:y*365+120]
        may[y*31:y*31+31] = daily_losses[y*365+120:y*365+151]
        jun[y*30:y*30+30] = daily_losses[y*365+151:y*365+181]
        jul[y*31:y*31+31] = daily_losses[y*365+181:y*365+212]
        aug[y*31:y*31+31] = daily_losses[y*365+212:y*365+243]
        sep[y*30:y*30+30] = daily_losses[y*365+243:y*365+273]
        oct[y*31:y*31+31] = daily_losses[y*365+273:y*365+304]
        nov[y*30:y*30+30] = daily_losses[y*365+304:y*365+334]
        dec[y*31:y*31+31] = daily_losses[y*365+334:y*365+365]
        
    #whitened loss data by month
    w_losses = np.zeros((days,1))    
        
    for i in range(0,3):
        w_losses[i*365:i*365+31] = (daily_losses[i*365:i*365+31] - np.mean(jan))/np.std(jan)
        w_losses[i*365+31:i*365+59] = (daily_losses[i*365+31:i*365+59] - np.mean(feb))/np.std(feb)
        w_losses[i*365+59:i*365+90] = (daily_losses[i*365+59:i*365+90] - np.mean(mar))/np.std(mar)
        w_losses[i*365+90:i*365+120] = (daily_losses[i*365+90:i*365+120] - np.mean(apr))/np.std(apr)
        w_losses[i*365+120:i*365+151] = (daily_losses[i*365+120:i*365+151] - np.mean(may))/np.std(may)
        w_losses[i*365+151:i*365+181] = (daily_losses[i*365+151:i*365+181] - np.mean(jun))/np.std(jun)
        w_losses[i*365+181:i*365+212] = (daily_losses[i*365+181:i*365+212] - np.mean(jul))/np.std(jul)
        w_losses[i*365+212:i*365+243] = (daily_losses[i*365+212:i*365+243] - np.mean(aug))/np.std(aug)
        w_losses[i*365+243:i*365+273] = (daily_losses[i*365+243:i*365+273] - np.mean(sep))/np.std(sep)
        w_losses[i*365+273:i*365+304] = (daily_losses[i*365+273:i*365+304] - np.mean(oct))/np.std(oct)
        w_losses[i*365+304:i*365+334] = (daily_losses[i*365+304:i*365+334] - np.mean(nov))/np.std(nov)
        w_losses[i*365+334:i*365+365] = (daily_losses[i*365+334:i*365+365] - np.mean(dec))/np.std(dec)
        
    #add 2 to create a no-zero time series for statistical transformation
    w_losses = w_losses + 2
    
    #transform whitened, shifted losses to normal distribution 
    cdf_W = st.exponweib.cdf(w_losses, *st.exponweib.fit(w_losses, 1, 1, scale=2, loc=0))
    cdf_N = st.norm.ppf(cdf_W)
    transformed_data = cdf_N
             
    # model normalized daily losses using ARMA model 
    arma_model1 = ARIMA(transformed_data, order=(1,0,1))
    arma_fit1 = arma_model1.fit()
    ARMA_residuals = arma_fit1.resid
    
    #synthetic errors
    NT = 365*sim_years
    valuefeed = transformed_data[-1]
    errorfeed = ARMA_residuals[-1]
    Syn_residuals = np.random.normal(0,1,(NT,1))
    synvalue = []
    
    #simulate ARMA model
    for i in range(0,NT):
        
        a = arma_fit1.params[0] + valuefeed*arma_fit1.params[1] + errorfeed*arma_fit1.params[2] + Syn_residuals[i,0]
    
        valuefeed = a
        errorfeed = Syn_residuals[i]
        synvalue = np.append(synvalue,a)
        
    
    #adjust standard deviation
    synvalue = synvalue*(1/np.std(synvalue))
    
    #convert back to non-simgaussian
    new_N = st.norm.cdf(synvalue)
    new_WE = st.exponweib.ppf(new_N, *st.exponweib.fit(w_losses, 1, 1, scale=2, loc=0))
    new_ds = np.reshape(new_WE - 2,(NT,1))
    
    #add back monthly statistics
    sim_losses = np.zeros((NT,1))
    for i in range(0,sim_years):
        
        sim_losses[i*365:i*365+31] = (new_ds[i*365:i*365+31]*np.std(jan)) +np.mean(jan)
        sim_losses[i*365+31:i*365+59] = (new_ds[i*365+31:i*365+59]*np.std(feb)) +np.mean(feb)
        sim_losses[i*365+59:i*365+90] = (new_ds[i*365+59:i*365+90]*np.std(mar)) +np.mean(mar)
        sim_losses[i*365+90:i*365+120] = (new_ds[i*365+90:i*365+120]*np.std(apr)) +np.mean(apr)
        sim_losses[i*365+120:i*365+151] = (new_ds[i*365+120:i*365+151]*np.std(may)) +np.mean(may)
        sim_losses[i*365+151:i*365+181] = (new_ds[i*365+151:i*365+181]*np.std(jun)) +np.mean(jun)
        sim_losses[i*365+181:i*365+212] = (new_ds[i*365+181:i*365+212]*np.std(jul)) +np.mean(jul)
        sim_losses[i*365+212:i*365+243] = (new_ds[i*365+212:i*365+243]*np.std(aug)) +np.mean(aug)
        sim_losses[i*365+243:i*365+273] = (new_ds[i*365+243:i*365+273]*np.std(sep)) +np.mean(sep)
        sim_losses[i*365+273:i*365+304] = (new_ds[i*365+273:i*365+304]*np.std(oct)) +np.mean(oct)
        sim_losses[i*365+304:i*365+334] = (new_ds[i*365+304:i*365+334]*np.std(nov)) +np.mean(nov)
        sim_losses[i*365+334:i*365+365] = (new_ds[i*365+334:i*365+365]*np.std(dec)) +np.mean(dec)
        
    for i in range(0,len(sim_losses)):
        if sim_losses[i]<0:
            sim_losses[i] == 0
            
    # scalable sythetic daily solar
    sim_solar = np.zeros((NT,1))
    for i in range(0,sim_years):
        sim_solar[i*365:i*365+365] = no_clouds - sim_losses[i*365:i*365+365]
    
    #impose historical minimum    
    for i in range(0,len(sim_solar)):
        if sim_solar[i] < np.min(daily_sum):
            sim_solar[i] = np.min(daily_sum)
        
    #sample hourly loss patterns from historical record based on calender day
    sim_hourly = np.zeros((NT*24,1))
    
    daily = np.reshape(daily_sum,(3,365))
    daily = np.transpose(daily)
    
    #tolerance
    t = 0.01
    
    days = np.zeros((365,sim_years))
    years = np.zeros((365,sim_years))
    
    #match daily sum with hourly profile of historical day with similar date/production
    for i in range(0,sim_years):
        for j in range(0,365):
            target = sim_solar[i*365+j]
            s = 0
            tol = 100
            
            while (tol > t and s < 10):
                
                if j + s > 364:
                    up = j + s - 365
                else:
                    up = j + s
                
                if j - s < 0:
                    down = j - s + 365
                else:
                    down = j - s
                
                for k in range(0,3):
                    if np.abs(sim_solar[i*365+j] - daily[up,k]) < tol:
                        tol = np.abs(sim_solar[i*365+j] - daily[up,k])
                        day = up
                        year = k
                
                for k in range(0,3):
                    if np.abs(sim_solar[i*365+j] - daily[down,k]) < tol:
                        tol = np.abs(sim_solar[i*365+j] - daily[down,k])
                        day = down
                        year = k                    
                        
                s = s + 1
                
                days[j,i] = day
                years[j,i] = year
            
            sim_hourly[i*8760+j*24:i*8760+j*24+24] = st_recent[year*8760+day*24:year*8760+day*24+24]*(sim_solar[i*365+j]/daily[day,year])
    
    #impose maximum constraint
    for i in range(0,len(sim_hourly)):
       if sim_hourly[i] > 1:
           sim_hourly[i] = 1
           
    #multiply by installed capacity
    solar_sim = sim_hourly*cap
    
    h = int(len(solar_sim))
    solar_sim = solar_sim[8760:h-2*8760,:]
    S = pd.DataFrame(solar_sim)
    S.columns = ['CAISO']
    S.to_csv('Synthetic_solar_power/solar_power_sim.csv')
           
    return None
           
