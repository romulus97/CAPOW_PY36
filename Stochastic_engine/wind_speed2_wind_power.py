# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 01:01:40
 2018

@author: jdkern
"""

from __future__ import division
from sklearn import linear_model
from statsmodels.tsa.api import VAR
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

########################################################
# This script uses historical records of hourly wind power
# production in both the BPA and CAISO zones, as well as 
# synthetic records of average daily wind speeds, to create
# new synthetic records of hourly wind power production in the CAISO
# and PNW zones (PNW includes BPA and other BAs. CAISO wind power production is
# disaggregated into values
# for each sub-zone (PG&E, SCE, SDGE in a separate script)
########################################################

def wind_sim(sim_years, PNW_cap, CAISO_cap):
    
    sim_years = sim_years+3
    
    # First do analysis of historical wind power production data
    
    #load historical renewable energy production data
    df_BPA = pd.read_excel('Synthetic_wind_power/renewables_2011_2017.xlsx',sheetname='BPA',header=0)
    df_CAISO = pd.read_excel('Synthetic_wind_power/renewables_2011_2017.xlsx',sheetname='CAISO',header=0)
    
    BPA = df_BPA.values
    CAISO = df_CAISO.loc[:,'wind'].values
    
    # form a single matrix, and select only 2013-2017 data
    data = np.column_stack((BPA,CAISO))
    df_data = pd.DataFrame(data[17520:,:])
    sites = ['BPA','CAISO']
    years = range(2013,2018)
    df_data.columns = ['Month','Day','Year','Hour','BPA','CAISO']
    
    #convert hourly data to capacity factor by dividing by installed capacity
    df_cap = pd.read_excel('Synthetic_wind_power/cap_by_month.xlsx',sheetname='wind',header=0)
    cf = np.zeros((len(df_data),2))
    
    for i in range(0,len(df_data)):
        m = df_data.loc[i,'Month']
        y = df_data.loc[i,'Year']
        
        CAISOcap = df_cap.loc[(df_cap['Month']==m) & (df_cap['Year']==y),'CAISO']
        BPAcap = df_cap.loc[(df_cap['Month']==m) & (df_cap['Year']==y),'BPA']
        
        cf[i,0] = df_data.loc[i,'BPA']/BPAcap
        cf[i,1] = df_data.loc[i,'CAISO']/CAISOcap
        
    data = np.column_stack((BPA[17520:,0:4],cf))
    df_data = pd.DataFrame(data)
    df_data.columns = ['Month','Day','Year','Hour','BPA','CAISO']
    
    # arrange hourly data by site into 24-hr fraction profiles, corresponding daily sums (max daily value is 24, min is 0)
    days = int(len(data)/24)
    num_years = len(years)
    BPA_M = np.reshape(cf[:,0],(days,24))
    CAISO_M = np.reshape(cf[:,1],(days,24))
    
    BPA_f = np.zeros((365,24,num_years))
    CAISO_f = np.zeros((365,24,num_years))
    BPA_daily = np.zeros((365,num_years))
    CAISO_daily = np.zeros((365,num_years))
    
    
    for y in range(0,num_years):
        for i in range(0,365):
            
            BPA_f[i,:,y] = BPA_M[y*365+i,:]/np.sum(BPA_M[y*365+i,:])
            CAISO_f[i,:,y] = CAISO_M[y*365+i,:]/np.sum(CAISO_M[y*365+i,:])
            BPA_daily[i,y] = np.sum(BPA_M[y*365+i,:])
            CAISO_daily[i,y] = np.sum(CAISO_M[y*365+i,:])
            
            
    # Create regression models for predicting daily wind power production as a function of 
    # average daily wind speeds 
            
    # load records of daily summed capacity factors (max daily value is 24, min is 0)
    # alongside contemporaneous records of average daily wind speeds at selected
    # meteorological stations
    df_data = pd.read_excel('Synthetic_wind_power/power_speed_daily.xlsx',sheetname='Sheet1',header=0)
    
    # separate data by month
    jan2 = df_data.loc[df_data['Month'] == 1,:]
    feb2 = df_data.loc[df_data['Month'] == 2,:]
    mar2 = df_data.loc[df_data['Month'] == 3,:]
    apr2 = df_data.loc[df_data['Month'] == 4,:]
    may2 = df_data.loc[df_data['Month'] == 5,:]
    jun2 = df_data.loc[df_data['Month'] == 6,:]
    jul2 = df_data.loc[df_data['Month'] == 7,:]
    aug2 = df_data.loc[df_data['Month'] == 8,:]
    sep2 = df_data.loc[df_data['Month'] == 9,:]
    oct2 = df_data.loc[df_data['Month'] == 10,:]
    nov2 = df_data.loc[df_data['Month'] == 11,:]
    dec2 = df_data.loc[df_data['Month'] == 12,:] 
    
    systems = ['BPA','CAISO']
    predicted = np.zeros((len(df_data),2))
    residuals = np.zeros((len(df_data),2))
    
    #load synthetic wind speed data
        
    #pull relevant fields (not all meteorological stations are used in regressions)
    S = list(df_data)
    fields = S[5:]
    
    df_sim = pd.read_csv('Synthetic_weather/synthetic_weather_data.csv',header=0)
    df_sim = df_sim[fields]
    
    # add calender to synthetic weather data
    calender = pd.read_excel('Synthetic_wind_power/calender.xlsx',header=0)
    for i in range(0,sim_years):
        if i < 1:
            m = calender.loc[:,'Month']
            m = m[:,None]
            d = calender.loc[:,'Day']
            d = d[:,None]
            months = m
            days = d
        else:
            months = np.vstack((months,m))
            days = np.vstack((days,d))
    
    df_sim.loc[:,'Month'] = months
    df_sim.loc[:,'Day'] = days
    
    predicted_sim = np.zeros((len(df_sim),2))
    
    # for each zone, create a separate regression to predict wind power 
    # production as a function of wind speeds
    for sy in systems:
        
        #daily summed totals
        y = df_data.loc[:,sy]
        
        s_index = systems.index(sy)
          
        #multivariate regressions
        jan_reg = linear_model.LinearRegression()
        feb_reg = linear_model.LinearRegression()
        mar_reg = linear_model.LinearRegression()
        apr_reg = linear_model.LinearRegression()
        may_reg = linear_model.LinearRegression()
        jun_reg = linear_model.LinearRegression()
        jul_reg = linear_model.LinearRegression()
        aug_reg = linear_model.LinearRegression()
        sep_reg = linear_model.LinearRegression()
        oct_reg = linear_model.LinearRegression()
        nov_reg = linear_model.LinearRegression()
        dec_reg = linear_model.LinearRegression()
        
        # Train the models using the training sets
        jan_reg.fit(jan2.loc[:,'SALEM_W':],jan2.loc[:,sy])
        feb_reg.fit(feb2.loc[:,'SALEM_W':],feb2.loc[:,sy])
        mar_reg.fit(mar2.loc[:,'SALEM_W':],mar2.loc[:,sy])
        apr_reg.fit(apr2.loc[:,'SALEM_W':],apr2.loc[:,sy])
        may_reg.fit(may2.loc[:,'SALEM_W':],may2.loc[:,sy])
        jun_reg.fit(jun2.loc[:,'SALEM_W':],jun2.loc[:,sy])
        jul_reg.fit(jul2.loc[:,'SALEM_W':],jul2.loc[:,sy])
        aug_reg.fit(aug2.loc[:,'SALEM_W':],aug2.loc[:,sy])
        sep_reg.fit(sep2.loc[:,'SALEM_W':],sep2.loc[:,sy])
        oct_reg.fit(oct2.loc[:,'SALEM_W':],oct2.loc[:,sy])
        nov_reg.fit(nov2.loc[:,'SALEM_W':],nov2.loc[:,sy])
        dec_reg.fit(dec2.loc[:,'SALEM_W':],dec2.loc[:,sy])
        
        # Number of wind data stations
        H = jan2.loc[:,'SALEM_W':]
        rc = np.shape(H)
        n = rc[1]
        
        # Make predictions using the training set    
        for i in range(0,len(y)):
            
            m = df_data.loc[i,'Month']
            
            if m==1:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = jan_reg.predict(s)
                predicted[i,s_index] = p
            elif m==2:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = feb_reg.predict(s)
                predicted[i,s_index] = p
            elif m==3:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = mar_reg.predict(s)
                predicted[i,s_index] = p
            elif m==4:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = apr_reg.predict(s)
                predicted[i,s_index] = p
            elif m==5:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = may_reg.predict(s)
                predicted[i,s_index] = p
            elif m==6:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = jun_reg.predict(s)
                predicted[i,s_index] = p
            elif m==7:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = jul_reg.predict(s)
                predicted[i,s_index] = p
            elif m==8:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = aug_reg.predict(s)
                predicted[i,s_index] = p
            elif m==9:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = sep_reg.predict(s)
                predicted[i,s_index] = p
            elif m==10:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = oct_reg.predict(s)
                predicted[i,s_index] = p
            elif m==11:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = nov_reg.predict(s)
                predicted[i,s_index] = p
            else:
                s = df_data.loc[i,'SALEM_W':] 
                s = np.reshape(s[:,None],(1,n))
                p = dec_reg.predict(s)
                predicted[i,s_index] = p
        
        # Residuals
        residuals[:,s_index] = predicted[:,s_index] - y.values
               
    #    #R2
    #    a=st.pearsonr(y,predicted[:,s_index])
    #    print a[0]**2
        
    #####################################################################
    # Now use synthetic wind speed data in the same regressions to predict
    # daily wind power production
                            
        # Make predictions using the training set    
        for i in range(0,len(df_sim)):
            
            m = df_sim.loc[i,'Month']
            
            if m==1:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = jan_reg.predict(s)
                predicted_sim[i,s_index] = p
            elif m==2:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = feb_reg.predict(s)
                predicted_sim[i,s_index] = p
            elif m==3:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = mar_reg.predict(s)
                predicted_sim[i,s_index] = p
            elif m==4:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = apr_reg.predict(s)
                predicted_sim[i,s_index] = p
            elif m==5:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = may_reg.predict(s)
                predicted_sim[i,s_index] = p
            elif m==6:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = jun_reg.predict(s)
                predicted_sim[i,s_index] = p
            elif m==7:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = jul_reg.predict(s)
                predicted_sim[i,s_index] = p
            elif m==8:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = aug_reg.predict(s)
                predicted_sim[i,s_index] = p
            elif m==9:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = sep_reg.predict(s)
                predicted_sim[i,s_index] = p
            elif m==10:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = oct_reg.predict(s)
                predicted_sim[i,s_index] = p
            elif m==11:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = nov_reg.predict(s)
                predicted_sim[i,s_index] = p
            else:
                s = df_sim.loc[i,'SALEM_W':'PASCO_W'] 
                s = np.reshape(s[:,None],(1,n))
                p = dec_reg.predict(s)
                predicted_sim[i,s_index] = p
    
    
    #####################################################################
    #                       Residual Analysis
    #####################################################################
    
    # residuals values in wind power production are correlated across the 
    # two zones. We use a VAR model to capture this.
        
    R = residuals
    rc = np.shape(R)
    cols = rc[1]
    mus = np.zeros((cols,1))
    stds = np.zeros((cols,1))
    R_w = np.zeros(np.shape(R))
    
    for i in range(0,cols):
        mus[i] = np.mean(R[:,i])
        stds[i] = np.std(R[:,i])
        R_w[:,i] = (R[:,i] - mus[i])/stds[i]
    
    model = VAR(R_w)
    results = model.fit(1)
    sim_days = sim_years*365
    sim_residuals = np.zeros((sim_days,cols))
    errors = np.zeros((sim_days,cols))
    p = results.params
    y_seeds = R_w[-1]
    C = results.sigma_u
    E  = np.random.multivariate_normal([0,0],C,sim_days)
    
    for i in range(0,sim_days):
        
        y1 = p[0,0] + p[1,0]*y_seeds[0] + p[2,0]*y_seeds[1] + E[i,0]
        y2 = p[0,1] + p[1,1]*y_seeds[0] + p[2,1]*y_seeds[1] + E[i,1]
        
        y_seeds[0] = y1
        y_seeds[1] = y2
        
        sim_residuals[i,:] = [y1,y2]
    
    
    for i in range(0,cols):
        sim_residuals[:,i] = sim_residuals[:,i]*stds[i]*(1/np.std(sim_residuals[:,i])) + mus[i]
    
    # combine residuals with output from regression
    combined_BPA = sim_residuals[:,0] + predicted_sim[:,0]
    combined_CAISO = sim_residuals[:,1] + predicted_sim[:,1]
    
    #impose minimum and maximum CFs
    for i in range(0,len(combined_BPA)):
        if combined_BPA[i] < np.min(df_data.loc[:,'BPA']):
            combined_BPA[i] = np.min(df_data.loc[:,'BPA'])
        elif combined_BPA[i] > np.max(df_data.loc[:,'BPA']):
            combined_BPA[i] = np.max(df_data.loc[:,'BPA'])
        
        if combined_CAISO[i] < np.min(df_data.loc[:,'CAISO']):
            combined_CAISO[i] = np.min(df_data.loc[:,'CAISO'])
        elif combined_CAISO[i] > np.max(df_data.loc[:,'CAISO']):
            combined_CAISO[i] = np.max(df_data.loc[:,'CAISO'])
    
    ############################################################################
    # Now we have to use the daily wind power production values (in daily summed 
    # capacity factors) to hourly values
            
    # rename
    total_BPA = combined_BPA
    total_CAISO = combined_CAISO
    
    
    #sample historical hourly profiles based on daily value and calendar day
    sim_hourly = np.zeros((8760*sim_years,2))
    
    #tolerance
    t = 0.01
    
    days = np.zeros((365,sim_years))
    years = np.zeros((365,sim_years))
    
    #match daily sum with hourly profile of historical day with similar date/production
    dif = []
    
    #BPA
    for i in range(0,sim_years):
        for j in range(0,365):
            target = total_BPA[i*365+j]
            s = 0
            tol = 100
            
            while (tol > t and s < 15):
                
                if j + s > 364:
                    up = j + s - 365
                else:
                    up = j + s
                
                if j - s < 0:
                    down = j - s + 365
                else:
                    down = j - s
                
                for k in range(0,num_years):
                    if np.abs(total_BPA[i*365+j] - BPA_daily[up,k]) < tol:
                        tol = np.abs(total_BPA[i*365+j] - BPA_daily[up,k])
                        day = up
                        year = k
                
                for k in range(0,num_years):
                    if np.abs(total_BPA[i*365+j] - BPA_daily[down,k]) < tol:
                        tol = np.abs(total_BPA[i*365+j] - BPA_daily[down,k])
                        day = down
                        year = k                    
                        
                s = s + 1
                
                days[j,i] = day
                years[j,i] = year
            
            #Use hourly profile and daily value to calculate hourly values
            sim_hourly[i*8760+j*24:i*8760+j*24+24,0] = BPA_f[day,:,year]*total_BPA[i*365+j]
            
            dif = np.append(dif,tol)
    
    # CAISO
    dif = []
    for i in range(0,sim_years):
        for j in range(0,365):
            target = total_CAISO[i*365+j]
            s = 0
            tol = 100
            
            while (tol > t and s < 15):
                
                if j + s > 364:
                    up = j + s - 365
                else:
                    up = j + s
                
                if j - s < 0:
                    down = j - s + 365
                else:
                    down = j - s
                
                for k in range(0,num_years):
                    if np.abs(total_CAISO[i*365+j] - CAISO_daily[up,k]) < tol:
                        tol = np.abs(total_CAISO[i*365+j] - CAISO_daily[up,k])
                        day = up
                        year = k
                
                for k in range(0,num_years):
                    if np.abs(total_CAISO[i*365+j] - CAISO_daily[down,k]) < tol:
                        tol = np.abs(total_CAISO[i*365+j] - CAISO_daily[down,k])
                        day = down
                        year = k                    
                        
                s = s + 1
                
                days[j,i] = day
                years[j,i] = year
            
            #Use hourly profile and daily value to calculate hourly values
            sim_hourly[i*8760+j*24:i*8760+j*24+24,1] = CAISO_f[day,:,year]*total_CAISO[i*365+j]
            
            dif = np.append(dif,tol)
                  
    #system capacity
    BPA = PNW_cap*sim_hourly[:,0]
    CAISO = CAISO_cap*sim_hourly[:,1]
    
    #remove 1st and last year
    h = int(len(BPA))
    BPA = BPA[8760:h-2*8760]
    CAISO = CAISO[8760:h-2*8760]
    
    # BPA represents 90% of installed wind power capacity in PNW
    M = np.column_stack((BPA*.766,BPA,CAISO))
    df_M = pd.DataFrame(M)
    df_M.columns = ['BPA','PNW','CAISO']
    df_M.to_csv('Synthetic_wind_power/wind_power_sim.csv')
    
    return None
