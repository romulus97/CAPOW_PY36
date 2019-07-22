# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:06:16 2018

@author: Joy Hill
"""

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import autocorrelation_plot
from pandas import ExcelWriter
import numpy as np
import scipy as sp

###this file is used to calculate local flows for control points##

#reading in cp historical data#
#data starts 10/01/1952

cfs_to_cms = 0.0283168

ALBin = pd.read_excel('CP_historical/ALBANY.xlsx',usecols=[2,3],skiprows=1736+92,skipfooter=3379+274,header=None)
SALin = pd.read_excel('CP_historical/SALEM.xlsx',usecols=[2,3],skiprows=1736+92,skipfooter=3379+274,header=None)
HARin = pd.read_excel('CP_historical/HARRISBURG.xlsx',usecols=[2,3],skiprows=1736+92,skipfooter=3379+274,header=None) 
HARshift = pd.read_excel('CP_historical/HARRISBURG.xlsx',usecols=[2,3],skiprows=1735+92,skipfooter=3380+274,header=None) #shifted one day ahead
VIDin = pd.read_excel('CP_historical/VIDA.xlsx',usecols=[2,3],skiprows=1736+92,skipfooter=3379+274,header=None)
JEFin = pd.read_excel('CP_historical/JEFFERSON.xlsx',usecols=[2,3],skiprows=1736+92,skipfooter=3379+274,header=None)
MEHin = pd.read_excel('CP_historical/MEHAMA.xlsx',usecols=[2,3],skiprows=1736+92,skipfooter=3379+274,header=None)
MONin = pd.read_excel('CP_historical/MONROE.xlsx',usecols=[2,3],skiprows=1736+92,skipfooter=3379+274,header=None) 
MONshift = pd.read_excel('CP_historical/MONROE.xlsx',usecols=[2,3],skiprows=1735+92,skipfooter=3380+274,header=None) #shifted one day ahead
WATin = pd.read_excel('CP_historical/WATERLOO.xlsx',usecols=[2,3],skiprows=1736+92,skipfooter=3379+274,header=None)
JASin = pd.read_excel('CP_historical/JASPER.xlsx',usecols=[2,3],skiprows=93,skipfooter=3379+274,header=None)
GOSin = pd.read_excel('CP_historical/GOSHEN.xlsx',usecols=[2,3],skiprows=732+91,skipfooter=3379+274,header=None)



#read in historical res outflow BPA data###
top=8951
bottom=274
BLUout = pd.read_excel('BLU5H_daily.xls',skiprows=top, skipfooter=bottom,header=None) #only using data from 2005
BCLout = pd.read_excel('BCL5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)#only using data from 2005
CGRout = pd.read_excel('CGR5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
DETout = pd.read_excel('DET5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
DEXout = pd.read_excel('LOP5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
DORout = pd.read_excel('DOR5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
FALout = pd.read_excel('FAL5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
FOSout = pd.read_excel('FOS5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
FRNout = pd.read_excel('FRN5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
GPRout = pd.read_excel('GPR5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
HCRout = pd.read_excel('HCR5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
LOPout = pd.read_excel('LOP5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
COTout = pd.read_excel('COT5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
FOSout = pd.read_excel('FOS5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)
LOPout = pd.read_excel('LOP5H_daily.xls',skiprows=top, skipfooter=bottom,header=None)



#calculate local flows#

SALloc = (SALin.iloc[:,1] - ALBin.iloc[:,1] - JEFin.iloc[:,1])*cfs_to_cms
JEFloc = (JEFin.iloc[:,1] - WATin.iloc[:,1] - MEHin.iloc[:,1])*cfs_to_cms
MEHloc = (MEHin.iloc[:,1] - BCLout.iloc[:,1])*cfs_to_cms
WATloc = (WATin.iloc[:,1] - FOSout.iloc[:,1])*cfs_to_cms
ALBloc = (ALBin.iloc[:,1] - MONshift.iloc[:,1] - HARshift.iloc[:,1])*cfs_to_cms
MONloc = (MONin.iloc[:,1] - FRNout.iloc[:,1])*cfs_to_cms
HARloc = (HARin.iloc[:,1] - VIDin.iloc[:,1] - GOSin.iloc[:,1] - JASin.iloc[:,1])*cfs_to_cms
VIDloc = (VIDin.iloc[:,1] - CGRout.iloc[:,1] - BLUout.iloc[:,1])*cfs_to_cms
JASloc = (JASin.iloc[:,1] - DEXout.iloc[:,1] - FALout.iloc[:,1])*cfs_to_cms
GOSloc = (GOSin.iloc[:,1] - COTout.iloc[:,1] - DORout.iloc[:,1])*cfs_to_cms

#need to remove leap days?


local_flows_all = pd.concat([SALloc,JEFloc,MEHloc,WATloc,ALBloc,MONloc,HARloc,VIDloc,JASloc,GOSloc],axis=1)
local_flows_all.columns = ['Salem','Jefferson','Mehama','Waterloo','Albany','Monroe','Harrisburg','Vida','Jasper','Goshen']
                            
#remove and correct NaN vals                    
writer = pd.ExcelWriter('Willamette_cp_local_flows.xlsx')
local_flows_all.to_excel(writer,'cp local flows')
writer.save()













