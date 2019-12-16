# -*- coding: utf-8 -*-
"""
Created on Mon May 27 11:13:15 2019

@author: jkern
"""

from __future__ import division
import pandas as pd 
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

#def hydro(sim_years):
    
#########################################################################
# This purpose of this script is to use synthetic streamflows at major California
# reservoir sites to simulate daily hydropower production for the PG&E and SCE 
# zones of the California electricty market (CAISO), using parameters optimized
# via a differential evolution algorithm. 
#########################################################################
    
    
sim_years = sim_years + 3
# load California storage reservoir (ORCA) sites
df_sites = pd.read_excel('CA_hydropower/sites.xlsx',sheetname = 'ORCA',header=0)
ORCA_sites = list(df_sites)

# load upper generation amounts for each predicted hydropower dam (PG&E and SCE)
upper_gen = pd.read_excel('CA_hydropower/upper.xlsx',header =0)

# month-day calender
calender = pd.read_excel('CA_hydropower/calender.xlsx',header=0)

# load simulated full natural flows at each California storage reservoir (ORCA site)
df_sim = pd.read_excel('CA_hydropower/hist_reservoir_inflows.xlsx',sheet_name='val_flows',header=0)

#Add month and day columns to the dataframe
Month = []
Day = []
count = 0
for i in range(0,len(df_sim)):
    if count < 365:
        Month = np.append(Month,calender.loc[count,'Month'])
        Day = np.append(Day,calender.loc[count,'Day'])
        count = count + 1
    else:
        count = 0
        Month = np.append(Month,calender.loc[count,'Month'])
        Day = np.append(Day,calender.loc[count,'Day'])
        count = count + 1
df_sim['Month']=Month
df_sim['Day']=Day

# calculate simulated totals
Sim_totals = []
for i in range(0,sim_years):
    sample = df_sim.loc[i*365:i*365+365,'ORO_fnf':'ISB_fnf']
    total = np.sum(np.sum(sample))
    Sim_totals = np.append(Sim_totals,total)

# load historical full natural flows for 2001, 2005, 2010 and 2011
df_hist = pd.read_excel('CA_hydropower/hist_reservoir_inflows.xlsx',header=0)
Hist_totals = []
Hist_years = [2001,2005,2010,2011]

for i in Hist_years:
    sample = df_hist[df_hist['year'] == i]
    sample = sample.loc[:,'ORO_fnf':'ISB_fnf']
    total = np.sum(np.sum(sample))
    Hist_totals = np.append(Hist_totals,total)


# find most similar historical year for each simulated year
Rule_list=[]

for i in range(0,sim_years):
    Difference=abs(Sim_totals[i]- Hist_totals)

#Select which rule to use
    for n in range(0,len(Hist_years)):
        if Difference[n]==np.min(Difference):
         Rule=n
    Rule_list.append(Rule)

# PGE hydro projects
PGE_names = pd.read_excel('CA_hydropower/sites.xlsx',sheetname ='PGE',header=0)
PGE_dams = list(PGE_names.loc[:,'Balch 1':])
PGE_Storage=[PGE_dams[3],PGE_dams[7],PGE_dams[8],PGE_dams[9]]
PGE_No_Data_Dams=[PGE_dams[2],PGE_dams[4],PGE_dams[10],PGE_dams[11],PGE_dams[15],PGE_dams[16],PGE_dams[17],PGE_dams[26],PGE_dams[30],PGE_dams[38],PGE_dams[39],PGE_dams[55],PGE_dams[60],PGE_dams[65]]

## SCE hydro projects
SCE_names = pd.read_excel('CA_hydropower/sites.xlsx',sheetname ='SCE',header=0)
SCE_dams = list(SCE_names.loc[:,'Big_Creek_1 ':])
SCE_No_Data_Dams=[SCE_dams[7],SCE_dams[8],SCE_dams[12]]

#Simulate all the PGE inflow dams
check_unused = []
PGE_name_list = []
SCE_name_list = []
for name in PGE_dams:
    
    est_power = []
    for year in range(0,sim_years):
        if name in PGE_No_Data_Dams:
            pass

        elif name in PGE_Storage:
            
            # which operating rule to use?
            Rule=Rule_list[year]
            File_name='CA_hydropower/A1.0_FNF_Storage_Rule_' + str(name) +'.txt'
            Temp_Rule=pd.read_csv(File_name,delimiter=' ',header=None)
            peak_flow,starting,ending,refill_1_date,evac_date,peak_end,refill_2_date,storage,power_cap,eff,min_power=Temp_Rule.loc[Rule][:]
                      
            flow_weekly = []
            k = str(PGE_names.loc[0][name])
            I_O=str(PGE_names.loc[1][name])

            #Which site to use
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
                None

            flow_ts = df_sim.loc[:,site_name].values  
            flow_daily = flow_ts[year*365:year*365+365]
            
            for i in range(0,52):
                flow_weekly = np.append(flow_weekly,np.sum(flow_daily[i*7:i*7+7]))
                    
            x = np.max(flow_weekly[15:36])
            L = list(flow_weekly)
            peak_flow = L.index(x)
                
                
            for week in range(0,52):
                
                    # available hydro production based on water availability
                    avail_power = flow_weekly[week]*eff
                    
                    # if it's during first refill
                    if week < refill_1_date:
                        
                        gen =starting- ((starting-min_power)/refill_1_date)*week
                        storage = avail_power-gen
                                            
                    
                    # if it maintains the water
                    elif week >=  refill_1_date and week <  evac_date:
                    
                            gen=min_power
                            storage= storage + (avail_power- gen)
    
                                    # if it's in evac period 2
                    elif week >= evac_date and week <  peak_end:
                        
                        gen= min_power+ ((power_cap-min_power)/(peak_end-evac_date)* (week- evac_date))
                            
                        if gen > power_cap:
                            gen=power_cap
                            storage= storage + (avail_power- gen)
                        else:
                            
                            storage= storage + (avail_power- gen)    
                                                              
                    # if it's in evac period 2
                    elif week >= peak_end and week <  refill_2_date:
                        
                        gen= power_cap
                        if gen > power_cap:
                            gen=power_cap
                            storage= storage + (avail_power- gen)
                        else:
    
                            storage= storage + (avail_power- gen)    
                                                              
                    
                    elif week >=refill_2_date :
                        
                            gen = power_cap-((power_cap-ending)/(52-refill_2_date)* (week-refill_2_date))
                        
    
                    est_power = np.append(est_power,gen)
            
        else:
            upper_now=upper_gen.loc[upper_gen.loc[:,'Name']== name]
            upper_now=upper_now.reset_index(drop=True)
            upper=upper_now.loc[0]['Max Gen']
            Rule=Rule_list[year]
            File_name='CA_hydropower/PGE_DE_V1/FNF_' + str(name) +'.txt'
            Temp_Rule=pd.read_csv(File_name,delimiter=' ',header=None)
            peak_flow,sum_cap,spr_cap,fall_cap,win_date,spr_date,sum_date,fall_date,eff,check_surplus=Temp_Rule.loc[Rule][:]

            surplus = 0
            transfer = 0
            flow_weekly = []
            k = str(PGE_names.loc[0][name])
            I_O=str(PGE_names.loc[1][name])
                        
                    
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
                None

            flow_ts = df_sim.loc[:,site_name].values  
            flow_daily = flow_ts[year*365:year*365+365]
            
            for i in range(0,52):
                flow_weekly = np.append(flow_weekly,np.sum(flow_daily[i*7:i*7+7]))
                    
            x = np.max(flow_weekly[15:36])
            L = list(flow_weekly)
            peak_flow = L.index(x)

            for week in range(0,52):
                
                # available hydro production based on water availability
                avail_power = flow_weekly[week]*eff
                
                # if it's still winter, operate as RoR
                if week < peak_flow - win_date:
                        gen=avail_power
                        if gen >= upper:
                            gen = upper
#                            surplus = surplus + (avail_power - upper)
                        else:
                            gen = gen
                
                # if it's spring, operate as RoR with upper limit
                elif week >= peak_flow - win_date and week < peak_flow - spr_date:
                    
                    
                    if avail_power + surplus> upper:
                        surplus = surplus + (avail_power - upper)
                        gen = upper
                        
                    elif avail_power > spr_cap and avail_power + surplus < upper:
  
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
                elif week >= peak_flow - spr_date and week < peak_flow + sum_date:
                    
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
                elif week >= peak_flow + sum_date and week < peak_flow + fall_date:
                    
                    if avail_power > upper:
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
                        
                
                elif week >= peak_flow + fall_date:
                    
                        if avail_power >= upper:
                            gen = upper
                            surplus = surplus + (avail_power - upper)
                        else:
                            gen = avail_power
                    
                else: 
                        gen=avail_power
                        if gen+surplus >= upper:    
                            gen = upper
                            surplus = gen + surplus - upper
                        else:
                            gen = avail_power+surplus
                        
                est_power = np.append(est_power,gen)
            
            unused=surplus
            check_unused.append(surplus)
    rest_surplus=sum(check_unused)           

    if name in PGE_No_Data_Dams:
        pass
    else:
        PGE_name_list = np.append(PGE_name_list,name)
        name_index = PGE_dams.index(name)
        if name_index < 1:
            M_PGE = est_power
        else:
            M_PGE = np.column_stack((M_PGE,est_power))
        

##Simulate all the SCE inflow dams
for name in SCE_dams:
    est_power = []
    for year in range(0,sim_years):

        if name in SCE_No_Data_Dams:
            pass
        else:
            Rule=Rule_list[year]
            File_name='CA_hydropower/SCE_DE_V1/SCE_fnf_' + str(name) +'.txt'
            Temp_Rule=pd.read_csv(File_name,delimiter=' ',header=None)
            peak_flow,sum_cap,spr_cap,fall_cap,win_date,spr_date,sum_date,fall_date,eff,check_surplus=Temp_Rule.loc[Rule][:]

            surplus = 0
            transfer = 0
            flow_weekly = []
            k = str(SCE_names.loc[0][name])
            I_O=str(SCE_names.loc[1][name])
            
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
                None

            flow_ts = df_sim.loc[:,site_name].values
            flow_daily = flow_ts[year*365:year*365+365]
            
            for i in range(0,52):
                flow_weekly = np.append(flow_weekly,np.sum(flow_daily[i*7:i*7+7]))
                    
            x = np.max(flow_weekly[15:36])
            L = list(flow_weekly)
            peak_flow = L.index(x)


            for week in range(0,52):
                
                # available hydro production based on water availability
                avail_power = flow_weekly[week]*eff
                
                # if it's still winter, operate as RoR
                if week < peak_flow - win_date:
                    
                    gen = avail_power
                
                # if it's spring, operate as RoR with upper limit
                elif week >= peak_flow - win_date and week < peak_flow - spr_date:
                
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
                elif week >= peak_flow - spr_date and week < peak_flow + sum_date:
                    
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
                elif week >= peak_flow + sum_date and week < peak_flow + fall_date:
                    
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
                        
                
                elif week >= peak_flow + fall_date:
                    
                        gen = avail_power
                    
                else: 
                    
                    gen = avail_power
                
                est_power = np.append(est_power,gen)
        
    if name in SCE_No_Data_Dams:
        pass
    else:
        SCE_name_list = np.append(SCE_name_list,name)
        name_index = SCE_dams.index(name)
        if name_index < 1:
            M_SCE = est_power
        else:
            M_SCE = np.column_stack((M_SCE,est_power))


df_PGE = pd.DataFrame(M_PGE)
df_PGE.columns = PGE_name_list
df_PGE.to_excel('PGE_output.xlsx')

df_SCE = pd.DataFrame(M_SCE)
df_SCE.columns = SCE_name_list
df_SCE.to_excel('SCE_output.xlsx')


PGE_total=np.sum(M_PGE,axis=1)
SCE_total=np.sum(M_SCE,axis=1)
# more maximum generation constraints
for i in range(0,len(PGE_total)):
    PGE_total[i] = np.min((PGE_total[i],851000))
    SCE_total[i] = np.min((SCE_total[i],153000))
combined = np.column_stack((PGE_total,SCE_total))
Totals = pd.DataFrame(combined)
zones = ['PGE','SCE']
Totals.columns = zones

# Convert to daily, cut 1st and last 2 years
sim_years2 = sim_years - 3
daily = np.zeros((sim_years2*365,2))
for i in range(0,sim_years2):
    for z in zones:
        z_index = zones.index(z)
        s = Totals.loc[(i+1)*52:(i+1)*52+52,z].values
        for w in range(0,52):
            daily[i*365+w*7:i*365+w*7+7,z_index] = s[w]/7
        daily[i*365+364,z_index] =  daily[i*365+w*7+6,z_index]
 
df_D = pd.DataFrame(daily)
df_D.columns = ['PGE_valley','SCE']
df_D.to_excel('CA_hydropower/CA_hydro_weekly_val.xlsx')

#    return None 

# create smoothed daily hydropower and simulate residual noise. 
 
# first read in historical hydropower
df_hist = pd.read_excel('CA_hydropower/SCE_FNF_V2/SCE_data.xlsx',sheet_name = 'WECC_daily',header=0)
df_hist = df_hist.loc[3:,:]
df_new2 = df_hist.reset_index(drop=True)

df_hist = pd.read_excel('CA_hydropower/hist_reservoir_inflows.xlsx',sheet_name = 'WECC_daily',header=0)
df_hist = df_hist.loc[3:,:]
df_new = df_hist.reset_index(drop=True)

PGE = df_new[PGE_dams]
SCE = df_new2[SCE_dams]

PGE_total = []
SCE_total = []

for i in range(0,len(PGE)):
    PGE_total = np.append(PGE_total,np.sum(PGE.loc[i,:]))
    SCE_total = np.append(SCE_total,np.sum(SCE.loc[i,:]))
    
# convert to 1-week blocks

no_weeks = len(PGE)//7
no_years = len(PGE)//365

PGE_block = np.zeros((len(PGE),1))
SCE_block = np.zeros((len(PGE),1))

for i in range(0,no_years):
    for j in range(0,52):
        PGE_block[i*365+j*7:i*365+j*7+7] = np.mean(PGE_total[i*365+j*7:i*365+j*7+7])
        SCE_block[i*365+j*7:i*365+j*7+7] = np.mean(SCE_total[i*365+j*7:i*365+j*7+7])
    PGE_block[i*365+364] = PGE_block[i*365+363]
    SCE_block[i*365+364] = SCE_block[i*365+363]
    
# calculate smoothed version
PGE_smooth = np.zeros((len(PGE)))    
SCE_smooth = np.zeros((len(PGE)))  
PGE_smooth[0:4] = PGE_block[0]
PGE_smooth[-4:] = PGE_block[-1]
SCE_smooth[0:4] = SCE_block[0]
SCE_smooth[-4:] = SCE_block[-1]

for i in range(4,len(PGE)-4):
    PGE_smooth[i] = np.mean(PGE_block[i-3:i+3])
    SCE_smooth[i] = np.mean(SCE_block[i-3:i+3])
    
# residuals
PGE_residuals = PGE_smooth[365:] - PGE_total[365:]
SCE_residuals = SCE_smooth[365:] - SCE_total[365:]

# new residuals 
PGE_new = PGE_smooth + np.random.randn(len(PGE_smooth))*np.std(PGE_residuals) 
SCE_new = SCE_smooth + np.random.randn(len(SCE_smooth))*np.std(SCE_residuals) 

