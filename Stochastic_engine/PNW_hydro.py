# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 22:17:00 2018

@author: jkern
"""

from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

########################################################
# This script calculates daily hydropower production for
# PNW zone using FCRPS, Willamette, and missing dams.

# FCRPS
df_FCRPS = pd.read_csv('PNW_hydro/FCRPS/Total_PNW_dams.csv',header=None)
FCRPS = df_FCRPS.values
F = np.sum(FCRPS,axis=1)

df_total = pd.DataFrame(F)
df_total.columns = ['PNW']
df_total.to_excel('PNW_hydro/PNW_hydro_daily.xlsx')
#################################################################


#BPA owned
df_BPA_own = pd.read_csv('PNW_hydro/FCRPS/BPA_owned_dams.csv',header=None)
BPA_own=pd.DataFrame(np.sum(df_BPA_own.values,axis=1))

# Willamette
import os
os.chdir("../Model_setup/")
df_streamflow = pd.read_csv('../Stochastic_engine/Synthetic_streamflows/synthetic_streamflows_Willamette.csv',header=0)
df_streamflow = df_streamflow.loc[:,'Albany':]
df_streamflow.to_csv('Willamette/one_year_Willamette.csv')
import Willamette_launch
df_Willamette = pd.read_excel('Willamette/Output/WillametteDAMS_hydropower.xlsx', usecols=np.arange(1,9))
Willamette=pd.DataFrame(24*df_Willamette.sum(axis=1),columns=['tot_Willamette_dailySum'])
#cut first and last year plus start at 243 to align with FCRPS output
Willamette = Willamette.iloc[365+243:len(Willamette)-(122+365),:]
Willamette= Willamette.reset_index(drop=True)
LC=Willamette*0.12 #Lost Creek
GP=Willamette*0.03 #Green Springs

BPA=sum([BPA_own, Willamette,LC,GP])
BPA.columns=['BPA_tot']
os.chdir("../Stochastic_engine/")
BPA.to_csv('PNW_hydro/BPA_total_daily')
