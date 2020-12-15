# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 22:06:31 2020

@author: 11487
"""
# define the number of standard years of simulations, begin and end year of historical data
import matplotlib.pyplot as plt
import visualization as visu
import numpy as np
import pandas as pd

stoch_years=1000;yearbegs=[2005,2035]; yearends=[2034,2064];           

# %% caculating correlation matrix

# stoch_years=1000;yearbeg=2005;yearend=2034;   #2005/01/01-2034/12/31        
# stoch_years=1000;yearbeg=2035;yearend=2064;     #2035/01/01-2064/12/31
for period in range(0,len(yearbegs)):
    yearbeg=yearbegs[period]; yearend=yearends[period];
    title0='Scenario{}: {}-{}'.format(2,yearbeg,yearend)
    # f0=visu.str_sta_fig(stoch_years,yearbeg,yearend,title0)

    sim_years2=stoch_years+3;
    # %% reading weather data
    filename1='Historical_weather_analysis/WIND_TEMP_{}-{}.csv'.format(yearbeg, yearend)
    filename2='Synthetic_weather/synthetic_weather_data_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2)
    wea_obs0=pd.read_csv(filename1); wea_obs1=wea_obs0.iloc[:,1:]
    wea_sim0=pd.read_csv(filename2); wea_sim1=wea_sim0.iloc[:,1:]
    # sorting the columns into temperature and windspeed 
    reorder=[int(i) for i in [*range(0,wea_obs1.shape[1],2),*range(1,wea_obs1.shape[1]+1,2)]];
    wea_obs=wea_obs1.iloc[:,reorder]
    wea_sim=wea_sim1.iloc[:,reorder]
    
    if period==0:
        wea_obs_t=wea_obs.copy(deep=True); wea_sim_t=wea_sim.copy(deep=True);
    elif period==1:
        dwea_obs=wea_obs-wea_obs_t; dwea_sim=wea_sim-wea_sim_t;
        f=visu.wea_sta_fig(dwea_obs,dwea_sim,title0)
        plt.show()
        a=0
            
    
    f=visu.wea_sta_fig(wea_obs,wea_sim,title0)
    
    # plt.savefig('Wea_sta_fig_{}-{}.png'.format(yearbeg,yearend),dpi=400,bbox_inches='tight')
    plt.show()
    a=0;
a=0    
# %% reading streamflow data
    
# =============================================================================
#     str_BPA_obs0=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_BPA_{}-{}.csv'.format(yearbeg, yearend),header=0)
#     str_Hov_obs0=pd.read_csv('Synthetic_streamflows/synthetic_discharge_Hoover_{}-{}.csv'.format(yearbeg, yearend),header=0)
#     str_Cal_obs0=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_CA_{}-{}.csv'.format(yearbeg, yearend),header=0)
#     str_Wil_obs0=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_Willamette_{}-{}.csv'.format(yearbeg, yearend),header=0)
#     
#     str_BPA_obs=str_BPA_obs0.iloc[:,3:];
#     str_Hov_obs=str_Hov_obs0.iloc[:,3:];
#     str_Cal_obs=str_Cal_obs0.iloc[:,3:];
#     str_Wil_obs=str_Wil_obs0.iloc[:,3:];
#     
#     str_BPA_sim=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_FCRPS_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=False,header=None)
#     str_Hov_sim=pd.read_csv('Synthetic_streamflows/synthetic_discharge_Hoover_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=False,header=None)
#     str_Cal_sim=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_CA_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=0,header=0)
#     str_Wil_sim=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_Willamette_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=0,header=0)
# 
#     strs_obs0=np.column_stack((str_BPA_obs,str_Cal_obs,str_Wil_obs,str_Hov_obs))
#     strs_sim0=np.column_stack((str_BPA_sim,str_Cal_sim,str_Wil_sim,str_Hov_sim))
#     
#     # removing records with invalid streamflow values
#     need_to_remove=np.where(np.min(strs_obs0,axis=0)==np.max(strs_obs0,axis=0));
#     strs_obs=np.delete(strs_obs0,need_to_remove,axis=1)
#     strs_sim=np.delete(strs_sim0,need_to_remove,axis=1)
# =============================================================================
a=0;

# cor_mat=cal_cor_mat.cal_cor_mats(stoch_years, yearbeg, yearend)