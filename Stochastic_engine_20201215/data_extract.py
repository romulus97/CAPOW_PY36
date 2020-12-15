# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 23:48:47 2020

@author: 11487
"""

from __future__ import division
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta


def data_extract_wea(filename,yearbeg,yearend):
    
    
    datas0=pd.read_csv(filename);
    
    yearbeg0=int(filename[-13:-9]);
    yearend0=int(filename[-8:-4]);
    
    # remove the date with 29 days in Feb
    Date_index0=pd.date_range(datetime(yearbeg0,1,1),datetime(yearend0,12,31),freq='D');
    date_mask0 = (Date_index0.month==2) & (Date_index0.day==29);
    Date_index1=Date_index0[~date_mask0];
    
    # extract the data from beginning to the end
    date_mask1=(Date_index1>=datetime(yearbeg,1,1)) & (Date_index1<=datetime(yearend,12,31));
    
    Date_index=Date_index1[date_mask1];
    datas1=datas0[date_mask1];
    
    datas1.insert(1,'datetime', Date_index);
    datas2=datas1.drop(['Unnamed: 0'], axis=1);
    datas=datas2.reset_index(drop=True);
    
    return datas


def data_extract_irr(filename,yearbeg,yearend):
    
    datas0=pd.read_csv(filename);
    
    yearbeg0=int(filename[-13:-9]);
    yearend0=int(filename[-8:-4]);
    
    # remove the date with 29 days in Feb
    Date_index0=pd.date_range(datetime(yearbeg0,1,1),datetime(yearend0,12,31),freq='D');
    date_mask0 = (Date_index0.month==2) & (Date_index0.day==29);
    Date_index1=Date_index0[~date_mask0];
    
    # extract the data from beginning to the end
    date_mask1=(Date_index1>=datetime(yearbeg,1,1)) & (Date_index1<=datetime(yearend,12,31));
    
    Date_index=Date_index1[date_mask1];
    datas1=datas0[date_mask1];
    
    datas1.insert(1,'datetime', Date_index);
    datas2=datas1.drop(['Date'], axis=1);
    datas=datas2.reset_index(drop=True);

    return datas

def data_extract_str1(filename,yearbeg,yearend,index_col0,header0):
    
    # filename='Synthetic_streamflows/synthetic_discharge_Hoover_1954-2100.csv';
    datas0=pd.read_csv(filename,index_col=index_col0,header=header0);
    
    yearbeg0=int(filename[-13:-9]);
    yearend0=int(filename[-8:-4]);
    
    # remove the date with 29 days in Feb
    Date_index0=pd.date_range(datetime(yearbeg0,1,1),datetime(yearend0,12,31),freq='D');
    date_mask0 = (Date_index0.month==2) & (Date_index0.day==29);
    Date_index1=Date_index0[~date_mask0];
    
    # extract the data from beginning to the end
    date_mask1=(Date_index1>=datetime(yearbeg,1,1)) & (Date_index1<=datetime(yearend,12,31));
    
    Date_index=Date_index1[date_mask1];
    datas1=datas0[date_mask1];
    
    month=Date_index.month; day=Date_index.day; year=Date_index.year;
    
    datas1.insert(0,'month', month); datas1.insert(1,'day', day); datas1.insert(2,'year', year);

    # datas2=datas1.drop(['Date'], axis=1);
    datas=datas1.reset_index(drop=True);
    
    return datas

# yearbeg=2005; yearend=2034;

def data_extracts(yearbeg,yearend):
    # %%
    filename='Synthetic_streamflows/synthetic_streamflows_FCRPS_1954-2100.csv';
    datas_str_BPA=data_extract_str1(filename,yearbeg,yearend,index_col0=False,header0=None)
    column_names=pd.read_csv('Synthetic_streamflows/BPA_hist_streamflow-columns.csv', index_col=False,header=None);
    datas_str_BPA.columns.values[3:]=column_names.values;
    datas_str_BPA.to_csv('Synthetic_streamflows/synthetic_streamflows_BPA_{}-{}.csv'.format(yearbeg, yearend),index=False);
    
    filename='Synthetic_streamflows/synthetic_streamflows_Willamette_1954-2100.csv';
    datas_str_Willamette=data_extract_str1(filename,yearbeg,yearend,index_col0=0,header0=0)
    datas_str_Willamette.to_csv('Synthetic_streamflows/synthetic_streamflows_Willamette_{}-{}.csv'.format(yearbeg, yearend),index=False);
    
    filename='Synthetic_streamflows/synthetic_streamflows_CA_1954-2100.csv';
    datas_str_CA=data_extract_str1(filename,yearbeg,yearend,index_col0=0,header0=0)
    datas_str_CA.to_csv('Synthetic_streamflows/synthetic_streamflows_CA_{}-{}.csv'.format(yearbeg, yearend),index=False);
    
    filename='Synthetic_streamflows/synthetic_discharge_Hoover_1954-2100.csv';
    datas_str_Hoover=data_extract_str1(filename,yearbeg,yearend,index_col0=False,header0=0)
    datas_str_Hoover.columns.values[3]='Discharge'
    datas_str_Hoover.to_csv('Synthetic_streamflows/synthetic_discharge_Hoover_{}-{}.csv'.format(yearbeg, yearend),index=False);    
    
    # %%
    filename_irr='Historical_weather_analysis/synthetic_irradiance_data_1954-2097.csv';
    datas_irr=data_extract_irr(filename_irr,yearbeg, yearend);
    datas_irr.to_csv('Historical_weather_analysis/synthetic_irradiance_data_{}-{}.csv'.format(yearbeg, yearend));
    
    filename_wea='Historical_weather_analysis/synthetic_weather_data_1954-2100.csv';
    datas_wea=data_extract_wea(filename_wea,yearbeg, yearend);
    datas_wea.to_csv('Historical_weather_analysis/synthetic_weather_data_{}-{}.csv'.format(yearbeg, yearend));
    
    return None
