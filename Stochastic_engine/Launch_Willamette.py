# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 16:44:20 2018

@author: sdenaro
"""
# this file runs the Willamette operational model following the settings 
# specified in the file settings.xml and plots/validates the results

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import autocorrelation_plot
from pandas import ExcelWriter
import numpy as np
import scipy as sp
from scipy import stats
from scipy.interpolate import interp2d
from sklearn import linear_model
from sklearn.metrics import r2_score
import xmltodict as xmld
import datetime as dt
import Willamette_model as inner #reading in the inner function
import os
import pylab as py
import sys

#%%
T=365 #Set the simulation horizon (in days)
initial_doy=1 #Set the simulation initial_doy
sys.argv = ["settings.xml", str(initial_doy), str(T)] #simulation inputs
execfile("Willamette_outer.py")
