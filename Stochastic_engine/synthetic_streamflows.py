# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import division
from datetime import datetime
from sklearn import linear_model
import pandas as pd
import numpy as np
import scipy.stats as st

#########################################################################
# This purpose of this script is to use historical temperature and streamflow data
# to calculate synthetic time series of daily flows at each of the stream gages
# used in the hydropower production models. 

# Regression and vector-autoregressive errors are used to simulate total annual
# streamflows, and these are then paired with daily streamflow fractions tied 
# to daily temperature dynamics
#########################################################################

# Import historical tmeperature data
df_temp = pd.read_excel('Synthetic_streamflows/hist_temps_1953_2007.xlsx')
his_temp_matrix = df_temp.values 

# Import calender 
calender=pd.read_excel('Synthetic_streamflows/BPA_hist_streamflow.xlsx',sheetname='Calender',header= None)
calender=calender.values
julian=calender[:,2]

###############################
# Synthetic HDD CDD calculation

# Simulation data
sim_weather=pd.read_csv('Synthetic_weather/synthetic_weather_data.csv',header=0)



# Load temperature data only
cities = ['SALEM_T','EUGENE_T','SEATTLE_T','BOISE_T','PORTLAND_T','SPOKANE_T','FRESNO_T','LOS ANGELES_T','SAN DIEGO_T','SACRAMENTO_T','SAN JOSE_T','SAN FRANCISCO_T','TUCSON_T','PHOENIX_T','LAS VEGAS_T']
sim_temperature=sim_weather[cities]

# Convert temperatures to Fahrenheit 
sim_temperature= (sim_temperature*(9/5))+32
sim_temperature=sim_temperature.values



num_cities = len(cities)
num_sim_days = len(sim_temperature)

HDD_sim = np.zeros((num_sim_days,num_cities))
CDD_sim = np.zeros((num_sim_days,num_cities))

# calculate daily records of heating (HDD) and cooling (CDD) degree days
for i in range(0,num_sim_days):
    for j in range(0,num_cities):
        HDD_sim[i,j] = np.max((0,65-sim_temperature[i,j]))
        CDD_sim[i,j] = np.max((0,sim_temperature[i,j] - 65))        

# calculate annual totals of heating and cooling degree days for each city
annual_HDD_sim=np.zeros((int(len(HDD_sim)/365),num_cities))
annual_CDD_sim=np.zeros((int(len(CDD_sim)/365),num_cities))

for i in range(0,int(len(HDD_sim)/365)):
    for j in range(0,num_cities):
        annual_HDD_sim[i,j]=np.sum(HDD_sim[0+(i*365):365+(i*365),j])
        annual_CDD_sim[i,j]=np.sum(CDD_sim[0+(i*365):365+(i*365),j])
        
   
########################################################################
#Calculate HDD and CDD for historical temperature data

num_cities = len(cities)
num_days = len(his_temp_matrix)

# daily records
HDD = np.zeros((num_days,num_cities))
CDD = np.zeros((num_days,num_cities))

for i in range(0,num_days):
    for j in range(0,num_cities):
        HDD[i,j] = np.max((0,65-his_temp_matrix[i,j+1]))
        CDD[i,j] = np.max((0,his_temp_matrix[i,j+1] - 65))

# annual sums
annual_HDD=np.zeros((int(len(HDD)/365),num_cities))
annual_CDD=np.zeros((int(len(CDD)/365),num_cities))

for i in range(0,int(len(HDD)/365)):
    for j in range(0,num_cities):
        annual_HDD[i,j]=np.sum(HDD[0+(i*365):365+(i*365),j])
        annual_CDD[i,j]=np.sum(CDD[0+(i*365):365+(i*365),j])
        
###########################################################################################
#This section is used for calculating total hydro 
        
# Load relevant streamflow data (1953-2007)
BPA_streamflow=pd.read_excel('Synthetic_streamflows/BPA_hist_streamflow.xlsx',sheetname='Inflows',header=0)
Hoover_streamflow=pd.read_csv('Synthetic_streamflows/Hoover_hist_streamflow.csv',header=0)
CA_streamflow=pd.read_excel('Synthetic_streamflows/CA_hist_streamflow.xlsx',header=0)
Willamette_streamflow=pd.read_csv('Synthetic_streamflows/Willamette_hist_streamflow.csv',header=0)

# headings
name_Will=list(Willamette_streamflow.loc[:,'Albany':])
name_CA = list(CA_streamflow.loc[:,'ORO_fnf':])
name_BPA = list(BPA_streamflow.loc[:,'1M':])

# number of streamflow gages considered
num_BPA = len(name_BPA)
num_CA = len(name_CA)
num_Will = len(name_Will)
num_gages= num_BPA + num_CA + num_Will + 1
    
# Calculate historical totals for 1953-2007
years = range(1953,2008)

for y in years:
    
    y_index = years.index(y)
    
    BPA = BPA_streamflow.loc[BPA_streamflow['year'] ==y,'1M':]
    CA = CA_streamflow.loc[CA_streamflow['year'] == y,'ORO_fnf':]
    WB = Willamette_streamflow.loc[Willamette_streamflow['year'] == y,'Albany':]
    HO = Hoover_streamflow.loc[Hoover_streamflow['year'] == y,'Discharge']
    
    BPA_sums = np.reshape(np.sum(BPA,axis= 0).values,(1,num_BPA))
    CA_sums = np.reshape(np.sum(CA,axis=0).values,(1,num_CA))
    WB_sums = np.reshape(np.sum(WB,axis=0).values,(1,num_Will))
    HO_sums = np.reshape(np.sum(HO,axis=0),(1,1))
    
    # matrix of annual flows for each stream gage
    joined = np.column_stack((BPA_sums,CA_sums,WB_sums,HO_sums))

    if y_index < 1:
        
        hist_totals = joined
        
    else:
        
        hist_totals = np.vstack((hist_totals,joined))            
        
BPA_headers = np.reshape(list(BPA_streamflow.loc[:,'1M':]),(1,num_BPA))
CA_headers = np.reshape(list(CA_streamflow.loc[:,'ORO_fnf':]),(1,num_CA))
WB_headers = np.reshape(list(Willamette_streamflow.loc[:,'Albany':]),(1,num_Will))
HO_headers = np.reshape(['Hoover'],(1,1))

headers = np.column_stack((BPA_headers,CA_headers,WB_headers,HO_headers))

# annual streamflow totals for 1953-2007
df_hist_totals = pd.DataFrame(hist_totals)
df_hist_totals.columns = headers[0,:]
df_hist_totals.loc[38,'83L']=df_hist_totals.loc[36,'83L']
added_value=abs(np.min((df_hist_totals)))+5
log_hist_total=np.log(df_hist_totals+abs(added_value))



#########################################
# annual flow regression - predicts annual flows at each site as a function
# of total annual HDD and CDD across every weather station
        
#train on historical data
M = np.column_stack((annual_CDD,annual_HDD))

#streamflow gages
H = list(headers[0])

# number of weather stations
z = np.shape(M)
num_w_fields = z[1]

# iterate through sites
count = 0
rsquared = []

DE=[]
for h in H:
    N=added_value[h]
    
    # form linear regression model
    S = log_hist_total.loc[:,h]
    name='reg' + h
    locals()[name] = linear_model.LinearRegression()
          
    # Train the model using the training sets
    locals()[name].fit(M,S)
    score=locals()[name].score(M,S)
    print(name,score)
    predicted = []
    
    # predicted values
    for i in range(0,len(M)):
            
            m = M[i,:]
            
            x = np.reshape(m,(1,num_w_fields))
            p = locals()[name].predict(x)
            
            predicted = np.append(predicted,p)
    DE.append(predicted)
    
    residuals = predicted -S
    
    if count < 1:
        E = residuals
    else:
        E = np.column_stack((E,residuals))        
    
    count = count + 1
    
    
# Now iterate through sites and use sythetic HDD, CDD data to simulated new
# annual streamflow values
count = 0
X_CDD = annual_CDD_sim
X_HDD = annual_HDD_sim
M = np.column_stack((X_CDD,X_HDD))


# for each site
for h in H:
    N=added_value[h]
    # load simulated temperature data

    # Simulate using synthetic CDD, HDD data
    predicted = []
    
    # predicted values
    for i in range(0,len(M)):
            
            m = M[i,:]
            
            x = np.reshape(m,(1,num_w_fields))
            name='reg' + h
            x=np.nan_to_num(x)
            p = locals()[name].predict(x)
            predicted = np.append(predicted,p)
    predicted=np.exp(predicted)-N        
    if count < 1:
        P = predicted
    else:
        P = np.column_stack((P,predicted))
            
    count = count + 1

#mean=[]
#mean2=[]
#for i in range(0,108):
#    m1=np.average(DE2[:,i])
#    m2=np.average(P[:,i])
#    mean.append(m1)
#    mean2.append(m2)
#
#import matplotlib.pyplot as plt
#
#plt.plot(mean)
#plt.plot(mean2)
#    
######################################################################
# now combine values predicted via regression with synthetic residuals
    
# whiten historical residuals
Z = np.shape(E)
std_dev = np.zeros((1,num_gages))
mus = np.zeros((num_gages))
wE = np.zeros(np.shape(E))

# address any zero values
for i in range(0,num_gages):
    a = np.std(E[:,i])
    std_dev[0,i] = a
    
    if a == 0:
        wE[:,i] = 0
    else: 
        wE[:,i] = E[:,i]/a

# covariance matrix
C = np.cov(np.transpose(wE))

# simulate residuals and add to regression predictions
sim_totals = np.zeros(np.shape(P))

for i in range(0,len(P)):
    e = np.random.multivariate_normal(mus,C,1)
    sim_totals[i,:] = P[i,:] + (np.exp(e*std_dev)+list(added_value))
    
# impose logical constraints
mins = np.min(df_hist_totals.loc[:,:'Hoover'],axis=0)

for i in range(0,num_gages):
    lower_bound = mins[i]
          
    for j in range(0,len(P)):
        if sim_totals[j,i] < lower_bound:
            sim_totals[j,i] = lower_bound*np.random.uniform(0,1)
                
df_sim_totals = pd.DataFrame(sim_totals)
H = list(headers)
df_sim_totals.columns = H


#A1=[]
#A2=[]
#for h in H:
#    a1=np.average(df_hist_totals.loc[:,h])
#    a2=np.average(df_sim_totals.loc[:,h])
#    A1.append(a1)
#    A2.append(a2)
#
#plt.plot(A1)
#plt.plot(A2)
#####################################################################################
# This section selects daily fractions which are paired with 
# annual totals to arrive at daily streamflows

# 4 cities are nearest to all 109 stream gage sites
Fraction_calculation_cities=['Spokane','Boise','Sacramento','Fresno']

# Each is weighted by average annual flow at nearby gage sites
Temperature_weights=pd.read_excel('Synthetic_streamflows/city_weights.xlsx',header=0)

# historical temperatures for those 4 cities
fraction_hist_temp=df_temp[Fraction_calculation_cities]
fraction_hist_temp_matrix=fraction_hist_temp.values

# calculate daily record of weighted temperatures across 4 cities
weighted_T=np.zeros(len(fraction_hist_temp_matrix))
for i in range(0,len(fraction_hist_temp_matrix)):
    weighted_T[i]=fraction_hist_temp_matrix[i,0]*Temperature_weights['Spokane'] + fraction_hist_temp_matrix[i,1] * Temperature_weights['Boise'] + fraction_hist_temp_matrix[i,2] * Temperature_weights['Sacramento'] + fraction_hist_temp_matrix[i,3]*Temperature_weights['Fresno']

# synthetic temperatures for each of the cities
fcc = list(['SPOKANE_T','BOISE_T','SACRAMENTO_T','FRESNO_T'])
fraction_sim=sim_weather[fcc]
fraction_sim_matrix=fraction_sim.values

weighted_T_sim=np.zeros(len(fraction_sim_matrix))

# calculate synthetic weighted temperature (in Fahrenheit) 
for i in range(0,len(fraction_sim_matrix)):
    weighted_T_sim[i]=fraction_sim_matrix[i,0]*Temperature_weights['Spokane'] +     fraction_sim_matrix[i,1] * Temperature_weights['Boise'] + fraction_sim_matrix[i,2] * Temperature_weights['Sacramento'] + fraction_sim_matrix[i,3]*Temperature_weights['Fresno']

weighted_T_sim=(weighted_T_sim * (9/5)) +32  


#Sample synthetic fractions, then combine with totals
sim_years=int(len(fraction_sim_matrix)/365)
sim_T=np.zeros((365,sim_years))

hist_years=int(len(fraction_hist_temp)/365)
hist_T=np.zeros((365,hist_years))

# reshape historical and simulated weighted temperatures in new variables 
for i in range(0,hist_years):
    hist_T[:,i] = weighted_T[i*365:365+(i*365)]
    
for i in range(0,sim_years):
    sim_T[:,i] = weighted_T_sim[i*365:365+(i*365)]      

# aggregate weighted temperatures into monthly values
Normal_Starting=datetime(1900,1,1)
datelist=pd.date_range(Normal_Starting,periods=365)
count=0
m=np.zeros(365)
for i in range(0,365):
    m[i]=int(datelist[count].month)
    count= count +1
    if count >364:
        count=0
hist_T_monthly=np.column_stack((hist_T,m))

monthly_hist_T=np.zeros((12,hist_years))
for i in range(0,sim_years):
    for j in range(1,13):
        d1=hist_T_monthly[hist_T_monthly[:,hist_years]==j]
        d2=d1[:,:hist_years]
        monthly_hist_T[j-1,:]=np.sum(d2,axis=0)
    
Normal_Starting=datetime(1900,1,1)
datelist=pd.date_range(Normal_Starting,periods=365)
count=0
m=np.zeros(365)
for i in range(0,365):
    m[i]=int(datelist[count].month)
    count= count +1
    if count >364:
        count=0
sim_T_monthly=np.column_stack((sim_T,m))

monthly_sim_T=np.zeros((12,sim_years))
for i in range(0,sim_years):
    for j in range(1,13):
        d1=sim_T_monthly[sim_T_monthly[:,sim_years]==j]
        d2=d1[:,:sim_years]
        monthly_sim_T[j-1,:]=np.sum(d2,axis=0)


# select historical year with most similar spring and summer temperatures
# to new simulated years
year_list=np.zeros(sim_years)
Best_RMSE = 9999999999
CHECK=np.zeros((sim_years,hist_years))

for i in range(0,sim_years):
    for j in range(0,hist_years):
        RMSE = (np.sum(np.abs(monthly_sim_T[3:8,i]-monthly_hist_T[3:8,j])))
        CHECK[i,j]=RMSE
        if RMSE <= Best_RMSE:
            year_list[i] = j
            Best_RMSE=RMSE
            
        else:
            pass
    Best_RMSE = 9999999999

################################################################################
#Generate streamflow 
TDA=np.zeros((int(365*sim_years),2))
totals_hist=np.zeros((num_gages,hist_years))   
fractions_hist=np.zeros((hist_years,365,num_gages))

totals_hist_hoover=np.zeros((1,hist_years))
output_BPA=np.zeros((sim_years*365,num_BPA))
output_Hoover=np.zeros((sim_years*365,1))
output_CA=np.zeros((sim_years*365,num_CA))
output_WI=np.zeros((sim_years*365,num_Will))

# historical daily flows
x_Hoover=Hoover_streamflow.loc[:,'Discharge'].values
x_BPA=BPA_streamflow.loc[:,'1M':].values
x_CA=CA_streamflow.loc[:,'ORO_fnf':].values
x_WI=Willamette_streamflow.loc[:,'Albany':'LOP5E'].values
x=np.column_stack((x_BPA,x_CA,x_WI,x_Hoover))
x=np.reshape(x,(hist_years,365,num_gages))

# historical daily fractions
for i in range(0,hist_years):
    for j in range(0,num_gages):
        totals_hist[j,i] = np.sum(np.abs(x[i,:,j]))
        if totals_hist[j,i] ==0:
            fractions_hist[i,:,j]=0
        else:
            fractions_hist[i,:,j]= x[i,:,j]/totals_hist[j,i]
        
# sample simulated daily fractions
for i in range(0,sim_years):
    for j in range(0,num_gages):
        
        if j <=num_BPA-1:
            output_BPA[(i*365):(i*365)+365,j]=fractions_hist[int(year_list[i]),:,j]*sim_totals[i,j]
        elif j == num_gages-1:
            output_Hoover[(i*365):(i*365)+365,0]=fractions_hist[int(year_list[i]),:,j]*sim_totals[i,j]
        elif j>num_BPA-1 and j<=num_BPA+num_CA-1:
            output_CA[(i*365):(i*365)+365,j-num_BPA]=fractions_hist[int(year_list[i]),:,j]*sim_totals[i,j]
        else:
            output_WI[(i*365):(i*365)+365,j-num_BPA-num_CA]=fractions_hist[int(year_list[i]),:,j]*sim_totals[i,j]
    
    TDA[(i*365):(i*365)+365,0]=range(1,366)

# assign flows to the Dalles, OR
TDA[:,1]=output_BPA[:,47]


###############################################################################
# Output
np.savetxt('Synthetic_streamflows/synthetic_streamflows_FCRPS.csv',output_BPA,delimiter=',')
np.savetxt('Synthetic_streamflows/synthetic_streamflows_TDA.csv',TDA[:,1],delimiter=',')
np.savetxt('Synthetic_streamflows/synthetic_discharge_Hoover.csv',output_Hoover,delimiter=',')
CA=pd.DataFrame(output_CA,columns=name_CA)
CA.to_csv('Synthetic_streamflows/synthetic_streamflows_CA.csv')
Willamatte_Syn=pd.DataFrame(output_WI,columns=name_Will)
Willamatte_Syn.to_csv('Synthetic_streamflows/synthetic_streamflows_Willamette.csv')

