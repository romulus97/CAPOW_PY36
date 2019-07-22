# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:25:32 2019

@author: YSu
"""


from __future__ import division
from sklearn import linear_model
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.api import VAR, DynamicVAR
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from datetime import datetime
from datetime import timedelta
import math
from calendar import isleap



data=pd.read_csv('Long_his_temp.csv',index_col=0)

title=list(data)

def whiten_data(Q):
    y=len(Q)
    year=int(y/365)
    Q_2=np.reshape(Q.values,(year,365))
    
    mean=np.average(Q_2,axis=0)
    std=np.std(Q_2,axis=0)
    res_1=(Q_2-mean)/std
    res=np.reshape(res_1,y)
    
    return mean,std,res


store_mean=np.zeros((365,17))
store_std=np.zeros((365,17))
store_res=np.zeros((20075,17))

c=0
for i in title:
    Q=data[i]
    mean,std,res=whiten_data(Q)
    store_mean[:,c]=mean
    store_std[:,c]=std
    store_res[:,c]=res
    c=c+1

W_T_res=pd.DataFrame(store_res)

W_T_ave=pd.DataFrame(store_mean)
W_T_std=pd.DataFrame(store_std)

W_T_ave.columns=title
W_T_res.columns=title
W_T_std.columns=title

W_T_ave.to_csv('Temp_ave.csv')
W_T_std.to_csv('Temp_Std.csv')
W_T_res.to_csv('Temp_res.csv')