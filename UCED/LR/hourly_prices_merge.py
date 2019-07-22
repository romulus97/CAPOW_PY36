# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 17:17:19 2019

@author: sdenaro
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


prices=pd.DataFrame()
for i in range(0,200):
    df=pd.read_csv('PNW'+str(i)+'/sim_hourly_prices.csv')
    prices=pd.concat([prices, df.PNW])
    
prices.reset_index(inplace=True)
prices.columns=['index','hourly prices']
prices=pd.DataFrame(prices['hourly prices'])

prices.to_csv('PNW_hourly_prices_merged.csv')

