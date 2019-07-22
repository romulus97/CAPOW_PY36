# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:44:59 2019

@author: sdenaro
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


prices_d=pd.read_csv('PNW_daily_prices_merged.csv', usecols=[1])
prices_d=pd.DataFrame(np.reshape(prices_d.values, (364,200)))
prices_d.loc[364,:]=prices_d.loc[363,:]
prices_d=pd.DataFrame(np.reshape(prices_d.values, (200*365,-1)),columns=['MidC'])
#prices_d.to_csv('PNW_prices_200.csv')


plt.figure()
plt.plot(prices_d.loc[0:364*10,'MidC'])
plt.title('Synthetic MidC prices')
#plt.xticks(np.arange(0,364*10 ,365))
#
#plt.figure()
#plt.plot(prices_d.loc[364*6:364*7,'daily prices'])

prices_h=pd.read_csv('PNW_hourly_prices_merged.csv',usecols=[1])
prices_h[prices_h==700]=178.583229
prices_h=pd.DataFrame(np.reshape(prices_h.values, (364*24,200)))
last_days=prices_h.loc[24*364-24:24*364,:]
prices_h=prices_h.append(last_days)
prices_h=pd.DataFrame(np.reshape(prices_h.values, (200*365*24,-1)),columns=['MidC'])


# fix slack variable
no_days=365*200
daily_prices_fix = np.zeros((no_days,1))
for i in range(0,no_days):  
          daily_prices_fix[i] = np.mean(prices_h[i*24:i*24+24])


plt.figure()
plt.plot(daily_prices_fix)

plt.figure()
plt.plot(daily_prices_fix[0:364*10])
plt.xticks(np.arange(0,364*10 ,365))

daily_prices_fix=pd.DataFrame(daily_prices_fix, columns=['MidC'])

daily_prices_fix.to_csv('PNW_prices_200_FIX.csv')