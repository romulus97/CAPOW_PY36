# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 10:00:33 2018

@author: jdkern
"""

from __future__ import division
from sklearn import linear_model
from statsmodels.tsa.api import VAR
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

######################################################################
#                                LOAD
######################################################################

#import data
df_load = pd.read_excel('Synthetic_demand_pathflows/hist_demanddata.xlsx',sheet_name='hourly_load',header=0)
df_weather = pd.read_excel('Synthetic_demand_pathflows/hist_demanddata.xlsx',sheet_name='weather',header=0)
BPA_weights = pd.read_excel('Synthetic_demand_pathflows/hist_demanddata.xlsx',sheet_name='BPA_location_weights',header=0)
CAISO_weights = pd.read_excel('Synthetic_demand_pathflows/hist_demanddata.xlsx',sheet_name='CAISO_location_weights',header=0)

Name_list=pd.read_csv('Synthetic_demand_pathflows/Covariance_Calculation.csv')
Name_list=list(Name_list.loc['SALEM_T':])
Name_list=Name_list[1:]
sim_weather=pd.read_csv('Synthetic_weather/synthetic_weather_data.csv',header=0)

#weekday designation
dow = df_weather.loc[:,'Weekday']


#generate simulated day of the week assuming starts from monday
count=0
sim_dow= np.zeros(len(sim_weather))
for i in range(0,len(sim_weather)):
    count = count +1
    if count <=5:
        sim_dow[i]=1
    elif count > 5:
        sim_dow[i]=0
    
    if count ==7:
        count =0

#Generate a datelist
datelist=pd.date_range(pd.datetime(2017,1,1),periods=365).tolist()  
sim_month=np.zeros(len(sim_weather))  
sim_day=np.zeros(len(sim_weather))
sim_year=np.zeros(len(sim_weather))

count=0
for i in range(0,len(sim_weather)):
    
    if count <=364:
        sim_month[i]=datelist[count].month
        sim_day[i]=datelist[count].day
        sim_year[i]=datelist[count].year
    else:
        count=0
        sim_month[i]=datelist[count].month
        sim_day[i]=datelist[count].day
        sim_year[i]=datelist[count].year        
    count=count+1

######################################################################
#                                BPAT
######################################################################
#Find the simulated data at the sites

col_BPA_T = ['SALEM_T','SEATTLE_T','PORTLAND_T','EUGENE_T','BOISE_T']
col_BPA_W = ['SALEM_W','SEATTLE_W','PORTLAND_W','EUGENE_W','BOISE_W']

BPA_sim_T=sim_weather[col_BPA_T].values
BPA_sim_W=sim_weather[col_BPA_W].values

sim_days = len(sim_weather)

weighted_SimT = np.zeros((sim_days,1))

###########################################
#find average temps 
cities = ['Salem','Seattle','Portland','Eugene','Boise']
num_cities = len(cities)
num_days = len(df_weather)

AvgT = np.zeros((num_days,num_cities))
Wind = np.zeros((num_days,num_cities))
weighted_AvgT = np.zeros((num_days,1))

for i in cities:
    n1 = i + '_MaxT'
    n2 = i + '_MinT'
    n3 = i + '_Wind'
    
    j = int(cities.index(i))
    
    AvgT[:,j] = 0.5*df_weather.loc[:,n1] + 0.5*df_weather.loc[:,n2]
    weighted_AvgT[:,0] = weighted_AvgT[:,0] + AvgT[:,j]*BPA_weights.loc[0,i]
    Wind[:,j] = df_weather.loc[:,n3]

    weighted_SimT[:,0] = weighted_SimT[:,0] + BPA_sim_T[:,j]*BPA_weights.loc[0,i]     

#Convert simulated temperature to F
weighted_SimT=(weighted_SimT * 9/5) +32   
BPA_sim_T_F=(BPA_sim_T * 9/5) +32   
       
#convert to degree days
HDD = np.zeros((num_days,num_cities))
CDD = np.zeros((num_days,num_cities))

HDD_sim = np.zeros((sim_days,num_cities))
CDD_sim = np.zeros((sim_days,num_cities))
for i in range(0,num_days):
    for j in range(0,num_cities):
        HDD[i,j] = np.max((0,65-AvgT[i,j]))
        CDD[i,j] = np.max((0,AvgT[i,j] - 65))

for i in range(0,sim_days):
    for j in range(0,num_cities):
        HDD_sim[i,j] = np.max((0,65-BPA_sim_T_F[i,j]))
        CDD_sim[i,j] = np.max((0,BPA_sim_T_F[i,j] - 65))   

#separate wind speed by cooling/heating degree day
binary_CDD = CDD>0
binary_HDD = HDD>0
CDD_wind = np.multiply(Wind,binary_CDD)
HDD_wind = np.multiply(Wind,binary_HDD)

binary_CDD_sim = CDD_sim > 0
binary_HDD_sim = HDD_sim > 0
CDD_wind_sim = np.multiply(BPA_sim_W,binary_CDD_sim)
HDD_wind_sim = np.multiply(BPA_sim_W,binary_HDD_sim)

#convert load to array 
BPA_load = df_load.loc[:,'BPA'].values

#remove NaNs
a = np.argwhere(np.isnan(BPA_load))
for i in a:
    BPA_load[i] = BPA_load[i+24]   

peaks = np.zeros((num_days,1))

#find peaks
for i in range(0,num_days):
    peaks[i] = np.max(BPA_load[i*24:i*24+24])
 
#Separate data by weighted temperature
M = np.column_stack((weighted_AvgT,peaks,dow,HDD,CDD,HDD_wind,CDD_wind))
M_sim=np.column_stack((weighted_SimT,sim_dow,HDD_sim,CDD_sim,HDD_wind_sim,CDD_wind_sim))

X70p = M[(M[:,0] >= 70),2:]
y70p = M[(M[:,0] >= 70),1] 
X65_70 = M[(M[:,0] >= 65) & (M[:,0] < 70),2:]
y65_70 = M[(M[:,0] >= 65) & (M[:,0] < 70),1]  
X60_65 = M[(M[:,0] >= 60) & (M[:,0] < 65),2:]
y60_65 = M[(M[:,0] >= 60) & (M[:,0] < 65),1]  
X55_60 = M[(M[:,0] >= 55) & (M[:,0] < 60),2:]
y55_60 = M[(M[:,0] >= 55) & (M[:,0] < 60),1]  
X50_55 = M[(M[:,0] >= 50) & (M[:,0] < 55),2:]
y50_55 = M[(M[:,0] >= 50) & (M[:,0] < 55),1]      
X40_50 = M[(M[:,0] >= 40) & (M[:,0] < 50),2:]
y40_50 = M[(M[:,0] >= 40) & (M[:,0] < 50),1]      
X30_40 = M[(M[:,0] >= 30) & (M[:,0] < 40),2:]
y30_40 = M[(M[:,0] >= 30) & (M[:,0] < 40),1] 
X25_30 = M[(M[:,0] >= 25) & (M[:,0] < 30),2:]
y25_30 = M[(M[:,0] >= 25) & (M[:,0] < 30),1]  
X25m = M[(M[:,0] < 25),2:]
y25m = M[(M[:,0] < 25),1]  

X70p_Sim = M_sim[(M_sim[:,0] >= 70),1:]
X65_70_Sim = M_sim[(M_sim[:,0] >= 65) & (M_sim[:,0] < 70),1:]
X60_65_Sim = M_sim[(M_sim[:,0] >= 60) & (M_sim[:,0] < 65),1:]
X55_60_Sim = M_sim[(M_sim[:,0] >= 55) & (M_sim[:,0] < 60),1:]
X50_55_Sim = M_sim[(M_sim[:,0] >= 50) & (M_sim[:,0] < 55),1:]
X40_50_Sim = M_sim[(M_sim[:,0] >= 40) & (M_sim[:,0] < 50),1:]
X30_40_Sim = M_sim[(M_sim[:,0] >= 30) & (M_sim[:,0] < 40),1:]
X25_30_Sim = M_sim[(M_sim[:,0] >= 25) & (M_sim[:,0] < 30),1:]
X25m_Sim = M_sim[(M_sim[:,0] < 25),1:]
#multivariate regression

#Create linear regression object
reg70p = linear_model.LinearRegression()
reg65_70 = linear_model.LinearRegression()
reg60_65 = linear_model.LinearRegression()
reg55_60 = linear_model.LinearRegression()
reg50_55 = linear_model.LinearRegression()
reg40_50 = linear_model.LinearRegression()
reg30_40 = linear_model.LinearRegression()
reg25_30 = linear_model.LinearRegression()
reg25m = linear_model.LinearRegression()

# Train the model using the training sets
if len(y70p) > 0:
    reg70p.fit(X70p,y70p)
if len(y65_70) > 0:
    reg65_70.fit(X65_70,y65_70)
if len(y60_65) > 0:
    reg60_65.fit(X60_65,y60_65)
if len(y55_60) > 0:
    reg55_60.fit(X55_60,y55_60)
if len(y50_55) > 0:
    reg50_55.fit(X50_55,y50_55)
if len(y40_50) > 0:
    reg40_50.fit(X40_50,y40_50)
if len(y30_40) > 0:
    reg30_40.fit(X30_40,y30_40)
if len(y25_30) > 0:
    reg25_30.fit(X25_30,y25_30)
if len(y25m) > 0:
    reg25m.fit(X25m,y25m)

# Make predictions using the testing set
predicted = []
for i in range(0,num_days):
    s = M[i,2:]
    s = s.reshape((1,len(s)))
    if M[i,0]>=70:      
        y_hat = reg70p.predict(s)
    elif M[i,0] >= 65 and M[i,0] < 70:
        y_hat = reg65_70.predict(s)
    elif M[i,0] >= 60 and M[i,0] < 65:
        y_hat = reg60_65.predict(s)        
    elif M[i,0] >= 55 and M[i,0] < 60:
        y_hat = reg55_60.predict(s)
    elif M[i,0] >= 50 and M[i,0] < 55:
        y_hat = reg50_55.predict(s)          
    elif M[i,0] >= 40 and M[i,0] < 50:
        y_hat = reg40_50.predict(s)
    elif M[i,0] >= 30 and M[i,0] < 40:
        y_hat = reg30_40.predict(s)
    elif M[i,0] >= 25 and M[i,0] < 30:
        y_hat = reg25_30.predict(s)
    elif M[i,0] < 25:
        y_hat = reg25m.predict(s)

    predicted = np.append(predicted,y_hat)
    BPA_p = predicted.reshape((len(predicted),1))

#Simulate using the regression above
simulated=[]
for i in range(0,sim_days):
    s = M_sim[i,1:]
    s = s.reshape((1,len(s)))
    if M_sim[i,0]>=70:      
        y_hat = reg70p.predict(s)
    elif M_sim[i,0] >= 65 and M_sim[i,0] < 70:
        y_hat = reg65_70.predict(s)
    elif M_sim[i,0] >= 60 and M_sim[i,0] < 65:
        y_hat = reg60_65.predict(s)        
    elif M_sim[i,0] >= 55 and M_sim[i,0] < 60:
        y_hat = reg55_60.predict(s)
    elif M_sim[i,0] >= 50 and M_sim[i,0] < 55:
        y_hat = reg50_55.predict(s)          
    elif M_sim[i,0] >= 40 and M_sim[i,0] < 50:
        y_hat = reg40_50.predict(s)
    elif M_sim[i,0] >= 30 and M_sim[i,0] < 40:
        y_hat = reg30_40.predict(s)
    elif M_sim[i,0] >= 25 and M_sim[i,0] < 30:
        y_hat = reg25_30.predict(s)
    elif M_sim[i,0] < 25:
        y_hat = reg25m.predict(s)

    simulated = np.append(simulated,y_hat)
    BPA_sim = simulated.reshape((len(simulated),1))  
    
#a=st.pearsonr(peaks,BPA_p)
#print a[0]**2

# Residuals
BPAresiduals = BPA_p - peaks
BPA_y = peaks

# RMSE
RMSE = (np.sum((BPAresiduals**2))/len(BPAresiduals))**.5

output = np.column_stack((BPA_p,peaks))


#########################################################################
#                               CAISO 
#########################################################################
#Find the simulated data at the sites
col_CAISO_T = ['FRESNO_T','OAKLAND_T','LOS ANGELES_T','SAN DIEGO_T','SACRAMENTO_T','SAN JOSE_T','SAN FRANCISCO_T']
col_CAISO_W = ['FRESNO_W','OAKLAND_W','LOS ANGELES_W','SAN DIEGO_W','SACRAMENTO_W','SAN JOSE_W','SAN FRANCISCO_W']


CAISO_sim_T=sim_weather[col_CAISO_T].values
CAISO_sim_W=sim_weather[col_CAISO_W].values

sim_days = len(sim_weather)

weighted_SimT = np.zeros((sim_days,1))
#find average temps 
cities = ['Fresno','Oakland','LA','SanDiego','Sacramento','SanJose','SanFran']
num_cities = len(cities)
num_days = len(df_weather)

AvgT = np.zeros((num_days,num_cities))
Wind = np.zeros((num_days,num_cities))
weighted_AvgT = np.zeros((num_days,1))

for i in cities:
    n1 = i + '_MaxT'
    n2 = i + '_MinT'
    n3 = i + '_Wind'
    
    j = int(cities.index(i))
    
    AvgT[:,j] = 0.5*df_weather.loc[:,n1] + 0.5*df_weather.loc[:,n2]
    Wind[:,j] = df_weather.loc[:,n3]
    weighted_AvgT[:,0] = weighted_AvgT[:,0] + AvgT[:,j]*CAISO_weights.loc[1,i]
    weighted_SimT[:,0] = weighted_SimT[:,0] + CAISO_sim_T[:,j]*CAISO_weights.loc[1,i]   
    
#Convert simulated temperature to F
weighted_SimT=(weighted_SimT * 9/5) +32   
CAISO_sim_T_F=(CAISO_sim_T * 9/5) +32   
#convert to degree days
HDD = np.zeros((num_days,num_cities))
CDD = np.zeros((num_days,num_cities))

HDD_sim = np.zeros((sim_days,num_cities))
CDD_sim = np.zeros((sim_days,num_cities))

for i in range(0,num_days):
    for j in range(0,num_cities):
        HDD[i,j] = np.max((0,65-AvgT[i,j]))
        CDD[i,j] = np.max((0,AvgT[i,j] - 65))

for i in range(0,sim_days):
    for j in range(0,num_cities):
        HDD_sim[i,j] = np.max((0,65-CAISO_sim_T_F[i,j]))
        CDD_sim[i,j] = np.max((0,CAISO_sim_T_F[i,j] - 65))  
        
#separate wind speed by cooling/heating degree day
binary_CDD = CDD>0
binary_HDD = HDD>0
binary_CDD_sim = CDD_sim > 0
binary_HDD_sim = HDD_sim > 0

CDD_wind = np.multiply(Wind,binary_CDD)
HDD_wind = np.multiply(Wind,binary_HDD)
CDD_wind_sim = np.multiply(CAISO_sim_W,binary_CDD_sim)
HDD_wind_sim = np.multiply(CAISO_sim_W,binary_HDD_sim)

###########################
#      CAISO - SDGE
###########################
#convert load to array 
SDGE_load = df_load.loc[:,'SDGE'].values

#remove NaNs
a = np.argwhere(np.isnan(SDGE_load))
for i in a:
    SDGE_load[i] = SDGE_load[i+24]   

peaks = np.zeros((num_days,1))

#find peaks
for i in range(0,num_days):
    peaks[i] = np.max(SDGE_load[i*24:i*24+24])
 
#Separate data by weighted temperature
M = np.column_stack((weighted_AvgT,peaks,dow,HDD,CDD,HDD_wind,CDD_wind))
M_sim=np.column_stack((weighted_SimT,sim_dow,HDD_sim,CDD_sim,HDD_wind_sim,CDD_wind_sim))


X80p = M[(M[:,0] >= 80),2:]
y80p = M[(M[:,0] >= 80),1]
X75_80 = M[(M[:,0] >= 75) & (M[:,0] < 80),2:]
y75_80 = M[(M[:,0] >= 75) & (M[:,0] < 80),1]
X70_75 = M[(M[:,0] >= 70) & (M[:,0] < 75),2:]
y70_75 = M[(M[:,0] >= 70) & (M[:,0] < 75),1]
X65_70 = M[(M[:,0] >= 65) & (M[:,0] < 70),2:]
y65_70 = M[(M[:,0] >= 65) & (M[:,0] < 70),1]  
X60_65 = M[(M[:,0] >= 60) & (M[:,0] < 65),2:]
y60_65 = M[(M[:,0] >= 60) & (M[:,0] < 65),1]  
X55_60 = M[(M[:,0] >= 55) & (M[:,0] < 60),2:]
y55_60 = M[(M[:,0] >= 55) & (M[:,0] < 60),1]  
X50_55 = M[(M[:,0] >= 50) & (M[:,0] < 55),2:]
y50_55 = M[(M[:,0] >= 50) & (M[:,0] < 55),1]   
X50 = M[(M[:,0] < 50),2:]
y50 = M[(M[:,0] < 50),1]  
   

X80p_Sim = M_sim[(M_sim[:,0] >= 80),1:]
X75_80_Sim = M_sim[(M_sim[:,0] >= 75) & (M_sim[:,0] < 80),1:]
X70_75_Sim = M_sim[(M_sim[:,0] >= 70) & (M_sim[:,0] < 75),1:]
X65_70_Sim = M_sim[(M_sim[:,0] >= 65) & (M_sim[:,0] < 70),1:]
X60_65_Sim = M_sim[(M_sim[:,0] >= 60) & (M_sim[:,0] < 65),1:]
X55_60_Sim = M_sim[(M_sim[:,0] >= 55) & (M_sim[:,0] < 60),1:]
X50_55_Sim = M_sim[(M_sim[:,0] >= 50) & (M_sim[:,0] < 55),1:]
X50_Sim = M_sim[(M_sim[:,0] < 50),1:]


#Create linear regression object
reg80p = linear_model.LinearRegression()
reg75_80 = linear_model.LinearRegression()
reg70_75 = linear_model.LinearRegression()
reg65_70 = linear_model.LinearRegression()
reg60_65 = linear_model.LinearRegression()
reg55_60 = linear_model.LinearRegression()
reg50_55 = linear_model.LinearRegression()
reg50m = linear_model.LinearRegression()

## Train the model using the training sets
if len(y80p) > 0:
    reg80p.fit(X80p,y80p)   
if len(y75_80) > 0:
    reg75_80.fit(X75_80,y75_80)
if len(y70_75) > 0:
    reg70_75.fit(X70_75,y70_75)      
if len(y65_70) > 0:
    reg65_70.fit(X65_70,y65_70)
if len(y60_65) > 0:
    reg60_65.fit(X60_65,y60_65)
if len(y55_60) > 0:
    reg55_60.fit(X55_60,y55_60)
if len(y50_55) > 0:
    reg50_55.fit(X50_55,y50_55)
if len(y50) > 0:
    reg50m.fit(X50,y50)
    
# Make predictions using the testing set
predicted = []
for i in range(0,num_days):
    s = M[i,2:]
    s = s.reshape((1,len(s)))
    if M[i,0]>=80:      
        y_hat = reg80p.predict(s)
    elif M[i,0] >= 75 and M[i,0] < 80:
        y_hat = reg75_80.predict(s)
    elif M[i,0] >= 70 and M[i,0] < 75:
        y_hat = reg70_75.predict(s)           
    elif M[i,0] >= 65 and M[i,0] < 70:
        y_hat = reg65_70.predict(s)
    elif M[i,0] >= 60 and M[i,0] < 65:
        y_hat = reg60_65.predict(s)        
    elif M[i,0] >= 55 and M[i,0] < 60:
        y_hat = reg55_60.predict(s)
    elif M[i,0] >= 50 and M[i,0] < 55:
        y_hat = reg50_55.predict(s)    
    elif M[i,0] < 50:
        y_hat = reg50m.predict(s)

    predicted = np.append(predicted,y_hat)
    SDGE_p = predicted.reshape((len(predicted),1))

simulated=[]
for i in range(0,sim_days):
    s = M_sim[i,1:]
    s = s.reshape((1,len(s)))
    if M_sim[i,0]>=80:      
        y_hat = reg80p.predict(s)
    elif M_sim[i,0] >= 75 and M_sim[i,0] < 80:
        y_hat = reg75_80.predict(s)
    elif M_sim[i,0] >= 70 and M_sim[i,0] < 75:
        y_hat = reg70_75.predict(s)
    elif M_sim[i,0] >= 65 and M_sim[i,0] < 70:
        y_hat = reg65_70.predict(s)
    elif M_sim[i,0] >= 60 and M_sim[i,0] < 65:
        y_hat = reg60_65.predict(s)        
    elif M_sim[i,0] >= 55 and M_sim[i,0] < 60:
        y_hat = reg55_60.predict(s)
    elif M_sim[i,0] >= 50 and M_sim[i,0] < 55:
        y_hat = reg50_55.predict(s)
    elif M_sim[i,0] < 50:
        y_hat = reg50m.predict(s)          
#        
    simulated = np.append(simulated,y_hat)
    SDGE_sim = simulated.reshape((len(simulated),1))   

# Residuals
SDGEresiduals = SDGE_p - peaks
SDGE_y = peaks

#a=st.pearsonr(peaks,SDGE_p)
#print a[0]**2

# RMSE
RMSE = (np.sum((SDGEresiduals**2))/len(SDGEresiduals))**.5


###########################
#      CAISO - SCE
###########################
#convert load to array 
SCE_load = df_load.loc[:,'SCE'].values

#remove NaNs
a = np.argwhere(np.isnan(SCE_load))
for i in a:
    SCE_load[i] = SCE_load[i+24]   

peaks = np.zeros((num_days,1))

#find peaks
for i in range(0,num_days):
    peaks[i] = np.max(SCE_load[i*24:i*24+24])
 
#Separate data by weighted temperature
M = np.column_stack((weighted_AvgT,peaks,dow,HDD,CDD,HDD_wind,CDD_wind))
M_sim=np.column_stack((weighted_SimT,sim_dow,HDD_sim,CDD_sim,HDD_wind_sim,CDD_wind_sim))


X80p = M[(M[:,0] >= 80),2:]
y80p = M[(M[:,0] >= 80),1]
X75_80 = M[(M[:,0] >= 75) & (M[:,0] < 80),2:]
y75_80 = M[(M[:,0] >= 75) & (M[:,0] < 80),1]
X70_75 = M[(M[:,0] >= 70) & (M[:,0] < 75),2:]
y70_75 = M[(M[:,0] >= 70) & (M[:,0] < 75),1]
X65_70 = M[(M[:,0] >= 65) & (M[:,0] < 70),2:]
y65_70 = M[(M[:,0] >= 65) & (M[:,0] < 70),1]  
X60_65 = M[(M[:,0] >= 60) & (M[:,0] < 65),2:]
y60_65 = M[(M[:,0] >= 60) & (M[:,0] < 65),1]  
X55_60 = M[(M[:,0] >= 55) & (M[:,0] < 60),2:]
y55_60 = M[(M[:,0] >= 55) & (M[:,0] < 60),1]  
X50_55 = M[(M[:,0] >= 50) & (M[:,0] < 55),2:]
y50_55 = M[(M[:,0] >= 50) & (M[:,0] < 55),1]   
X50 = M[(M[:,0] < 50),2:]
y50 = M[(M[:,0] < 50),1]  
   

X80p_Sim = M_sim[(M_sim[:,0] >= 80),1:]
X75_80_Sim = M_sim[(M_sim[:,0] >= 75) & (M_sim[:,0] < 80),1:]
X70_75_Sim = M_sim[(M_sim[:,0] >= 70) & (M_sim[:,0] < 75),1:]
X65_70_Sim = M_sim[(M_sim[:,0] >= 65) & (M_sim[:,0] < 70),1:]
X60_65_Sim = M_sim[(M_sim[:,0] >= 60) & (M_sim[:,0] < 65),1:]
X55_60_Sim = M_sim[(M_sim[:,0] >= 55) & (M_sim[:,0] < 60),1:]
X50_55_Sim = M_sim[(M_sim[:,0] >= 50) & (M_sim[:,0] < 55),1:]
X50_Sim = M_sim[(M_sim[:,0] < 50),1:]


##multivariate regression
#
#Create linear regression object
reg80p = linear_model.LinearRegression()
reg75_80 = linear_model.LinearRegression()
reg70_75 = linear_model.LinearRegression()
reg65_70 = linear_model.LinearRegression()
reg60_65 = linear_model.LinearRegression()
reg55_60 = linear_model.LinearRegression()
reg50_55 = linear_model.LinearRegression()
reg50m = linear_model.LinearRegression()

## Train the model using the training sets
if len(y80p) > 0:
    reg80p.fit(X80p,y80p)
if len(y75_80) > 0:
    reg75_80.fit(X75_80,y75_80)
if len(y70_75) > 0:
    reg70_75.fit(X70_75,y70_75)      
if len(y65_70) > 0:
    reg65_70.fit(X65_70,y65_70)
if len(y60_65) > 0:
    reg60_65.fit(X60_65,y60_65)
if len(y55_60) > 0:
    reg55_60.fit(X55_60,y55_60)
if len(y50_55) > 0:
    reg50_55.fit(X50_55,y50_55)
if len(y50) > 0:
    reg50m.fit(X50,y50)

# Make predictions using the testing set
predicted = []
for i in range(0,num_days):
    s = M[i,2:]
    s = s.reshape((1,len(s)))
    if M[i,0]>=80:      
        y_hat = reg80p.predict(s)
    elif M[i,0] >= 75 and M[i,0] < 80:
        y_hat = reg75_80.predict(s)
    elif M[i,0] >= 70 and M[i,0] < 75:
        y_hat = reg70_75.predict(s)           
    elif M[i,0] >= 65 and M[i,0] < 70:
        y_hat = reg65_70.predict(s)
    elif M[i,0] >= 60 and M[i,0] < 65:
        y_hat = reg60_65.predict(s)        
    elif M[i,0] >= 55 and M[i,0] < 60:
        y_hat = reg55_60.predict(s)
    elif M[i,0] >= 50 and M[i,0] < 55:
        y_hat = reg50_55.predict(s)    
    elif M[i,0] < 50:
        y_hat = reg50m.predict(s)

    predicted = np.append(predicted,y_hat)
    SCE_p = predicted.reshape((len(predicted),1))

simulated=[]
for i in range(0,sim_days):
    s = M_sim[i,1:]
    s = s.reshape((1,len(s)))
    if M_sim[i,0]>=80:      
        y_hat = reg80p.predict(s)
    elif M_sim[i,0] >= 75 and M_sim[i,0] < 80:
        y_hat = reg75_80.predict(s)
    elif M_sim[i,0] >= 70 and M_sim[i,0] < 75:
        y_hat = reg70_75.predict(s)
    elif M_sim[i,0] >= 65 and M_sim[i,0] < 70:
        y_hat = reg65_70.predict(s)
    elif M_sim[i,0] >= 60 and M_sim[i,0] < 65:
        y_hat = reg60_65.predict(s)        
    elif M_sim[i,0] >= 55 and M_sim[i,0] < 60:
        y_hat = reg55_60.predict(s)
    elif M_sim[i,0] >= 50 and M_sim[i,0] < 55:
        y_hat = reg50_55.predict(s)
    elif M_sim[i,0] < 50:
        y_hat = reg50m.predict(s)          
    
    simulated = np.append(simulated,y_hat)
    SCE_sim = simulated.reshape((len(simulated),1))


#a=st.pearsonr(peaks,SCE_p)
#print a[0]**2

# Residuals
SCEresiduals = SCE_p - peaks
SCE_y = peaks

# RMSE
RMSE = (np.sum((SCEresiduals**2))/len(SCEresiduals))**.5


###########################
#      CAISO - PG&E Valley
###########################
#convert load to array 
PGEV_load = df_load.loc[:,'PGE_V'].values

#remove NaNs
a = np.argwhere(np.isnan(PGEV_load))
for i in a:
    PGEV_load[i] = PGEV_load[i+24]   

peaks = np.zeros((num_days,1))

#find peaks
for i in range(0,num_days):
    peaks[i] = np.max(PGEV_load[i*24:i*24+24])
 
#Separate data by weighted temperature
M = np.column_stack((weighted_AvgT,peaks,dow,HDD,CDD,HDD_wind,CDD_wind))
M_sim=np.column_stack((weighted_SimT,sim_dow,HDD_sim,CDD_sim,HDD_wind_sim,CDD_wind_sim))


X80p = M[(M[:,0] >= 80),2:]
y80p = M[(M[:,0] >= 80),1]
X75_80 = M[(M[:,0] >= 75) & (M[:,0] < 80),2:]
y75_80 = M[(M[:,0] >= 75) & (M[:,0] < 80),1]
X70_75 = M[(M[:,0] >= 70) & (M[:,0] < 75),2:]
y70_75 = M[(M[:,0] >= 70) & (M[:,0] < 75),1]
X65_70 = M[(M[:,0] >= 65) & (M[:,0] < 70),2:]
y65_70 = M[(M[:,0] >= 65) & (M[:,0] < 70),1]  
X60_65 = M[(M[:,0] >= 60) & (M[:,0] < 65),2:]
y60_65 = M[(M[:,0] >= 60) & (M[:,0] < 65),1]  
X55_60 = M[(M[:,0] >= 55) & (M[:,0] < 60),2:]
y55_60 = M[(M[:,0] >= 55) & (M[:,0] < 60),1]  
X50_55 = M[(M[:,0] >= 50) & (M[:,0] < 55),2:]
y50_55 = M[(M[:,0] >= 50) & (M[:,0] < 55),1]   
X50 = M[(M[:,0] < 50),2:]
y50 = M[(M[:,0] < 50),1]  
   

X80p_Sim = M_sim[(M_sim[:,0] >= 80),1:]
X75_80_Sim = M_sim[(M_sim[:,0] >= 75) & (M_sim[:,0] < 80),1:]
X70_75_Sim = M_sim[(M_sim[:,0] >= 70) & (M_sim[:,0] < 75),1:]
X65_70_Sim = M_sim[(M_sim[:,0] >= 65) & (M_sim[:,0] < 70),1:]
X60_65_Sim = M_sim[(M_sim[:,0] >= 60) & (M_sim[:,0] < 65),1:]
X55_60_Sim = M_sim[(M_sim[:,0] >= 55) & (M_sim[:,0] < 60),1:]
X50_55_Sim = M_sim[(M_sim[:,0] >= 50) & (M_sim[:,0] < 55),1:]
X50_Sim = M_sim[(M_sim[:,0] < 50),1:]


##multivariate regression
#
#Create linear regression object
reg80p = linear_model.LinearRegression()
reg75_80 = linear_model.LinearRegression()
reg70_75 = linear_model.LinearRegression()
reg65_70 = linear_model.LinearRegression()
reg60_65 = linear_model.LinearRegression()
reg55_60 = linear_model.LinearRegression()
reg50_55 = linear_model.LinearRegression()
reg50m = linear_model.LinearRegression()


## Train the model using the training sets
if len(y80p) > 0:
    reg80p.fit(X80p,y80p)
if len(y75_80) > 0:
    reg75_80.fit(X75_80,y75_80)
if len(y70_75) > 0:
    reg70_75.fit(X70_75,y70_75)      
if len(y65_70) > 0:
    reg65_70.fit(X65_70,y65_70)
if len(y60_65) > 0:
    reg60_65.fit(X60_65,y60_65)
if len(y55_60) > 0:
    reg55_60.fit(X55_60,y55_60)
if len(y50_55) > 0:
    reg50_55.fit(X50_55,y50_55)
if len(y50) > 0:
    reg50m.fit(X50,y50)

# Make predictions using the testing set
predicted = []
for i in range(0,num_days):
    s = M[i,2:]
    s = s.reshape((1,len(s)))
    if M[i,0]>=80:      
        y_hat = reg80p.predict(s)
    elif M[i,0] >= 75 and M[i,0] < 80:
        y_hat = reg75_80.predict(s)
    elif M[i,0] >= 70 and M[i,0] < 75:
        y_hat = reg70_75.predict(s)           
    elif M[i,0] >= 65 and M[i,0] < 70:
        y_hat = reg65_70.predict(s)
    elif M[i,0] >= 60 and M[i,0] < 65:
        y_hat = reg60_65.predict(s)        
    elif M[i,0] >= 55 and M[i,0] < 60:
        y_hat = reg55_60.predict(s)
    elif M[i,0] >= 50 and M[i,0] < 55:
        y_hat = reg50_55.predict(s)    
    elif M[i,0] < 50:
        y_hat = reg50m.predict(s)

    predicted = np.append(predicted,y_hat)
    PGEV_p = predicted.reshape((len(predicted),1))
    
simulated=[]
for i in range(0,sim_days):
    s = M_sim[i,1:]
    s = s.reshape((1,len(s)))
    if M_sim[i,0]>=80:      
        y_hat = reg80p.predict(s)
    elif M_sim[i,0] >= 75 and M_sim[i,0] < 80:
        y_hat = reg75_80.predict(s)
    elif M_sim[i,0] >= 70 and M_sim[i,0] < 75:
        y_hat = reg70_75.predict(s)
    elif M_sim[i,0] >= 65 and M_sim[i,0] < 70:
        y_hat = reg65_70.predict(s)
    elif M_sim[i,0] >= 60 and M_sim[i,0] < 65:
        y_hat = reg60_65.predict(s)        
    elif M_sim[i,0] >= 55 and M_sim[i,0] < 60:
        y_hat = reg55_60.predict(s)
    elif M_sim[i,0] >= 50 and M_sim[i,0] < 55:
        y_hat = reg50_55.predict(s)
    elif M_sim[i,0] < 50:
        y_hat = reg50m.predict(s)          
    
    simulated = np.append(simulated,y_hat)
    PGEV_sim = simulated.reshape((len(simulated),1))    

#a=st.pearsonr(peaks,PGEV_p)
#print a[0]**2

# Residuals
PGEVresiduals = PGEV_p - peaks
PGEV_y = peaks

# RMSE
RMSE = (np.sum((PGEVresiduals**2))/len(PGEVresiduals))**.5


###########################
#      CAISO - PG&E Bay
###########################
#convert load to array 
PGEB_load = df_load.loc[:,'PGE_B'].values

#remove NaNs
a = np.argwhere(np.isnan(PGEB_load))
for i in a:
    PGEB_load[i] = PGEB_load[i+24]   

peaks = np.zeros((num_days,1))

#find peaks
for i in range(0,num_days):
    peaks[i] = np.max(PGEB_load[i*24:i*24+24])
 
#Separate data by weighted temperature
M = np.column_stack((weighted_AvgT,peaks,dow,HDD,CDD,HDD_wind,CDD_wind))
M_sim=np.column_stack((weighted_SimT,sim_dow,HDD_sim,CDD_sim,HDD_wind_sim,CDD_wind_sim))


X80p = M[(M[:,0] >= 80),2:]
y80p = M[(M[:,0] >= 80),1]
X75_80 = M[(M[:,0] >= 75) & (M[:,0] < 80),2:]
y75_80 = M[(M[:,0] >= 75) & (M[:,0] < 80),1]
X70_75 = M[(M[:,0] >= 70) & (M[:,0] < 75),2:]
y70_75 = M[(M[:,0] >= 70) & (M[:,0] < 75),1]
X65_70 = M[(M[:,0] >= 65) & (M[:,0] < 70),2:]
y65_70 = M[(M[:,0] >= 65) & (M[:,0] < 70),1]  
X60_65 = M[(M[:,0] >= 60) & (M[:,0] < 65),2:]
y60_65 = M[(M[:,0] >= 60) & (M[:,0] < 65),1]  
X55_60 = M[(M[:,0] >= 55) & (M[:,0] < 60),2:]
y55_60 = M[(M[:,0] >= 55) & (M[:,0] < 60),1]  
X50_55 = M[(M[:,0] >= 50) & (M[:,0] < 55),2:]
y50_55 = M[(M[:,0] >= 50) & (M[:,0] < 55),1]   
X50 = M[(M[:,0] < 50),2:]
y50 = M[(M[:,0] < 50),1]  

X80p_Sim = M_sim[(M_sim[:,0] >= 80),1:]
X75_80_Sim = M_sim[(M_sim[:,0] >= 75) & (M_sim[:,0] < 80),1:]
X70_75_Sim = M_sim[(M_sim[:,0] >= 70) & (M_sim[:,0] < 75),1:]
X65_70_Sim = M_sim[(M_sim[:,0] >= 65) & (M_sim[:,0] < 70),1:]
X60_65_Sim = M_sim[(M_sim[:,0] >= 60) & (M_sim[:,0] < 65),1:]
X55_60_Sim = M_sim[(M_sim[:,0] >= 55) & (M_sim[:,0] < 60),1:]
X50_55_Sim = M_sim[(M_sim[:,0] >= 50) & (M_sim[:,0] < 55),1:]
X50_Sim = M_sim[(M_sim[:,0] < 50),1:]


#Create linear regression object
reg80p = linear_model.LinearRegression()
reg75_80 = linear_model.LinearRegression()
reg70_75 = linear_model.LinearRegression()
reg65_70 = linear_model.LinearRegression()
reg60_65 = linear_model.LinearRegression()
reg55_60 = linear_model.LinearRegression()
reg50_55 = linear_model.LinearRegression()
reg50m = linear_model.LinearRegression()


## Train the model using the training sets
if len(y80p) > 0:
    reg80p.fit(X80p,y80p)   
if len(y75_80) > 0:
    reg75_80.fit(X75_80,y75_80)
if len(y70_75) > 0:
    reg70_75.fit(X70_75,y70_75)      
if len(y65_70) > 0:
    reg65_70.fit(X65_70,y65_70)
if len(y60_65) > 0:
    reg60_65.fit(X60_65,y60_65)
if len(y55_60) > 0:
    reg55_60.fit(X55_60,y55_60)
if len(y50_55) > 0:
    reg50_55.fit(X50_55,y50_55)
if len(y50) > 0:
    reg50m.fit(X50,y50)

# Make predictions using the testing set
predicted = []
for i in range(0,num_days):
    s = M[i,2:]
    s = s.reshape((1,len(s)))
    if M[i,0]>=80:      
        y_hat = reg80p.predict(s)
    elif M[i,0] >= 75 and M[i,0] < 80:
        y_hat = reg75_80.predict(s)
    elif M[i,0] >= 70 and M[i,0] < 75:
        y_hat = reg70_75.predict(s)           
    elif M[i,0] >= 65 and M[i,0] < 70:
        y_hat = reg65_70.predict(s)
    elif M[i,0] >= 60 and M[i,0] < 65:
        y_hat = reg60_65.predict(s)        
    elif M[i,0] >= 55 and M[i,0] < 60:
        y_hat = reg55_60.predict(s)
    elif M[i,0] >= 50 and M[i,0] < 55:
        y_hat = reg50_55.predict(s)    
    elif M[i,0] < 50:
        y_hat = reg50m.predict(s)

    predicted = np.append(predicted,y_hat)
    PGEB_p = predicted.reshape((len(predicted),1))


simulated=[]
for i in range(0,sim_days):
    s = M_sim[i,1:]
    s = s.reshape((1,len(s)))
    if M_sim[i,0]>=80:      
        y_hat = reg80p.predict(s)
    elif M_sim[i,0] >= 75 and M_sim[i,0] < 80:
        y_hat = reg75_80.predict(s)
    elif M_sim[i,0] >= 70 and M_sim[i,0] < 75:
        y_hat = reg70_75.predict(s)
    elif M_sim[i,0] >= 65 and M_sim[i,0] < 70:
        y_hat = reg65_70.predict(s)
    elif M_sim[i,0] >= 60 and M_sim[i,0] < 65:
        y_hat = reg60_65.predict(s)        
    elif M_sim[i,0] >= 55 and M_sim[i,0] < 60:
        y_hat = reg55_60.predict(s)
    elif M_sim[i,0] >= 50 and M_sim[i,0] < 55:
        y_hat = reg50_55.predict(s)
    elif M_sim[i,0] < 50:
        y_hat = reg50m.predict(s)      #        
    
    simulated = np.append(simulated,y_hat)
    PGEB_sim = simulated.reshape((len(simulated),1))

#a=st.pearsonr(peaks,PGEB_p)
#print a[0]**2

# Residuals
PGEBresiduals = PGEB_p - peaks
PGEB_y = peaks

# RMSE
RMSE = (np.sum((PGEBresiduals**2))/len(PGEBresiduals))**.5


#Collect residuals from load regression
R = np.column_stack((BPAresiduals,SDGEresiduals,SCEresiduals,PGEVresiduals,PGEBresiduals))
ResidualsLoad = R[0:3*365,:]


###################################
#            PATH 46
###################################

#import data
df_data1 = pd.read_excel('Synthetic_demand_pathflows/46_daily.xlsx',sheet_name='Sheet1',header=0)

#find average temps 
cities = ['Tuscon','Phoenix','Vegas','Fresno','Oakland','LA','SanDiego','Sacramento','SanJose','SanFran']
num_cities = len(cities)
num_days = len(df_data1)

AvgT = np.zeros((num_days,num_cities))
Wind = np.zeros((num_days,num_cities))

for i in cities:
    n1 = i + '_AvgT'
    n2 = i + '_Wind'
    
    j = int(cities.index(i))
    
    AvgT[:,j] = df_data1.loc[:,n1] 
    Wind[:,j] = df_data1.loc[:,n2]
       
#convert to degree days
HDD = np.zeros((num_days,num_cities))
CDD = np.zeros((num_days,num_cities))


for i in range(0,num_days):
    for j in range(0,num_cities):
        HDD[i,j] = np.max((0,65-AvgT[i,j]))
        CDD[i,j] = np.max((0,AvgT[i,j] - 65))


#separate wind speed by cooling/heating degree day
binary_CDD = CDD>0
binary_HDD = HDD>0
CDD_wind = np.multiply(Wind,binary_CDD)
HDD_wind = np.multiply(Wind,binary_HDD)


X1 = np.array(df_data1.loc[:,'Month':'Path66'])
X2 = np.column_stack((HDD,CDD,HDD_wind,CDD_wind))
cX = np.column_stack((X1,X2))
df_data = pd.DataFrame(cX)
df_data.rename(columns={0:'Month'}, inplace=True)
df_data.rename(columns={3:'Path46'}, inplace=True)
df_data.rename(columns={4:'Weekday'}, inplace=True)


jan = df_data.loc[df_data['Month'] == 1,:]
feb = df_data.loc[df_data['Month'] == 2,:]
mar = df_data.loc[df_data['Month'] == 3,:]
apr = df_data.loc[df_data['Month'] == 4,:]
may = df_data.loc[df_data['Month'] == 5,:]
jun = df_data.loc[df_data['Month'] == 6,:]
jul = df_data.loc[df_data['Month'] == 7,:]
aug = df_data.loc[df_data['Month'] == 8,:]
sep = df_data.loc[df_data['Month'] == 9,:]
oct = df_data.loc[df_data['Month'] == 10,:]
nov = df_data.loc[df_data['Month'] == 11,:]
dec = df_data.loc[df_data['Month'] == 12,:] 

y = df_data.loc[:,'Path46']

#multivariate regression
jan_reg_46 = linear_model.LinearRegression()
feb_reg_46 = linear_model.LinearRegression()
mar_reg_46 = linear_model.LinearRegression()
apr_reg_46 = linear_model.LinearRegression()
may_reg_46 = linear_model.LinearRegression()
jun_reg_46 = linear_model.LinearRegression()
jul_reg_46 = linear_model.LinearRegression()
aug_reg_46 = linear_model.LinearRegression()
sep_reg_46 = linear_model.LinearRegression()
oct_reg_46 = linear_model.LinearRegression()
nov_reg_46 = linear_model.LinearRegression()
dec_reg_46 = linear_model.LinearRegression()


# Train the model using the training sets
jan_reg_46.fit(jan.loc[:,'Weekday':],jan.loc[:,'Path46'])
feb_reg_46.fit(feb.loc[:,'Weekday':],feb.loc[:,'Path46'])
mar_reg_46.fit(mar.loc[:,'Weekday':],mar.loc[:,'Path46'])
apr_reg_46.fit(apr.loc[:,'Weekday':],apr.loc[:,'Path46'])
may_reg_46.fit(may.loc[:,'Weekday':],may.loc[:,'Path46'])
jun_reg_46.fit(jun.loc[:,'Weekday':],jun.loc[:,'Path46'])
jul_reg_46.fit(jul.loc[:,'Weekday':],jul.loc[:,'Path46'])
aug_reg_46.fit(aug.loc[:,'Weekday':],aug.loc[:,'Path46'])
sep_reg_46.fit(sep.loc[:,'Weekday':],sep.loc[:,'Path46'])
oct_reg_46.fit(oct.loc[:,'Weekday':],oct.loc[:,'Path46'])
nov_reg_46.fit(nov.loc[:,'Weekday':],nov.loc[:,'Path46'])
dec_reg_46.fit(dec.loc[:,'Weekday':],dec.loc[:,'Path46'])

# Make predictions using the testing set
predicted = []
rc = np.shape(jan.loc[:,'Weekday':])
n = rc[1] 

for i in range(0,len(y)):
    
    m = df_data.loc[i,'Month']
    
    if m==1:
        s = jan.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = jan_reg_46.predict(s)
        predicted = np.append(predicted,p)
    elif m==2:
        s = feb.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))        
        p = feb_reg_46.predict(s)
        predicted = np.append(predicted,p)
    elif m==3:
        s = mar.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = mar_reg_46.predict(s)
        predicted = np.append(predicted,p)
    elif m==4:
        s = apr.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = apr_reg_46.predict(s)
        predicted = np.append(predicted,p)
    elif m==5:
        s = may.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = may_reg_46.predict(s)
        predicted = np.append(predicted,p)
    elif m==6:
        s = jun.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = jun_reg_46.predict(s)
        predicted = np.append(predicted,p)
    elif m==7:
        s = jul.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = jul_reg_46.predict(s)
        predicted = np.append(predicted,p)
    elif m==8:
        s = aug.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = aug_reg_46.predict(s)
        predicted = np.append(predicted,p)
    elif m==9:
        s = sep.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = sep_reg_46.predict(s)
        predicted = np.append(predicted,p)
    elif m==10:
        s = oct.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = oct_reg_46.predict(s)
        predicted = np.append(predicted,p)
    elif m==11:
        s = nov.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = nov_reg_46.predict(s)
        predicted = np.append(predicted,p)
    else:
        s = dec.loc[i,'Weekday':]
        s = np.reshape(s[:,None],(1,n))
        p = dec_reg_46.predict(s)
        predicted = np.append(predicted,p)


Path46_p = predicted

# Residuals
residuals = predicted - y.values
Residuals46 = np.reshape(residuals[730:],(1095,1))
Path46_y = y.values

# RMSE
RMSE = (np.sum((residuals**2))/len(residuals))**.5

##R2
#a=st.pearsonr(y,predicted)
#print a[0]**2


###############################
#        NW PATHS 
###############################

#import data
df_data1 = pd.read_excel('Synthetic_demand_pathflows/NW_Path_data.xlsx',sheet_name='Daily',header=0)

#find average temps 
cities = ['Salem','Seattle','Portland','Eugene','Boise','Tuscon','Phoenix','Vegas','Fresno','Oakland','LA','SanDiego','Sacramento','SanJose','SanFran']
num_cities = len(cities)
num_days = len(df_data1)

AvgT = np.zeros((num_days,num_cities))
Wind = np.zeros((num_days,num_cities))

for i in cities:
    n1 = i + '_AvgT'
    n2 = i + '_Wind'
    
    j = int(cities.index(i))
    
    AvgT[:,j] = df_data1.loc[:,n1] 
    Wind[:,j] = df_data1.loc[:,n2]
       
#convert to degree days
HDD = np.zeros((num_days,num_cities))
CDD = np.zeros((num_days,num_cities))

for i in range(0,num_days):
    for j in range(0,num_cities):
        HDD[i,j] = np.max((0,65-AvgT[i,j]))
        CDD[i,j] = np.max((0,AvgT[i,j] - 65))

#separate wind speed by cooling/heating degree day
binary_CDD = CDD>0
binary_HDD = HDD>0
CDD_wind = np.multiply(Wind,binary_CDD)
HDD_wind = np.multiply(Wind,binary_HDD)

X1 = np.array(df_data1.loc[:,'Month':'Weekday'])
X2 = np.column_stack((HDD,CDD,HDD_wind,CDD_wind))
cX = np.column_stack((X1,X2))
df_data = pd.DataFrame(cX)
H = df_data
#df_data.to_excel('Synthetic_demand_pathflows/cX.xlsx')
df_data.rename(columns={0:'Month'}, inplace=True)
df_data.rename(columns={3:'Path8'}, inplace=True)
df_data.rename(columns={4:'Path14'}, inplace=True)
df_data.rename(columns={5:'Path3'}, inplace=True)
df_data.rename(columns={6:'BPA_wind'}, inplace=True)
df_data.rename(columns={7:'BPA_hydro'}, inplace=True)
df_data.rename(columns={8:'Weekday'}, inplace=True)
df_data.rename(columns={9:'Salem_HDD'}, inplace=True)

jan = df_data.loc[df_data['Month'] == 1,:]
feb = df_data.loc[df_data['Month'] == 2,:]
mar = df_data.loc[df_data['Month'] == 3,:]
apr = df_data.loc[df_data['Month'] == 4,:]
may = df_data.loc[df_data['Month'] == 5,:]
jun = df_data.loc[df_data['Month'] == 6,:]
jul = df_data.loc[df_data['Month'] == 7,:]
aug = df_data.loc[df_data['Month'] == 8,:]
sep = df_data.loc[df_data['Month'] == 9,:]
oct = df_data.loc[df_data['Month'] == 10,:]
nov = df_data.loc[df_data['Month'] == 11,:]
dec = df_data.loc[df_data['Month'] == 12,:] 

lines = ['Path8','Path14','Path3']
num_lines = len(lines)

export_residuals = np.zeros((len(cX),num_lines))
NWPaths_p= np.zeros((len(cX),num_lines))
NWPaths_y = np.zeros((len(cX),num_lines))

for line in lines:
    
    y = df_data.loc[:,line]
    line_index = lines.index(line)
    
    #multivariate regression
    name='jan_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()
    
    name='feb_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()
    
    name='mar_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()
    
    name='apr_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()
    
    name='may_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()

    name='jun_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()
    
    name='jul_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()
    
    name='aug_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()
    
    name='sep_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()
    
    name='oct_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()    
    
    name='nov_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()
    
    name='dec_reg_NW' + str(line)
    locals()[name] = linear_model.LinearRegression()        

    
    
    # Train the model using the training sets
    
    name='jan_reg_NW' + str(line)
    locals()[name].fit(jan.loc[:,'BPA_wind':],jan.loc[:,line]) 
    
    name='feb_reg_NW' + str(line)
    locals()[name].fit(feb.loc[:,'BPA_wind':],feb.loc[:,line])
    
    name='mar_reg_NW' + str(line)
    locals()[name].fit(mar.loc[:,'BPA_wind':],mar.loc[:,line])
    
    name='apr_reg_NW' + str(line)
    locals()[name].fit(apr.loc[:,'BPA_wind':],apr.loc[:,line])
    
    name='may_reg_NW' + str(line)
    locals()[name].fit(may.loc[:,'BPA_wind':],may.loc[:,line])

    name='jun_reg_NW' + str(line)
    locals()[name].fit(jun.loc[:,'BPA_wind':],jun.loc[:,line])
    
    name='jul_reg_NW' + str(line)
    locals()[name].fit(jul.loc[:,'BPA_wind':],jul.loc[:,line])
    
    name='aug_reg_NW' + str(line)
    locals()[name].fit(aug.loc[:,'BPA_wind':],aug.loc[:,line])
    
    name='sep_reg_NW' + str(line)
    locals()[name].fit(sep.loc[:,'BPA_wind':],sep.loc[:,line])
    
    name='oct_reg_NW' + str(line)
    locals()[name].fit(oct.loc[:,'BPA_wind':],oct.loc[:,line])
    
    name='nov_reg_NW' + str(line)
    locals()[name].fit(nov.loc[:,'BPA_wind':],nov.loc[:,line])
    
    name='dec_reg_NW' + str(line)
    locals()[name].fit(dec.loc[:,'BPA_wind':],dec.loc[:,line])    

    
    # Make predictions using the testing set
    predicted = []
    rc = np.shape(jan.loc[:,'BPA_wind':])
    n = rc[1] 
    
    for i in range(0,len(y)):
        
        m = df_data.loc[i,'Month']
        
        if m==1:
            s = jan.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='jan_reg_NW' + str(line)
            p = locals()[name].predict(s)

            predicted = np.append(predicted,p)
        elif m==2:
            s = feb.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='feb_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
        elif m==3:
            s = mar.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='mar_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
        elif m==4:
            s = apr.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='apr_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
        elif m==5:
            s = may.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='may_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
        elif m==6:
            s = jun.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='jun_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
        elif m==7:
            s = jul.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='jul_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
        elif m==8:
            s = aug.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='aug_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
        elif m==9:
            s = sep.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='sep_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
        elif m==10:
            s = oct.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='oct_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
        elif m==11:
            s = nov.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='nov_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
        else:
            s = dec.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            
            name='dec_reg_NW' + str(line)
            p = locals()[name].predict(s)
            
            predicted = np.append(predicted,p)
    
    NWPaths_p[:,line_index] = predicted
    
    # Residuals
    residuals = predicted - y.values
    export_residuals[:,line_index] = residuals
    NWPaths_y[:,line_index] = y.values
   
    # RMSE
    RMSE = (np.sum((residuals**2))/len(residuals))**.5
    
#    #R2
#    a=st.pearsonr(y,predicted)
#    print a[0]**2
      
ResidualsNWPaths = export_residuals

###############################
#        Other CA PATHS 
###############################

#import data
df_data1 = pd.read_excel('Synthetic_demand_pathflows/OtherCA_Path_data.xlsx',sheet_name='Daily',header=0)

#find average temps 
cities = ['Salem','Seattle','Portland','Eugene','Boise','Tuscon','Phoenix','Vegas','Fresno','Oakland','LA','SanDiego','Sacramento','SanJose','SanFran']
num_cities = len(cities)
num_days = len(df_data1)

AvgT = np.zeros((num_days,num_cities))
Wind = np.zeros((num_days,num_cities))

for i in cities:
    n1 = i + '_AvgT'
    n2 = i + '_Wind'
    
    j = int(cities.index(i))
    
    AvgT[:,j] = df_data1.loc[:,n1] 
    Wind[:,j] = df_data1.loc[:,n2]
       
#convert to degree days
HDD = np.zeros((num_days,num_cities))
CDD = np.zeros((num_days,num_cities))

for i in range(0,num_days):
    for j in range(0,num_cities):
        HDD[i,j] = np.max((0,65-AvgT[i,j]))
        CDD[i,j] = np.max((0,AvgT[i,j] - 65))

#separate wind speed by cooling/heating degree day
binary_CDD = CDD>0
binary_HDD = HDD>0
CDD_wind = np.multiply(Wind,binary_CDD)
HDD_wind = np.multiply(Wind,binary_HDD)

X1 = np.array(df_data1.loc[:,'Month':'Path66'])
X2 = np.column_stack((HDD,CDD,HDD_wind,CDD_wind))
cX = np.column_stack((X1,X2))
df_data = pd.DataFrame(cX)
df_data.rename(columns={0:'Month'}, inplace=True)
df_data.rename(columns={3:'Path61'}, inplace=True)
df_data.rename(columns={4:'Path42'}, inplace=True)
df_data.rename(columns={5:'Path24'}, inplace=True)
df_data.rename(columns={6:'Path45'}, inplace=True)
df_data.rename(columns={7:'BPA_wind'}, inplace=True)

jan = df_data.loc[df_data['Month'] == 1,:]
feb = df_data.loc[df_data['Month'] == 2,:]
mar = df_data.loc[df_data['Month'] == 3,:]
apr = df_data.loc[df_data['Month'] == 4,:]
may = df_data.loc[df_data['Month'] == 5,:]
jun = df_data.loc[df_data['Month'] == 6,:]
jul = df_data.loc[df_data['Month'] == 7,:]
aug = df_data.loc[df_data['Month'] == 8,:]
sep = df_data.loc[df_data['Month'] == 9,:]
oct = df_data.loc[df_data['Month'] == 10,:]
nov = df_data.loc[df_data['Month'] == 11,:]
dec = df_data.loc[df_data['Month'] == 12,:] 

lines = ['Path61','Path42','Path24','Path45']
num_lines = len(lines)

export_residuals = np.zeros((len(cX),num_lines))
OtherCA_Paths_p= np.zeros((len(cX),num_lines))
OtherCA_Paths_y = np.zeros((len(cX),num_lines))

for line in lines:
    
    y = df_data.loc[:,line]
    line_index = lines.index(line)
    
    #multivariate regression
    
    name_1='jan_reg_CA' + str(line)   
    name_2='feb_reg_CA' + str(line)   
    name_3='mar_reg_CA' + str(line)
    name_4='apr_reg_CA' + str(line)
    name_5='may_reg_CA' + str(line)
    name_6='jun_reg_CA' + str(line) 
    name_7='jul_reg_CA' + str(line)    
    name_8='aug_reg_CA' + str(line)   
    name_9='sep_reg_CA' + str(line)    
    name_10='oct_reg_CA' + str(line)  
    name_11='nov_reg_CA' + str(line)    
    name_12='dec_reg_CA' + str(line)
        

    locals()[name_1] = linear_model.LinearRegression()
    locals()[name_2] = linear_model.LinearRegression()
    locals()[name_3] = linear_model.LinearRegression()
    locals()[name_4] = linear_model.LinearRegression()
    locals()[name_5] = linear_model.LinearRegression()
    locals()[name_6] = linear_model.LinearRegression()
    locals()[name_7] = linear_model.LinearRegression()
    locals()[name_8] = linear_model.LinearRegression()
    locals()[name_9] = linear_model.LinearRegression()
    locals()[name_10] = linear_model.LinearRegression()
    locals()[name_11] = linear_model.LinearRegression()
    locals()[name_12] = linear_model.LinearRegression()


    
    # Train the model using the training sets
    locals()[name_1].fit(jan.loc[:,'BPA_wind':],jan.loc[:,line])
    locals()[name_2].fit(feb.loc[:,'BPA_wind':],feb.loc[:,line])
    locals()[name_3].fit(mar.loc[:,'BPA_wind':],mar.loc[:,line])
    locals()[name_4].fit(apr.loc[:,'BPA_wind':],apr.loc[:,line])
    locals()[name_5].fit(may.loc[:,'BPA_wind':],may.loc[:,line])
    locals()[name_6].fit(jun.loc[:,'BPA_wind':],jun.loc[:,line])
    locals()[name_7].fit(jul.loc[:,'BPA_wind':],jul.loc[:,line])
    locals()[name_8].fit(aug.loc[:,'BPA_wind':],aug.loc[:,line])
    locals()[name_9].fit(sep.loc[:,'BPA_wind':],sep.loc[:,line])
    locals()[name_10].fit(oct.loc[:,'BPA_wind':],oct.loc[:,line])
    locals()[name_11].fit(nov.loc[:,'BPA_wind':],nov.loc[:,line])
    locals()[name_12].fit(dec.loc[:,'BPA_wind':],dec.loc[:,line])

    
    # Make predictions using the testing set
    predicted = []
    rc = np.shape(jan.loc[:,'BPA_wind':])
    n = rc[1] 
    
    for i in range(0,len(y)):
        
        m = df_data.loc[i,'Month']
        
        if m==1:
            s = jan.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_1].predict(s)
            predicted = np.append(predicted,p)
        elif m==2:
            s = feb.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_2].predict(s)
            predicted = np.append(predicted,p)
        elif m==3:
            s = mar.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_3].predict(s)
            predicted = np.append(predicted,p)
        elif m==4:
            s = apr.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_4].predict(s)
            predicted = np.append(predicted,p)
        elif m==5:
            s = may.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_5].predict(s)
            predicted = np.append(predicted,p)
        elif m==6:
            s = jun.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_6].predict(s)
            predicted = np.append(predicted,p)
        elif m==7:
            s = jul.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_7].predict(s)
            predicted = np.append(predicted,p)
        elif m==8:
            s = aug.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_8].predict(s)
            predicted = np.append(predicted,p)
        elif m==9:
            s = sep.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_9].predict(s)
            predicted = np.append(predicted,p)
        elif m==10:
            s = oct.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_10].predict(s)
            predicted = np.append(predicted,p)
        elif m==11:
            s = nov.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_11].predict(s)
            predicted = np.append(predicted,p)
        else:
            s = dec.loc[i,'BPA_wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_12].predict(s)
            predicted = np.append(predicted,p)
       
    OtherCA_Paths_p[:,line_index] = predicted
    
    # Residuals
    residuals = predicted - y.values
    export_residuals[:,line_index] = residuals
    OtherCA_Paths_y[:,line_index] = y.values
   
    # RMSE
    RMSE = (np.sum((residuals**2))/len(residuals))**.5
    
#    #R2
#    a=st.pearsonr(y,predicted)
#    print a[0]**2

    
ResidualsOtherCA_Paths = export_residuals

##########################
#    PATH 65 & 66
##########################

#import data
df_data1 = pd.read_excel('Synthetic_demand_pathflows/Path65_66_regression_data.xlsx',sheet_name='Sheet1',header=0)

#find average temps 
cities = ['Salem','Seattle','Portland','Eugene','Boise','Fresno','Oakland','LA','SanDiego','Sacramento','SanJose','SanFran']
num_cities = len(cities)
num_days = len(df_data1)

AvgT = np.zeros((num_days,num_cities))
Wind = np.zeros((num_days,num_cities))

for i in cities:
    n1 = i + '_AvgT'
    n2 = i + '_Wind'
    
    j = int(cities.index(i))
    
    AvgT[:,j] = df_data1.loc[:,n1] 
    Wind[:,j] = df_data1.loc[:,n2]
       
#convert to degree days
HDD = np.zeros((num_days,num_cities))
CDD = np.zeros((num_days,num_cities))

for i in range(0,num_days):
    for j in range(0,num_cities):
        HDD[i,j] = np.max((0,65-AvgT[i,j]))
        CDD[i,j] = np.max((0,AvgT[i,j] - 65))

#separate wind speed by cooling/heating degree day
binary_CDD = CDD>0
binary_HDD = HDD>0
CDD_wind = np.multiply(Wind,binary_CDD)
HDD_wind = np.multiply(Wind,binary_HDD)

X1 = np.array(df_data1.loc[:,'Month':'Weekday'])
X2 = np.column_stack((HDD,CDD,HDD_wind,CDD_wind))
cX = np.column_stack((X1,X2))
df_data = pd.DataFrame(cX)
df_data.rename(columns={0:'Month'}, inplace=True)
df_data.rename(columns={3:'Path65'}, inplace=True)
df_data.rename(columns={4:'Path66'}, inplace=True)
df_data.rename(columns={5:'Wind'}, inplace=True)

jan = df_data.loc[df_data['Month'] == 1,:]
feb = df_data.loc[df_data['Month'] == 2,:]
mar = df_data.loc[df_data['Month'] == 3,:]
apr = df_data.loc[df_data['Month'] == 4,:]
may = df_data.loc[df_data['Month'] == 5,:]
jun = df_data.loc[df_data['Month'] == 6,:]
jul = df_data.loc[df_data['Month'] == 7,:]
aug = df_data.loc[df_data['Month'] == 8,:]
sep = df_data.loc[df_data['Month'] == 9,:]
oct = df_data.loc[df_data['Month'] == 10,:]
nov = df_data.loc[df_data['Month'] == 11,:]
dec = df_data.loc[df_data['Month'] == 12,:] 

lines = ['Path65','Path66']

num_lines = len(lines)

export_residuals = np.zeros((len(cX),num_lines))
Path65_66_p = np.zeros((len(cX),num_lines))
Path65_66_y = np.zeros((len(cX),num_lines))

for line in lines:
    
    y = df_data.loc[:,line]
    line_index = lines.index(line)
    
    #multivariate regression

    name_1='jan_reg_6566' + str(line)   
    name_2='feb_reg_6566' + str(line)   
    name_3='mar_reg_6566' + str(line)
    name_4='apr_reg_6566' + str(line)
    name_5='may_reg_6566' + str(line)
    name_6='jun_reg_6566' + str(line) 
    name_7='jul_reg_6566' + str(line)    
    name_8='aug_reg_6566' + str(line)   
    name_9='sep_reg_6566' + str(line)    
    name_10='oct_reg_6566' + str(line)  
    name_11='nov_reg_6566' + str(line)    
    name_12='dec_reg_6566' + str(line)
    
    locals()[name_1] = linear_model.LinearRegression()
    locals()[name_2] = linear_model.LinearRegression()
    locals()[name_3] = linear_model.LinearRegression()
    locals()[name_4] = linear_model.LinearRegression()
    locals()[name_5] = linear_model.LinearRegression()
    locals()[name_6] = linear_model.LinearRegression()
    locals()[name_7] = linear_model.LinearRegression()
    locals()[name_8] = linear_model.LinearRegression()
    locals()[name_9] = linear_model.LinearRegression()
    locals()[name_10] = linear_model.LinearRegression()
    locals()[name_11] = linear_model.LinearRegression()
    locals()[name_12] = linear_model.LinearRegression()
    
    
    # Train the model using the training sets
    locals()[name_1].fit(jan.loc[:,'Wind':],jan.loc[:,line])
    locals()[name_2].fit(feb.loc[:,'Wind':],feb.loc[:,line])
    locals()[name_3].fit(mar.loc[:,'Wind':],mar.loc[:,line])
    locals()[name_4].fit(apr.loc[:,'Wind':],apr.loc[:,line])
    locals()[name_5].fit(may.loc[:,'Wind':],may.loc[:,line])
    locals()[name_6].fit(jun.loc[:,'Wind':],jun.loc[:,line])
    locals()[name_7].fit(jul.loc[:,'Wind':],jul.loc[:,line])
    locals()[name_8].fit(aug.loc[:,'Wind':],aug.loc[:,line])
    locals()[name_9].fit(sep.loc[:,'Wind':],sep.loc[:,line])
    locals()[name_10].fit(oct.loc[:,'Wind':],oct.loc[:,line])
    locals()[name_11].fit(nov.loc[:,'Wind':],nov.loc[:,line])
    locals()[name_12].fit(dec.loc[:,'Wind':],dec.loc[:,line])
    

    
    # Make predictions using the testing set
    predicted = []
    rc = np.shape(jan.loc[:,'Wind':])
    n = rc[1] 
    
    for i in range(0,len(y)):
        
        m = df_data.loc[i,'Month']
        
        if m==1:
            s = jan.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_1].predict(s)
            predicted = np.append(predicted,p)
        elif m==2:
            s = feb.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_2].predict(s)
            predicted = np.append(predicted,p)
        elif m==3:
            s = mar.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_3].predict(s)
            predicted = np.append(predicted,p)
        elif m==4:
            s = apr.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_4].predict(s)
            predicted = np.append(predicted,p)
        elif m==5:
            s = may.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_5].predict(s)
            predicted = np.append(predicted,p)
        elif m==6:
            s = jun.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_6].predict(s)
            predicted = np.append(predicted,p)
        elif m==7:
            s = jul.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_7].predict(s)
            predicted = np.append(predicted,p)
        elif m==8:
            s = aug.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_8].predict(s)
            predicted = np.append(predicted,p)
        elif m==9:
            s = sep.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_9].predict(s)
            predicted = np.append(predicted,p)
        elif m==10:
            s = oct.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_10].predict(s)
            predicted = np.append(predicted,p)
        elif m==11:
            s = nov.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_11].predict(s)
            predicted = np.append(predicted,p)
        else:
            s = dec.loc[i,'Wind':]
            s = np.reshape(s[:,None],(1,n))
            p = locals()[name_12].predict(s)
            predicted = np.append(predicted,p)
    
    
    Path65_66_p[:,line_index] = predicted
    Path65_66_y[:,line_index] = y.values
    
    # Residuals
    residuals = predicted - y.values
    export_residuals[:,line_index] = residuals
#    
    # RMSE
    RMSE = (np.sum((residuals**2))/len(residuals))**.5
    
    #R2
#    a=st.pearsonr(y,predicted)
#    print a[0]**2
    
    Residuals65_66 = export_residuals[730:,:]


#####################################################################
#                       Residual Analysis
#####################################################################
    
R = np.column_stack((ResidualsLoad,ResidualsNWPaths,ResidualsOtherCA_Paths,Residuals46,Residuals65_66))

rc = np.shape(R)
cols = rc[1]
mus = np.zeros((cols,1))
stds = np.zeros((cols,1))
R_w = np.zeros(np.shape(R))
sim_days = len(R_w)

#whiten residuals
for i in range(0,cols):
    mus[i] = np.mean(R[:,i])
    stds[i] = np.std(R[:,i])
    R_w[:,i] = (R[:,i] - mus[i])/stds[i]

#Vector autoregressive model on residuals
model = VAR(R_w)
results = model.fit(1)
sim_residuals = np.zeros((sim_days,cols))
errors = np.zeros((sim_days,cols))
p = results.params
y_seeds = R_w[-1]
C = results.sigma_u
means = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
E  = np.random.multivariate_normal(means,C,sim_days)
ys = np.zeros((cols,1))

# Generate cross correlated residuals
for i in range(0,sim_days):
    
    for j in range(1,cols+1):
        name='y' + str(j) 
        locals()[name]= p[0,j-1] + p[1,j-1]*y_seeds[0]+ p[2,j-1]*y_seeds[1]+ p[3,j-1]*y_seeds[2]+ p[4,j-1]*y_seeds[3]+ p[5,j-1]*y_seeds[4]+ p[6,j-1]*y_seeds[5]+ p[7,j-1]*y_seeds[6]+ p[8,j-1]*y_seeds[7]+ p[9,j-1]*y_seeds[8]+ p[10,j-1]*y_seeds[9]+ p[11,j-1]*y_seeds[10]+ p[12,j-1]*y_seeds[11]+ p[13,j-1]*y_seeds[12]+ p[13,j-1]*y_seeds[12]+ p[14,j-1]*y_seeds[13]+ p[15,j-1]*y_seeds[14]+E[i,j-1]

    for j in range(1,cols+1):
        name='y' + str(j) 
        y_seeds[j-1]=locals()[name]
    
    sim_residuals[i,:] = [y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15]
            

for i in range(0,cols):
    sim_residuals[:,i] = sim_residuals[:,i]*stds[i]*(1/np.std(sim_residuals[:,i])) + mus[i]

#validation
Y = np.column_stack((np.reshape(BPA_y[0:3*365],(1095,1)),np.reshape(SDGE_y[0:3*365],(1095,1)),np.reshape(SCE_y[0:3*365],(1095,1)),np.reshape(PGEV_y[0:3*365],(1095,1)),np.reshape(PGEB_y[0:3*365],(1095,1)),NWPaths_y,OtherCA_Paths_y,np.reshape(Path46_y[730:],(1095,1)),np.reshape(Path65_66_y[730:,:],(1095,2))))

combined_BPA = np.reshape(sim_residuals[:,0],(1095,1)) + np.reshape(BPA_p[0:3*365],(1095,1))
combined_SDGE = np.reshape(sim_residuals[:,1],(1095,1)) + np.reshape(SDGE_p[0:3*365],(1095,1))
combined_SCE = np.reshape(sim_residuals[:,2],(1095,1)) + np.reshape(SCE_p[0:3*365],(1095,1))
combined_PGEV = np.reshape(sim_residuals[:,3],(1095,1)) + np.reshape(PGEV_p[0:3*365],(1095,1))
combined_PGEB = np.reshape(sim_residuals[:,4],(1095,1)) + np.reshape(PGEB_p[0:3*365],(1095,1))
combined_Path8 = np.reshape(sim_residuals[:,5],(1095,1)) + np.reshape(NWPaths_p[:,0],(1095,1))
combined_Path14 = np.reshape(sim_residuals[:,6],(1095,1)) + np.reshape(NWPaths_p[:,1],(1095,1))
combined_Path3 = np.reshape(sim_residuals[:,7],(1095,1)) + np.reshape(NWPaths_p[:,2],(1095,1))
combined_Path61 = np.reshape(sim_residuals[:,8],(1095,1)) + np.reshape(OtherCA_Paths_p[:,0],(1095,1))
combined_Path42 = np.reshape(sim_residuals[:,9],(1095,1)) + np.reshape(OtherCA_Paths_p[:,1],(1095,1))
combined_Path24 = np.reshape(sim_residuals[:,10],(1095,1)) + np.reshape(OtherCA_Paths_p[:,2],(1095,1))
combined_Path45 = np.reshape(sim_residuals[:,11],(1095,1)) + np.reshape(OtherCA_Paths_p[:,3],(1095,1))
combined_Path46 = np.reshape(sim_residuals[:,12],(1095,1)) + np.reshape(Path46_p[730:],(1095,1))
combined_Path65 = np.reshape(sim_residuals[:,13],(1095,1)) + np.reshape(Path65_66_p[730:,0],(1095,1))
combined_Path66 = np.reshape(sim_residuals[:,14],(1095,1)) + np.reshape(Path65_66_p[730:,1],(1095,1))

combined = np.column_stack((combined_BPA,combined_SDGE,combined_SCE,combined_PGEV,combined_PGEB,combined_Path8,combined_Path14,combined_Path3,combined_Path61,combined_Path42,combined_Path24,combined_Path45,combined_Path46,combined_Path65,combined_Path66))

rc = np.shape(Y)
cols = rc[1]

names = ['BPA','SDGE','SCE','PGEV','PGEB','Path8','Path14','Path3','Path61','Path42','Path24','Path45','Path46','Path65','Path66']

#for n in names:
#    
#    n_index = names.index(n)
#    
#    plt.figure()
#    plt.plot(combined[:,n_index],'r')
#    plt.plot(Y[:,n_index],'b')
#    plt.title(n)
#   

##########################################################################################################################################################
#Simulating demand and path
#########################################################################################################################################################

#Sim Residual
simulation_length=len(sim_weather)
f_horizon = 7

syn_residuals = np.zeros((simulation_length,cols))
errors = np.zeros((simulation_length,cols))
y_seeds = R_w[-1]
C = results.sigma_u
means = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
E  = np.random.multivariate_normal(means,C,simulation_length)
ys = np.zeros((cols,1))


for i in range(0,simulation_length):
    
    for n in range(0,cols):
        
        ys[n] = p[0,n] 
        
        for m in range(0,cols):
    
            ys[n] = ys[n] + p[m+1,n]*y_seeds[n]
            
       
        ys[n] = ys[n] + E[i,n]
        
    for n in range(0,cols):
        y_seeds[n] = ys[n]
        
    syn_residuals[i,:] = np.reshape([ys],(1,cols))
            

for i in range(0,cols):
    syn_residuals[:,i] = syn_residuals[:,i]*stds[i]*(1/np.std(syn_residuals[:,i])) + mus[i]

##################################################
#                    PATH NW
##################################################
#This only uses BPA wind and hydro
col_nw_T =['SALEM_T','SEATTLE_T','PORTLAND_T','EUGENE_T','BOISE_T','TUCSON_T','PHOENIX_T','LAS VEGAS_T','FRESNO_T','OAKLAND_T','LOS ANGELES_T','SAN DIEGO_T','SACRAMENTO_T','SAN JOSE_T','SAN FRANCISCO_T']
col_nw_W =['SALEM_W','SEATTLE_W','PORTLAND_W','EUGENE_W','BOISE_W','TUCSON_W','PHOENIX_W','LAS VEGAS_W','FRESNO_W','OAKLAND_W','LOS ANGELES_W','SAN DIEGO_W','SACRAMENTO_W','SAN JOSE_W','SAN FRANCISCO_W']

num_cities = len(col_nw_T)
NW_sim_T=sim_weather[col_nw_T].values
NW_sim_W=sim_weather[col_nw_W].values

NW_sim_T=sim_weather[col_nw_T].values
NW_sim_W=sim_weather[col_nw_W].values

NW_sim_T_F=(NW_sim_T * 9/5) +32   
NW_sim_W =NW_sim_W *2.23694

HDD_sim = np.zeros((simulation_length,num_cities))
CDD_sim = np.zeros((simulation_length,num_cities))

for i in range(0,simulation_length):
    for j in range(0,num_cities):
        HDD_sim[i,j] = np.max((0,65-NW_sim_T_F[i,j]))
        CDD_sim[i,j] = np.max((0,NW_sim_T_F[i,j] - 65))   

binary_CDD_sim = CDD_sim > 0
binary_HDD_sim = HDD_sim > 0
CDD_wind_sim = np.multiply(NW_sim_W,binary_CDD_sim)
HDD_wind_sim = np.multiply(NW_sim_W,binary_HDD_sim)

#Need Month,Day,Year,8 14 3 BPA_wind，BPA_hydro

for fd in range(0,f_horizon):
    
    filename = 'PNW_hydro/FCRPS/Path_dams_forecast_%d.xlsx' % fd
    sim_BPA_hydro = pd.read_excel(filename, header=0,index_col = 0)
    a=sim_BPA_hydro.values
    
    if fd < 1:
        combined = a
    else:
        combined = np.dstack([combined,a])
    
sim_BPA_hydro=combined
sim_BPA_hydro=np.sum(sim_BPA_hydro,axis=1)/24

#What is the common length
effect_sim_year=int(len(sim_BPA_hydro)/365)
sim_month=sim_month[:len(sim_BPA_hydro)]
sim_day=sim_day[:len(sim_BPA_hydro)]
sim_year=sim_year[:len(sim_BPA_hydro)]
sim_dow= sim_dow[:len(sim_BPA_hydro)]

sim_wind_power=pd.read_csv('Synthetic_wind_power/wind_power_sim.csv',header=0)
sim_BPA_wind_power= sim_wind_power.loc[:,'BPA']/24
sim_wind_daily = np.zeros((effect_sim_year*365,1))

for i in range(0,effect_sim_year*365):
    sim_wind_daily[i] = np.sum((sim_BPA_wind_power.loc[i*24:i*24+24]))

HDD_sim=HDD_sim[365:len(HDD_sim)-730]
CDD_sim=CDD_sim[365:len(CDD_sim)-730]

HDD_wind_sim=HDD_wind_sim[365:len(HDD_wind_sim)-730]
CDD_wind_sim=CDD_wind_sim[365:len(CDD_wind_sim)-730]


for d in range(0,effect_sim_year*365-f_horizon):
    print('PNW Paths %d' % d)
    
    collect_data=np.column_stack((sim_month[d:d+f_horizon],sim_day[d:d+f_horizon],sim_year[d:d+f_horizon],np.zeros(f_horizon),np.zeros(f_horizon),np.zeros(f_horizon),sim_wind_daily[d:d+f_horizon],sim_BPA_hydro[d,:],sim_dow[d:d+f_horizon]))
    collect_data_2=np.column_stack((HDD_sim[d:d+f_horizon],CDD_sim[d:d+f_horizon],HDD_wind_sim[d:d+f_horizon],CDD_wind_sim[d:d+f_horizon]))
    Combined=np.column_stack((collect_data,collect_data_2))
    
#    NEED TO ONLY COLLECT 7 DAYS OF DATA, OR BUILD LARGER MATRICES AND ONLY SELECT FIRST SEVEN
#    FIRST SEVEN FROM HYDRO NEEDS TO BE FORECAST
#    
#    WHERE TO LOOP?
    
    
    df_data_sim = pd.DataFrame(Combined)
    df_data_sim.rename(columns={0:'Month'}, inplace=True)
    df_data_sim.rename(columns={3:'Path8'}, inplace=True)
    df_data_sim.rename(columns={4:'Path14'}, inplace=True)
    df_data_sim.rename(columns={5:'Path3'}, inplace=True)
    df_data_sim.rename(columns={6:'BPA_wind'}, inplace=True)
    df_data_sim.rename(columns={7:'BPA_hydro'}, inplace=True)
    df_data_sim.rename(columns={8:'Weekday'}, inplace=True)
    df_data_sim.rename(columns={9:'Salem_HDD'}, inplace=True)
    
    jan2 = df_data_sim.loc[df_data_sim['Month'] == 1,:]
    feb2 = df_data_sim.loc[df_data_sim['Month'] == 2,:]
    mar2 = df_data_sim.loc[df_data_sim['Month'] == 3,:]
    apr2 = df_data_sim.loc[df_data_sim['Month'] == 4,:]
    may2 = df_data_sim.loc[df_data_sim['Month'] == 5,:]
    jun2 = df_data_sim.loc[df_data_sim['Month'] == 6,:]
    jul2 = df_data_sim.loc[df_data_sim['Month'] == 7,:]
    aug2 = df_data_sim.loc[df_data_sim['Month'] == 8,:]
    sep2 = df_data_sim.loc[df_data_sim['Month'] == 9,:]
    oct2 = df_data_sim.loc[df_data_sim['Month'] == 10,:]
    nov2 = df_data_sim.loc[df_data_sim['Month'] == 11,:]
    dec2 = df_data_sim.loc[df_data_sim['Month'] == 12,:] 
    
    lines = ['Path8','Path14','Path3']
    upper = [1900,1500,1900]
    lower = [-600,-900,-2200]
    
    
    for line in lines:
        name='predicted_' + str(line)   
        locals()[name]=[]
    for line in lines:
        predicted=[]
        rc = np.shape(jan2.loc[:,'BPA_wind':])
        n = rc[1] 
        y = df_data_sim.loc[:,line]
        line_index = lines.index(line)
        
        #regression names
        name_1='jan_reg_NW' + str(line)   
        name_2='feb_reg_NW' + str(line)   
        name_3='mar_reg_NW' + str(line)
        name_4='apr_reg_NW' + str(line)
        name_5='may_reg_NW' + str(line)
        name_6='jun_reg_NW' + str(line) 
        name_7='jul_reg_NW' + str(line)    
        name_8='aug_reg_NW' + str(line)   
        name_9='sep_reg_NW' + str(line)    
        name_10='oct_reg_NW' + str(line)  
        name_11='nov_reg_NW' + str(line)    
        name_12='dec_reg_NW' + str(line)
        
        for i in range(0,len(y)):
            
            m = df_data_sim.loc[i,'Month']
            
            if m==1:
                s = jan2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n)) 
                p = locals()[name_1].predict(s)
                predicted = np.append(predicted,p)
            elif m==2:
                s = feb2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_2].predict(s)
                predicted = np.append(predicted,p)
            elif m==3:
                s = mar2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_3].predict(s)
                predicted = np.append(predicted,p)
            elif m==4:
                s = apr2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_4].predict(s)
                predicted = np.append(predicted,p)
            elif m==5:
                s = may2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_5].predict(s)
                predicted = np.append(predicted,p)
            elif m==6:
                s = jun2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_6].predict(s)
                predicted = np.append(predicted,p)
            elif m==7:
                s = jul2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_7].predict(s)
                predicted = np.append(predicted,p)
            elif m==8:
                s = aug2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_8].predict(s)
                predicted = np.append(predicted,p)
            elif m==9:
                s = sep2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_9].predict(s)
                predicted = np.append(predicted,p)
            elif m==10:
                s = oct2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_10].predict(s)
                predicted = np.append(predicted,p)
            elif m==11:
                s = nov2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_11].predict(s)
                predicted = np.append(predicted,p)
            else:
                s = dec2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_12].predict(s)
                predicted = np.append(predicted,p)
        
            if predicted[i] > upper[line_index]:
                predicted[i] = upper[line_index]
            elif predicted[i] < lower[line_index]:
                predicted[i] = lower[line_index]
        
        name='predicted_' + str(line)              
        locals()[name]=predicted
            
    syn_Path8=predicted_Path8+syn_residuals[d:d+f_horizon,5]
    syn_Path14=predicted_Path14+syn_residuals[d:d+f_horizon,6]
    syn_Path3=predicted_Path3+syn_residuals[d:d+f_horizon,7]
    
    if d < 1:
        
        syn_8M = syn_Path8
        syn_14M = syn_Path14
        syn_3M = syn_Path3
    
    else:
        
        syn_8M = np.column_stack((syn_8M,syn_Path8))
        syn_14M = np.column_stack((syn_14M,syn_Path14))
        syn_3M = np.column_stack((syn_3M,syn_Path3))
    
#    bias = np.mean(syn_Path8) - np.mean(NWPaths_y[:,0])
#    syn_Path8 = syn_Path8 - bias
#    
#    bias = np.mean(syn_Path14) - np.mean(NWPaths_y[:,1])
#    syn_Path14 = syn_Path14 - bias
#    
#    bias = np.mean(syn_Path3) - np.mean(NWPaths_y[:,2])
#    syn_Path3 = syn_Path3 - bias
    
#    S = df_data_sim.values
#    HO = H.values
#    stats = np.zeros((69,4))
#    
#    for i in range(0,69):
#        stats[i,0] = np.mean(S[:,i])
#        stats[i,1] = np.mean(HO[:,i])
#        stats[i,2] = np.std(S[:,i])
#        stats[i,3] = np.std(HO[:,i])
    

################################################################################
###################################################
##                 PATH 65 & 66
###################################################
col_6566_T = ['SALEM_T','SEATTLE_T','PORTLAND_T','EUGENE_T','BOISE_T','FRESNO_T','OAKLAND_T','LOS ANGELES_T','SAN DIEGO_T','SACRAMENTO_T','SAN JOSE_T','SAN FRANCISCO_T']    
col_6566_W = ['SALEM_W','SEATTLE_W','PORTLAND_W','EUGENE_W','BOISE_W','FRESNO_W','OAKLAND_W','LOS ANGELES_W','SAN DIEGO_W','SACRAMENTO_W','SAN JOSE_W','SAN FRANCISCO_W']    
num_cities = len(col_6566_T)

P6566_sim_T=sim_weather[col_6566_T].values
P6566_sim_W=sim_weather[col_6566_W].values

P6566_sim_W =P6566_sim_W*2.23694

sim_days = len(sim_weather)
P6566_sim_T_F=(P6566_sim_T * 9/5) +32 

HDD_sim = np.zeros((simulation_length,num_cities))
CDD_sim = np.zeros((simulation_length,num_cities))

for i in range(0,simulation_length):
    for j in range(0,num_cities):
        HDD_sim[i,j] = np.max((0,65-P6566_sim_T_F[i,j]))
        CDD_sim[i,j] = np.max((0,P6566_sim_T_F[i,j] - 65))  

binary_CDD_sim = CDD_sim > 0
binary_HDD_sim = HDD_sim > 0

CDD_wind_sim = np.multiply(P6566_sim_W,binary_CDD_sim)
HDD_wind_sim = np.multiply(P6566_sim_W,binary_HDD_sim)

HDD_sim=HDD_sim[365:len(HDD_sim)-730]
CDD_sim=CDD_sim[365:len(CDD_sim)-730]

HDD_wind_sim=HDD_wind_sim[365:len(HDD_wind_sim)-730]
CDD_wind_sim=CDD_wind_sim[365:len(CDD_wind_sim)-730]


for d in range(0,effect_sim_year*365-f_horizon):
    
    print('Paths 65 & 66 %d' % d)
    
    collect_data=np.column_stack((sim_month[d:d+f_horizon],sim_day[d:d+f_horizon],sim_year[d:d+f_horizon],np.zeros(f_horizon),np.zeros(f_horizon),sim_wind_daily[d:d+f_horizon],sim_BPA_hydro[d,:],syn_3M[:,d],syn_8M[:,d],syn_14M[:,d],sim_dow[d:d+f_horizon]))
    collect_data_2=np.column_stack((HDD_sim[d:d+f_horizon],CDD_sim[d:d+f_horizon],HDD_wind_sim[d:d+f_horizon],CDD_wind_sim[d:d+f_horizon]))
    Combined=np.column_stack((collect_data,collect_data_2))

    df_data_sim = pd.DataFrame(Combined)
    df_data_sim.rename(columns={0:'Month'}, inplace=True)
    df_data_sim.rename(columns={3:'Path65'}, inplace=True)
    df_data_sim.rename(columns={4:'Path66'}, inplace=True)
    df_data_sim.rename(columns={5:'Wind'}, inplace=True)
    
    jan2 = df_data_sim.loc[df_data_sim['Month'] == 1,:]
    feb2 = df_data_sim.loc[df_data_sim['Month'] == 2,:]
    mar2 = df_data_sim.loc[df_data_sim['Month'] == 3,:]
    apr2 = df_data_sim.loc[df_data_sim['Month'] == 4,:]
    may2 = df_data_sim.loc[df_data_sim['Month'] == 5,:]
    jun2 = df_data_sim.loc[df_data_sim['Month'] == 6,:]
    jul2 = df_data_sim.loc[df_data_sim['Month'] == 7,:]
    aug2 = df_data_sim.loc[df_data_sim['Month'] == 8,:]
    sep2 = df_data_sim.loc[df_data_sim['Month'] == 9,:]
    oct2 = df_data_sim.loc[df_data_sim['Month'] == 10,:]
    nov2 = df_data_sim.loc[df_data_sim['Month'] == 11,:]
    dec2 = df_data_sim.loc[df_data_sim['Month'] == 12,:] 
    
    lines = ['Path65','Path66']
    upper = [3100,4300]
    lower = [-2210,-500]
    
    for line in lines:
        name='predicted_' + str(line)   
        locals()[name]=[]
        
    for line in lines:    
        predicted=[]
        rc = np.shape(jan2.loc[:,'Wind':])
        n = rc[1] 
        y = df_data_sim.loc[:,line]
        line_index = lines.index(line)
    
        #regression names
        name_1='jan_reg_6566' + str(line)   
        name_2='feb_reg_6566' + str(line)   
        name_3='mar_reg_6566' + str(line)
        name_4='apr_reg_6566' + str(line)
        name_5='may_reg_6566' + str(line)
        name_6='jun_reg_6566' + str(line) 
        name_7='jul_reg_6566' + str(line)    
        name_8='aug_reg_6566' + str(line)   
        name_9='sep_reg_6566' + str(line)    
        name_10='oct_reg_6566' + str(line)  
        name_11='nov_reg_6566' + str(line)    
        name_12='dec_reg_6566' + str(line)
        
        for i in range(0,len(y)):
            
            m = df_data_sim.loc[i,'Month']
            
            if m==1:
                s = jan2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_1].predict(s)
                predicted = np.append(predicted,p)
            elif m==2:
                s = feb2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_2].predict(s)
                predicted = np.append(predicted,p)
            elif m==3:
                s = mar2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_3].predict(s)
                predicted = np.append(predicted,p)
            elif m==4:
                s = apr2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_4].predict(s)
                predicted = np.append(predicted,p)
            elif m==5:
                s = may2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_5].predict(s)
                predicted = np.append(predicted,p)
            elif m==6:
                s = jun2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_6].predict(s)
                predicted = np.append(predicted,p)
            elif m==7:
                s = jul2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_7].predict(s)
                predicted = np.append(predicted,p)
            elif m==8:
                s = aug2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_8].predict(s)
                predicted = np.append(predicted,p)
            elif m==9:
                s = sep2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_9].predict(s)
                predicted = np.append(predicted,p)
            elif m==10:
                s = oct2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_10].predict(s)
                predicted = np.append(predicted,p)
            elif m==11:
                s = nov2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_11].predict(s)
                predicted = np.append(predicted,p)
            else:
                s = dec2.loc[i,'Wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_12].predict(s)
                predicted = np.append(predicted,p)
                
            if predicted[i] > upper[line_index]:
                predicted[i] = upper[line_index]
            elif predicted[i] < lower[line_index]:
                predicted[i] = lower[line_index]
                
    
        name='predicted_' + str(line)              
        locals()[name]=predicted
    
    syn_Path65= predicted_Path65 + syn_residuals[d:d+f_horizon,13]
    syn_Path66 = predicted_Path66 + syn_residuals[d:d+f_horizon,14]
    
    if d < 1:
        
        syn_65M = syn_Path65
        syn_66M = syn_Path66
    
    else:
        
        syn_65M = np.column_stack((syn_65M,syn_Path65))
        syn_66M = np.column_stack((syn_66M,syn_Path66))


#bias = np.mean(syn_Path65) - np.mean(Path65_66_y[:,0])
#syn_Path65 = syn_Path65 - bias
#
#bias = np.mean(syn_Path66) - np.mean(Path65_66_y[:,1])
#syn_Path66 = syn_Path66 - bias

###################################################
##                    PATH 46
###################################################

#Find the simulated data at the sites
col_46_T = ['TUCSON_T','PHOENIX_T','LAS VEGAS_T','FRESNO_T','OAKLAND_T','LOS ANGELES_T','SAN DIEGO_T','SACRAMENTO_T','SAN JOSE_T','SAN FRANCISCO_T']
col_46_W = ['TUCSON_W','PHOENIX_W','LAS VEGAS_W','FRESNO_W','OAKLAND_W','LOS ANGELES_W','SAN DIEGO_W','SACRAMENTO_W','SAN JOSE_W','SAN FRANCISCO_W']

num_cities = len(col_46_T)

P46_sim_T=sim_weather[col_46_T].values
P46_sim_W=sim_weather[col_46_W].values

P46_sim_W =P46_sim_W *2.23694

sim_days = len(sim_weather)

P46_sim_T_F=(P46_sim_T * 9/5) +32 

HDD_sim = np.zeros((simulation_length,num_cities))
CDD_sim = np.zeros((simulation_length,num_cities))

for i in range(0,simulation_length):
    for j in range(0,num_cities):
        HDD_sim[i,j] = np.max((0,65-P46_sim_T_F[i,j]))
        CDD_sim[i,j] = np.max((0,P46_sim_T_F[i,j] - 65))  

binary_CDD_sim = CDD_sim > 0
binary_HDD_sim = HDD_sim > 0


CDD_wind_sim = np.multiply(P46_sim_W,binary_CDD_sim)
HDD_wind_sim = np.multiply(P46_sim_W,binary_HDD_sim)

HDD_sim=HDD_sim[365:len(HDD_sim)-730]
CDD_sim=CDD_sim[365:len(CDD_sim)-730]

HDD_wind_sim=HDD_wind_sim[365:len(HDD_wind_sim)-730]
CDD_wind_sim=CDD_wind_sim[365:len(CDD_wind_sim)-730]

sim_Hoover = pd.read_csv('Synthetic_streamflows/synthetic_discharge_Hoover.csv',header=None)
sim_Hoover=sim_Hoover.values
sim_Hoover = sim_Hoover[:effect_sim_year*365]

for d in range(0,effect_sim_year*365-f_horizon):

    print('Path 46 %d' % d)

    collect_data=np.column_stack((sim_month[d:d+f_horizon],sim_day[d:d+f_horizon],sim_year[d:d+f_horizon],np.zeros(f_horizon),sim_dow[d:d+f_horizon],sim_Hoover[d:d+f_horizon],syn_65M[:,d],syn_66M[:,d]))
    collect_data_2=np.column_stack((HDD_sim[d:d+f_horizon],CDD_sim[d:d+f_horizon],HDD_wind_sim[d:d+f_horizon],CDD_wind_sim[d:d+f_horizon]))
    Combined=np.column_stack((collect_data,collect_data_2))
    df_data_sim = pd.DataFrame(Combined)
    
    df_data_sim.rename(columns={0:'Month'}, inplace=True)
    df_data_sim.rename(columns={3:'Path46'}, inplace=True)
    df_data_sim.rename(columns={4:'Weekday'}, inplace=True)
    
    jan2 = df_data_sim.loc[df_data_sim['Month'] == 1,:]
    feb2 = df_data_sim.loc[df_data_sim['Month'] == 2,:]
    mar2 = df_data_sim.loc[df_data_sim['Month'] == 3,:]
    apr2 = df_data_sim.loc[df_data_sim['Month'] == 4,:]
    may2 = df_data_sim.loc[df_data_sim['Month'] == 5,:]
    jun2 = df_data_sim.loc[df_data_sim['Month'] == 6,:]
    jul2 = df_data_sim.loc[df_data_sim['Month'] == 7,:]
    aug2 = df_data_sim.loc[df_data_sim['Month'] == 8,:]
    sep2 = df_data_sim.loc[df_data_sim['Month'] == 9,:]
    oct2 = df_data_sim.loc[df_data_sim['Month'] == 10,:]
    nov2 = df_data_sim.loc[df_data_sim['Month'] == 11,:]
    dec2 = df_data_sim.loc[df_data_sim['Month'] == 12,:] 
    
    y = df_data_sim.loc[:,'Path46']
    
    predicted_Path46 =[]
    rc = np.shape(jan2.loc[:,'Weekday':])
    n = rc[1] 
    
    upper = 185000
    lower = 48000
    
    predicted=[]
    for i in range(0,len(y)):
        
        m = df_data_sim.loc[i,'Month']
        
        if m==1:
            s = jan2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = jan_reg_46.predict(s)
            predicted = np.append(predicted,p)
        elif m==2:
            s = feb2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = feb_reg_46.predict(s)
            predicted = np.append(predicted,p)
        elif m==3:
            s = mar2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = mar_reg_46.predict(s)
            predicted = np.append(predicted,p)
        elif m==4:
            s = apr2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = apr_reg_46.predict(s)
            predicted = np.append(predicted,p)
        elif m==5:
            s = may2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = may_reg_46.predict(s)
            predicted = np.append(predicted,p)
        elif m==6:
            s = jun2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = jun_reg_46.predict(s)
            predicted = np.append(predicted,p)
        elif m==7:
            s = jul2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = jul_reg_46.predict(s)
            predicted = np.append(predicted,p)
        elif m==8:
            s = aug2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = aug_reg_46.predict(s)
            predicted = np.append(predicted,p)
        elif m==9:
            s = sep2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = sep_reg_46.predict(s)
            predicted = np.append(predicted,p)
        elif m==10:
            s = oct2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = oct_reg_46.predict(s)
            predicted = np.append(predicted,p)
        elif m==11:
            s = nov2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = nov_reg_46.predict(s)
            predicted = np.append(predicted,p)
        else:
            s = dec2.loc[i,'Weekday':]
            s = np.reshape(s[:,None],(1,n))
            p = dec_reg_46.predict(s)
            predicted = np.append(predicted,p)
            
        if predicted[i] > upper:
            predicted[i] = upper
        elif predicted[i] < lower:
            predicted[i] = lower  
            
    predicted_Path46=predicted
    
    syn_Path46=predicted_Path46+syn_residuals[d:d+f_horizon,12]
        
#    bias = np.mean(syn_Path46) - np.mean(Path46_y)
#    syn_Path46 = syn_Path46 - bias
    syn_Path46 = syn_Path46/24
    
    if d < 1:
        
        syn_46M = syn_Path46
    
    else:
        
        syn_46M = np.column_stack((syn_46M,syn_Path46))
        
    
    
################################
##        Other CA PATHS 
################################
col_ca_T = ['SALEM_T','SEATTLE_T','PORTLAND_T','EUGENE_T','BOISE_T','TUCSON_T','PHOENIX_T','LAS VEGAS_T','FRESNO_T','OAKLAND_T','LOS ANGELES_T','SAN DIEGO_T','SACRAMENTO_T','SAN JOSE_T','SAN FRANCISCO_T']
col_ca_W = ['SALEM_W','SEATTLE_W','PORTLAND_W','EUGENE_W','BOISE_W','TUCSON_W','PHOENIX_W','LAS VEGAS_W','FRESNO_W','OAKLAND_W','LOS ANGELES_W','SAN DIEGO_W','SACRAMENTO_W','SAN JOSE_W','SAN FRANCISCO_W']

num_cities = len(col_ca_T)
CA_sim_T=sim_weather[col_ca_T].values
CA_sim_W=sim_weather[col_ca_W].values

CA_sim_W =CA_sim_W *2.23694
CA_sim_T_F=(CA_sim_T * 9/5) +32   

HDD_sim = np.zeros((simulation_length,num_cities))
CDD_sim = np.zeros((simulation_length,num_cities))

for i in range(0,simulation_length):
    for j in range(0,num_cities):
        HDD_sim[i,j] = np.max((0,65-CA_sim_T_F[i,j]))
        CDD_sim[i,j] = np.max((0,CA_sim_T_F[i,j] - 65))  

binary_CDD_sim = CDD_sim > 0
binary_HDD_sim = HDD_sim > 0


CDD_wind_sim = np.multiply(CA_sim_W,binary_CDD_sim)
HDD_wind_sim = np.multiply(CA_sim_W,binary_HDD_sim)

HDD_sim=HDD_sim[365:len(HDD_sim)-730]
CDD_sim=CDD_sim[365:len(CDD_sim)-730]

HDD_wind_sim=HDD_wind_sim[365:len(HDD_wind_sim)-730]
CDD_wind_sim=CDD_wind_sim[365:len(CDD_wind_sim)-730]

for d in range(0,effect_sim_year*365-f_horizon):
    
    print('Other CA Paths %d' % d)
    
    collect_data=np.column_stack((sim_month[d:d+f_horizon],sim_day[d:d+f_horizon],sim_year[d:d+f_horizon],np.zeros(f_horizon),np.zeros(f_horizon),np.zeros(f_horizon),np.zeros(f_horizon),sim_wind_daily[d:d+f_horizon],sim_BPA_hydro[d,:],sim_dow[d:d+f_horizon],syn_46M[:,d],sim_Hoover[d:d+f_horizon],syn_65M[:,d],syn_66M[:,d]))
    collect_data_2=np.column_stack((HDD_sim[d:d+f_horizon],CDD_sim[d:d+f_horizon],HDD_wind_sim[d:d+f_horizon],CDD_wind_sim[d:d+f_horizon]))
    Combined=np.column_stack((collect_data,collect_data_2))
    df_data_sim = pd.DataFrame(Combined)
    
    df_data_sim.rename(columns={0:'Month'}, inplace=True)
    df_data_sim.rename(columns={3:'Path61'}, inplace=True)
    df_data_sim.rename(columns={4:'Path42'}, inplace=True)
    df_data_sim.rename(columns={5:'Path24'}, inplace=True)
    df_data_sim.rename(columns={6:'Path45'}, inplace=True)
    df_data_sim.rename(columns={7:'BPA_wind'}, inplace=True)
    
    jan2 = df_data_sim.loc[df_data_sim['Month'] == 1,:]
    feb2 = df_data_sim.loc[df_data_sim['Month'] == 2,:]
    mar2 = df_data_sim.loc[df_data_sim['Month'] == 3,:]
    apr2 = df_data_sim.loc[df_data_sim['Month'] == 4,:]
    may2 = df_data_sim.loc[df_data_sim['Month'] == 5,:]
    jun2 = df_data_sim.loc[df_data_sim['Month'] == 6,:]
    jul2 = df_data_sim.loc[df_data_sim['Month'] == 7,:]
    aug2 = df_data_sim.loc[df_data_sim['Month'] == 8,:]
    sep2 = df_data_sim.loc[df_data_sim['Month'] == 9,:]
    oct2 = df_data_sim.loc[df_data_sim['Month'] == 10,:]
    nov2 = df_data_sim.loc[df_data_sim['Month'] == 11,:]
    dec2 = df_data_sim.loc[df_data_sim['Month'] == 12,:] 
    
    lines = ['Path61','Path42','Path24','Path45']
    upper = [1940,98,92,340]
    lower = [240,-400,-48,-190]
    num_lines = len(lines)
    
    for line in lines:
        name='predicted_' + str(line)   
        locals()[name]=[]
    
    for line in lines:    
        predicted=[]
        rc = np.shape(jan2.loc[:,'BPA_wind':])
        n = rc[1] 
        y = df_data_sim.loc[:,line]
        line_index = lines.index(line)
    
        #regression names
        name_1='jan_reg_CA' + str(line)   
        name_2='feb_reg_CA' + str(line)   
        name_3='mar_reg_CA' + str(line)
        name_4='apr_reg_CA' + str(line)
        name_5='may_reg_CA' + str(line)
        name_6='jun_reg_CA' + str(line) 
        name_7='jul_reg_CA' + str(line)    
        name_8='aug_reg_CA' + str(line)   
        name_9='sep_reg_CA' + str(line)    
        name_10='oct_reg_CA' + str(line)  
        name_11='nov_reg_CA' + str(line)    
        name_12='dec_reg_CA' + str(line)
        
        for i in range(0,len(y)):
            
            m = df_data_sim.loc[i,'Month']
            
            if m==1:
                s = jan2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_1].predict(s)
                predicted = np.append(predicted,p)
            elif m==2:
                s = feb2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_2].predict(s)
                predicted = np.append(predicted,p)
            elif m==3:
                s = mar2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_3].predict(s)
                predicted = np.append(predicted,p)
            elif m==4:
                s = apr2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_4].predict(s)
                predicted = np.append(predicted,p)
            elif m==5:
                s = may2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_5].predict(s)
                predicted = np.append(predicted,p)
            elif m==6:
                s = jun2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_6].predict(s)
                predicted = np.append(predicted,p)
            elif m==7:
                s = jul2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_7].predict(s)
                predicted = np.append(predicted,p)
            elif m==8:
                s = aug2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_8].predict(s)
                predicted = np.append(predicted,p)
            elif m==9:
                s = sep2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_9].predict(s)
                predicted = np.append(predicted,p)
            elif m==10:
                s = oct2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_10].predict(s)
                predicted = np.append(predicted,p)
            elif m==11:
                s = nov2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_11].predict(s)
                predicted = np.append(predicted,p)
            else:
                s = dec2.loc[i,'BPA_wind':]
                s = np.reshape(s[:,None],(1,n))
                p = locals()[name_12].predict(s)
                predicted = np.append(predicted,p)
                
    #        if predicted[i] > upper[line_index]:
    #            predicted[i] = upper[line_index]
    #        elif predicted[i] < lower[line_index]:
    #            predicted[i] = lower[line_index]   
                
            if predicted[i] > upper[line_index]:
                predicted[i] = np.mean(OtherCA_Paths_y[:,line_index])
            elif predicted[i] < lower[line_index]:
                predicted[i] = np.mean(OtherCA_Paths_y[:,line_index])
                
    
        name='predicted_' + str(line)              
        locals()[name]=predicted
        
    syn_Path61= predicted_Path61 + syn_residuals[d:d+f_horizon,8]
    syn_Path42 = predicted_Path42 + syn_residuals[d:d+f_horizon,9]
    syn_Path24= predicted_Path24 + syn_residuals[d:d+f_horizon,10]
    syn_Path45 = predicted_Path45 + syn_residuals[d:d+f_horizon,11]

#bias = np.mean(syn_Path61) - np.mean(OtherCA_Paths_y[:,0])
#syn_Path61 = syn_Path61 - bias
#
#bias = np.mean(syn_Path42) - np.mean(OtherCA_Paths_y[:,1])
#syn_Path42 = syn_Path42 - bias
#
#bias = np.mean(syn_Path24) - np.mean(OtherCA_Paths_y[:,2])
#syn_Path24 = syn_Path24 - bias
#
#bias = np.mean(syn_Path45) - np.mean(OtherCA_Paths_y[:,3])
#syn_Path45 = syn_Path45 - bias

    if d < 1:
        
        syn_61M = syn_Path61
        syn_42M = syn_Path42
        syn_24M = syn_Path24
        syn_45M = syn_Path45
    
    else:
        
        syn_61M = np.column_stack((syn_61M,syn_Path61))
        syn_42M = np.column_stack((syn_42M,syn_Path42))
        syn_24M = np.column_stack((syn_24M,syn_Path24))
        syn_45M = np.column_stack((syn_45M,syn_Path45))

############################################################################
syn_BPA= BPA_sim + np.reshape(syn_residuals[:,0],(len(BPA_sim),1))
syn_BPA= syn_BPA[365:len(BPA_sim)-730]
syn_BPA=np.reshape(syn_BPA,(effect_sim_year*365))


syn_SDGE= SDGE_sim + np.reshape(syn_residuals[:,1],(len(BPA_sim),1))
syn_SDGE= syn_SDGE[365:len(BPA_sim)-730]
syn_SDGE=np.reshape(syn_SDGE,(effect_sim_year*365))


syn_SCE= SCE_sim + np.reshape(syn_residuals[:,2],(len(BPA_sim),1))
syn_SCE= syn_SCE[365:len(BPA_sim)-730]
syn_SCE=np.reshape(syn_SCE,(effect_sim_year*365))


syn_PGEV= PGEV_sim + np.reshape(syn_residuals[:,3],(len(BPA_sim),1))
syn_PGEV= syn_PGEV[365:len(BPA_sim)-730]
syn_PGEV=np.reshape(syn_PGEV,(effect_sim_year*365))

syn_PGEB= PGEB_sim + np.reshape(syn_residuals[:,4],(len(BPA_sim),1))
syn_PGEB= syn_PGEB[365:len(BPA_sim)-730]
syn_PGEB=np.reshape(syn_PGEB,(effect_sim_year*365))

###############################################################################
Demand_Path=pd.DataFrame()
Demand_Path['BPA_Load_sim']=syn_BPA.tolist()
Demand_Path['SDGE_Load_sim']= syn_SDGE.tolist()
Demand_Path['SCE_Load_sim']= syn_SCE.tolist()
Demand_Path['PGEV_Load_sim']= syn_PGEV.tolist()
Demand_Path['PGEB_Load_sim']=syn_PGEB.tolist()

#Forecast analysis
sum_variable = syn_66M
TG = sum_variable
r,c = np.shape(TG)
differences=np.zeros((c-f_horizon+1,f_horizon))
for i in range(0,c-f_horizon+1):
    differences[i,:] = (TG[:,i] - TG[0,i:i+f_horizon])/1000

month_ID = np.zeros(((effect_sim_year+3)*365,1))
for i in range(0,effect_sim_year+3):
    month_ID[i*365+0:i*365+31] = 1
    month_ID[i*365+31:i*365+59]=2
    month_ID[i*365+59:i*365+90]=3
    month_ID[i*365+90:i*365+120]=4
    month_ID[i*365+120:i*365+151]=5
    month_ID[i*365+151:i*365+181]=6
    month_ID[i*365+181:i*365+212]=7
    month_ID[i*365+212:i*365+243]=8
    month_ID[i*365+243:i*365+273]=9
    month_ID[i*365+273:i*365+304]=10
    month_ID[i*365+304:i*365+334]=11
    month_ID[i*365+334:i*365+365]=12
    
month_ID = month_ID[0:len(differences)]
    
combined = np.column_stack((differences,month_ID))
df_combined = pd.DataFrame(combined)
df_combined.columns = ['1','2','3','4','5','6','7','Month']

plt.figure()
#plt.style.use('default')

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for i in range(0,12):
    plt.subplot(4,3,i+1)
    
    month_selection = df_combined.loc[df_combined['Month']==i+1,:]
    
    for j in range(0,len(month_selection)):
       
        plt.plot(month_selection.iloc[j,0:f_horizon])
        
    if i ==6:
        plt.ylabel('Difference (GWh)',fontweight='bold') 
    if i == 10:
        plt.xlabel('Forecast Horizon (Days)',fontweight='bold')
    plt.title(months[i],fontweight='bold')
    plt.ylim([-4,4])
plt.subplots_adjust(wspace=0.6,hspace=1.2)

plt.savefig('Path66_perfect_foresight.png', dpi=2000)

#START HERE
#
#Demand_Path['Path8_sim']=syn_Path8.tolist()
#Demand_Path['Path3_sim']=syn_Path3.tolist()
#Demand_Path['Path14_sim']=syn_Path14.tolist()
#Demand_Path['Path65_sim']=syn_Path65.tolist()
#Demand_Path['Path66_sim']=syn_Path66.tolist()
#Demand_Path['Path46_sim']=syn_Path46.tolist()
#Demand_Path['Path61_sim']=syn_Path61.tolist()
#Demand_Path['Path42_sim']=syn_Path42.tolist()
#Demand_Path['Path24_sim']=syn_Path24.tolist()
#Demand_Path['Path45_sim']=syn_Path45.tolist()
#
#Demand_Path.to_csv('Synthetic_demand_pathflows/Load_Path_Sim.csv')
#
#######################################################################
###                         Hourly Demand Simulation
#######################################################################
##
#BPA_profile = np.zeros((24,365))
#SDGE_profile = np.zeros((24,365))
#SCE_profile = np.zeros((24,365))
#PGEV_profile = np.zeros((24,365))
#PGEB_profile = np.zeros((24,365))
#
## number of historical days
#hist_days = len(SCE_load)/24
#hist_years = int(hist_days/365)
#sim_years = int(len(sim_weather)/365)
#
## create profiles
#for i in range(0,hist_years):
#    for j in range(0,365):
#        
#        # pull 24 hours of demand
#        BPA_sample = BPA_load[i*8760+j*24:i*8760+j*24+24]
#        SDGE_sample = SDGE_load[i*8760+j*24:i*8760+j*24+24]
#        SCE_sample = SCE_load[i*8760+j*24:i*8760+j*24+24]
#        PGEV_sample = PGEV_load[i*8760+j*24:i*8760+j*24+24]
#        PGEB_sample = PGEB_load[i*8760+j*24:i*8760+j*24+24]
#        
#        # create fractional profile (relative to peak demand)
#        sample_peak = np.max(BPA_sample)
#        BPA_fraction = BPA_sample/sample_peak
#        BPA_profile[:,j] = BPA_profile[:,j] + BPA_fraction*(1/hist_years)
# 
#        sample_peak = np.max(SDGE_sample)
#        SDGE_fraction = SDGE_sample/sample_peak
#        SDGE_profile[:,j] = SDGE_profile[:,j] + SDGE_fraction*(1/hist_years)
#
#        sample_peak = np.max(SCE_sample)
#        SCE_fraction = SCE_sample/sample_peak
#        SCE_profile[:,j] = SCE_profile[:,j] + SCE_fraction*(1/hist_years)
#
#        sample_peak = np.max(PGEV_sample)
#        PGEV_fraction = PGEV_sample/sample_peak
#        PGEV_profile[:,j] = PGEV_profile[:,j] + PGEV_fraction*(1/hist_years) 
#        
#        sample_peak = np.max(PGEB_sample)
#        PGEB_fraction = PGEB_sample/sample_peak
#        PGEB_profile[:,j] = PGEB_profile[:,j] + PGEB_fraction*(1/hist_years)        
#        
## simulate using synthetic peaks
#BPA_hourly = np.zeros((8760*effect_sim_year,1))
#SDGE_hourly = np.zeros((8760*effect_sim_year,1))
#SCE_hourly = np.zeros((8760*effect_sim_year,1))
#PGEV_hourly = np.zeros((8760*effect_sim_year,1))
#PGEB_hourly = np.zeros((8760*effect_sim_year,1))
#PNW_hourly = np.zeros((8760*effect_sim_year,1))
#
#for i in range(0,effect_sim_year):
#    for j in range(0,365):
#        v = syn_BPA[i*365+j]*BPA_profile[:,j]
#        a = np.reshape(v,(24,1))
#        BPA_hourly[i*8760+24*j:i*8760+24*j+24] = a
#        
#        v = syn_SDGE[i*365+j]*SDGE_profile[:,j]
#        a = np.reshape(v,(24,1))
#        SDGE_hourly[i*8760+24*j:i*8760+24*j+24] = a
#        
#        v = syn_SCE[i*365+j]*SCE_profile[:,j]
#        a = np.reshape(v,(24,1))
#        SCE_hourly[i*8760+24*j:i*8760+24*j+24] = a
#        
#        v = syn_PGEV[i*365+j]*PGEV_profile[:,j]
#        a = np.reshape(v,(24,1))
#        PGEV_hourly[i*8760+24*j:i*8760+24*j+24] = a
#        
#        v = syn_PGEB[i*365+j]*PGEB_profile[:,j]
#        a = np.reshape(v,(24,1))
#        PGEB_hourly[i*8760+24*j:i*8760+24*j+24] = a
#        
##Scale BPA demand up to PNW region wide total
#import PNW_demand_scaling
#
#for i in range(0,effect_sim_year):
#    
#    A = PNW_demand_scaling.PNW_demand(BPA_hourly[i*8760:i*8760+8760,0])
#    B = np.reshape(A[:,None],(8760,1))
#    PNW_hourly[i*8760:i*8760+8760] = B
#
#Combined = np.column_stack((BPA_hourly,PNW_hourly,SDGE_hourly,SCE_hourly,PGEV_hourly,PGEB_hourly))
#df_C = pd.DataFrame(Combined)
#df_C.columns = ['BPA','PNW','SDGE','SCE','PGE_valley','PGE_bay']
#df_C.to_csv('Synthetic_demand_pathflows/Sim_hourly_load.csv')

#plt.figure()
#sns.distplot(NWPaths_y[:,0], color="skyblue", label="Hist")
#sns.distplot(syn_Path8, color="red", label="Sim").set_title("Path8")
#
#plt.figure()
#sns.distplot(NWPaths_y[:,1], color="skyblue", label="Hist")
#sns.distplot(syn_Path14, color="red", label="Sim").set_title("Path14")
#
#plt.figure()
#sns.distplot(NWPaths_y[:,2], color="skyblue", label="Hist")
#sns.distplot(syn_Path3, color="red", label="Sim").set_title("Path3")
#
#plt.figure()
#sns.distplot(Path65_66_y[:,0], color="skyblue", label="Hist")
#sns.distplot(syn_Path65, color="red", label="Sim").set_title("Path65")
#
#plt.figure()
#sns.distplot(Path65_66_y[:,1], color="skyblue", label="Hist")
#sns.distplot(syn_Path66, color="red", label="Sim").set_title("Path66")
#
#plt.figure()
#sns.distplot(Path46_y, color="skyblue", label="Hist")
#sns.distplot(syn_Path46, color="red", label="Sim").set_title("Path46")
#
#plt.figure()
#sns.distplot(OtherCA_Paths_y[:,0], color="skyblue", label="Hist")
#sns.distplot(syn_Path61, color="red", label="Sim").set_title("Path61")
#
#plt.figure()
#sns.distplot(OtherCA_Paths_y[:,1], color="skyblue", label="Hist")
#sns.distplot(syn_Path42, color="red", label="Sim").set_title("Path42")
#
#plt.figure()
#sns.distplot(OtherCA_Paths_y[:,2], color="skyblue", label="Hist")
#sns.distplot(syn_Path24, color="red", label="Sim").set_title("Path24")
#
#plt.figure()
#sns.distplot(OtherCA_Paths_y[:,3], color="skyblue", label="Hist")
#sns.distplot(syn_Path45, color="red", label="Sim").set_title("Path45")