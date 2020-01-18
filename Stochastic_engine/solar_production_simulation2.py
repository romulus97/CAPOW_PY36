# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:59:27 2019

@author: YSu
"""

import pandas as pd
import numpy as np
from sklearn import linear_model
from statsmodels.tsa.arima_model import ARMA
from datetime import datetime
from datetime import timedelta

def solar_sim(sim_years,cap):
    sim_years=sim_years+3
    df_CAISO = pd.read_excel('Synthetic_wind_power/renewables_2011_2017.xlsx',sheetname='CAISO',header=0)
    df_BPA = pd.read_excel('Synthetic_wind_power/renewables_2011_2017.xlsx',sheetname='BPA',header=0)
    df_cap = pd.read_excel('Synthetic_wind_power/cap_by_month.xlsx',sheetname = 'solar',header=0)
    
    years = range(2011,2018)
    
    ## first standardize solar by installed capacity, yielding hourly capacity factors
    hours = len(df_CAISO)
    num_years = int(len(years))
    st_solar = np.zeros((hours,2))
    
    
    for i in years:
        
        year_index = years.index(i)
    
        for j in range(0,31):
            for k in range(0,24):
                
                st_solar[year_index*8760 +j*24+k,0] = df_CAISO.loc[year_index*8760 + j*24+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==1),'CAISO']
                st_solar[year_index*8760 +j*24+1416+k,0] = df_CAISO.loc[year_index*8760 + j*24+1416+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==3),'CAISO']
                st_solar[year_index*8760 +j*24+2880+k,0] = df_CAISO.loc[year_index*8760 + j*24+2880+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==5),'CAISO']
                st_solar[year_index*8760 +j*24+4344+k,0] = df_CAISO.loc[year_index*8760 + j*24+4344+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==7),'CAISO']
                st_solar[year_index*8760 +j*24+5088+k,0] = df_CAISO.loc[year_index*8760 + j*24+5088+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==8),'CAISO']
                st_solar[year_index*8760 +j*24+6552+k,0] = df_CAISO.loc[year_index*8760 + j*24+6552+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==10),'CAISO']
                st_solar[year_index*8760 +j*24+8016+k,0] = df_CAISO.loc[year_index*8760 + j*24+8016+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==12),'CAISO']

                st_solar[year_index*8760 +j*24+k,1] = df_BPA.loc[year_index*8760 + j*24+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==1),'BPA']
                st_solar[year_index*8760 +j*24+1416+k,1] = df_BPA.loc[year_index*8760 + j*24+1416+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==3),'BPA']
                st_solar[year_index*8760 +j*24+2880+k,1] = df_BPA.loc[year_index*8760 + j*24+2880+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==5),'BPA']
                st_solar[year_index*8760 +j*24+4344+k,1] = df_BPA.loc[year_index*8760 + j*24+4344+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==7),'BPA']
                st_solar[year_index*8760 +j*24+5088+k,1] = df_BPA.loc[year_index*8760 + j*24+5088+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==8),'BPA']
                st_solar[year_index*8760 +j*24+6552+k,1] = df_BPA.loc[year_index*8760 + j*24+6552+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==10),'BPA']
                st_solar[year_index*8760 +j*24+8016+k,1] = df_BPA.loc[year_index*8760 + j*24+8016+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==12),'BPA']
    
        for j in range(0,30):
            for k in range(0,24):
    
                st_solar[year_index*8760 +j*24+2160+k,0] = df_CAISO.loc[year_index*8760 + j*24+2160+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==4),'CAISO']
                st_solar[year_index*8760 +j*24+3624+k,0] = df_CAISO.loc[year_index*8760 + j*24+3624+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==6),'CAISO']
                st_solar[year_index*8760 +j*24+5832+k,0] = df_CAISO.loc[year_index*8760 + j*24+5832+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==9),'CAISO']
                st_solar[year_index*8760 +j*24+7296+k,0] = df_CAISO.loc[year_index*8760 + j*24+7296+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==11),'CAISO']

                st_solar[year_index*8760 +j*24+2160+k,1] = df_BPA.loc[year_index*8760 + j*24+2160+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==4),'BPA']
                st_solar[year_index*8760 +j*24+3624+k,1] = df_BPA.loc[year_index*8760 + j*24+3624+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==6),'BPA']
                st_solar[year_index*8760 +j*24+5832+k,1] = df_BPA.loc[year_index*8760 + j*24+5832+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==9),'BPA']
                st_solar[year_index*8760 +j*24+7296+k,1] = df_BPA.loc[year_index*8760 + j*24+7296+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==11),'BPA']
                
        for j in range(0,28):
            for k in range(0,24):
    
                st_solar[year_index*8760 +j*24+744+k,0] = df_CAISO.loc[year_index*8760 + j*24+744+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==2),'CAISO']
                st_solar[year_index*8760 +j*24+744+k,1] = df_BPA.loc[year_index*8760 + j*24+744+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==2),'BPA']
   
    st_solar=st_solar[35040:,:]
    daily_st_solar_CAISO=np.reshape(st_solar[:,0],(3*365,24))
    daily_st_solar_BPA=np.reshape(st_solar[:,1],(3*365,24))
    
    
    daily_st_solar_CAISO=np.sum(daily_st_solar_CAISO,axis=1)
    daily_st_solar_BPA = np.sum(daily_st_solar_BPA,axis=1)
    irrediance=pd.read_csv('Synthetic_solar_power/Solar_data_GHI_regress.csv',header=0)
    
    #CAISO simulation
    
    Normal_Starting=datetime(1900,1,1)
    
    datelist=pd.date_range(Normal_Starting,periods=365)
    count=0
    m=np.zeros(len(daily_st_solar_CAISO))
    for i in range(0,len(daily_st_solar_CAISO)):
        m[i]=int(datelist[count].month)
        count= count +1
        if count >364:
            count=0
    
    X=pd.DataFrame()
       
    X['Month']=m
    X['y']=daily_st_solar_CAISO
    X['1']=np.sum(np.reshape(irrediance['Site1'].values[35040:],(3*365,24)),axis=1)
    X['2']=np.sum(np.reshape(irrediance['Site2'].values[35040:],(3*365,24)),axis=1)
    X['3']=np.sum(np.reshape(irrediance['Site3'].values[35040:],(3*365,24)),axis=1)
    X['4']=np.sum(np.reshape(irrediance['Site4'].values[35040:],(3*365,24)),axis=1)
    X['5']=np.sum(np.reshape(irrediance['Site5'].values[35040:],(3*365,24)),axis=1)
    X['6']=np.sum(np.reshape(irrediance['Site6'].values[35040:],(3*365,24)),axis=1)
    X['7']=np.sum(np.reshape(irrediance['Site7'].values[35040:],(3*365,24)),axis=1)
    X['8']=np.sum(np.reshape(irrediance['Site8'].values[35040:],(3*365,24)),axis=1)
    X['9']=np.sum(np.reshape(irrediance['Site9'].values[35040:],(3*365,24)),axis=1)
    X['10']=np.sum(np.reshape(irrediance['Site10'].values[35040:],(3*365,24)),axis=1)
   
           
    
    for i in range(1,13):
        name='reg_' + str(i)
        data=X.loc[X['Month']==i]
        y=data['y']
        x=data.loc[:,'1':]
    #    y=np.log(y+1)
    #    x=np.log(x+1)
        locals()[name]=linear_model.LinearRegression(fit_intercept=False)
        locals()[name].fit(x,y)
#        print(locals()[name].score(x,y))
        
    Syn_irr=pd.read_csv('Synthetic_weather/synthetic_irradiance_data.csv',header=0,index_col=0)
    Syn_irr = Syn_irr.loc[0:365*sim_years-1,:]
    
    Normal_Starting=datetime(1900,1,1)
    
    datelist=pd.date_range(Normal_Starting,periods=365)
    count=0
    m=np.zeros(len(Syn_irr))
    for i in range(0,len(Syn_irr)):
        m[i]=int(datelist[count].month)
        count= count +1
        if count >364:
            count=0
    d_sim=np.column_stack((Syn_irr.values,m))   
    #
    ##Test the fit
    predicted = np.zeros(len(X))
    
    for i in range(0,len(X)):
        data=X.loc[i,:]
        Month=int(data['Month'])
        x_values=data['1':].values
        x_values = np.reshape(x_values,(1,10))
        reg_name='reg_' + str(Month)
        p=locals()[reg_name].predict(x_values)
        predicted[i]=p
    residules= predicted - X['y'].values
    

    predicted_sim=np.zeros(len(Syn_irr))
    for i in range(0,len(Syn_irr)):
        data=d_sim[i,:]
        Month=int(data[10])
        x_values=data[:10]
        x_values = np.reshape(x_values,(1,10))
        reg_name='reg_' + str(Month)
        p=locals()[reg_name].predict(x_values)
        predicted_sim[i]=p
    
    
    
    Model=ARMA(residules,order=(7,0))
    arma_fit1 = Model.fit()
    #ARMA_residuals = arma_fit1.resid
    
    
    y_seeds=residules[-7:]
    e=np.random.normal(np.mean(residules),np.std(residules),len(Syn_irr))
    

    
    p=arma_fit1.params
    
    res_sim=np.zeros(len(Syn_irr)+7)
    res_sim[0:7]=y_seeds
    for i in range(0,len(Syn_irr)):
        y=p[0]+p[1]*y_seeds[6]+ p[2]*y_seeds[5] + p[3]*y_seeds[4] + p[4]*y_seeds[3] +p[5]*y_seeds[2] + p[6]*y_seeds[1] + p[7]*y_seeds[0]+e[i]
        res_sim[i+7]=y
        y_seeds=res_sim[i:i+7]
        
        
        
    Solar=predicted_sim -e
    
    Solar[Solar<np.min(daily_st_solar_CAISO)]=np.min(daily_st_solar_CAISO)
    NT=int(sim_years*365)
    # scalable sythetic daily solar
    sim_solar = np.zeros((NT,1))
    
    sim_solar=Solar
    #impose historical minimum    
    
        
    #sample hourly loss patterns from historical record based on calender day
    sim_hourly = np.zeros((NT*24,1))
    
    daily = np.reshape(daily_st_solar_CAISO,(3,365))
    daily = np.transpose(daily)
    
    #tolerance
    t = 0.01
    
    days = np.zeros((365,int(sim_years)))
    years = np.zeros((365,int(sim_years)))
    
    #match daily sum with hourly profile of historical day with similar date/production
    for i in range(0,int(sim_years)):
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
            
            sim_hourly[i*8760+j*24:i*8760+j*24+24] = st_solar[year*8760+day*24:year*8760+day*24+24,0]*(sim_solar[i*365+j]/daily[day,year])
    
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
    
     #BPA simulation
    
    Normal_Starting=datetime(1900,1,1)
    
    datelist=pd.date_range(Normal_Starting,periods=365)
    count=0
    m=np.zeros(len(daily_st_solar_BPA))
    for i in range(0,len(daily_st_solar_BPA)):
        m[i]=int(datelist[count].month)
        count= count +1
        if count >364:
            count=0
    
    X=pd.DataFrame()
       
    X['Month']=m
    X['y']=daily_st_solar_BPA
    X['1']=np.sum(np.reshape(irrediance['Site1'].values[35040:],(3*365,24)),axis=1)
    X['2']=np.sum(np.reshape(irrediance['Site2'].values[35040:],(3*365,24)),axis=1)
    X['3']=np.sum(np.reshape(irrediance['Site3'].values[35040:],(3*365,24)),axis=1)
    X['4']=np.sum(np.reshape(irrediance['Site4'].values[35040:],(3*365,24)),axis=1)
    X['5']=np.sum(np.reshape(irrediance['Site5'].values[35040:],(3*365,24)),axis=1)
    X['6']=np.sum(np.reshape(irrediance['Site6'].values[35040:],(3*365,24)),axis=1)
    X['7']=np.sum(np.reshape(irrediance['Site7'].values[35040:],(3*365,24)),axis=1)
    X['8']=np.sum(np.reshape(irrediance['Site8'].values[35040:],(3*365,24)),axis=1)
    X['9']=np.sum(np.reshape(irrediance['Site9'].values[35040:],(3*365,24)),axis=1)
    X['10']=np.sum(np.reshape(irrediance['Site10'].values[35040:],(3*365,24)),axis=1)
   
           
    
    for i in range(1,13):
        name='reg_' + str(i)
        data=X.loc[X['Month']==i]
        y=data['y']
        x=data.loc[:,'1':]
    #    y=np.log(y+1)
    #    x=np.log(x+1)
        locals()[name]=linear_model.LinearRegression(fit_intercept=False)
        locals()[name].fit(x,y)
#        print(locals()[name].score(x,y))
        
    Syn_irr=pd.read_csv('Synthetic_weather/synthetic_irradiance_data.csv',header=0,index_col=0)
    Syn_irr = Syn_irr.loc[0:365*sim_years-1,:]
    
    Normal_Starting=datetime(1900,1,1)
    
    datelist=pd.date_range(Normal_Starting,periods=365)
    count=0
    m=np.zeros(len(Syn_irr))
    for i in range(0,len(Syn_irr)):
        m[i]=int(datelist[count].month)
        count= count +1
        if count >364:
            count=0
    d_sim=np.column_stack((Syn_irr.values,m))   
    #
    ##Test the fit
    predicted = np.zeros(len(X))
    
    for i in range(0,len(X)):
        data=X.loc[i,:]
        Month=int(data['Month'])
        x_values=data['1':].values
        x_values = np.reshape(x_values,(1,10))
        reg_name='reg_' + str(Month)
        p=locals()[reg_name].predict(x_values)
        predicted[i]=p
    residules= predicted - X['y'].values
    

    predicted_sim=np.zeros(len(Syn_irr))
    for i in range(0,len(Syn_irr)):
        data=d_sim[i,:]
        Month=int(data[10])
        x_values=data[:10]
        x_values = np.reshape(x_values,(1,10))
        reg_name='reg_' + str(Month)
        p=locals()[reg_name].predict(x_values)
        predicted_sim[i]=p
    
    
    
    Model=ARMA(residules,order=(7,0))
    arma_fit1 = Model.fit()
    #ARMA_residuals = arma_fit1.resid
    
    
    y_seeds=residules[-7:]
    e=np.random.normal(np.mean(residules),np.std(residules),len(Syn_irr))
    

    
    p=arma_fit1.params
    
    res_sim=np.zeros(len(Syn_irr)+7)
    res_sim[0:7]=y_seeds
    for i in range(0,len(Syn_irr)):
        y=p[0]+p[1]*y_seeds[6]+ p[2]*y_seeds[5] + p[3]*y_seeds[4] + p[4]*y_seeds[3] +p[5]*y_seeds[2] + p[6]*y_seeds[1] + p[7]*y_seeds[0]+e[i]
        res_sim[i+7]=y
        y_seeds=res_sim[i:i+7]
        
        
        
    Solar=predicted_sim -e
    
    Solar[Solar<np.min(daily_st_solar_BPA)]=np.min(daily_st_solar_BPA)
    NT=int(sim_years*365)
    # scalable sythetic daily solar
    sim_solar = np.zeros((NT,1))
    
    sim_solar=Solar
    #impose historical minimum    
    
        
    #sample hourly loss patterns from historical record based on calender day
    sim_hourly = np.zeros((NT*24,1))
    
    daily = np.reshape(daily_st_solar_BPA,(3,365))
    daily = np.transpose(daily)
    
    #tolerance
    t = 0.01
    
    days = np.zeros((365,int(sim_years)))
    years = np.zeros((365,int(sim_years)))
    
    #match daily sum with hourly profile of historical day with similar date/production
    for i in range(0,int(sim_years)):
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
            
            st_solar_reshape = np.reshape(st_solar[:,1],(24,1))
            sim_hourly[i*8760+j*24:i*8760+j*24+24] = st_solar_reshape*(sim_solar[i*365+j]/daily[day,year])
    
    #impose maximum constraint
    for i in range(0,len(sim_hourly)):
       if sim_hourly[i] > 1:
           sim_hourly[i] = 1
           
    #multiply by installed capacity
    solar_sim = sim_hourly*cap
    
    h = int(len(solar_sim))
    solar_sim = solar_sim[8760:h-2*8760,:]
    S['BPA'] = solar_sim
    
    S.to_csv('Synthetic_solar_power/solar_power_sim.csv')
    
    return None