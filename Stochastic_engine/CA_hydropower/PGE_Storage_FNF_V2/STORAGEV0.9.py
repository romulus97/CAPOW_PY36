# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:31:32 2018

@author: YSu
"""



from __future__ import division
from scipy.optimize import differential_evolution
import pandas as pd 
import numpy as np
from datetime import datetime

# ORCA flow data
df_flows = pd.read_excel('reservoir_inflows.xlsx',sheet_name='Hist_flows',header=0)
sites = list(df_flows.loc[:,'Oroville':])

# WECC hydro time series
df_hydro = pd.read_excel('reservoir_inflows.xlsx',sheet_name='WECC_daily',header=0)
dams = list(df_hydro.loc[:,'Balch 1':])


df_useful_data = pd.read_excel('reservoir_inflows.xlsx',sheet_name='Full_flows',header=0)



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
df_flows = pd.read_excel('reservoir_inflows.xlsx',sheet_name='Hist_flows',header=0)
sites = list(df_flows.loc[:,'Oroville':])
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



for z in [3,7,8,9]:
#for z in [9]:
#    
    s = str(dams[z])
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
    if k in sites:
        d = []
        
        # pull relevant hydropower and flow data
        h = df_hydro.loc[:,s]            
        flow_ts = His_selection.loc[:,site_name].values
        hydro_ts = h.loc[3:].values
        weeks = int(np.floor(len(hydro_ts)/7))    
        years = int(len(hydro_ts)/365)
        
        # upper bound of hydropower production
        upper = np.ceil(np.max(hydro_ts))
            
        # function definition
        def res_fit(params,optimizing=True):
            
            est_power = []
            refill_1_date,evac_date,peak_end,refill_2_date,storage,power_cap,starting,ending= params       
            

            #Not really assuming storage to be 0. 
            #This assumes there is a set starting storage level
          
                                                                            
            # iterate through every week of the year
            for day in range(0,365):
                
                # available hydro production based on water availability
                avail_power = flow_ts[year*365+day]*eff
                
                # if it's during first refill
                if day < refill_1_date:
                    
                    gen =starting- ((starting-min_power)/refill_1_date)*day
                    storage = avail_power-gen
                                        
                
                # if it maintains the water
                elif day >=  refill_1_date and day <  evac_date:
                
                    gen=min_power
                    storage= storage + (avail_power- gen)

                                # if it's in evac period 2
                elif day >= evac_date and day <  peak_end:
                    
                    gen= min_power+ ((power_cap-min_power)/(peak_end-evac_date)* (day- evac_date))
                    if gen > power_cap:
                        gen=power_cap
                        storage= storage + (avail_power- gen)
                    else:
                        storage= storage + (avail_power- gen)    
                                                          
                # if it's in evac period 2
                elif day >= peak_end and day <  refill_2_date:
                    
                    gen= power_cap
                    if gen > power_cap:
                        gen=power_cap
                        storage= storage + (avail_power- gen)
                    else:
   
                        storage= storage + (avail_power- gen)    
                                                          
                
                elif day >=refill_2_date :
                    
                        gen = power_cap-((power_cap-ending)/(365- refill_2_date)* (day-refill_2_date))
                    

                est_power = np.append(est_power,gen)
                
           
                if optimizing:
                    rmse = np.sqrt(((est_power-hydro_ts[year*365:year*365+365])**2).mean())
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
            max_power = np.max(annual_power)
            min_power =np.min(annual_power)
            max_flow = np.max(annual[105:260])
            L = list(annual)
            peak_flow = L.index(max_flow)
            d = np.append(d,peak_flow) 

            best_rmse = 100000
#               
            for i in range(0,100):
        
                # optimize with DE
                result = differential_evolution(res_fit, bounds=[(5,15),(15,30),(20,40),(25,50),(1000,3000),(0.5*max_power,max_power),(min_power,max_power),(min_power,max_power)], maxiter=10000, popsize=1000,polish=False)
                parameters = result.x
       
                
                refill_1_date = parameters[0]    
                evac_date = parameters[1]    
                peak_end=parameters[2]
                refill_2_date = parameters[3]    
                storage = parameters[4]
                power_cap= parameters[5]
                starting=parameters[6]
                ending=parameters[7]                       
                
                est_power = [] 
                                                                                    
                # iterate through every day of the year
                for day in range(0,365):
                
                    # available hydro production based on water availability
                    avail_power = flow_ts[year*356+day]*eff
                    
                    # if it's during first refill
                    if day < refill_1_date:
                        
                        gen =starting- ((starting-min_power)/refill_1_date)*day
                        storage = avail_power-gen
                                            
                    
                    # if it maintains the water
                    elif day >=  refill_1_date and day <  evac_date:
                    
                            gen=min_power
                            storage= storage + (avail_power- gen)
    
                    # if it's in evac period 2
                    elif day >= evac_date and day <  peak_end:
                        
                        gen= min_power+ ((power_cap-min_power)/(peak_end-evac_date)* (day- evac_date))
                            
                        if gen > power_cap:
                            gen=power_cap
                            storage= storage + (avail_power- gen)
                        else:
                            
                            storage= storage + (avail_power- gen)    
                                                              
                    # if it's in evac period 2
                    elif day >= peak_end and day <  refill_2_date:
                        
                        gen= power_cap
                        if gen > power_cap:
                            gen=power_cap
                            storage= storage + (avail_power- gen)
                        else:

                            storage= storage + (avail_power- gen)    
                                                              
                    
                    elif day >=refill_2_date :
                        
                            gen = power_cap-((power_cap-ending)/(365-refill_2_date)* (day-refill_2_date))
                        
    
                    est_power = np.append(est_power,gen)
                    
               
         
                rmse = np.sqrt(((est_power-hydro_ts[year*365:year*365+365])**2).mean())
    

                if rmse < best_rmse:
                    best_rmse = rmse
                    best_parameters = result.x
                    
                    
            # use best fit parameters
            refill_1_date = best_parameters[0]    
            evac_date = best_parameters[1]    
            peak_end=best_parameters[2]
            refill_2_date = best_parameters[3]    
            storage = best_parameters[4]
            power_cap= best_parameters[5]
            starting=best_parameters[6]
            ending=best_parameters[7]
            
    
   
            
            Results=[d[year],starting,ending,refill_1_date,evac_date,peak_end,refill_2_date,storage,power_cap,eff,min_power]        
            exec('Results%d=np.array(Results)' %(year))
            surplus = 0
            transfer = 0            
            est_power = [] 
            
            # iterate through every day of the year
            for day in range(0,365):
                
                    # available hydro production based on water availability
                    avail_power = flow_ts[year*365+day]*eff
                    
                    # if it's during first refill
                    if day < refill_1_date:
                        
                        gen =starting- ((starting-min_power)/refill_1_date)*day
                        storage = avail_power-gen
                                            
                    
                    # if it maintains the water
                    elif day >=  refill_1_date and day <  evac_date:
                    
                        gen=min_power
                        storage= storage + (avail_power- gen)
    
                                    # if it's in evac period 2
                    elif day >= evac_date and day <  peak_end:
                        
                        gen= min_power+ ((power_cap-min_power)/(peak_end-evac_date)* (day- evac_date))
                        if gen > power_cap:
                            gen=power_cap
                            storage= storage + (avail_power- gen)
                        else:
                              
                            storage= storage + (avail_power- gen)    
                                                              
                    # if it's in evac period 2
                    elif day >= peak_end and day <  refill_2_date:
                        
                        gen= power_cap
                        if gen > power_cap:
                            gen=power_cap
                            storage= storage + (avail_power- gen)
                        else:
        
                            storage= storage + (avail_power- gen)    
                                                              
                    
                    elif day >=refill_2_date :
                        
                            gen = power_cap-((power_cap-ending)/(365-refill_2_date)* (day-refill_2_date))
                        
    
                    est_power = np.append(est_power,gen)
                    
               
         


                       
           
         
            est_power2= np.append(est_power2,est_power)
        Save_Results=np.array([Results0,Results1,Results2,Results3])
        exec("np.savetxt('1.0_FNF_Storage_Rule_%s.txt',Save_Results,delimiter = ' ')" %(s))

        print(s)
    else:
        print(s)
        pass
