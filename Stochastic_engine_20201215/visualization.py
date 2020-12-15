# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 00:15:34 2020

@author: 11487
"""
import seaborn as sns; sns.set(color_codes=True)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def sub_fig1(C_obs,C_sim,title0):
    
    bar_min=min(np.nanmin(C_obs),np.nanmin(C_sim))
    bar_max=max(np.nanmax(C_obs),np.nanmax(C_sim))
    
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
    
    fig.suptitle(title0)
    
    # plt.close(fig)
    # plt.savefig('test.png',dpi=1000,bbox_inches='tight')
    # plt.show()  
    
    return plt

def sub_fig2(C_obs,C_sim,title0):
    import seaborn as sns; sns.set()
    dC=C_sim-C_obs
    bar_min=np.nanmin(dC)
    bar_max=np.nanmax(dC)
    # fig = matplotlib.pyplot.gcf()
    # fig.set_size_inches(18.5, 10.5)
    ax2=plt.figure()
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    cmap = sns.diverging_palette(20, 200, sep=20, as_cmap=True)
    ax = sns.heatmap(dC,cmap=cmap, vmin=bar_min, vmax=bar_max)
    ax.tick_params(labelsize='large')

    # ax.set_title(subtitle0)
    
    
    plt.axis('off')
    
    ax2.suptitle(title0)
    
    # plt.close(ax2)
    # plt.savefig('test.png',dpi=1000,bbox_inches='tight')
    # plt.show()  
    
    return plt

def plot_cor_mat1(cor_mat):
    
    plt2=sub_fig1(cor_mat.C_wea_irr_obs,cor_mat.C_wea_irr_sim)
    plt2.savefig('corrcoef_strs_{}.png'.format(strs_obs.shape[1]),dpi=1000,bbox_inches='tight')
    plt2.show()
    
    return None

def wea_sta_fig(wea_obs,wea_sim,title0):
    # sim_years=1000; yearbeg=2005; yearend=2034;
    # sim_years2=sim_years+3;
    # %% reading weather data
    # filename1='Historical_weather_analysis/WIND_TEMP_{}-{}.csv'.format(yearbeg, yearend)
    # filename2='Synthetic_weather/synthetic_weather_data_{}-{}_{}.csv'.format(yearbeg, yearend, sim_years2)
    # wea_obs0=pd.read_csv(filename1); wea_obs1=wea_obs0.iloc[:,1:]
    # wea_sim0=pd.read_csv(filename2); wea_sim1=wea_sim0.iloc[:,1:]
    # # sorting the columns into temperature and windspeed 
    # reorder=[int(i) for i in [*range(0,wea_obs1.shape[1],2),*range(1,wea_obs1.shape[1]+1,2)]];
    # wea_obs=wea_obs1.iloc[:,reorder]
    # wea_sim=wea_sim1.iloc[:,reorder]
    
    #     # comparing the percentiles of obs and sim
    percentiles=[0,1,50,99,100]
    perc_obs=np.percentile(wea_obs,percentiles ,axis=0)
    perc_sim=np.percentile(wea_sim,percentiles ,axis=0)
    
    num_site=int(perc_obs.shape[1]/2);# number of stations or sites
    num_perc=len(percentiles)
    tem_obs=perc_obs[:,0:num_site]; win_obs=perc_obs[:,num_site:];
    tem_sim=perc_sim[:,0:num_site]; win_sim=perc_sim[:,num_site:];
    
    fig, (ax1, ax2) = plt.subplots(2, 1)
    
    x=np.arange(1,num_site+1,1)
    labels1=['Obs$\mathregular{_{min}}$','Obs$\mathregular{_{1\%}}$','Obs$\mathregular{_{50\%}}$','Obs$\mathregular{_{99\%}}$','Obs$\mathregular{_{max}}$']
    labels2=['Sim$\mathregular{_{min}}$','Sim$\mathregular{_{1\%}}$','Sim$\mathregular{_{50\%}}$','Sim$\mathregular{_{99\%}}$','Sim$\mathregular{_{max}}$']
    clist=[[158,1,66],[244,109,67],[102,194,165],[50,136,189],[94,79,162]]
    colors = np.array(clist)/255
    for i in np.arange(0,num_perc):
        ax1.plot(x,tem_obs[i,:],color=colors[i,:],marker='.',ls='-',linewidth=0.75,label=labels1[i])
        ax1.plot(x,tem_sim[i,:],color=colors[i,:],ls='--',linewidth=1,label=labels2[i])
        
        ax2.plot(x,win_obs[i,:],color=colors[i,:],marker='.',ls='-',linewidth=0.75,label=labels1[i])
        ax2.plot(x,win_sim[i,:],color=colors[i,:],ls='--',linewidth=1,label=labels2[i])
        
    ax1.set_ylabel('Temperature ($^\circ$C)');
    ax1.set_title(title0)
    ax2.set_ylabel('Wind speed (m/s)');
    
    
    plt.xlabel('Site number')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 2.8),fancybox=True, shadow=True, ncol=5,fontsize=12,frameon=False)
     
    fig.subplots_adjust(bottom=0.0, left=-0.2)
    # fig.suptitle('Original and synthetic weather')
    
    # plt.show()
    # plt.close('all')
    
    return fig

def str_sta_fig(sim_years,yearbeg,yearend,title0):
    # sim_years=1000; yearbeg=2005; yearend=2034;
    sim_years2=sim_years+3;
    # %% reading weather data
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
    
    #     # comparing the percentiles of obs and sim
    percentiles=[0,1,50,99,100]
    perc_obs=np.percentile(strs_obs,percentiles ,axis=0)
    perc_sim=np.percentile(strs_sim,percentiles ,axis=0)
    
    num_site=int(perc_obs.shape[1]);# number of stations or sites
    num_perc=len(percentiles)
    # tem_obs=perc_obs[:,0:num_site]; win_obs=perc_obs[:,num_site:];
    # tem_sim=perc_sim[:,0:num_site]; win_sim=perc_sim[:,num_site:];
    
    fig, (ax1) = plt.subplots(1, 1)
    
    x=np.arange(1,num_site+1,1)
    labels1=['Obs$\mathregular{_{min}}$','Obs$\mathregular{_{1\%}}$','Obs$\mathregular{_{50\%}}$','Obs$\mathregular{_{99\%}}$','Obs$\mathregular{_{max}}$']
    labels2=['Sim$\mathregular{_{min}}$','Sim$\mathregular{_{1\%}}$','Sim$\mathregular{_{50\%}}$','Sim$\mathregular{_{99\%}}$','Sim$\mathregular{_{max}}$']
    clist=[[158,1,66],[244,109,67],[102,194,165],[50,136,189],[94,79,162]]
    colors = np.array(clist)/255
    for i in np.arange(0,num_perc):
        ax1.plot(x,perc_obs[i,:],color=colors[i,:],marker='.',ls='-',linewidth=0.75,label=labels1[i])
        ax1.plot(x,perc_sim[i,:],color=colors[i,:],ls='--',linewidth=1,label=labels2[i])
        
    ax1.set_ylabel('Temperature ($^\circ$C)');
    ax1.set_title(title0)

    
    
    plt.xlabel('Site number')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0),fancybox=True, shadow=True, ncol=5,fontsize=12,frameon=False)
     
    # fig.subplots_adjust(bottom=0.0, left=-0.2)
    # fig.suptitle('Original and synthetic weather')
    
    plt.show()
    # plt.close('all')
    
    return fig
    
    
    
    
    
    