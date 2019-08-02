# -*- coding: utf-8 -*-
"""
Created on Wed May 03 15:01:31 2017

@author: jdkern
"""
import pandas as pd
import numpy as np

#==============================================================================

df_mwh1 = pd.read_csv('mwh_1.csv',header=0)
df_mwh2 = pd.read_csv('mwh_2.csv',header=0)
df_mwh3 = pd.read_csv('mwh_3.csv',header=0)
df_gen = pd.read_csv('generators.csv',header=0)

last_hour = df_mwh1['Time'].iloc[-1]

zonal_prices = np.zeros((last_hour,1))

zones = ['PNW']


for z in zones:

    z_index = zones.index(z)

    z1 = df_mwh1.loc[df_mwh1['Zones']==z]
    z2 = df_mwh2.loc[df_mwh1['Zones']==z]
    z3 = df_mwh3.loc[df_mwh1['Zones']==z]

    for i in range(0,last_hour):

        h1 = z1.loc[z1['Time']==i+1]
        h2 = z2.loc[z1['Time']==i+1]
        h3 = z3.loc[z1['Time']==i+1]

        o1 = h1.loc[h1['Value']>0]
        o2 = h2.loc[h2['Value']>0]
        o3 = h3.loc[h3['Value']>0]

        m1 = np.max(o1.loc[:,'$/MWh'])
        m2 = np.max(o2.loc[:,'$/MWh'])
        m3 = np.max(o3.loc[:,'$/MWh'])

        if np.isnan(m1) > 0:
            m1 = 0
        if np.isnan(m2) > 0:
            m2 = 0
        if np.isnan(m3) > 0:
            m3 = 0

        zonal_prices[i,z_index] = np.max((m1,m2,m3))
        

no_hours = last_hour
no_days = int(no_hours/24)

daily_prices = np.zeros((no_days,1))

for i in range(0,no_days):

    for z in zones:

        z_index = zones.index(z)

        daily_prices[i,z_index] = np.mean(zonal_prices[i*24:i*24+24,z_index])


hourly = pd.DataFrame(zonal_prices)
hourly.columns = zones
hourly.to_csv('sim_hourly_prices.csv')

daily = pd.DataFrame(daily_prices)
daily.columns = zones
daily.to_csv('sim_daily_prices.csv')
