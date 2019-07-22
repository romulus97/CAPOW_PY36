# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:21:06 2019

@author: sdenaro
"""



import pandas as pd
import numpy as np

######################################################################
#                                LOAD
######################################################################

#import data
df_weather = pd.read_excel('Synthetic_demand_pathflows/hist_demanddata.xlsx',sheetname='weather',header=0)
BPA_weights = pd.read_excel('Synthetic_demand_pathflows/hist_demanddata.xlsx',sheetname='BPA_location_weights',header=0)
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

HDD_weighted_sim = np.zeros((sim_days,1))
CDD_weighted_sim = np.zeros((sim_days,1))
for i in range(0,num_days):
    for j in range(0,num_cities):
        HDD[i,j] = np.max((0,65-AvgT[i,j]))
        CDD[i,j] = np.max((0,AvgT[i,j] - 65))

for i in range(0,sim_days):
    for j in range(0,num_cities):
        HDD_sim[i,j] = np.max((0,65-BPA_sim_T_F[i,j]))
        CDD_sim[i,j] = np.max((0,BPA_sim_T_F[i,j] - 65))   

for i in range(0,sim_days):
        HDD_weighted_sim[i] = np.max((0,65-weighted_SimT[i]))
        CDD_weighted_sim[i] = np.max((0,weighted_SimT[i] - 65))   

#separate wind speed by cooling/heating degree day
binary_CDD = CDD>0
binary_HDD = HDD>0
CDD_wind = np.multiply(Wind,binary_CDD)
HDD_wind = np.multiply(Wind,binary_HDD)

binary_CDD_sim = CDD_sim > 0
binary_HDD_sim = HDD_sim > 0
CDD_wind_sim = np.multiply(BPA_sim_W,binary_CDD_sim)
HDD_wind_sim = np.multiply(BPA_sim_W,binary_HDD_sim)

#Separate data by weighted temperature
M=pd.DataFrame(np.column_stack((weighted_SimT,HDD_weighted_sim,CDD_weighted_sim,
                                    sim_dow,HDD_sim,CDD_sim,HDD_wind_sim,CDD_wind_sim)),
                                    columns=['T_w','HDD_w','CDD_w','dow',
                                             'SALEM_HDD','SEATTLE_HDD','PORTLAND_HDD','EUGENE_HDD','BOISE_HDD',
                                             'SALEM_CDD','SEATTLE_CDD','PORTLAND_CDD','EUGENE_CDD','BOISE_CDD',
                                             'SALEM_wind_HDD','SEATTLE_wind_HDD','PORTLAND_wind_HDD','EUGENE_wind_HDD','BOISE_wind_HDD',
                                             'SALEM_wind_CDD','SEATTLE_wind_CDD','PORTLAND_wind_CDD','EUGENE_wind_CDD','BOISE_wind_CDD'])

M.to_csv('Synthetic_weather/INDEX_synthetic_temp_wind.csv')    