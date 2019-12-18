# -*- coding: utf-8 -*-
"""
Created on Tue May  8 09:09:37 2018

@author:  Simona Denaro
"""

#this file will be the outer shell of the Willamette code

#this code will take the inflows as an input (at various timesteps)
#use balance eqns for reservoirs and control points

#initialize reservoirs
#running the inner function for each reservoir along with the timing of the routing

import pandas as pd
import numpy as np
import xmltodict as xmld
import Willamette_model as inner #reading in the inner function
import os
import sys
from sklearn import linear_model

   
def simulate(sim_years):
    
    #%%  load reservoirs and control point infos
    #with open('settings.xml') as fd:
    with open(str(sys.argv[0])) as fd:
        settings = xmld.parse(fd.read())
    
    data_filenames=settings["settings"]['data_inputs']['filenames']
    controlPoints = settings["settings"]["controlPoints"]['controlPoint']
    reservoirs = settings["settings"]["reservoirs"]['reservoir']
    output_filenames=settings["settings"]['data_outputs']['filenames']
    path=settings["settings"]['data_inputs']['path']
    path=path['@path']
    
    
    
    #Create Reservoir class
    class Reservoir:
        def __init__(self, ID):
            self.ID=ID
            self.name=str()
            self.Restype=[]
            self.AreaVolCurve=pd.DataFrame
            self.RuleCurve=pd.DataFrame
            self.Composite=pd.DataFrame
            self.RO=pd.DataFrame
            self.RulePriorityTable=pd.DataFrame
            self.Buffer=pd.DataFrame
            self.Spillway=pd.DataFrame
            self.ruleDir =str()
            self.cpDir =str()
            self.minOutflow=[]
            self.maxVolume=[]
            self.Td_elev=[]
            self.inactive_elev=[]
            self.Fc1_elev=[]
            self.Fc2_elev=[]
            self.Fc3_elev=[]
            self.GateMaxPowerFlow=[]
            self.maxHydro=[]
            self.maxPowerFlow=[]
            self.maxRO_Flow =[]
            self.maxSpillwayFlow=[]
            self.minPowerFlow=0
            self.minRO_Flow =0
            self.minSpillwayFlow=0
            self.Tailwater_elev=[]
            self.Turbine_eff=[]
            self.R2 = float()
            self.zone=1 #assumed as the initial zone
            self.filename_dataIN=str()
            self.dataIN=[]
            self.dataOUT=[]
            self.initVol=[]
    
    #Create ControlPoint class
    class ControlPoint:
        def __init__(self, ID):
            self.ID=ID
            self.name=str()
            self.COMID=str()
            self.influencedReservoirs=[]
            self.hist_dis=[]
            self.loc=[]
    
    
    #RESERVOIR rules
    #in order of RES ID
    res_list =('HCR', 'LOP', 'DEX', 'FAL', 'DOR', 'COT', 'FRN', 'CGR', 'BLU', 'GPR', 'FOS', 'DET', 'BCL')
    RES = [Reservoir(id) for id in range(1,len(res_list)+1)]
    
    for res in RES:
        id = res.ID
        res.name = res_list[id-1]
        res.Restype = str(reservoirs[id-1]['@reservoir_type'])
        res.AreaVolCurve=pd.read_csv(os.path.join(str(path),'Area_Capacity_Curves/', str(reservoirs[id-1]['@area_vol_curve'])))
        res.Composite=pd.read_csv(os.path.join(str(path),'Rel_Cap/', str(reservoirs[id-1]['@composite_rc'])))
        res.RO=pd.read_csv(os.path.join(str(path),'Rel_Cap/', str(reservoirs[id-1]['@RO_rc'])))
        res.Spillway=pd.read_csv(os.path.join(str(path),'Rel_Cap/', str(reservoirs[id-1]['@spillway_rc'])))
        res.minOutflow=float(reservoirs[id-1]["@minOutflow"])
        res.inactive_elev=float(reservoirs[id-1]["@inactive_elev"])
        res.GateMaxPowerFlow=float(reservoirs[id-1]["@maxPowerFlow"])
        res.Tailwater_elev=float(reservoirs[id-1]["@tailwater_elev"])
        res.Turbine_eff=float(reservoirs[id-1]["@turbine_efficiency"])
        res.maxHydro = float(reservoirs[id-1]["@max_hydro_production"])
        if res.Restype != "RunOfRiver":
            res.ruleDir=os.path.join(str(path),str(reservoirs[id-1]["@rp_dir"]))
            res.cpDir=os.path.join(str(path),str(reservoirs[id-1]["@cp_dir"]))
            res.RuleCurve=pd.read_csv(os.path.join(str(path),'Rule_Curves/', str(reservoirs[id-1]['@rule_curve'])))
            res.RulePriorityTable=pd.read_csv(os.path.join(str(path),'Rule_Priorities/', str(reservoirs[id-1]['@rule_priorities'])))
            res.Buffer=pd.read_csv(os.path.join(str(path),'Rule_Curves/', str(reservoirs[id-1]['@buffer_zone'])))
            res.maxVolume=float(reservoirs[id-1]["@maxVolume"])
            res.Td_elev=float(reservoirs[id-1]["@td_elev"])
            res.Fc1_elev=float(reservoirs[id-1]["@fc1_elev"])
            res.Fc2_elev=float(reservoirs[id-1]["@fc2_elev"])
            res.Fc2_elev=float(reservoirs[id-1]["@fc3_elev"])
    
    HCR=RES[0]; LOP=RES[1]; DEX=RES[2]; FAL=RES[3]; DOR=RES[4]; COT=RES[5]; FRN=RES[6];
    CGR=RES[7]; BLU=RES[8]; GPR=RES[9]; FOS=RES[10]; DET=RES[11]; BCL=RES[12]
    
    
    #Control Points
    cp_list =['SAL', 'ALB', 'JEF', 'MEH', 'HAR', 'VID', 'JAS', 'GOS', 'WAT', 'MON', 'FOS_out', 'FOS_in']
    del id
    CP = [ControlPoint(id) for id in range(1, len(cp_list)+1)]
    
    for cp in CP:
        id = cp.ID
        cp.name=str(controlPoints[id-1]["@name"])
        cp.influencedReservoirs =np.array((str(controlPoints[id-1]["@reservoirs"]).split(',')))
        cp.COMID=str(controlPoints[id-1]["@location"])
    
    
    SAL=CP[0]; ALB=CP[1]; JEF=CP[2]; MEH=CP[3]; HAR=CP[4]; VID=CP[5]; JAS=CP[6];
    GOS=CP[7]; WAT=CP[8]; MON=CP[9]; FOS_out=CP[10]; FOS_in=CP[11]
    
    #%% LOAD DATA
    
    #converters
    cfs_to_cms = 0.0283168
    M3_PER_ACREFT = 1233.4
    
    #load reservoirs inflow and volume data:
    inflow_data=pd.read_csv(data_filenames['@inflow_data_filename'])
    initial_doy=int(sys.argv[1])
    #initial_doy=1
    for res in RES:
        res.filename_dataIN = str(reservoirs[res.ID-1]['@filename_dataIN'])
        res.dataIN = inflow_data[res.filename_dataIN]*cfs_to_cms
        initial_data=pd.read_excel(os.path.join(str(path),data_filenames['@hist_res_filename']),sheet_name=res.name)
        res.initVol=initial_data['cyclo_mean_volume_m3_2005_2016'][initial_doy-1:] #already in m3
        res.dataOUT =initial_data['cyclo_mean_release_cms_1929_2007'][initial_doy-1:] #already in cms
        if res.name=="LOP":
            res.dataEV =inflow_data['LOP5E']*cfs_to_cms
    
    #load cp data:
    for cp in CP:
        hist_dis=pd.read_excel(os.path.join(str(path),data_filenames['@hist_cp_filename']),sheet_name=cp.name)
        cp.hist_dis= hist_dis['cyclo_mean_discharge_cms_1989_2007'][initial_doy-1:] #historic discharge, already in cms
        if cp.name not in ("Foster_in","Foster_out") :
            cp.loc=inflow_data[cp.name] #already in cms
    
    #%% Allocate and initialize
    #T=res.dataIN.size-1 #Get the simulation horizon from input
    #T =10 #Set the simulation horizon
    T = (sim_years+3)*365 - 1
    
    n_res=len(res_list)
    n_HPres=8
    n_cp = len(cp_list)
    
    #=======
    # allocate output
    outflows_all = np.full((T+2,n_res),np.nan) #we can fill these in later, or make them empty and 'append' the values
    hydropower_all = np.full((T+2,n_HPres), np.nan)
    volumes_all = np.full((T+2,n_res),np.nan)
    elevations_all = np.full((T+2,n_res),np.nan)
    cp_discharge_all = np.full((T+2,(n_cp)),np.nan)
    
    #initialize values
    for  i in range(0,n_res):
        outflows_all[0:3,i] = RES[i].dataOUT[0:3]
        volumes_all[0:3,i] = RES[i].initVol[0:3]
        elevations_all[0:3,i]=inner.GetPoolElevationFromVolume(volumes_all[0:3,i],RES[i])
    
    for  i in range(0,n_cp):
         cp_discharge_all[0:3,i] = CP[i].hist_dis[0:3]
    
    InitwaterYear = 1.2  #assume strt from normal water year
    waterYear = InitwaterYear
    
    #%% SIMULATION
    doy = initial_doy
    
    #Daily loop
    for t in range(1,T-1):
    
        if doy==120:
            waterYear = inner.UpdateReservoirWaterYear(doy,t,volumes_all) #function missing
    
        #COTTAGE GROVE ID=6 count=5 NO HYDROPOWER
        COT_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t-1,COT.ID-1],COT)
        [COT_outflow, _,_,_, COT.zone] = inner.GetResOutflow(COT,volumes_all[t-1,COT.ID-1],COT.dataIN[t],COT.dataIN[t-1],outflows_all[t-1,COT.ID-1],doy,waterYear,CP,cp_discharge_all[t-1,:],COT.zone)
        [COT_volume,COT_elevation] = inner.UpdateVolume_elev (COT, COT.dataIN[t], COT_outflow, volumes_all[t-1,COT.ID-1])
    
        outflows_all[t,COT.ID-1] = COT_outflow
        volumes_all[t,COT.ID-1] =  COT_volume
        elevations_all[t,COT.ID-1]=  COT_elevation
    
    
        #DORENA ID=5 count=4 NO HYDROPOWER
        DOR_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t-1,DOR.ID-1],DOR)
        [DOR_outflow, _,_,_, DOR.zone] = inner.GetResOutflow(DOR,volumes_all[t-1,DOR.ID-1],DOR.dataIN[t],DOR.dataIN[t-1],outflows_all[t-1,DOR.ID-1],doy,waterYear,CP,cp_discharge_all[t-1,:],DOR.zone)
        [DOR_volume,DOR_elevation] = inner.UpdateVolume_elev (DOR, DOR.dataIN[t], DOR_outflow,volumes_all[t-1,DOR.ID-1])
    
        outflows_all[t,DOR.ID-1] = DOR_outflow
        volumes_all[t,DOR.ID-1] =  DOR_volume
        elevations_all[t,DOR.ID-1]=  DOR_elevation
    
    
        #FERN RIDGE ID=7 count=6 NO HYDROPOWER
        FRN_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t-1,FRN.ID-1],FRN)
        [FRN_outflow,_,_,_, FRN.zone] = inner.GetResOutflow(FRN,volumes_all[t-1,FRN.ID-1],FRN.dataIN[t],FRN.dataIN[t-1],outflows_all[t-1,FRN.ID-1],doy,waterYear,CP,cp_discharge_all[t-1,:],FRN.zone)
        [FRN_volume,FRN_elevation] = inner.UpdateVolume_elev (FRN, FRN.dataIN[t], FRN_outflow,volumes_all[t-1,FRN.ID-1])
    
        outflows_all[t,FRN.ID-1] = FRN_outflow
        volumes_all[t,FRN.ID-1] =  FRN_volume
        elevations_all[t,FRN.ID-1]=  FRN_elevation
    
    
        #HILLS CREEK ID=1 count =0
        HCR_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t-1,HCR.ID-1],HCR)
        [HCR_outflow,powerFlow,RO_flow,spillwayFlow, HCR.zone] = inner.GetResOutflow(HCR,volumes_all[t-1,HCR.ID-1],HCR.dataIN[t],HCR.dataIN[t-1],outflows_all[t-1,HCR.ID-1],doy,waterYear,CP,cp_discharge_all[t-1,:],HCR.zone)
        HCR_power_output = inner.CalculateHydropowerOutput(HCR,HCR_poolElevation,powerFlow)
        [HCR_volume,HCR_elevation] = inner.UpdateVolume_elev (HCR, HCR.dataIN[t], HCR_outflow,volumes_all[t-1,HCR.ID-1])
    
        outflows_all[t,HCR.ID-1] = HCR_outflow
        volumes_all[t,HCR.ID-1] =  HCR_volume
        elevations_all[t,HCR.ID-1]=  HCR_elevation
        hydropower_all[t,0] = HCR_power_output
    
        #LOOKOUT POINT ID=2 count=1
        LOP_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t-1,LOP.ID-1],LOP)
        LOP_inflow =  HCR_outflow + LOP.dataIN[t] + LOP.dataEV[t] #balance equation
        LOP_inflow_lag =  outflows_all[t-1,HCR.ID-1] + LOP.dataIN[t-1] + LOP.dataEV[t-1] #balance equation
        [LOP_outflow,powerFlow,RO_flow,spillwayFlow, LOP.zone]  = inner.GetResOutflow(LOP,volumes_all[t-1,LOP.ID-1],LOP_inflow,LOP_inflow_lag,outflows_all[t-1,LOP.ID-1],doy,waterYear,CP,cp_discharge_all[t-1,:],LOP.zone)
        LOP_power_output = inner.CalculateHydropowerOutput(LOP,LOP_poolElevation,powerFlow)
        [LOP_volume,LOP_elevation] = inner.UpdateVolume_elev (LOP, LOP_inflow, LOP_outflow,volumes_all[t-1,LOP.ID-1])
    
        outflows_all[t,LOP.ID-1] = LOP_outflow
        volumes_all[t,LOP.ID-1] =  LOP_volume
        elevations_all[t,LOP.ID-1]=  LOP_elevation
        hydropower_all[t,1] = LOP_power_output
    
        #DEXTER ID=3 count=2
        DEX_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t-1,DEX.ID-1],DEX)
        DEX_inflow =  LOP_outflow + DEX.dataIN[t] #balance equation
        DEX_inflow_lag =  outflows_all[t-1,LOP.ID-1] + DEX.dataIN[t-1] #balance equation
        [DEX_outflow,powerFlow,RO_flow,spillwayFlow, DEX.zone] = inner.GetResOutflow(DEX,volumes_all[t-1,DEX.ID-1],DEX_inflow,DEX_inflow_lag,outflows_all[t-1,DEX.ID-1],doy,waterYear,CP,cp_discharge_all[t-1,:],DEX.zone)
        DEX_power_output = inner.CalculateHydropowerOutput(DEX,DEX_poolElevation,powerFlow)
        [DEX_volume,DEX_elevation] = inner.UpdateVolume_elev (DEX, LOP_outflow, DEX_outflow,volumes_all[t-1,DEX.ID-1])
    
        outflows_all[t,DEX.ID-1] = DEX_outflow
        volumes_all[t,DEX.ID-1] =  DEX_volume
        elevations_all[t,DEX.ID-1]=  DEX_elevation
        hydropower_all[t,2] = DEX_power_output
    
        #FALL CREEK ID=4 count=3 NO HYDROPOWER
        FAL_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t-1,FAL.ID-1],FAL)
        [FAL_outflow, _,_,_, FAL.zone] = inner.GetResOutflow(FAL,volumes_all[t-1,FAL.ID-1],FAL.dataIN[t],FAL.dataIN[t-1],outflows_all[t-1,FAL.ID-1],doy,waterYear,CP,cp_discharge_all[t-1,:],FAL.zone)
        [FAL_volume,FAL_elevation] = inner.UpdateVolume_elev (FAL, FAL.dataIN[t], FAL_outflow,volumes_all[t-1,FAL.ID-1])
    
        outflows_all[t,FAL.ID-1] = FAL_outflow
        volumes_all[t,FAL.ID-1] =  FAL_volume
        elevations_all[t,FAL.ID-1]=  FAL_elevation
    
        #COUGAR ID=8 count=7
        CGR_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t-1,CGR.ID-1],CGR)
        [CGR_outflow,powerFlow,RO_flow,spillwayFlow, CGR.zone] = inner.GetResOutflow(CGR,volumes_all[t-1,CGR.ID-1],CGR.dataIN[t],CGR.dataIN[t-1],outflows_all[t-1,CGR.ID-1],doy,waterYear,CP,cp_discharge_all[t-1,:],CGR.zone)
        CGR_power_output = inner.CalculateHydropowerOutput(CGR,CGR_poolElevation,powerFlow)
        [CGR_volume,CGR_elevation] = inner.UpdateVolume_elev (CGR, CGR.dataIN[t], CGR_outflow,volumes_all[t-1,CGR.ID-1])
    
        outflows_all[t,CGR.ID-1] = CGR_outflow
        volumes_all[t,CGR.ID-1] =  CGR_volume
        elevations_all[t,CGR.ID-1]=  CGR_elevation
        hydropower_all[t,3] = CGR_power_output
    
    
        #BLUE RIVER ID=9 count= 8 NO HYDROPOWER
        BLU_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t-1,BLU.ID-1],BLU)
        [BLU_outflow,_,_,_, BLU.zone]  = inner.GetResOutflow(BLU,volumes_all[t-1,BLU.ID-1],BLU.dataIN[t],BLU.dataIN[t-1],outflows_all[t-1,BLU.ID-1],doy,waterYear,CP,cp_discharge_all[t-1,:],BLU.zone)
        [BLU_volume,BLU_elevation] = inner.UpdateVolume_elev (BLU, BLU.dataIN[t], BLU_outflow,volumes_all[t-1,BLU.ID-1])
    
        outflows_all[t,BLU.ID-1] = BLU_outflow
        volumes_all[t,BLU.ID-1] =  BLU_volume
        elevations_all[t,BLU.ID-1]=  BLU_elevation
    
        #Update cp discharge
        #in order of upstream to down
        #GOSHEN ID=7
        cp_discharge_all[t,7] = COT_outflow + DOR_outflow + GOS.loc[t]
        #MONROE ID=9
        cp_discharge_all[t,9] = FRN_outflow + MON.loc[t]
        #JASPER ID=6
        cp_discharge_all[t,6] = DEX_outflow + FAL_outflow + JAS.loc[t]
        #VIDA ID=5
        cp_discharge_all[t,5] = CGR_outflow + BLU_outflow + VID.loc[t]
        #HARRISBURG ID=4
        cp_discharge_all[t,4] = cp_discharge_all[t,7] + cp_discharge_all[t,6] + cp_discharge_all[t,5] + HAR.loc[t]
        #____t+1
        #ALBANY ID=1
        cp_discharge_all[t+1,1] = cp_discharge_all[t,9] + cp_discharge_all[t,4]+ ALB.loc[t+1]
        #WATERLOO ID=8
        cp_discharge_all[t+1,8] = outflows_all[t+1,FOS.ID-1] + WAT.loc[t+1]
        #MEHAMA ID=3
        cp_discharge_all[t+1,3] = outflows_all[t+1,BCL.ID-1] + MEH.loc[t+1]
        #JEFFERSON ID=2
        cp_discharge_all[t+1,2] = cp_discharge_all[t+1,8] + cp_discharge_all[t+1,3] + JEF.loc[t+1]
        #SALEM ID=0
        cp_discharge_all[t+1,0] = cp_discharge_all[t+1,1] + cp_discharge_all[t+1,2] + SAL.loc[t+1]
        #FOSTER-out ID=10 (reservoir ID=11)
        cp_discharge_all[t+1,10] = outflows_all[t+1,FOS.ID-1]
        #FOSTER-in ID=11 (reservoir ID=11)
        cp_discharge_all[t+1,11] = outflows_all[t+1,GPR.ID-1] + FOS.dataIN[t+1]
    
        #the next reservoirs are at time "t+2"
        #GREEN PETER ID=10 count=9
        GPR_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t+1,GPR.ID-1],GPR)
        [GPR_outflow, powerFlow,RO_flow,spillwayFlow,GPR.zone] = inner.GetResOutflow(GPR,volumes_all[t+1,GPR.ID-1],GPR.dataIN[t+2],GPR.dataIN[t+1],outflows_all[t+1,GPR.ID-1],doy,waterYear,CP,cp_discharge_all[t+1,:],GPR.zone)
        GPR_power_output = inner.CalculateHydropowerOutput(GPR,GPR_poolElevation,powerFlow)
        [GPR_volume,GPR_elevation] = inner.UpdateVolume_elev (GPR, GPR.dataIN[t+2], GPR_outflow,volumes_all[t+1,GPR.ID-1])
    
        outflows_all[t+2,GPR.ID-1] = GPR_outflow
        volumes_all[t+2,GPR.ID-1] =  GPR_volume
        elevations_all[t+2,GPR.ID-1]=  GPR_elevation
        hydropower_all[t+2,4] = GPR_power_output
    
    
        #FOSTER ID=11 count=10
        FOS_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t+1,FOS.ID-1],FOS)
        FOS_inflow =GPR_outflow + FOS.dataIN[t+2] #balance equation
        FOS_inflow_lag =outflows_all[t+1,GPR.ID-1] + FOS.dataIN[t+1] #balance equation
        [FOS_outflow, powerFlow,RO_flow,spillwayFlow, FOS.zone] = inner.GetResOutflow(FOS,volumes_all[t+1,FOS.ID-1],FOS_inflow,FOS_inflow_lag,outflows_all[t+1,FOS.ID-1],doy,waterYear,CP,cp_discharge_all[t+1,:],FOS.zone)
        FOS_power_output = inner.CalculateHydropowerOutput(FOS,FOS_poolElevation,powerFlow)
        [FOS_volume,FOS_elevation] = inner.UpdateVolume_elev (FOS, FOS_inflow, FOS_outflow,volumes_all[t+1,FOS.ID-1])
    
        outflows_all[t+2,FOS.ID-1] = FOS_outflow
        volumes_all[t+2,FOS.ID-1] =  FOS_volume
        elevations_all[t+2,FOS.ID-1]=  FOS_elevation
        hydropower_all[t+2,5] = FOS_power_output
    
    
        #DETROIT ID=12 count=11
        DET_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t+1,DET.ID-1],DET)
        [DET_outflow, powerFlow,RO_flow,spillwayFlow, DET.zone] = inner.GetResOutflow(DET,volumes_all[t+1,DET.ID-1],DET.dataIN[t+2],DET.dataIN[t+1],outflows_all[t+1,DET.ID-1],doy,waterYear,CP,cp_discharge_all[t+1,:],DET.zone)
        DET_power_output = inner.CalculateHydropowerOutput(DET,DET_poolElevation,powerFlow)
        [DET_volume,DET_elevation] = inner.UpdateVolume_elev (DET, DET.dataIN[t+2], DET_outflow,volumes_all[t+1,DET.ID-1])
    
        outflows_all[t+2,DET.ID-1] = DET_outflow
        volumes_all[t+2,DET.ID-1] =  DET_volume
        elevations_all[t+2,DET.ID-1]=  DET_elevation
        hydropower_all[t+2,6] = DET_power_output
    
        #BIG CLIFF ID=13 count=12
        BCL_poolElevation = inner.GetPoolElevationFromVolume(volumes_all[t+1,BCL.ID-1],BCL)
        BCL_inflow =DET_outflow + BCL.dataIN[t+2] #balance equation
        BCL_inflow_lag =outflows_all[t+1,DET.ID-1] + BCL.dataIN[t+1] #balance equation
        [BCL_outflow, powerFlow,RO_flow,spillwayFlow, BCL.zone] = inner.GetResOutflow(BCL,volumes_all[t+1,BCL.ID-1],BCL_inflow,BCL_inflow_lag ,outflows_all[t+1,BCL.ID-1],doy,waterYear,CP,cp_discharge_all[t+1,:],BCL.zone)
        BCL_power_output = inner.CalculateHydropowerOutput(BCL,BCL_poolElevation,powerFlow)
        [BCL_volume,BCL_elevation] = inner.UpdateVolume_elev (BCL, DET_outflow, BCL_outflow,volumes_all[t+1,BCL.ID-1])
    
        outflows_all[t+2,BCL.ID-1] = BCL_outflow
        volumes_all[t+2,BCL.ID-1] =  BCL_volume
        elevations_all[t+2,BCL.ID-1]=  BCL_elevation
        hydropower_all[t+2,7] = BCL_power_output
    
        doy = initial_doy+t
    
    
    #%%
    #SAVE DATA
    
    #hydropower
    HP_res_list =('HCR', 'LOP', 'DEX', 'CGR', 'GPR', 'FOS', 'DET', 'BCL')
    Output_HP=pd.DataFrame(hydropower_all.clip(min=0),columns=HP_res_list)
    #fill the first day of HP production assuming HP_day0 = HP_day1
    Output_HP.iloc[0]=Output_HP.iloc[1]
    # fill the first 3 days of the 4 upstream dams with multivariate linear regression
    lm=linear_model.LinearRegression()
    X=Output_HP.iloc[3:-3,0:4]
    for res in HP_res_list[4:8]:
        y=Output_HP[res][3:-3]
        model=lm.fit(X,y)
        Output_HP[res][0:3]=lm.predict(X.iloc[0:3]).clip(min=0)
    # fill the last 3 days of the 4 downstream dams with multivariate linear regression
    X=Output_HP.iloc[0:-3,4:8]
    for res in HP_res_list[0:4]:
        y=Output_HP[res][0:-3]
        model=lm.fit(X,y)
        Output_HP[res][-3:]=lm.predict(X.iloc[-3:]).clip(min=0)
    #remove the last 2 values, so that result is mod(365)
    Output_HP=Output_HP[:-1]
    
    #total HP as average hourly production 
    tot_HP=Output_HP.sum(axis=1)
    
    
    writer = pd.ExcelWriter(os.path.join(str(path),output_filenames['@hydropower_filename']))
    Output_HP.to_excel(writer,'Willamette_HP')
    writer.save()
    
    
    #control points
    Output_CP=pd.DataFrame(cp_discharge_all,columns=cp_list)
    writer = pd.ExcelWriter(os.path.join(str(path),output_filenames['@cpDischarge_filename']))
    Output_CP.to_excel(writer,'CP_discharge_cms')
    writer.save()
    
    #summary
    Output_release=pd.DataFrame(outflows_all,columns=res_list)
    Output_volume=pd.DataFrame(volumes_all,columns=res_list)
    Output_elev=pd.DataFrame(elevations_all,columns=res_list)
    writer = pd.ExcelWriter(os.path.join(str(path),output_filenames['@summary_filename']))
    Output_release.to_excel(writer,'release_cms')
    Output_volume.to_excel(writer,'volume_m3')
    Output_elev.to_excel(writer,'elevation_m')
    Output_HP.to_excel(writer,'dams_HP_MW')
    tot_HP.to_excel(writer,'total_HP_MW')
    writer.save()
    
    return None
