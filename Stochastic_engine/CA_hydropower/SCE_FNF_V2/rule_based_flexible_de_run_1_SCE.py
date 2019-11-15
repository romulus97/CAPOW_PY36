# -*- coding: utf-8 -*-
#This is the first modified version of the DE
#The main difference is add surplus as a objective and add maximun discharge
"""
Created on Thu Nov 30 17:19:24 2017

@author: jdkern
"""

from __future__ import division
from scipy.optimize import differential_evolution
import pandas as pd 
import numpy as np
from datetime import datetime

# ORCA flow data


# WECC hydro time series
df_hydro = pd.read_excel('SCE_data.xlsx',sheet_name='WECC_daily',header=0)
SCE_dams = list(df_hydro.loc[:,'Big_Creek_1 ':])



SCE_No_Data_Dams=[SCE_dams[7],SCE_dams[8],SCE_dams[12]]

# Note that the starting data in this model is 1/1/1906 simulated data (index 92) the end year would be 2015

df_useful_data = pd.read_excel('reservoir_inflows.xlsx',sheet_name='Full_flows',header=0)
upper_gen = pd.read_excel('upper_SCE.xlsx',header =0)


#Useful simulated ORCA sites name
ORCA_sites = list(df_useful_data)
ORCA_sites = ORCA_sites[3:]
O_site=[]
Data_needed=[]
#If we have all of the outflow data then we will use range(0,24). For now we just have inflow data. (0,15)
for i in range(0,24):
    O_site=np.append(O_site,str(ORCA_sites[i]))
    
Data_needed=np.append(O_site,['datetime']) 

Validation_Year=[2005,2010,2011]
# ORCA flow data
df_flows = pd.read_excel('SCE_data.xlsx',sheet_name='Hist_flows',header=0)
sites = list(df_flows.loc[:,'Millerton':])

Hist_flows = pd.read_excel('cord-data.xlsx',header=0)
#Add year colum to the dataframe
Year=[]
Month=[]
Day=[]
for i in range(0,len(Hist_flows)):
        datetime_object=datetime.strftime(Hist_flows.loc[i]['datetime'],'%Y-%m-%d %H:%M:%S')
        Date=datetime.strptime(datetime_object,'%Y-%m-%d %H:%M:%S')
        Year=np.append(Year,Date.year)
        Month=np.append(Month,Date.month)
        Day=np.append(Day,Date.day)
Hist_flows['Year']=Year
Hist_flows['Month']=Month
Hist_flows['Day']=Day
His_selection = Hist_flows.loc[Hist_flows.loc[:,'Year']==2001]
flows=[]
for y in Validation_Year:
    His_selection_2 = Hist_flows.loc[Hist_flows.loc[:,'Year']==y]
    His_selection=His_selection.append(His_selection_2)


for dam in SCE_dams:
    if dam in SCE_No_Data_Dams:
        pass

    else:
        
    
        s = str(dam)
        k = str(df_hydro.loc[1][s])
        I_O=str(df_hydro.loc[2][s])
        if k =='Oroville' and I_O =='Inflows':
            site_name=['ORO_fnf']
        elif k =='Oroville' and I_O =='Outflows':
            site_name=['ORO_otf']
        elif k =='Pine Flat' and I_O =='Inflows':
            site_name=['PFT_fnf']
        elif k =='Pine Flat' and I_O =='Outflows':
            site_name=['PFT_otf']
        elif k =='Shasta' and I_O =='Inflows':
            site_name=['SHA_fnf']
        elif k =='Shasta' and I_O =='Outflows':
            site_name=['SHA_otf']
        elif k =='New Melones' and I_O =='Inflows':
            site_name=['NML_fnf']
        elif k =='New Melones' and I_O =='Outflows':
            site_name=['NML_otf']
        elif k =='Pardee' and I_O =='Inflows':
            site_name=['PAR_fnf']
        elif k =='Pardee' and I_O =='Outflows':
            site_name=['PAR_otf']
        elif k =='New Exchequer' and I_O =='Inflows':
            site_name=['EXC_fnf']
        elif k =='New Exchequer' and I_O =='Outflows':
            site_name=['EXC_otf']
        elif k =='Folsom' and I_O =='Inflows':
            site_name=['FOL_fnf']
        elif k =='Folsom' and I_O =='Outflows':
            site_name=['FOL_otf']
        elif k =='Don Pedro' and I_O =='Inflows':
            site_name=['DNP_fnf']
        elif k =='Don Pedro' and I_O =='Outflows':
            site_name=['DNP_otf']
        elif k =='Millerton' and I_O =='Inflows':
            site_name=['MIL_fnf']
        elif k =='Millerton' and I_O =='Outflows':
            site_name=['MIL_otf']
        elif k =='Isabella' and I_O =='Inflows':
            site_name=['ISB_fnf']
        elif k =='Isabella' and I_O =='Outflows':
            site_name=['ISB_otf']
        elif k =='Yuba' and I_O =='Inflows':
            site_name=['YRS_fnf']
        elif k =='Yuba' and I_O =='Outflows':
            site_name=['YRS_otf']
        else:
            print(s)
    
        if k in sites: #and I_O=='Inflows':
            d = []
            
            # pull relevant hydropower and flow data
            h = df_hydro.loc[:,s]            
            flow_ts = His_selection.loc[:,site_name].values
            hydro_ts = h.loc[3:].values
            years = int(len(hydro_ts)/365)
                  
            
            # upper bound of hydropower production
            upper = np.ceil(np.max(hydro_ts))
                
                # function definition
            def res_fit(params,optimizing=True):
                
                est_power = []
                sum_cap,spr_cap,fall_cap,win_date,spr_date,sum_date,fall_date = params       
                    
                surplus = 0
                transfer = 0
                                                                                
                # iterate through every day of the year
                for day in range(0,365):
                    
                    # available hydro production based on water availability
                    avail_power = flow_ts[year*365+day]*eff
                    
                    # if it's still winter, operate as RoR
                    if day < d[year] - win_date:
                        
                            if avail_power >= upper:
                                gen = upper
                                surplus = surplus + (avail_power - upper)
                            else:
                                gen = avail_power
                    
                    # if it's spring, operate as RoR with upper limit
                    elif day >= d[year] - win_date and day < d[year] - spr_date:
                    
                        if avail_power > spr_cap:
                            surplus = surplus + (avail_power - spr_cap)
                            gen = spr_cap
                            
                        elif avail_power <= spr_cap:
                            deficit = spr_cap - avail_power
                            if surplus>0:
                                transfer = np.min((surplus,deficit))
                                surplus = surplus - transfer
                            else: 
                                transfer = 0
                            
                            gen = avail_power + transfer
                    
                    # if it's summer, operate as RoR with upper limit
                    elif day >= d[year] - spr_date and day < d[year] + sum_date:
                        
                        if avail_power > sum_cap:
                            surplus = surplus + (avail_power - sum_cap)
                            gen = sum_cap
                            
                        elif avail_power <= sum_cap:
                            deficit = sum_cap - avail_power
                            if surplus>0:
                                transfer = np.min((surplus,deficit))
                                surplus = surplus - transfer
                            else: 
                                transfer = 0
                                
                            gen = avail_power + transfer
                        
                    # if it's fall, operate as RoR with upper limit
                    elif day >= d[year] + sum_date and day < d[year] + fall_date:
                        
                        if avail_power > fall_cap:
                            surplus = surplus + (avail_power - fall_cap)
                            gen = fall_cap
                            
                        elif avail_power <= fall_cap:
                            deficit = fall_cap - avail_power
                            if surplus>0:
                                transfer = np.min((surplus,deficit))
                                surplus = surplus - transfer
                            else: 
                                transfer = 0
                                
                            gen = avail_power + transfer
                            
                    
                    elif day >= d[year] + fall_date:
                        
                            if avail_power >= upper:
                                gen = upper
                                surplus = surplus + (avail_power - upper)
                            else:
                                gen = avail_power
                        
                    else: 
                        
                            if avail_power >= upper:
                                gen = upper
                                surplus = surplus + (avail_power - upper)
                            else:
                                gen = avail_power
                        
                    est_power = np.append(est_power,gen)
                    
                    if optimizing:
                        rmse = np.sqrt(((est_power-hydro_ts[year*365:year*365+365])**2).mean())+(surplus**2)
                        return rmse
                    else:
                        return est_power
               
              
            # years: 2001, 2005, 2010, 2011
            
            est_power2=[]
            Save_Results=[]
              
            for year in range(0,4):
            
                # identify date of maximum inflow at ORCA site
                annual = flow_ts[year*365:year*365+365]
                annual_power = hydro_ts[year*365:year*365+365]
                eff=np.sum(annual_power)/np.sum(annual)
                max_flow = np.max(annual[105:260])
                L = list(annual)
                peak_flow = L.index(max_flow)
                d = np.append(d,peak_flow) 
                
                best_rmse = 10000000000000
                   
                for i in range(0,100):
            
                    # optimize with DE
                    result = differential_evolution(res_fit, bounds=[(0,upper),(0,upper),(0,upper),(0,25),(0,25),(0,25),(0,25)], maxiter=10000, popsize=1000,polish=False)
                    parameters = result.x
                    
                    
                    sum_cap = parameters[0]    
                    spr_cap = parameters[1]    
                    fall_cap = parameters[2]    
                    win_date = parameters[3]    
                    spr_date = parameters[4]    
                    sum_date = parameters[5]    
                    fall_date = parameters[6]     
                            
                    surplus = 0
                    transfer = 0
                    
                    est_power = [] 
                                                                                        
                    # iterate through every day of the year
                    for day in range(0,365):
                        
                        # available hydro production based on water availability
                        avail_power = flow_ts[year*365+day]*eff
                        
                        # if it's still winter, operate as RoR
                        if day < d[year] - win_date:
                            
                            if avail_power >= upper:
                                gen = upper
                                surplus = surplus + (avail_power - upper)
                            else:
                                gen = avail_power
                        
                        # if it's spring, operate as RoR with upper limit
                        elif day >= d[year] - win_date and day < d[year] - spr_date:
                        
                            if avail_power > spr_cap:
                                surplus = surplus + (avail_power - spr_cap)
                                gen = spr_cap
                                
                            elif avail_power <= spr_cap:
                                deficit = spr_cap - avail_power
                                if surplus>0:
                                    transfer = np.min((surplus,deficit))
                                    surplus = surplus - transfer
                                else: 
                                    transfer = 0
                                
                                gen = avail_power + transfer
                        
                        # if it's summer, operate as RoR with upper limit
                        elif day >= d[year] - spr_date and day < d[year] + sum_date:
                            
                            if avail_power > sum_cap:
                                surplus = surplus + (avail_power - sum_cap)
                                gen = sum_cap
                                
                            elif avail_power <= sum_cap:
                                deficit = sum_cap - avail_power
                                if surplus>0:
                                    transfer = np.min((surplus,deficit))
                                    surplus = surplus - transfer
                                else: 
                                    transfer = 0
                                    
                                gen = avail_power + transfer
                            
                        # if it's fall, operate as RoR with upper limit
                        elif day >= d[year] + sum_date and day < d[year] + fall_date:
                            
                            if avail_power > fall_cap:
                                surplus = surplus + (avail_power - fall_cap)
                                gen = fall_cap
                                
                            elif avail_power <= fall_cap:
                                deficit = fall_cap - avail_power
                                if surplus>0:
                                    transfer = np.min((surplus,deficit))
                                    surplus = surplus - transfer
                                else: 
                                    transfer = 0
                                    
                                gen = avail_power + transfer
                                
                        
                        elif day >= d[year] + fall_date:
                            
                            if avail_power >= upper:
                                gen = upper
                                surplus = surplus + (avail_power - upper)
                            else:
                                gen = avail_power
                            
                        else: 
                            
                            if avail_power >= upper:
                                gen = upper
                                surplus = surplus + (avail_power - upper)
                            else:
                                gen = avail_power
                        est_power = np.append(est_power,gen)
                        
                    rmse = np.sqrt(((est_power-hydro_ts[year*365:year*365+365])**2).mean())+ (surplus**2)
                    
                    if rmse < best_rmse:
                        best_rmse = rmse
                        best_parameters = result.x
                        
                        
                # use best fit parameters
                sum_cap = best_parameters[0]    
                spr_cap = best_parameters[1]    
                fall_cap = best_parameters[2]    
                win_date = best_parameters[3]    
                spr_date = best_parameters[4]    
                sum_date = best_parameters[5]    
                fall_date = best_parameters[6]     
                
                Results=[d[year],sum_cap,spr_cap,fall_cap,win_date,spr_date,sum_date,fall_date,eff,surplus]        
                exec('Results%d=np.array(Results)' %(year))
                surplus = 0
                transfer = 0            
                est_power = [] 
                
                # iterate through every day of the year
                for day in range(0,365):
                    
                    # available hydro production based on water availability
                    avail_power = flow_ts[year*365+day]*eff
                    
                    # if it's still winter, operate as RoR
                    if day < d[year] - win_date:
                        
                            if avail_power >= upper:
                                gen = upper
                                surplus = surplus + (avail_power - upper)
                            else:
                                gen = avail_power
                    
                    # if it's spring, operate as RoR with upper limit
                    elif day >= d[year] - win_date and day < d[year] - spr_date:
                    
                        if avail_power > spr_cap:
                            surplus = surplus + (avail_power - spr_cap)
                            gen = spr_cap
                            
                        elif avail_power <= spr_cap:
                            deficit = spr_cap - avail_power
                            if surplus>0:
                                transfer = np.min((surplus,deficit))
                                surplus = surplus - transfer
                            else: 
                                transfer = 0
                            
                            gen = avail_power + transfer
                    
                    # if it's summer, operate as RoR with upper limit
                    elif day >= d[year] - spr_date and day < d[year] + sum_date:
                        
                        if avail_power > sum_cap:
                            surplus = surplus + (avail_power - sum_cap)
                            gen = sum_cap
                            
                        elif avail_power <= sum_cap:
                            deficit = sum_cap - avail_power
                            if surplus>0:
                                transfer = np.min((surplus,deficit))
                                surplus = surplus - transfer
                            else: 
                                transfer = 0
                                
                            gen = avail_power + transfer
                        
                    # if it's fall, operate as RoR with upper limit
                    elif day >= d[year] + sum_date and day < d[year] + fall_date:
                        
                        if avail_power > fall_cap:
                            surplus = surplus + (avail_power - fall_cap)
                            gen = fall_cap
                            
                        elif avail_power <= fall_cap:
                            deficit = fall_cap - avail_power
                            if surplus>0:
                                transfer = np.min((surplus,deficit))
                                surplus = surplus - transfer
                            else: 
                                transfer = 0
                                
                            gen = avail_power + transfer
                            
                    
                    elif day >= d[year] + fall_date:
                        
                            if avail_power >= upper:
                                gen = upper
                                surplus = surplus + (avail_power - upper)
                            else:
                                gen = avail_power
                        
                    else: 
                        
                            if avail_power >= upper:
                                gen = upper
                                surplus = surplus + (avail_power - upper)
                            else:
                                gen = avail_power
                        
                    est_power = np.append(est_power,gen)
                    
                rmse = np.sqrt(((est_power-hydro_ts[year*365:year*365+365])**2).mean()) + (surplus**2)
             
                est_power2= np.append(est_power2,est_power)
            Save_Results=np.array([Results0,Results1,Results2,Results3])
            exec("np.savetxt('SCE_fnf_%s.txt',Save_Results,delimiter = ' ')" %(s))
            # re-run to get plot
    #        exec("plt.figure(%d)" %(z))
#            plt.plot(hydro_weekly, color='k')
#            plt.plot(est_power2, color='red')
#            plt.xlabel('Weeks')
#            plt.ylabel('Hydropower')
#            plt.legend(['Observed', 'Simulated'])
    #    
    #                
    #        exec("plt.savefig('R:\OneDrive - University of North Carolina at Chapel Hill\California Hydro\Debug\V2_Plus_Surplus%s.png')" % (s) )
            print(s)
            from scipy import stats
            r_value, p_value = stats.pearsonr(est_power2,hydro_ts)
            print(r_value)
