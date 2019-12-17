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

def hydro(sim_years):
    
#########################################################################
# This purpose of this script is to use synthetic streamflows at major California
# reservoir sites to simulate daily hydropower production for the PG&E and SCE 
# zones of the California electricty market (CAISO), using parameters optimized
# via a differential evolution algorithm. 
#########################################################################

    # load California storage reservoir (ORCA) sites
    df_sites = pd.read_excel('CA_hydropower/sites.xlsx',sheet_name = 'ORCA',header=0)
    ORCA_sites = list(df_sites)
    
    # load upper generation amounts for each predicted hydropower dam (PG&E and SCE)
    upper_gen = pd.read_excel('CA_hydropower/upper.xlsx',header =0)
    
    # month-day calender
    calender = pd.read_excel('CA_hydropower/calender.xlsx',header=0)
    
    # load simulated full natural flows at each California storage reservoir (ORCA site)
    df_sim = pd.read_csv('Synthetic_streamflows/synthetic_streamflows_CA.csv',header=0,index_col=0)
    df_sim = df_sim.loc[0:(sim_years+3)*365,:]
       
    # load simulated outflows calculated by ORCA
    df_ORCA = pd.read_csv('ORCA_output.csv')
    outflow_sites = ['SHA_otf','ORO_otf','YRS_otf','FOL_otf','NML_otf','DNP_otf','EXC_otf','MIL_otf','ISB_otf','SUC_otf','KWH_otf','PFT_otf']
    for i in range(0,len(df_ORCA)):       
        for s in outflow_sites:
            df_sim.loc[i,s] = df_ORCA.loc[i,s]
            
    sim_years = sim_years+3
    
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
    PGE_names = pd.read_excel('CA_hydropower/sites.xlsx',sheet_name ='PGE',header=0)
    PGE_dams = list(PGE_names.loc[:,'Balch 1':])
    PGE_Storage=[PGE_dams[3],PGE_dams[7],PGE_dams[8],PGE_dams[9]]
    PGE_No_Data_Dams=[PGE_dams[2],PGE_dams[4],PGE_dams[10],PGE_dams[11],PGE_dams[15],PGE_dams[16],PGE_dams[17],PGE_dams[26],PGE_dams[30],PGE_dams[38],PGE_dams[39],PGE_dams[55],PGE_dams[60],PGE_dams[65]]
    
    ## SCE hydro projects
    SCE_names = pd.read_excel('CA_hydropower/sites.xlsx',sheet_name ='SCE',header=0)
    SCE_dams = list(SCE_names.loc[:,'Big_Creek_1 ':])
    SCE_No_Data_Dams=[SCE_dams[7],SCE_dams[8],SCE_dams[12]]
    
    #Simulate all the PGE inflow dams
    check_unused = []
    PGE_name_list = []
    SCE_name_list = []
    
    f_horizon = 7
    
    for name in PGE_dams:
        
        STOR = np.zeros((365*(sim_years-1),1))
        
        for year in range(0,sim_years-1):
            
            GEN = np.zeros((365,7))
            
            if name in PGE_No_Data_Dams:
                pass
    
            elif name in PGE_Storage:
                
                # which operating rule to use?
                Rule=Rule_list[year]
                File_name='CA_hydropower/PGE_Storage_FNF_V2/1.0_FNF_Storage_Rule_' + str(name) +'.txt'
                Temp_Rule=pd.read_csv(File_name,delimiter=' ',header=None)
                peak_flow,starting,ending,refill_1_date,evac_date,peak_end,refill_2_date,storage,power_cap,eff,min_power=Temp_Rule.loc[Rule][:]
                          
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
                  
                # iterate through every day of the year
                for day in range(0,365):
                    
                    for fd in range(0,f_horizon):
                        
                        s = day + fd
                        
                        #forecast day? if not, take beginning storage from previous time step
                        if day>0 and fd < 1:
                            
                            storage = STOR[year*365+day-1]
                            
                        elif day<1 and fd <1:
                            
                            storage = 0
    
                        else:
                            
                            pass                        
                                   
                        # available hydro production based on water availability
                        avail_power = flow_ts[year*365+day]*eff
                        
                        # if it's during first refill
                        if s < refill_1_date:
                            
                            gen =starting- ((starting-min_power)/refill_1_date)*s
                            storage = avail_power-gen
                                                
                        
                        # if it maintains the water
                        elif s >=  refill_1_date and s <  evac_date:
                        
                            gen=min_power
                            storage= storage + (avail_power- gen)
        
                        # if it's in evac period 2
                        elif s >= evac_date and s <  peak_end:
                            
                            gen= min_power+ ((power_cap-min_power)/(peak_end-evac_date)* (s- evac_date))
                                
                            if gen > power_cap:
                                gen=power_cap
                                storage= storage + (avail_power- gen)
                            else:
                                
                                storage= storage + (avail_power- gen)    
                                                                  
                        # if it's in evac period 2
                        elif s >= peak_end and s <  refill_2_date:
                            
                            gen= power_cap
                            if gen > power_cap:
                                gen=power_cap
                                storage= storage + (avail_power- gen)
                            else:
        
                                storage= storage + (avail_power- gen)    
                                                                  
                        
                        elif s >=refill_2_date :
                            
                                gen = power_cap-((power_cap-ending)/(365-refill_2_date)* (s-refill_2_date))
                            
        
                        GEN[day,fd] = gen
                        
                        if fd < 1:
                            STOR[year*365+day] = storage
                
            else:
                
                upper_now=upper_gen.loc[upper_gen.loc[:,'Name']== name]
                upper_now=upper_now.reset_index(drop=True)
                upper=upper_now.loc[0]['Max Gen']
                Rule=Rule_list[year]
                File_name='CA_hydropower/PGE_FNF_2/FNF_' + str(name) +'.txt'
                Temp_Rule=pd.read_csv(File_name,delimiter=' ',header=None)
                peak_flow,sum_cap,spr_cap,fall_cap,win_date,spr_date,sum_date,fall_date,eff,check_surplus=Temp_Rule.loc[Rule][:]
    
                surplus = 0
                transfer = 0
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
                
                annual = flow_ts[year*365:year*365+365]
                max_flow = np.max(annual[105:260])
                L = list(annual)
                peak_flow = L.index(max_flow)
       
                for day in range(0,365):
                    
                    for fd in range(0,f_horizon):
                        
                        s = day + fd
                        
                        #forecast day? if not, take beginning storage from previous time step
                        if day>0 and fd < 1:
                            
                            surplus = STOR[year*365+day-1]
                            
                        elif day<1 and fd <1:
                            
                            surplus = 0
    
                        else:
                            
                            pass                
                    
                        # available hydro production based on water availability
                        avail_power = flow_ts[year*365+day]*eff
                        
                        # if it's still winter, operate as RoR
                        if s < peak_flow - win_date:
                            
                                if avail_power >= upper:
                                    gen = upper
                                    surplus = surplus + (avail_power - upper)
                                else:
                                    gen = avail_power
                        
                        # if it's spring, operate as RoR with upper limit
                        elif s >= peak_flow - win_date and s < peak_flow - spr_date:
                        
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
                        elif s >= peak_flow - spr_date and s < peak_flow + sum_date:
                            
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
                        elif s >= peak_flow + sum_date and s < peak_flow + fall_date:
                            
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
                                
                        
                        elif s >= peak_flow + fall_date:
                            
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
                            
                        GEN[day,fd] = gen
                        
                        if fd < 1:
                            STOR[year*365+day] = surplus
                
    #            unused=surplus
    #            check_unused.append(surplus)
    #    rest_surplus=sum(check_unused) 
                            
            if year < 1:
                A_PGE = GEN
            else:
                A_PGE = np.vstack((A_PGE,GEN))
    
        if name in PGE_No_Data_Dams:
            pass
        else:
            PGE_name_list = np.append(PGE_name_list,name)
            name_index = PGE_dams.index(name)
            if name_index < 1:
                M_PGE = A_PGE
            else:
                M_PGE = np.dstack((M_PGE,A_PGE))
                
    ##Simulate all the SCE inflow dams
    for name in SCE_dams:
        
        STOR = np.zeros((365*(sim_years-1),1))
        
        for year in range(0,sim_years-1):
            
            GEN = np.zeros((365,7))
    
            if name in SCE_No_Data_Dams:
                pass
            else:
                Rule=Rule_list[year]
                File_name='CA_hydropower/SCE_FNF_V2/SCE_fnf_' + str(name) +'.txt'
                Temp_Rule=pd.read_csv(File_name,delimiter=' ',header=None)
                peak_flow,sum_cap,spr_cap,fall_cap,win_date,spr_date,sum_date,fall_date,eff,check_surplus=Temp_Rule.loc[Rule][:]
    
                surplus = 0
                transfer = 0
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
                annual = flow_ts[year*365:year*365+365]
                max_flow = np.max(annual[105:260])
                L = list(annual)
                peak_flow = L.index(max_flow)    
    
                # iterate through every day of the year
                for day in range(0,365):
                    
                    for fd in range(0,f_horizon):
                        
                        s = day + fd
                        
                        #forecast day? if not, take beginning storage from previous time step
                        if day>1 and fd < 1:
                            
                            surplus = STOR[year*365+day-1]
                            
                        elif day<1 and fd <1:
                            
                            surplus = 0
    
                        else:
                            
                            pass  
                    
                        # available hydro production based on water availability
                        avail_power = flow_ts[year*365+day]*eff
                        
                        # if it's still winter, operate as RoR
                        if s < peak_flow - win_date:
                            
                                if avail_power >= upper:
                                    gen = upper
                                    surplus = surplus + (avail_power - upper)
                                else:
                                    gen = avail_power
                        
                        # if it's spring, operate as RoR with upper limit
                        elif s >= peak_flow - win_date and s < peak_flow - spr_date:
                        
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
                        elif s >= peak_flow - spr_date and s < peak_flow + sum_date:
                            
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
                        elif s >= peak_flow + sum_date and s < peak_flow + fall_date:
                            
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
                                
                        
                        elif s >= peak_flow + fall_date:
                            
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
                                    
                        GEN[day,fd] = gen
                        
                        if fd < 1:
                            STOR[year*365+day] = surplus
                                     
                    
            if year < 1:
                A_SCE = GEN
            else:
                A_SCE = np.vstack((A_SCE,GEN))
    
        if name in SCE_No_Data_Dams:
            pass
        else:
            SCE_name_list = np.append(SCE_name_list,name)
            name_index = SCE_dams.index(name)
            if name_index < 1:
                M_SCE = A_SCE
            else:
                M_SCE = np.dstack((M_SCE,A_SCE))
    
    
    #df_PGE = pd.DataFrame(M_PGE)
    #df_PGE.columns = PGE_name_list
    #df_PGE.to_excel('PGE_output_forecast.xlsx')
    #
    #df_SCE = pd.DataFrame(M_SCE)
    #df_SCE.columns = SCE_name_list
    #df_SCE.to_excel('SCE_output_forecast.xlsx')
    
    
    PGE_total=np.sum(M_PGE,axis=2)
    SCE_total=np.sum(M_SCE,axis=2)
    
    # more maximum generation constraints
    for i in range(0,len(PGE_total)):
        for fd in range(0,f_horizon):
            PGE_total[i,fd] = np.min((PGE_total[i,fd],851000/7))
            SCE_total[i,fd] = np.min((SCE_total[i,fd],153000/7))
    
    #Forecast analysis
    TG = PGE_total
    differences=np.zeros((len(PGE_total)-f_horizon+1,f_horizon))
    for i in range(0,len(PGE_total)-f_horizon+1):
        differences[i,:] = (TG[i,:] - TG[i:i+f_horizon,0])/1000  
    
    month_ID = np.zeros(((sim_years-1)*365,1))
    for i in range(0,sim_years-1):
        month_ID[i*365+0:i*365+31] = 1
        month_ID[i*365+31:i*365+59]=2
        month_ID[i*365+59:i*365+90]=3
        month_ID[i*365+90:i*365+120]=4
        month_ID[i*365+120:i*365+151]=5
        month_ID[i*365+151:i*365+181]=6
        month_ID[i*365+181:i*365+212]=7
        month_ID[i*365+212:i*365+243]=8
        month_ID[i*365+243:i*365+273]=9
        month_ID[i*365+273:i*365+304]=10
        month_ID[i*365+304:i*365+334]=11
        month_ID[i*365+334:i*365+365]=12
        
    month_ID = month_ID[:-6]
        
    combined = np.column_stack((differences,month_ID))
    df_combined = pd.DataFrame(combined)
    df_combined.columns = ['1','2','3','4','5','6','7','Month']
    
    plt.figure()
    
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(0,12):
        plt.subplot(4,3,i+1)
        
        month_selection = df_combined.loc[df_combined['Month']==i+1,:]
        
        for j in range(0,len(month_selection)):
           
            plt.plot(month_selection.iloc[j,0:f_horizon])
            
        if i ==6:
            plt.ylabel('Difference (GWh)',fontweight='bold') 
        if i == 10:
            plt.xlabel('Forecast Horizon (Days)',fontweight='bold')
        plt.title(months[i],fontweight='bold')
        plt.ylim([-120,120])
    plt.subplots_adjust(wspace=0.6,hspace=1.2)
    
    plt.savefig('PGE_perfect_foresight.png', dpi=2000)
    
    
    #Forecast analysis
    TG = SCE_total
    differences=np.zeros((len(SCE_total)-f_horizon+1,f_horizon))
    for i in range(0,len(SCE_total)-f_horizon+1):
        differences[i,:] = (TG[i,:] - TG[i:i+f_horizon,0])/1000  
    
    month_ID = np.zeros(((sim_years-1)*365,1))
    for i in range(0,sim_years-1):
        month_ID[i*365+0:i*365+31] = 1
        month_ID[i*365+31:i*365+59]=2
        month_ID[i*365+59:i*365+90]=3
        month_ID[i*365+90:i*365+120]=4
        month_ID[i*365+120:i*365+151]=5
        month_ID[i*365+151:i*365+181]=6
        month_ID[i*365+181:i*365+212]=7
        month_ID[i*365+212:i*365+243]=8
        month_ID[i*365+243:i*365+273]=9
        month_ID[i*365+273:i*365+304]=10
        month_ID[i*365+304:i*365+334]=11
        month_ID[i*365+334:i*365+365]=12
        
    month_ID = month_ID[:-6]
        
    combined = np.column_stack((differences,month_ID))
    df_combined = pd.DataFrame(combined)
    df_combined.columns = ['1','2','3','4','5','6','7','Month']
    
    plt.figure()
    
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(0,12):
        plt.subplot(4,3,i+1)
        
        month_selection = df_combined.loc[df_combined['Month']==i+1,:]
        
        for j in range(0,len(month_selection)):
           
            plt.plot(month_selection.iloc[j,0:f_horizon])
            
        if i ==6:
            plt.ylabel('Difference (GWh)',fontweight='bold') 
        if i == 10:
            plt.xlabel('Forecast Horizon (Days)',fontweight='bold')
        plt.title(months[i],fontweight='bold')
        plt.ylim([-25,25])
    plt.subplots_adjust(wspace=0.6,hspace=1.2)
    
    plt.savefig('SCE_perfect_foresight.png', dpi=2000)
    
    
    #combined = np.column_stack((PGE_total,SCE_total))
    #Totals = pd.DataFrame(combined)
    #zones = ['PGE','SCE']
    #Totals.columns = zones
    #
    ## Convert to daily, cut 1st and last 2 years
    #sim_years2 = sim_years - 3
    #daily = np.zeros((sim_years2*365,2))
    #for i in range(0,sim_years2):
    #    for z in zones:
    #        z_index = zones.index(z)
    #        s = Totals.loc[(i+1)*365:(i+1)*365+365,z].values
    #        for w in range(0,365):
    #            daily[i*365+w,z_index] = s[w]
    #            
    #df_D = pd.DataFrame(daily)
    #df_D.columns = ['PGE_valley','SCE']
    #df_D.to_excel('CA_hydropower/CA_hydro_daily_forecast.xlsx')
    #
    return None 

