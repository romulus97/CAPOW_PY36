# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import division
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import math

#########################################################################
# This purpose of this script is to use historical meteorological data
# to create daily temperature and wind profiles, and 
# a covariance matrix that describes statistical dependencies
# in daily temperature and wind speeds across the 17 National 
# Climatic Data Center GHN monitoring stations.
#
# This information is then used in a different script as part of vector -
# autoregressive (VAR) modeling of synthetic temperature and wind speed records.
#########################################################################


#read in historical meteorological data from NCDC GHN stations. data
# are average daily wind speeds (m/s), minimum/maximum daily temperatures (degrees C)
met_data=pd.read_csv('Historical_weather_analysis/Wind_Temps_1970_2017.csv',header =0, na_values=['#VALUE!', '#DIV/0!'])

#read in table of NCDC GHN station information
Station_name= pd.read_excel('Historical_weather_analysis/station_names.xlsx', header = 0)
Station_ID = list(Station_name.loc[:,'ID'])
Place= list(Station_name.loc[:,'Place'])
Dictionary=dict(zip(Station_ID,Place))

#Distinguish between 31-day, 30-day and 28-day months
Big_Month=[1,3,5,7,8,10,12]
Small_Month=[4,6,9,11]
Other=[2]

# creates a separate data frame for meteorological data for each station
for i in Station_ID:
    
    exec("ID_%s_Station_data=met_data.loc[met_data.loc[:,'STATION']== i]" %(i))
    exec("ID_%s_Station_data=ID_%s_Station_data.reset_index()" %(i,i))

# calculates average wind speeds and temperatues at each station
# for each calendar day, as well as standard deviations of deviations 
# from calculated average values
for i in Station_ID:
    
    print i 
    
    # store data for each station in a temporary variable
    exec('Temp= ID_%s_Station_data' %(i))
         
    # for each month 
    for j in range(1,13):
        
        # select relevant data
        Selected_Month=Temp.loc[Temp.loc[:,'Month']==j]
                        
        # allocate correct number of days
        if j in Big_Month:
            n=31
        elif j in Small_Month:
            n=30
        else:
            n=28
        
        # for each day in the selected month
        for d in range(1,n+1):
            
            #calculate average/std temperature for that calendar day
            Selected_Day = Selected_Month.loc[Selected_Month.loc[:,'Day']==d]
                        
            Selected_T=Selected_Day.loc[:,'TAVG']
            Selected_T = pd.to_numeric(Selected_T, errors='coerce')
            Selected_T=Selected_T.dropna(axis=0,how='all')
            Daily_average_T= np.nanmean(Selected_T)
            Daily_Std_T=np.nanstd(Selected_T)
            
            #calculate average/std wind speed for that calendar day
            Selected_W=Selected_Day.loc[:,'AWND']
            Selected_W = pd.to_numeric(Selected_W, errors='coerce')
            Selected_W=Selected_W.dropna(axis=0,how='all')
            Daily_average_wind=np.nanmean(Selected_W)
            Daily_Std_wind=np.nanstd(Selected_W)
            
            #create "whitened" residuals from average daily values
            for k in Selected_T.index:
                                
                # whitened residuals 
                res_T=(float(Selected_T.loc[k])-Daily_average_T)/Daily_Std_T
                
                # store with rest of station data
                exec("ID_%s_Station_data.loc[k,'Res_T']=res_T" %(i))
                exec("ID_%s_Station_data.loc[k,'Ave_T']=Daily_average_T" %(i))
                exec("ID_%s_Station_data.loc[k,'Std_T']=Daily_Std_T" %(i))

            for k in Selected_W.index:
                
                # whitened residuals                
                res_Wind=(float(Selected_W.loc[k]) - Daily_average_wind)/Daily_Std_wind
                
                exec("ID_%s_Station_data.loc[k,'Res_Wind']=res_Wind" %(i))
                exec("ID_%s_Station_data.loc[k,'Ave_W']=Daily_average_wind" %(i))
                exec("ID_%s_Station_data.loc[k,'Std_W']=Daily_Std_wind" %(i))

# Line up data across stations and calculate covariance matrix of whitened residuals

# for each station
for i in Station_ID:
    
    print i + ' 2'
    
    exec('Temp= ID_%s_Station_data' %(i))
    
    Store_Result=[]
    
    # load relevant statistical data 
    T_res_data= Temp.loc[:,'Res_T'] 
    Wind_res_data= Temp.loc[:,'Res_Wind']
    T_ave_data= Temp.loc[:,'Ave_T']
    W_ave_data= Temp.loc[:,'Ave_W'] 
    T_std_data= Temp.loc[:,'Std_T']
    W_std_data= Temp.loc[:,'Std_W']
    
    # get rid of any NaN values
    Org_T=T_res_data.dropna(axis=0,how='all')
    Org_W=Wind_res_data.dropna(axis=0,how='all')
    Org_T_ave=T_ave_data.dropna(axis=0,how='all')
    Org_W_ave=W_ave_data.dropna(axis=0,how='all')
    Org_T_Std=T_std_data.dropna(axis=0,how='all')
    Org_W_Std=W_std_data.dropna(axis=0,how='all')
    
    # identify index of first and last index of temperature data 
    Begin=Org_T.index[0]
    End=Org_T.index[-1]
    
    # identify date of first and last temperature value
    Start_month = Temp.loc[Begin,'Month']
    Start_day = Temp.loc[Begin,'Day']
    Start_year = Temp.loc[Begin,'Year']
    Start_time = str(Start_month) + '/' + str(Start_day) + '/' + str(Start_year)
    End_month = Temp.loc[End,'Month']
    End_day = Temp.loc[End,'Day']
    End_year = Temp.loc[End,'Year']
    End_time = str(End_month) + '/' + str(End_day) + '/' + str(End_year)

    
    # record relevant statistical data for each date
    for j in Org_T.index:
        month = Temp.loc[j,'Month']
        day = Temp.loc[j,'Day']
        year = Temp.loc[j,'Year']      
        date = str(month) + '/' + str(day) + '/' + str(year)

        T_org_data=Temp.loc[j,'Res_T']
        W_org_data=Temp.loc[j,'Res_Wind']
        T_ave_org=Temp.loc[j,'Ave_T']
        W_ave_org=Temp.loc[j,'Ave_W']
        T_std_org=Temp.loc[j,'Std_T']
        W_std_org=Temp.loc[j,'Std_W']

        # if wind data was not available, don't record anything
        if math.isnan(Temp.loc[j,'Res_Wind']) is True:
            pass
        # otherwise, store statistics for that day
        else:
            Store_Result.append([date,T_org_data,W_org_data,T_ave_org,W_ave_org,T_std_org,W_std_org])
    exec('Store_%s= Store_Result' %(i))

#Check imformation - prints station name, date of beginning and end of data
for i in Station_ID:

     exec("Result_%s_pd=pd.DataFrame(Store_%s,columns=('date','Temperature_Res','Wind_res','T_Ave','W_Ave','T_Std','W_Std'))" %(i,i))
     print(i)
     exec("print(Result_%s_pd.loc[0,'date'])" %(i))
     exec("In=Result_%s_pd.index[-1]" %(i))

     exec("print(Result_%s_pd.loc[In,'date'])" %(i))
     exec("print(len(Result_%s_pd))" %(i))
############################
    
    
#All fields are present starting from 1/1/2000. Use this as a starting point.

#Create a list of fields (temperature and wind speeds at each station)
index_list=[]
for i in Station_ID:
    exec("name='%s_T'" %(Dictionary[i]))
    index_list.append(name)
    exec("name='%s_W'" %(Dictionary[i]))
    index_list.append(name)

#Create a dataframe to store result
Covariance_Calculation=pd.DataFrame(index=index_list, columns=index_list)

Start= datetime(2000,01,01)
End = datetime(2018,1,1)
n = 6941 # number of days in continuous record
t = Start

# for each station
for i in Station_ID:
    
    print i + ' 3'
    
    # Store results in temporary variable
    exec('Temp_1= Result_%s_pd' %(i))
    
    # pairwise calculation of covariance
    for j in Station_ID:
        
        list_1_T=[]
        list_2_T=[]
        list_1_W=[]
        list_2_W=[]
        
        exec('Temp_2= Result_%s_pd' %(j))
        
        # go through each day of complete record
        for z in range(0,n):
            
            # create time element 
            time_element=t+timedelta(z)
            time_element=time_element.strftime('%m/%d/%Y')
            
            # Look for common days between two records
            if time_element in list(Temp_1.loc[:,'date']) and time_element in list(Temp_2.loc[:,'date']):
                
                #if the date is common across two stations, store temperature and wind residuals
                data_1=Temp_1.loc[Temp_1.loc[:,'date']== time_element]
                data_2=Temp_2.loc[Temp_2.loc[:,'date']== time_element]
                data_1=data_1.reset_index()
                data_2=data_2.reset_index()
                list_1_T.append(data_1.loc[0]['Temperature_Res'])
                list_2_T.append(data_2.loc[0]['Temperature_Res'])
                list_1_W.append(data_1.loc[0]['Wind_res'])
                list_2_W.append(data_2.loc[0]['Wind_res'])
                
            else:
                pass
            
        #calculate covariance of wind and temperature between two stations    
        co_1 = np.cov(list_1_T,list_1_W)[0][1]
        co_2 = np.cov(list_1_T,list_2_T)[0][1]
        co_3 = np.cov(list_1_T,list_2_W)[0][1]
        co_4 = np.cov(list_1_W,list_2_T)[0][1]
        co_5 = np.cov(list_1_W,list_2_W)[0][1]
        co_6 = np.cov(list_2_T,list_2_W)[0][1]

        exec("Covariance_Calculation.loc['%s_T','%s_W']=co_1" %(Dictionary[i],Dictionary[i]))
        exec("Covariance_Calculation.loc['%s_T','%s_T']=co_2" %(Dictionary[i],Dictionary[j]))
        exec("Covariance_Calculation.loc['%s_T','%s_W']=co_3" %(Dictionary[i],Dictionary[j]))
        exec("Covariance_Calculation.loc['%s_W','%s_T']=co_4" %(Dictionary[i],Dictionary[j]))
        exec("Covariance_Calculation.loc['%s_W','%s_W']=co_5" %(Dictionary[i],Dictionary[j]))
        exec("Covariance_Calculation.loc['%s_T','%s_W']=co_6" %(Dictionary[j],Dictionary[j]))   

Covariance_Calculation.to_csv('Historical_Weather_Analysis/Covariance_Calculation.csv')

##################################################################################
##This section is used for data orgnization

Date_index=pd.date_range(Start,End)
index_list=[]

for i in Station_ID:
    exec("name='%s_T'" %(Dictionary[i]))
    index_list.append(name)
    exec("name='%s_W'" %(Dictionary[i]))
    index_list.append(name)
    
#Create a dataframe to store result
W_T=pd.DataFrame(index=Date_index, columns=index_list)
W_T_res=pd.DataFrame(index=Date_index, columns=index_list)
W_T_ave=pd.DataFrame(index=Date_index, columns=index_list)
W_T_Std=pd.DataFrame(index=Date_index, columns=index_list)


for i in Station_ID:
    
    print i + ' 4'
    
    exec('Temp= ID_%s_Station_data' %(i))

    time_element=Start
    Time_Format=time_element.strftime('%m/%d/%Y')
    Time_List=[]
    C=Dictionary[i]
    
    for j in range(0,len(Temp)):
        
        month = Temp.loc[j,'Month']
        day = Temp.loc[j,'Day']
        year = Temp.loc[j,'Year']      
        date = str(month) + '/' + str(day) + '/' + str(year)
        
        Time_o=datetime.strptime(date,'%m/%d/%Y')
        Time_F=Time_o.strftime('%m/%d/%Y')
        Temp.loc[j,'DATE'] = Time_F
        
    
    # Store time series statistical information        
    for j in range(1,len(Date_index)):
        
        data_1=Temp.loc[Temp.loc[:,'DATE']== Time_Format]
        
        exec("W_T.loc[time_element,'%s_T']=float(data_1.loc[:,'TAVG'])" %(Dictionary[i]))
        exec("W_T.loc[time_element,'%s_W']=float(data_1.loc[:,'AWND'])" %(Dictionary[i]))
        exec("W_T_res.loc[time_element,'%s_T']=float(data_1.loc[:,'Res_T'])" %(Dictionary[i]))
        exec("W_T_res.loc[time_element,'%s_W']=float(data_1.loc[:,'Res_Wind'])" %(Dictionary[i]))
        exec("W_T_ave.loc[time_element,'%s_T']=float(data_1.loc[:,'Ave_T'])" %(Dictionary[i]))
        exec("W_T_ave.loc[time_element,'%s_W']=float(data_1.loc[:,'Ave_W'])" %(Dictionary[i]))
        exec("W_T_Std.loc[time_element,'%s_T']=float(data_1.loc[:,'Std_T'])" %(Dictionary[i]))
        exec("W_T_Std.loc[time_element,'%s_W']=float(data_1.loc[:,'Std_W'])" %(Dictionary[i]))
        time_element=time_element+ timedelta(1)
        Time_Format=time_element.strftime('%m/%d/%Y')
    
#Output temp and wind time series data here
W_T.rename({0:'Date'}, axis='columns')      
W_T.to_csv('Historical_weather_analysis/WIND_TEMP.csv')   
W_T_res.rename({0:'Date'}, axis='columns') 
W_T_res.to_csv('Historical_weather_analysis/WIND_TEMP_res.csv') 
W_T_ave.rename({0:'Date'}, axis='columns')  
W_T_ave.to_csv('Historical_weather_analysis/WIND_TEMP_ave.csv') 
W_T_Std.rename({0:'Date'}, axis='columns')  
W_T_Std.to_csv('Historical_weather_analysis/WIND_TEMP_Std.csv') 