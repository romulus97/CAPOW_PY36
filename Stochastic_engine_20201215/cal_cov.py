# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 08:41:48 2020

@author: 11487
"""

from __future__ import division
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import math
import matplotlib.pyplot as plt

# %%
class ReturnValue(object):
  __slots__ = ["Daily_Val", "Daily_Ave", "Daily_Std","Daily_Res","Daily_Cov"]
  def __init__(self, Daily_Val, Daily_Ave, Daily_Std, Daily_Res, Daily_Cov):
     self.Daily_Val = Daily_Val
     self.Daily_Ave = Daily_Ave
     self.Daily_Std = Daily_Std
     self.Daily_Res = Daily_Res
     self.Daily_Cov = Daily_Cov
     
# %%
class ReturnValue1(object):
  __slots__ = ["Daily_Val", "Daily_Ave", "Daily_Std","Daily_Res","Clear_Sky"]
  def __init__(self, Daily_Val, Daily_Ave, Daily_Std, Daily_Res, Clear_Sky):
     self.Daily_Val = Daily_Val
     self.Daily_Ave = Daily_Ave
     self.Daily_Std = Daily_Std
     self.Daily_Res = Daily_Res
     self.Clear_Sky = Clear_Sky
 # %%
     
 
def cal_cov(yearbeg,yearend):
    
    filename='Historical_weather_analysis/synthetic_weather_data_{}-{}.csv'.format(yearbeg, yearend);
    datas00=pd.read_csv(filename);
    
    # %% delete all the records with 29 days in Feb
    date_t0=pd.to_datetime(datas00.loc[:,'datetime']);
    date_mask=(pd.DatetimeIndex(date_t0).month==2) & (pd.DatetimeIndex(date_t0).day==29);
    datas0=datas00.drop(datas00.index[date_mask],axis=0);
    
    # %% organize the data
    dates0=datas0.loc[:,'datetime'];    
    Daily_Val=datas0.drop(datas0.columns[[0,1]], axis=1);
    Daily_Val.index=dates0 
    name_col=datas0.columns[2:];

    df0 = pd.DataFrame({'datetime': pd.to_datetime(dates0)})
    df0['year'] = pd.DatetimeIndex(df0['datetime']).year
    df0['month'] = pd.DatetimeIndex(df0['datetime']).month
    df0['day'] = pd.DatetimeIndex(df0['datetime']).day
    
    # %% calculate the values
    num_days,num_vars=Daily_Val.shape;
    arr1 = np.zeros((num_days,num_vars));
    Daily_Ave = pd.DataFrame(arr1,columns=name_col,index=dates0,copy=True);# copy=True is required to make the arr1 unchangable
    Daily_Std = pd.DataFrame(arr1,columns=name_col,index=dates0,copy=True);
    Daily_Res = pd.DataFrame(arr1,columns=name_col,index=dates0,copy=True);
    for i in name_col:
        temp0=datas0.loc[:,i]
        temp1=temp0.values.reshape([int(len(temp0)/365),365])
        Daily_Ave0 = np.nanmean(temp1,axis=0)
        Daily_Std0=np.nanstd(temp1,axis=0)
        
        Daily_Ave1 = np.tile(Daily_Ave0,(temp1.shape[0],1))
        Daily_Std1 = np.tile(Daily_Std0,(temp1.shape[0],1))
        
        
        Daily_Res1=(temp1-Daily_Ave1)/Daily_Std1;
        Daily_Res2=Daily_Res1.reshape([len(temp0),1])
        
        Daily_Ave2=Daily_Ave1.reshape([len(temp0),1])
        Daily_Std2=Daily_Std1.reshape([len(temp0),1])
        
        Daily_Res.loc[:,i]=Daily_Res2;
        Daily_Ave.loc[:,i]=Daily_Ave2;
        Daily_Std.loc[:,i]=Daily_Std2;
                
        # plt.plot(Daily_average.iloc[:,1]);plt.show();
        # plt.plot(Daily_Std)
    Daily_Cov=pd.DataFrame(np.cov(np.transpose(Daily_Res)),index=name_col,columns=name_col)
          
    # Date_index0=pd.date_range(pd.to_datetime(dates0.iloc[0]),pd.to_datetime(dates0.iloc[-1]),freq='D');
    # date_mask=(Date_index0.month==2) & (Date_index0.day==29)
    # B = np.empty((1,len(name_col)));
    # F1=np.zeros((len(Date_index0),len(name_col)));

    return ReturnValue(Daily_Val, Daily_Ave, Daily_Std, Daily_Res, Daily_Cov)


# %% 
def cal_irr(yearbeg,yearend):
    
    filename='Historical_weather_analysis/synthetic_irradiance_data_{}-{}.csv'.format(yearbeg, yearend);
    datas00=pd.read_csv(filename);
    
    # %% delete all the records with 29 days in Feb
    date_t0=pd.to_datetime(datas00.loc[:,'datetime']);
    date_mask=(pd.DatetimeIndex(date_t0).month==2) & (pd.DatetimeIndex(date_t0).day==29);
    datas0=datas00.drop(datas00.index[date_mask],axis=0);
    
    # %% organize the data
    dates0=datas0.loc[:,'datetime'];    
    Daily_Val=datas0.drop(datas0.columns[[0,1]], axis=1);
    Daily_Val.index=dates0 
    name_col=datas0.columns[2:];

    df0 = pd.DataFrame({'datetime': pd.to_datetime(dates0)})
    df0['year'] = pd.DatetimeIndex(df0['datetime']).year
    df0['month'] = pd.DatetimeIndex(df0['datetime']).month
    df0['day'] = pd.DatetimeIndex(df0['datetime']).day
    
    # %% calculate the values
    num_days,num_vars=Daily_Val.shape;
    arr1 = np.zeros((num_days,num_vars));
    Daily_Ave = pd.DataFrame(arr1,columns=name_col,copy=True);
    Daily_Std = pd.DataFrame(arr1,columns=name_col,copy=True);
    Daily_Res = pd.DataFrame(arr1,columns=name_col,index=dates0,copy=True);
    Clear_Sky = pd.DataFrame(arr1,columns=name_col,copy=True);
    for i in name_col:
        temp0_0=datas0.loc[:,i]
        temp1_0=temp0_0.values.reshape([int(len(temp0_0)/365),365])
        Clear_Sky0=np.max(temp1_0,axis=0)
        
        temp0=(np.tile(Clear_Sky0,(1,temp1_0.shape[0]))-temp0_0.values).transpose()
        temp1=temp0.reshape([int(len(temp0)/365),365])
        
        
        Daily_Ave0 = np.nanmean(temp1,axis=0)
        Daily_Std0=np.nanstd(temp1,axis=0)
        
        
        Daily_Ave1 = np.tile(Daily_Ave0,(temp1.shape[0],1))
        Daily_Std1 = np.tile(Daily_Std0,(temp1.shape[0],1))
        Clear_Sky1 = np.tile(Clear_Sky0,(temp1.shape[0],1))
        
        Daily_Res1=(temp1-Daily_Ave1)/Daily_Std1;      
        Daily_Res2=Daily_Res1.reshape([len(temp0),1])
        
        Daily_Ave2=Daily_Ave1.reshape([len(temp0),1])
        Daily_Std2=Daily_Std1.reshape([len(temp0),1])
        Clear_Sky2=Clear_Sky1.reshape([len(temp0),1])
        
        Daily_Res.loc[:,i]=Daily_Res2;
        Daily_Ave.loc[:,i]=Daily_Ave2;
        Daily_Std.loc[:,i]=Daily_Std2;
        Clear_Sky.loc[:,i]=Clear_Sky2;
                
        # plt.plot(Daily_average.iloc[:,1]);plt.show();
        # plt.plot(Daily_Std)
    # Daily_Cov=pd.DataFrame(np.cov(np.transpose(Daily_Res)),index=name_col,columns=name_col)     
    # Date_index0=pd.date_range(pd.to_datetime(dates0.iloc[0]),pd.to_datetime(dates0.iloc[-1]),freq='D');
    # date_mask=(Date_index0.month==2) & (Date_index0.day==29)
    # B = np.empty((1,len(name_col)));
    # F1=np.zeros((len(Date_index0),len(name_col)));

    return ReturnValue1(Daily_Val, Daily_Ave, Daily_Std, Daily_Res, Clear_Sky)

# %% getting values
# yearbeg=2005; yearend=2034;
def cal_covs(yearbeg, yearend):
    results0=cal_irr(yearbeg, yearend)
    # %% Exporting data
    results0.Daily_Ave.iloc[0:365,:].to_csv('Historical_weather_analysis/ave_irr_{}-{}.csv'.format(yearbeg, yearend))
    results0.Clear_Sky.iloc[0:365,:].to_csv('Historical_weather_analysis/clear_sky_{}-{}.csv'.format(yearbeg, yearend))
    results0.Daily_Res.to_csv('Historical_weather_analysis/res_irr_{}-{}.csv'.format(yearbeg, yearend))
    results0.Daily_Std.iloc[0:365,:].to_csv('Historical_weather_analysis/std_irr_{}-{}.csv'.format(yearbeg, yearend))
    results0.Daily_Val.to_csv('Historical_weather_analysis/daily_irr_{}-{}.csv'.format(yearbeg, yearend))
    
    # %% getting values
    results=cal_cov(yearbeg, yearend)
    # %% Exporting data
    results.Daily_Ave.to_csv('Historical_weather_analysis/WIND_TEMP_ave_{}-{}.csv'.format(yearbeg, yearend))
    results.Daily_Cov.to_csv('Historical_weather_analysis/Covariance_Calculation_{}-{}.csv'.format(yearbeg, yearend))
    results.Daily_Res.to_csv('Historical_weather_analysis/WIND_TEMP_res_{}-{}.csv'.format(yearbeg, yearend))
    results.Daily_Std.to_csv('Historical_weather_analysis/WIND_TEMP_Std_{}-{}.csv'.format(yearbeg, yearend))
    results.Daily_Val.to_csv('Historical_weather_analysis/WIND_TEMP_{}-{}.csv'.format(yearbeg, yearend))
    return None

