# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 15:54:17 2018

@author: YSu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CA_syn=pd.read_csv('synthetic_streamflows_CA.csv',header=0,index_col=0)
CA_hist=pd.read_excel('CA_hist_streamflow.xlsx',header=0)

title_list=CA_syn.columns

M1=[]
M2=[]
S1=[]
S2=[]

for element in title_list:
    
    hist=CA_hist[element]
    syn=CA_syn[element]
    M1.append(np.average(hist))
    M2.append(np.average(syn))
    
    S1.append(np.std(hist))
    S2.append(np.std(syn))
    
    
#    plt.figure()
#    plt.plot(hist,label='hist')
#    plt.plot(syn[:len(hist)],label='syn')
#    plt.title(element)
#    plt.legend()
#    
#    
plt.figure()
plt.plot(M1,label='hist')
plt.plot(M2)
plt.legend()


plt.figure()
plt.plot(S1,label='hist')
plt.plot(S2)
plt.legend()


BPA_syn=pd.read_csv('synthetic_streamflows_FCRPS.csv',header=None)
BPA_hist=pd.read_excel('BPA_hist_streamflow.xlsx',header=0)
BPA_hist=BPA_hist.values[:,3:]
BPA_syn=BPA_syn.values


M1=[]
M2=[]

S1=[]
S2=[]

for i in range(0,55):

    hist=BPA_hist[:,i]
    syn=BPA_syn[:,i]
    M1.append(np.average(hist))
    M2.append(np.average(syn))
    
    S1.append(np.std(hist))
    S2.append(np.std(syn))
    
plt.figure()
plt.plot(M1,label='hist')
plt.plot(M2)
plt.legend()


plt.figure()
plt.plot(S1,label='hist')
plt.plot(S2)
plt.legend()
