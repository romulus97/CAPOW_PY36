# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:36:13 2019

@author: YSu
"""

import pandas as pd
import numpy as np
import Fill_Gap


short=pd.read_csv('WIND_TEMP.csv',header=0)
long= pd.read_excel('hist_temps_1953_2007.xlsx')


cities = ['SALEM_T','EUGENE_T','SEATTLE_T','BOISE_T','PORTLAND_T','SPOKANE_T','FRESNO_T','LOS ANGELES_T','SAN DIEGO_T','SACRAMENTO_T','SAN FRANCISCO_T','TUCSON_T','PHOENIX_T','LAS VEGAS_T']
short_temperature=short[cities]

reg_1=['PASCO_T']
reg_2=['OAKLAND_T']
reg_3=['SAN JOSE_T']

reg_data1=short[reg_1]
reg_data2=short[reg_2]
reg_data3=short[reg_3]

store=np.zeros(np.shape(short_temperature))
c=0
for i in cities:
    Q=Fill_Gap.fillgap(short_temperature.loc[:,i],12)
    store[:,c]=Q
    c=c+1
    

d1=Fill_Gap.fillgap(reg_data1['PASCO_T'],12)
d2=Fill_Gap.fillgap(reg_data2['OAKLAND_T'],12)
d3=Fill_Gap.fillgap(reg_data3['SAN JOSE_T'],12)


#Set up regressions using all other station to predict the values in Pasco and Oakland
from sklearn import linear_model
p_reg=linear_model.LinearRegression()
o_reg=linear_model.LinearRegression()
s_reg=linear_model.LinearRegression()
#Train the model
o_reg.fit(store,d2)
o_reg.score(store,d2)

p_reg.fit(store,d1)
p_reg.score(store,d1)


s_reg.fit(store,d3)
s_reg.score(store,d3)


input_data=(long.values[:,1:]-32) * 5/9
o_pred=o_reg.predict(input_data)
p_pred=p_reg.predict(input_data)
s_pred=s_reg.predict(input_data)

new_temp=np.zeros((20075,17))
new_temp[:,:6]=input_data[:,:6]
new_temp[:,6]=p_pred
new_temp[:,7:11]=input_data[:,6:10]
new_temp[:,11]=s_pred
new_temp[:,12:16]=input_data[:,10:]
new_temp[:,16]=o_pred

cities2 = ['SALEM_T','EUGENE_T','SEATTLE_T','BOISE_T','PORTLAND_T','SPOKANE_T','PASCO_T','FRESNO_T','LOS ANGELES_T','SAN DIEGO_T','SACRAMENTO_T','SAN JOSE_T','SAN FRANCISCO_T','TUCSON_T','PHOENIX_T','LAS VEGAS_T','OAKLAND_T']

N=pd.DataFrame(new_temp)
N.columns=cities2
N.index=long['Time']
N.to_csv('Long_his_temp.csv')
