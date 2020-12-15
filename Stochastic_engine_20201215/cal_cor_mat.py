# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:04:00 2020

@author: 11487
"""
from __future__ import division
from datetime import datetime
from sklearn import linear_model
import pandas as pd
import numpy as np
import scipy.stats as st
import statsmodels.distributions.empirical_distribution as edis
import seaborn as sns; sns.set(color_codes=True)
import matplotlib.pyplot as plt

# %%
class Cor_Mat(object):
  # __slots__ = ["C_wea_irr_obs", "C_wea_irr_sim", "C_strs_obs","C_strs_sim","C_wea_irr_strs_obs","C_wea_irr_strs_sim","need_to_remove"]
  def __init__(self, C_wea_irr_obs, C_wea_irr_sim, C_strs_obs, C_strs_sim, C_wea_irr_strs_obs,C_wea_irr_strs_sim,need_to_remove):
     self.C_wea_irr_obs = C_wea_irr_obs
     self.C_wea_irr_sim = C_wea_irr_sim
     self.C_strs_obs = C_strs_obs
     self.C_strs_sim = C_strs_sim
     self.C_wea_irr_strs_obs = C_wea_irr_strs_obs
     self.C_wea_irr_strs_sim = C_wea_irr_strs_sim
     self.need_to_remove = need_to_remove

def cal_annual(x): 
    "calculate the annual sum values of variable x"
    y=np.zeros((int(x.shape[0]/365),x.shape[1]))
    for i in range(0,x.shape[1]):
        temp1=np.reshape(x[:,i], (int(x.shape[0]/365),365))
        temp2=np.transpose(temp1.sum(1))
        y[:,i]=temp2
    return y


def cal_cor_mats(sim_years,yearbeg,yearend):
    
    # sim_years=1000; yearbeg=2005; yearend=2034;
    sim_years2=sim_years+3;
    # %% reading weather data
    filename1='Historical_weather_analysis/WIND_TEMP_{}-{}.csv'.format(yearbeg, yearend)
    filename2='Synthetic_weather/synthetic_weather_data_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2)
    wea_obs0=pd.read_csv(filename1); wea_obs1=wea_obs0.iloc[:,1:]
    wea_sim0=pd.read_csv(filename2); wea_sim1=wea_sim0.iloc[:,1:]
    # sorting the columns into temperature and windspeed 
    reorder=[int(i) for i in [*range(0,wea_obs1.shape[1],2),*range(1,wea_obs1.shape[1]+1,2)]];
    wea_obs=wea_obs1.iloc[:,reorder]
    wea_sim=wea_sim1.iloc[:,reorder]
    
    # %% reading irradiance data
    filename1='Historical_weather_analysis/daily_irr_{}-{}.csv'.format(yearbeg, yearend)
    filename2='Synthetic_weather/synthetic_irradiance_data_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2)
    irr_obs0=pd.read_csv(filename1); irr_obs=irr_obs0.iloc[:,1:]
    irr_sim0=pd.read_csv(filename2); irr_sim=irr_sim0.iloc[:,1:]

    wea_irr_obs=np.column_stack((wea_obs,irr_obs))
    wea_irr_sim=np.column_stack((wea_sim,irr_sim))
    
    #correlation coefficient matrix of weather and irridiance
    C_wea_irr_obs=np.corrcoef(wea_irr_obs,rowvar=0)
    C_wea_irr_sim=np.corrcoef(wea_irr_sim,rowvar=0)
    
    # %% reading streamflow data
    
    str_BPA_obs0=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_BPA_{}-{}.csv'.format(yearbeg, yearend),header=0)
    str_Hov_obs0=pd.read_csv('Synthetic_streamflows/synthetic_discharge_Hoover_{}-{}.csv'.format(yearbeg, yearend),header=0)
    str_Cal_obs0=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_CA_{}-{}.csv'.format(yearbeg, yearend),header=0)
    str_Wil_obs0=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_Willamette_{}-{}.csv'.format(yearbeg, yearend),header=0)
    
    str_BPA_obs=str_BPA_obs0.iloc[:,3:]; num_str_BPA_obs=np.arange(0,str_BPA_obs.shape[1]);
    str_Cal_obs=str_Cal_obs0.iloc[:,3:]; num_str_Cal_obs=np.arange(num_str_BPA_obs[-1]+1,num_str_BPA_obs[-1]+1+str_Cal_obs.shape[1])
    str_Wil_obs=str_Wil_obs0.iloc[:,3:]; num_str_Wil_obs=np.arange(num_str_Cal_obs[-1]+1,num_str_Cal_obs[-1]+1+str_Wil_obs.shape[1])
    str_Hov_obs=str_Hov_obs0.iloc[:,3:]; num_str_Hov_obs=np.arange(num_str_Wil_obs[-1]+1,num_str_Wil_obs[-1]+1+str_Hov_obs.shape[1])
    
    
    str_BPA_sim=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_FCRPS_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=False,header=None)
    str_Hov_sim=pd.read_csv('Synthetic_streamflows/synthetic_discharge_Hoover_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=False,header=None)
    str_Cal_sim=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_CA_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=0,header=0)
    str_Wil_sim=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_Willamette_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=0,header=0)

    strs_obs0=np.column_stack((str_BPA_obs,str_Cal_obs,str_Wil_obs,str_Hov_obs))
    strs_sim0=np.column_stack((str_BPA_sim,str_Cal_sim,str_Wil_sim,str_Hov_sim))
    
    # removing records with invalid streamflow values
    need_to_remove=np.where(np.min(strs_obs0,axis=0)==np.max(strs_obs0,axis=0));
    strs_obs=np.delete(strs_obs0,need_to_remove,axis=1)
    strs_sim=np.delete(strs_sim0,need_to_remove,axis=1)
    
    aax0=np.where(num_str_BPA_obs==need_to_remove)
    
    num_str_BPA_obs2=num_str_BPA_obs[~np.in1d(num_str_BPA_obs, need_to_remove)];
    num_str_Cal_obs2=num_str_Cal_obs[~np.in1d(num_str_Cal_obs, need_to_remove)];
    num_str_Wil_obs2=num_str_Wil_obs[~np.in1d(num_str_Wil_obs, need_to_remove)];
    num_str_Hov_obs2=num_str_Hov_obs[~np.in1d(num_str_Hov_obs, need_to_remove)];
    import  itertools
    num_strs=list(itertools.chain(num_str_BPA_obs2,num_str_Cal_obs2,num_str_Wil_obs2,num_str_Hov_obs2));
    num_strs_num=[len(num_str_BPA_obs2),len(num_str_Cal_obs2),len(num_str_Wil_obs2),len(num_str_Hov_obs2)] # num_strs_num = [43, 22, 21, 1]
    
    
    # # calculating the annual steamflow
    # strs_obs_a=cal_annual(strs_obs)
    # strs_sim_a=cal_annual(strs_sim)
    # C_obs=np.corrcoef(strs_obs_a,rowvar=0)
    # C_sim=np.corrcoef(strs_sim_a,rowvar=0)

    #correlation coefficient matrix of streamflow
    C_strs_obs=np.corrcoef(strs_obs,rowvar=0)
    C_strs_sim=np.corrcoef(strs_sim,rowvar=0)
 
    wea_irr_strs_obs=np.column_stack((wea_irr_obs,strs_obs));
    wea_irr_strs_sim=np.column_stack((wea_irr_sim,strs_sim));
    #correlation coefficient matrix of weather, irridiance, and streamflow
    C_wea_irr_strs_obs=np.corrcoef(wea_irr_strs_obs,rowvar=0)
    C_wea_irr_strs_sim=np.corrcoef(wea_irr_strs_sim,rowvar=0)


    return Cor_Mat(C_wea_irr_obs, C_wea_irr_sim, C_strs_obs, C_strs_sim, C_wea_irr_strs_obs,C_wea_irr_strs_sim,need_to_remove)


def visualization(sim_years,yearbeg,yearend):
    
    sim_years=1000; yearbeg=2005; yearend=2034;
    sim_years2=sim_years+3;
    # %% reading weather data
    filename1='Historical_weather_analysis/WIND_TEMP_{}-{}.csv'.format(yearbeg, yearend)
    filename2='Synthetic_weather/synthetic_weather_data_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2)
    wea_obs0=pd.read_csv(filename1); wea_obs1=wea_obs0.iloc[:,1:]
    wea_sim0=pd.read_csv(filename2); wea_sim1=wea_sim0.iloc[:,1:]
    # sorting the columns into temperature and windspeed 
    reorder=[int(i) for i in [*range(0,wea_obs1.shape[1],2),*range(1,wea_obs1.shape[1]+1,2)]];
    wea_obs=wea_obs1.iloc[:,reorder]
    wea_sim=wea_sim1.iloc[:,reorder]
    
    # %% reading irradiance data
    filename1='Historical_weather_analysis/daily_irr_{}-{}.csv'.format(yearbeg, yearend)
    filename2='Synthetic_weather/synthetic_irradiance_data_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2)
    irr_obs0=pd.read_csv(filename1); irr_obs=irr_obs0.iloc[:,1:]
    irr_sim0=pd.read_csv(filename2); irr_sim=irr_sim0.iloc[:,1:]

    wea_irr_obs=np.column_stack((wea_obs,irr_obs))
    wea_irr_sim=np.column_stack((wea_sim,irr_sim))
    
    #correlation coefficient matrix of weather and irridiance
    C_obs=np.corrcoef(wea_irr_obs,rowvar=0)
    C_sim=np.corrcoef(wea_irr_sim,rowvar=0)
    
    
    
    plt1=sub_fig1(C_obs,C_sim)
    plt1.savefig('corrcoef_wea_{}_irr_{}.png'.format(wea_obs.shape[1],irr_obs.shape[1]),dpi=1000,bbox_inches='tight')
    plt1.show()
    
    plt0=sub_fig2(C_sim-C_obs)
    plt0.savefig('corrcoef_wea_{}_irr_{}_dso.png'.format(wea_obs.shape[1],irr_obs.shape[1]),dpi=1000,bbox_inches='tight')
    plt0.show()
    
    
    
    # %% reading streamflow data
    
    str_BPA_obs0=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_BPA_{}-{}.csv'.format(yearbeg, yearend),header=0)
    str_Hov_obs0=pd.read_csv('Synthetic_streamflows/synthetic_discharge_Hoover_{}-{}.csv'.format(yearbeg, yearend),header=0)
    str_Cal_obs0=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_CA_{}-{}.csv'.format(yearbeg, yearend),header=0)
    str_Wil_obs0=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_Willamette_{}-{}.csv'.format(yearbeg, yearend),header=0)
    
    str_BPA_obs=str_BPA_obs0.iloc[:,3:];
    str_Hov_obs=str_Hov_obs0.iloc[:,3:];
    str_Cal_obs=str_Cal_obs0.iloc[:,3:];
    str_Wil_obs=str_Wil_obs0.iloc[:,3:];
    
    str_BPA_sim=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_FCRPS_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=False,header=None)
    str_Hov_sim=pd.read_csv('Synthetic_streamflows/synthetic_discharge_Hoover_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=False,header=None)
    str_Cal_sim=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_CA_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=0,header=0)
    str_Wil_sim=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_Willamette_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2),index_col=0,header=0)

    strs_obs0=np.column_stack((str_BPA_obs,str_Cal_obs,str_Wil_obs,str_Hov_obs))
    strs_sim0=np.column_stack((str_BPA_sim,str_Cal_sim,str_Wil_sim,str_Hov_sim))
    
    # removing records with invalid streamflow values
    need_to_remove=np.where(np.min(strs_obs0,axis=0)==np.max(strs_obs0,axis=0));
    strs_obs=np.delete(strs_obs0,need_to_remove,axis=1)
    strs_sim=np.delete(strs_sim0,need_to_remove,axis=1)
    
    # calculating the annual steamflow
    strs_obs_a=cal_annual(strs_obs)
    strs_sim_a=cal_annual(strs_sim)
    C_obs=np.corrcoef(strs_obs_a,rowvar=0)
    C_sim=np.corrcoef(strs_sim_a,rowvar=0)
    plt2=sub_fig1(C_obs,C_sim)
    plt2.show()
    plt0=sub_fig2(C_sim-C_obs)
    plt0.show()
    
    
    #correlation coefficient matrix of streamflow
    C_obs=np.corrcoef(strs_obs,rowvar=0)
    C_sim=np.corrcoef(strs_sim,rowvar=0)
    plt2=sub_fig1(C_obs,C_sim)
    plt2.savefig('corrcoef_strs_{}.png'.format(strs_obs.shape[1]),dpi=1000,bbox_inches='tight')
    plt2.show()
    
    plt0=sub_fig2(C_sim-C_obs)
    plt0.savefig('corrcoef_strs_{}_dso.png'.format(strs_obs.shape[1]),dpi=1000,bbox_inches='tight')
    plt0.show() 
    # temp1=np.column_stack((str_BPA_obs.min(),str_BPA_sim.min(),str_BPA_obs.mean(),str_BPA_sim.mean(),str_BPA_obs.max(),str_BPA_sim.max()))
    # temp2=np.column_stack((str_Hov_obs.min(),str_Hov_sim.min(),str_Hov_obs.mean(),str_Hov_sim.mean(),str_Hov_obs.max(),str_Hov_sim.max()))
    # temp3=np.column_stack((str_Cal_obs.min(),str_Cal_sim.min(),str_Cal_obs.mean(),str_Cal_sim.mean(),str_Cal_obs.max(),str_Cal_sim.max()))
    # temp4=np.column_stack((str_Wil_obs.min(),str_Wil_sim.min(),str_Wil_obs.mean(),str_Wil_sim.mean(),str_Wil_obs.max(),str_Wil_sim.max()))


    #correlation coefficient matrix of weather, irridiance, and streamflow
    wea_irr_strs_obs=np.column_stack((wea_irr_obs,strs_obs));
    wea_irr_strs_sim=np.column_stack((wea_irr_sim,strs_sim));
    C_obs=np.corrcoef(wea_irr_strs_obs,rowvar=0)
    C_sim=np.corrcoef(wea_irr_strs_sim,rowvar=0)
    plt3=sub_fig1(C_obs,C_sim)
    plt3.savefig('corrcoef_wea_{}_irr_{}_strs_{}.png'.format(wea_obs.shape[1],irr_obs.shape[1],strs_obs.shape[1]),dpi=1000,bbox_inches='tight')
    plt3.show()
    plt0=sub_fig2(C_sim-C_obs)
    plt0.savefig('corrcoef_wea_{}_irr_{}_strs_{}_dso.png'.format(wea_obs.shape[1],irr_obs.shape[1],strs_obs.shape[1]),dpi=1000,bbox_inches='tight')
    plt0.show()
    
# =============================================================================
#     # comparing the percentiles of obs and sim
#     temp5=np.column_stack((wea_irr_strs_obs.min(0),wea_irr_strs_sim.min(0),wea_irr_strs_obs.mean(0),wea_irr_strs_sim.mean(0),wea_irr_strs_obs.max(0),wea_irr_strs_sim.max(0)))
#     percentiles=[*range(0,101,1)]
#     perc_obs=np.percentile(wea_irr_strs_obs,percentiles ,axis=0)
#     perc_sim=np.percentile(wea_irr_strs_sim,percentiles ,axis=0)
#     std_obs=np.std(wea_irr_strs_obs,axis=0)
#     std_sim=np.std(wea_irr_strs_sim,axis=0)
#     plt.subplot(121);plt.plot(np.transpose(perc_obs));
#     plt.subplot(122);plt.plot(np.transpose(perc_sim));plt.show()
#     plt.plot(np.transpose((perc_sim-perc_obs)/perc_obs));plt.show()
#     aa1=std_obs-std_sim
#     aa2=np.transpose(aa1)
#     plt.plot(aa2);plt.show()
# =============================================================================
    
    return None

def sub_fig1_1(C_obs,C_sim):
    import seaborn as sns; sns.set()
    
    grid_kws = {"height_ratios": (.9, .05), "hspace": .3}
    fig,ax=plt.subplots()
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    ax1=plt.subplot(121)
    sns.heatmap(C_obs,vmin=0,vmax=1,cbar=False)
    plt.axis('off')
    ax.set_title('Syn')
    
    
    ax2=plt.subplot(122)
    cbar_ax = fig.add_axes([.92, .15, .03, .7])  # <-- Create a colorbar axes
    
    fig2=sns.heatmap(C_sim,ax=ax2,cbar_ax=cbar_ax,vmin=0,vmax=1)
    cbar=ax2.collections[0].colorbar
    cbar.ax.tick_params(labelsize='large')
    
    fig2.axis('off') 
    # plt.savefig('test.png',dpi=1000,bbox_inches='tight')
    # plt.show()  
    
    return plt

def sub_fig1(C_obs,C_sim):
    
    bar_min=min(C_obs.min(),C_sim.min())
    bar_max=max(C_obs.max(),C_sim.max())
    bar_minmax=[bar_min,bar_max];
    
    import seaborn as sns; sns.set()
    cmap0=sns.diverging_palette(20, 200, s=90, sep=1, n=256, as_cmap=True)

    grid_kws = {"height_ratios": (.9, .05), "hspace": .3}
    fig,ax=plt.subplots()
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    ax1=plt.subplot(121)
    fig1=sns.heatmap(C_obs,vmin=bar_minmax[0],vmax=bar_minmax[1],center=0,cbar=False,cmap=cmap0)
    plt.axis('off')
    fig1.set_title('Obs')
    
    
    ax2=plt.subplot(122)
    cbar_ax = fig.add_axes([.92, .15, .03, .7])  # <-- Create a colorbar axes
    
    fig2=sns.heatmap(C_sim,ax=ax2,cbar_ax=cbar_ax,vmin=bar_minmax[0],vmax=bar_minmax[1],center=0,cmap=cmap0)
    cbar=ax2.collections[0].colorbar
    cbar.ax.tick_params(labelsize='large')
    
    fig2.axis('off')
    fig2.set_title('Sim')
    # plt.savefig('test.png',dpi=1000,bbox_inches='tight')
    # plt.show()  
    
    return plt

def sub_fig2(C_obs):
    import seaborn as sns; sns.set()
    bar_min=C_obs.min()
    bar_max=C_obs.max()
    # fig = matplotlib.pyplot.gcf()
    # fig.set_size_inches(18.5, 10.5)
    ax2=plt.figure()
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    cmap = sns.diverging_palette(20, 200, sep=20, as_cmap=True)
    ax = sns.heatmap(C_obs,cmap=cmap, vmin=bar_min, vmax=bar_max)
    ax.tick_params(labelsize='large')

    ax.set_title('Difference (Sim-Obs)')
    
    plt.axis('off')
    

    # plt.savefig('test.png',dpi=1000,bbox_inches='tight')
    # plt.show()  
    
    return plt



def cal_cor_mats2(sim_years,yearbeg,yearend):
# %% creating directory
    import os
    # define the name of the directory to be created
    newpath = "Correlation matrix/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        
    # %% caculating correlation matrix
    cor_mat1=cal_cor_mats(sim_years,yearbeg,yearend)
    # %% save matrix objectives in the file

    import pickle
    sim_years2=sim_years+3; # three more years of data are required
    filename=newpath+"cor_mat_{}-{}_{}.pkl".format(yearbeg, yearend, sim_years2)
    with open(filename, 'wb') as output:
        pickle.dump(cor_mat1, output, pickle.HIGHEST_PROTOCOL)

    # %% copy the module cal_cor_mat into the same folder of matrix files
        # this module or file is required to load the pkl files.
    import shutil  
    dest = shutil.copyfile('cal_cor_mat.py', newpath+'cal_cor_mat.py') 
    
    return cor_mat1
    
# %%
# sim_years=1000; yearbeg=2005; yearend=2034;
# newpath = "Correlation matrix/";
# filename=newpath+"cor_mat_{}-{}_{}.pkl".format(yearbeg, yearend, sim_years+3)

# import pickle
# cor_mat1=pd.read_pickle(filename) 
      
      
      
# object1 = pd.read_pickle(filename)
    
# visualization(sim_years,yearbeg,yearend)
# a=0;



    
    