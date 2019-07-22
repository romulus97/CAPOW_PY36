# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:29:02 2018

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
import statsmodels.api as sm
import random
from datetime import datetime
from datetime import timedelta

cities_var = ['Salem','Eugene','Seattle','Boise','Portland','Spokane','Pasco','Fresno','Los_Angeles','San_Diego','Sacramento','San_Jose','San_Francisco','Tucson','Phoenix','Las_Vegas','Oakland']

#############################################################################
#Validate wind and temperature 
sim_data=pd.read_csv('synthetic_weather_data.csv',header=0, index_col=0)
sim_data=sim_data.as_matrix()

Normal_Starting=datetime(1900,1,1)

datelist=pd.date_range(Normal_Starting,periods=365)
count=0
m=np.zeros(len(sim_data))
for i in range(0,len(sim_data)):
    m[i]=int(datelist[count].month)
    count= count +1
    if count >364:
        count=0
d_sim=np.column_stack((sim_data,m))        
sim_data_yearly= np.reshape(d_sim,(103,365,35))

his_data=pd.read_csv('WIND_TEMP.csv',header=0)
his_data=his_data.as_matrix()

m=np.zeros(len(his_data))
for i in range(0,len(his_data)):
    current_time=his_data[i,0]
    current_time_dt=datetime.strptime(current_time,'%m/%d/%Y')
    m[i]= int(current_time_dt.month)
d_his=np.column_stack((his_data,m))
d_his=d_his[:6935,1:36]
his_data_yearly= np.reshape(d_his,(18,365,35))


####################

for i in range(0,35):
    exec("t%s_ave_sim=np.zeros(12)" %(i))
    exec("t%s_std_sim=np.zeros(12)" %(i))
    exec("t%s_min_sim=np.zeros(12)" %(i))
    exec("t%s_max_sim=np.zeros(12)" %(i))

    exec("t%s_ave_his=np.zeros(12)" %(i))
    exec("t%s_std_his=np.zeros(12)" %(i))
    exec("t%s_min_his=np.zeros(12)" %(i))
    exec("t%s_max_his=np.zeros(12)" %(i))
    
    
    
    
for i in range(1,13):
    d1=sim_data_yearly[sim_data_yearly[:,:,34]==i]
    d2=his_data_yearly[his_data_yearly[:,:,34]==i]
    for j in range(0,34):
        exec("t%s_ave_sim[i-1]=np.nanmean(d1[:,j])" %(j))
        exec("t%s_std_sim[i-1]=np.nanstd(d1[:,j])" %(j))
        exec("t%s_min_sim[i-1]=np.min(d1[:,j])" %(j))
        exec("t%s_max_sim[i-1]=np.max(d1[:,j])" %(j))
        
        exec("t%s_ave_his[i-1]=np.nanmean(list(d2[:,j]))" %(j))
        exec("t%s_std_his[i-1]=np.nanstd(list(d2[:,j]))" %(j))
        exec("t%s_min_his[i-1]=np.min(list(d2[:,j]))" %(j))
        exec("t%s_max_his[i-1]=np.max(list(d2[:,j]))" %(j))
        
        
fig_1=plt.figure(1)
plt.title('Temperature Validation')

plt.subplot(451)
plt.errorbar(np.arange(12), t0_ave_sim, t0_std_sim, fmt='bv',lw=3)

#plt.errorbar(np.arange(12), t0_ave_sim, [t0_ave_sim - t0_min_sim, t0_max_sim - t0_ave_sim],
#             fmt='.b', ecolor='grey', lw=1)

plt.errorbar(np.arange(12), t0_ave_his, t0_std_his, fmt='ro',lw=3)
plt.title('Salem')

#plt.errorbar(np.arange(12), t0_ave_his, [t0_ave_his - t0_min_his, t0_max_his - t0_ave_his],
#             fmt='.r', ecolor='orange', lw=1)
plt.xlim(-1, 13)

plt.subplot(452)
plt.errorbar(np.arange(12), t2_ave_sim, t2_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t2_ave_his, t2_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[1])

plt.subplot(453)
plt.errorbar(np.arange(12), t4_ave_sim, t4_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t4_ave_his, t4_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[2])

plt.subplot(454)
plt.errorbar(np.arange(12), t6_ave_sim, t6_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t6_ave_his, t6_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[3])

plt.subplot(455)
plt.errorbar(np.arange(12), t8_ave_sim, t8_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t8_ave_his, t8_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[4])

plt.subplot(456)
plt.errorbar(np.arange(12), t10_ave_sim, t10_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t10_ave_his, t10_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[5])

plt.subplot(457)
plt.errorbar(np.arange(12), t12_ave_sim, t12_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t12_ave_his, t12_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[6])

plt.subplot(458)
plt.errorbar(np.arange(12), t14_ave_sim, t14_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t14_ave_his, t14_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[7])

plt.subplot(459)
plt.errorbar(np.arange(12), t16_ave_sim, t16_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t16_ave_his, t16_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[8])

plt.subplot(4,5,10)
plt.errorbar(np.arange(12), t18_ave_sim, t18_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t18_ave_his, t18_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[9])

plt.subplot(4,5,11)
plt.errorbar(np.arange(12), t20_ave_sim, t20_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t20_ave_his, t20_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[10])

plt.subplot(4,5,12)
plt.errorbar(np.arange(12), t22_ave_sim, t22_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t22_ave_his, t22_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[11])

plt.subplot(4,5,13)
plt.errorbar(np.arange(12), t24_ave_sim, t24_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t24_ave_his, t24_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[12])


plt.subplot(4,5,14)
plt.errorbar(np.arange(12), t26_ave_sim, t26_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t26_ave_his, t26_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[13])


plt.subplot(4,5,15)
plt.errorbar(np.arange(12), t28_ave_sim, t28_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t28_ave_his, t28_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[14])


plt.subplot(4,5,17)
plt.errorbar(np.arange(12), t30_ave_sim, t30_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t30_ave_his, t30_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[15])


plt.subplot(4,5,18)
plt.errorbar(np.arange(12), t32_ave_sim, t32_std_sim, fmt='bv',lw=3,label='Synthetic')
plt.errorbar(np.arange(12), t32_ave_his, t32_std_his, fmt='ro',lw=3,label='Historical')
plt.xlim(-1, 13)
plt.title(cities_var[16])

plt.subplots_adjust(top=0.90, bottom=0.08, left=0.10, right=0.95, hspace=0.8,wspace=0.35)
plt.legend(bbox_to_anchor=(1, 0, 2, 1))

fig_1.suptitle('Temperature Validation',size=18)
#############################################################################################
fig_2=plt.figure(2)

plt.subplot(451)
plt.errorbar(np.arange(12), t1_ave_sim, t1_std_sim, fmt='bv',lw=3)

#plt.errorbar(np.arange(12), t0_ave_sim, [t0_ave_sim - t0_min_sim, t0_max_sim - t0_ave_sim],
#             fmt='.b', ecolor='grey', lw=1)

plt.errorbar(np.arange(12), t1_ave_his, t1_std_his, fmt='ro',lw=3)
plt.title('Salem')

#plt.errorbar(np.arange(12), t0_ave_his, [t0_ave_his - t0_min_his, t0_max_his - t0_ave_his],
#             fmt='.r', ecolor='orange', lw=1)
plt.xlim(-1, 13)

plt.subplot(452)
plt.errorbar(np.arange(12), t3_ave_sim, t3_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t3_ave_his, t3_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[1])

plt.subplot(453)
plt.errorbar(np.arange(12), t5_ave_sim, t5_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t5_ave_his, t5_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[2])

plt.subplot(454)
plt.errorbar(np.arange(12), t7_ave_sim, t7_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t7_ave_his, t7_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[3])

plt.subplot(455)
plt.errorbar(np.arange(12), t9_ave_sim, t9_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t9_ave_his, t9_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[4])

plt.subplot(456)
plt.errorbar(np.arange(12), t11_ave_sim, t11_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t11_ave_his, t11_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[5])

plt.subplot(457)
plt.errorbar(np.arange(12), t13_ave_sim, t13_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t13_ave_his, t13_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[6])

plt.subplot(458)
plt.errorbar(np.arange(12), t15_ave_sim, t15_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t15_ave_his, t15_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[7])

plt.subplot(459)
plt.errorbar(np.arange(12), t17_ave_sim, t17_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t17_ave_his, t17_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[8])

plt.subplot(4,5,10)
plt.errorbar(np.arange(12), t19_ave_sim, t19_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t19_ave_his, t19_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[9])

plt.subplot(4,5,11)
plt.errorbar(np.arange(12), t21_ave_sim, t21_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t21_ave_his, t21_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[10])

plt.subplot(4,5,12)
plt.errorbar(np.arange(12), t23_ave_sim, t23_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t23_ave_his, t23_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[11])

plt.subplot(4,5,13)
plt.errorbar(np.arange(12), t25_ave_sim, t25_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t25_ave_his, t25_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[12])


plt.subplot(4,5,14)
plt.errorbar(np.arange(12), t27_ave_sim, t27_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t27_ave_his, t27_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[13])


plt.subplot(4,5,15)
plt.errorbar(np.arange(12), t29_ave_sim, t29_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t29_ave_his, t29_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[14])


plt.subplot(4,5,17)
plt.errorbar(np.arange(12), t31_ave_sim, t31_std_sim, fmt='bv',lw=3)
plt.errorbar(np.arange(12), t31_ave_his, t31_std_his, fmt='ro',lw=3)
plt.xlim(-1, 13)
plt.title(cities_var[15])


plt.subplot(4,5,18)
plt.errorbar(np.arange(12), t33_ave_sim, t33_std_sim, fmt='bv',lw=3,label='Synthetic')
plt.errorbar(np.arange(12), t33_ave_his, t33_std_his, fmt='ro',lw=3,label='Historical')
plt.xlim(-1, 13)
plt.title(cities_var[16])

plt.subplots_adjust(top=0.90, bottom=0.08, left=0.10, right=0.95, hspace=0.8,wspace=0.35)
plt.legend(bbox_to_anchor=(1, 0, 2, 1))

fig_2.suptitle('Wind Speed Validation',size=18)



#####################################################################################
##Covariance heat map
#cov_his=d_his[:,:33].astype(float)
#cov_sim=d_sim[:,:33]
#
#x=np.argwhere(np.isnan(cov_his))
#for i in range(0,len(x)):
#    cov_his[x[i,0],x[i,1]] = cov_his[x[i,0]-1,x[i,1]]
#
#x=np.argwhere(np.isnan(cov_his))
#
#cov_sim_cal=np.cov(cov_sim,rowvar=False)
#
#cov_his_cal=np.cov(cov_his,rowvar=False)
#cov_all=cov_sim_cal-cov_his_cal
#import seaborn as sns; sns.set()
#plt.figure(3)
#plt.subplot(221)
#sns.heatmap(cov_sim_cal)
#plt.axis('off')
#plt.title('Cov_Matrix for synthetic records')
#
#plt.subplot(222)
#sns.heatmap(cov_his_cal)
#plt.axis('off')
#plt.title('Cov_Matrix for historical records')
#
#plt.subplot(223)
#
#sns.heatmap(cov_all,vmin=-100,vmax=100)
#plt.axis('off')
#plt.title('Cov_Matrix difference')
#
#plt.subplot(224)
#sns.heatmap(cov_all)
#plt.axis('off')
#plt.title('Cov_Matrix difference - zoom in')
