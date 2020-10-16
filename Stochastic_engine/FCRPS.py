# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 08:58:04 2019

@author: Joy Hill
"""


####################################################################
#Federal Columbia River Power System Model developed from HYSSR
#This version operates on a daily time step.
####################################################################

import numpy as np
import pandas as pd

def simulate(sim_years):

    def ismember(A,B):
        x = np.in1d(A,B)
        return 1 if x==True else 0
    
    #Data input - select flows september 1 (244 julian date)
    #d=pd.read_excel('Synthetic_streamflows/BPA_hist_streamflow.xlsx',usecols=range(3,58), header=None, names=np.arange(0,55))
    d=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_FCRPS.csv',header=None)
    d = d.iloc[0:(sim_years+3)*365,:]
    d = d.iloc[243:len(d)-122,:]
    d= d.reset_index(drop=True)
    [r, c]= d.shape
    
    for i in range(0,r):
        for j in range(0,c):
            if np.isnan(d.iloc[i,j]) == True:
                d.iloc[i,j] = 0
    
    
    no_days = int(len(d))
    no_years = int(no_days/365)
    
    
    calender=pd.read_excel('PNW_hydro/FCRPS/daily_streamflows.xlsx','Calender',header=None)
    c=np.zeros((no_days,4))
    
    for i in range(0,no_years):
        c[i*365:i*365+365,0] = calender.iloc[:,0]
        c[i*365:i*365+365,1] = calender.iloc[:,1]
        c[i*365:i*365+365,2] = calender.iloc[:,2]
        c[i*365:i*365+365,3] = calender.iloc[:,3]+i
    
    
    #month, day, year of simulation data
    months = c[:,0]
    days = c[:,1]
    julians = c[:,2]
    no_days = len(c)
    years = c[:,3]
    
    #Simulated Runoff ("local" flow accretions defined by USACE and BPA)
    local = d
    
    #%Project indices (consistent with HYSSR)
    #% No. Name	HYSSR ID
    #% 0 MICA	1
    #% 1 ARROW	2
    #% 2 LIBBY	3
    #% 3 DUNCAN	5
    #% 4 CORRA LINN	6
    #% 5 HUNGRY HORSE	10
    #% 6 KERR	11
    #% 7 ALBENI FALLS	16
    #% 8 POST FALLS	18
    #% 9 GRAND COULEE	19
    #% 10 CHELAN	20
    #% 11 BROWNLEE	21
    #% 12 DWORSHAK	31
    #% 13 NOXON	38
    #% 14 ROUND BUTTE	40
    #% 15 REVELSTOKE	41
    #% 16 SEVEN MILE	46
    #% 17 BRILLIANT	50
    #% 18 THOMPSON FALLS	54
    #% 19 CABINET GRGE	56
    #% 20 BOX CANYON	57
    #% 21 BOUNDARY	58
    #% 22 WANETA	59
    #% 23 UPPER FALLS	61
    #% 24 MONROE ST	62
    #% 25 NINE MILE	63
    #% 26 LONG LAKE	64
    #% 27 LITTLE FALLS	65
    #% 28 CHIEF JOSEPH	66
    #% 29 WELLS	67
    #% 30 ROCKY REACH	68
    #% 31 ROCK ISLAND	69
    #% 32 WANAPUM	70
    #% 33 PRIEST RAPIDS	71
    #% 34 OXBOW	72
    #% 35 LOWER GRANITE	76
    #% 36 LITTLE GOOSE	77
    #% 37 LOWER MONUMENTAL	78
    #% 38 ICE HARBOR	79
    #% 39 MCNARY	80
    #% 40 JOHN DAY	81
    #% 41 DALLES	82
    #% 42 BONNEVILLE	83
    #% 43 HELLS CANYON	84
    #% 44 PELTON	95
    #% 45 PRIEST LAKE	146
    #% 46 BONNERS FERRY	400
    
    #%Simulated unregulated flows for The Dalles. These flows are used to
    #%adjust rule curves for storage reservoirs. In reality, ESP FORECASTS are
    #%used-- but for now, the model assumes that BPA/USACE gets the forecast
    #%exactly right.
    TDA_unreg = d.iloc[:,47]
    
    ############
    #%Additional input to fix the model
    #
    #%Fix No.1 Kerr Dam lack of input from CFM
    CFM5L= d.iloc[:,48]
    #%add to Kerr
    #
    #%Fix No.2 Lower Granite lack of input from 5 sources
    #%Following will be add ti LWG
    ORF5H= d.iloc[:,49]
    SPD5L= d.iloc[:,50]
    ANA5L= d.iloc[:,51]
    LIM5L= d.iloc[:,52]
    WHB5H= d.iloc[:,53]
    #%
    #%Fix No.3 lack of input McNary
    #%
    YAK5H= d.iloc[:,54]
    ##############################################
    ##############################################
    #%Flood control curves
    MCD_fc = pd.read_excel('PNW_hydro/FCRPS/res_specs2.xlsx',sheet_name='Mica_Daily',usecols='B:M',skiprows=3,header=None)
    ARD_fc = pd.read_excel('PNW_hydro/FCRPS/res_specs2.xlsx',sheet_name='Arrow_Daily',usecols='B:G',skiprows=3,header=None)
    LIB_fc = pd.read_excel('PNW_hydro/FCRPS/res_specs2.xlsx',sheet_name='Libby_Daily',usecols='B:F',skiprows=3,header=None)
    DNC_fc = pd.read_excel('PNW_hydro/FCRPS/res_specs2.xlsx',sheet_name='Duncan_Daily',usecols='B:F',skiprows=3,header=None)
    HHO_fc = pd.read_excel('PNW_hydro/FCRPS/res_specs2.xlsx',sheet_name='HungryHorse_Daily',usecols='B:I',skiprows=3,header=None)
    ALB_fc = pd.read_excel('PNW_hydro/FCRPS/res_specs2.xlsx',sheet_name='Albeni_Daily',usecols='B:C',skiprows=3,header=None)
    GCL_fc = pd.read_excel('PNW_hydro/FCRPS/res_specs2.xlsx',sheet_name='GrandCoulee_Daily',usecols='B:J',skiprows=3,header=None)
    BRN_fc = pd.read_excel('PNW_hydro/FCRPS/res_specs2.xlsx',sheet_name='Brownlee_Daily',usecols='B:U',skiprows=3,header=None)
    DWR_fc = pd.read_excel('PNW_hydro/FCRPS/res_specs2.xlsx',sheet_name='Dworshak_Daily',usecols='B:K',skiprows=3,header=None)
    
    
    #%Read Other CRCs
    LIB_CRC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='LIB_CRC',header=None)
    LIB_ARC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='LIB_ARC', header=None)
    #% COR_CRC_hm3 = pd.read_excel('ORC.xlsx','COR_CRC', 'A1:B365')
    HHO_CRC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='HHO_CRC', header=None)
    HHO_ARC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='HHO_ARC', header=None)
    #% KER_CRC_hm3 = pd.read_excel('ORC.xlsx','KER_CRC', 'A1:B365')
    ALF_CRC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='ALF_CRC', header=None)
    ALF_ARC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='ALF_ARC', header=None)
    GCL_CRC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='GCL_CRC', header=None)
    GCL_ARC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='GCL_ARC', header=None)
    #% CHL_CRC_hm3 = pd.read_excel('ORC.xlsx','CHL_CRC', 'A1:B365')
    BRN_CRC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='BRN_CRC', header=None)
    BRN_ARC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='BRN_ARC', header=None)
    DWR_CRC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='DWR_CRC', header=None)
    DWR_ARC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='DWR_ARC', header=None)
    
    
    #%Read Duncan's ARC and CRC (in hm3)
    DNC_ARC_hm3= pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='Duncan_ARC', header=None)
    DNC_CRC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='Duncan_CRC', header=None)
    
    DNC_ARC = np.zeros((len(DNC_ARC_hm3),2))
    DNC_CRC = np.zeros((len(DNC_CRC_hm3),2))
    DNC_ARC[:,1]=1.23*DNC_ARC_hm3.iloc[:,1]
    DNC_CRC[:,1] =1.23*DNC_CRC_hm3.iloc[:,1]
    
    #%Read Arrow's ARC and CRC (in hm3)
    
    ARD_ARC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='ARD_ARC', header=None)
    ARD_CRC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='ARD_CRC', header=None)
    #Read Mica's ARC and CRC (in hm3)
    MCD_ARC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='MCD_ARC', header=None)
    MCD_CRC_hm3 = pd.read_excel('PNW_hydro/FCRPS/ORC.xlsx',sheet_name='MCD_CRC', header=None)
    
    #convert to kAF
    DNC_ARC[:,0] = DNC_ARC_hm3.iloc[:,0]
    DNC_CRC[:,0] = DNC_CRC_hm3.iloc[:,0]
    
    
    ARD_ARC = np.zeros((len(ARD_ARC_hm3),2))
    ARD_CRC = np.zeros((len(ARD_CRC_hm3),2))
    ARD_ARC[:,0] =ARD_ARC_hm3.iloc[:,0]
    ARD_CRC[:,0] =ARD_CRC_hm3.iloc[:,0]
    
    MCD_ARC = np.zeros((len(MCD_ARC_hm3),2))
    MCD_CRC = np.zeros((len(MCD_CRC_hm3),2))
    MCD_ARC[:,0] =MCD_ARC_hm3.iloc[:,0]
    MCD_CRC[:,0] =MCD_CRC_hm3.iloc[:,0]
    
    
    ARD_ARC[:,1]=1.23*ARD_ARC_hm3.iloc[:,1]
    ARD_CRC[:,1] =1.23*ARD_CRC_hm3.iloc[:,1]
    
    
    MCD_ARC[:,1]=1.23*MCD_ARC_hm3.iloc[:,1]
    MCD_CRC[:,1] =1.23*MCD_CRC_hm3.iloc[:,1]
    
    
    #LIB_CRC(:,1) =LIB_CRC_hm3(:,1)
    #LIB_ARC(:,1) =LIB_ARC_hm3(:,1)
    LIB_ARC = np.zeros((len(LIB_ARC_hm3),2))
    LIB_CRC = np.zeros((len(LIB_CRC_hm3),2))
    LIB_ARC[:,0] =LIB_ARC_hm3.iloc[:,0]
    LIB_CRC[:,0] =LIB_CRC_hm3.iloc[:,0]
    
    #COR_CRC(:,1) =COR_CRC_hm3(:,1)
    #HHO_CRC(:,1) =HHO_CRC_hm3(:,1)
    #HHO_ARC(:,1) =HHO_ARC_hm3(:,1)
    HHO_ARC = np.zeros((len(HHO_ARC_hm3),2))
    HHO_CRC = np.zeros((len(HHO_CRC_hm3),2))
    HHO_ARC[:,0] =HHO_ARC_hm3.iloc[:,0]
    HHO_CRC[:,0] =HHO_CRC_hm3.iloc[:,0]
    
    #KER_CRC(:,1) =KER_CRC_hm3(:,1)
    
    ALB_ARC = np.zeros((len(ALF_ARC_hm3),2))
    ALB_CRC = np.zeros((len(ALF_CRC_hm3),2))
    ALB_ARC[:,0] =ALF_ARC_hm3.iloc[:,0]
    ALB_CRC[:,0] =ALF_CRC_hm3.iloc[:,0]
    
    #GCL_CRC(:,1) =GCL_CRC_hm3(:,1)
    #GCL_ARC(:,1) =GCL_ARC_hm3(:,1)
    GCL_ARC = np.zeros((len(GCL_ARC_hm3),2))
    GCL_CRC = np.zeros((len(GCL_CRC_hm3),2))
    GCL_ARC[:,0] =GCL_ARC_hm3.iloc[:,0]
    GCL_CRC[:,0] =GCL_CRC_hm3.iloc[:,0]
    
    #BRN_CRC(:,1) =BRN_CRC_hm3(:,1)
    #BRN_ARC(:,1) =BRN_ARC_hm3(:,1)
    BRN_ARC = np.zeros((len(BRN_ARC_hm3),2))
    BRN_CRC = np.zeros((len(BRN_CRC_hm3),2))
    BRN_ARC[:,0] =BRN_ARC_hm3.iloc[:,0]
    BRN_CRC[:,0] =BRN_CRC_hm3.iloc[:,0]
    
    #DWR_CRC(:,1) =DWR_CRC_hm3(:,1)
    #DWR_ARC(:,1) =DWR_ARC_hm3(:,1)
    DWR_ARC = np.zeros((len(DWR_ARC_hm3),2))
    DWR_CRC = np.zeros((len(DWR_CRC_hm3),2))
    DWR_ARC[:,0] =DWR_ARC_hm3.iloc[:,0]
    DWR_CRC[:,0] =DWR_CRC_hm3.iloc[:,0]
    #
    #LIB_CRC(:,2) =1.23*LIB_CRC_hm3(:,2)
    #LIB_ARC(:,2) =1.23*LIB_ARC_hm3(:,2)
    LIB_ARC[:,1] =1.23*LIB_ARC_hm3.iloc[:,1]
    LIB_CRC[:,1] =1.23*LIB_CRC_hm3.iloc[:,1]
    
    #COR_CRC(:,2) =1.23*COR_CRC_hm3(:,2)
    
    
    HHO_ARC[:,1]=1.23*HHO_ARC_hm3.iloc[:,1]
    HHO_CRC[:,1] =1.23*HHO_CRC_hm3.iloc[:,1]
    #KER_CRC(:,2) =1.23*KER_CRC_hm3(:,2)
    #ALB_CRC(:,2) =1.23*ALF_CRC_hm3(:,2)
    #ALB_ARC(:,2) =1.23*ALF_ARC_hm3(:,2)
    ALB_ARC[:,1]=1.23*ALF_ARC_hm3.iloc[:,1]
    ALB_CRC[:,1] =1.23*ALF_CRC_hm3.iloc[:,1]
    
    #GCL_CRC(:,2) =1.23*GCL_CRC_hm3(:,2)
    #GCL_ARC(:,2) =1.23*GCL_ARC_hm3(:,2)
    GCL_ARC[:,1]=1.23*GCL_ARC_hm3.iloc[:,1]
    GCL_CRC[:,1] =1.23*GCL_CRC_hm3.iloc[:,1]
    
    
    #BRN_CRC(:,2) =1.23*BRN_CRC_hm3(:,2)
    #BRN_ARC(:,2) =1.23*BRN_ARC_hm3(:,2)
    BRN_ARC[:,1]=1.23*BRN_ARC_hm3.iloc[:,1]
    BRN_CRC[:,1] =1.23*BRN_CRC_hm3.iloc[:,1]
    
    #DWR_CRC(:,2) =1.23*DWR_CRC_hm3(:,2)
    #DWR_ARC(:,2) =1.23*DWR_ARC_hm3(:,2)
    DWR_ARC[:,1]=1.23*DWR_ARC_hm3.iloc[:,1]
    DWR_CRC[:,1] =1.23*DWR_CRC_hm3.iloc[:,1]
    
    #Spillway storage levels (kAF).
    d=pd.read_excel('PNW_hydro/FCRPS/res_specs3.xlsx')
    s_max = d.iloc[:,1]
    
    #Maximum Hydraulic Capacity
    d=pd.read_excel('PNW_hydro/FCRPS/res_specs2.xlsx','HydraulicMax')
    f_max = d.iloc[:,3]*0.8
    
    #Storage-elevation curves
    d = pd.read_excel('PNW_hydro/FCRPS/res_specs.xlsx','StorEq')
    StorEq = d
    
    #Outflow-tailwater elevation curves
    d = pd.read_excel('PNW_hydro/FCRPS/res_specs.xlsx','TailEq')
    TailEq = d
    
    #Starting storage levels(kAF).
    #Note: model starts August 1, 1928, so reservoirs are assumed full to start.
    s_1= s_max[0]
    s_2=s_max[1]
    s_3=s_max[2]
    s_4=s_max[3]
    s_5=s_max[4]
    s_6=s_max[5]
    s_7=s_max[6]
    s_8=s_max[7]
    s_9=s_max[8]
    s_10=s_max[9]
    s_11=s_max[10]
    s_12=s_max[11]
    s_13=s_max[12]
    s_14=s_max[13]
    s_15=s_max[14]
    s_16=s_max[15]
    s_17=s_max[16]
    s_18=s_max[17]
    s_19=s_max[18]
    s_20=s_max[19]
    s_21=s_max[20]
    s_22=s_max[21]
    s_23=s_max[22]
    s_24=s_max[23]
    s_25=s_max[24]
    s_26=s_max[25]
    s_27=s_max[26]
    s_28=s_max[27]
    s_29=s_max[28]
    s_30=s_max[29]
    s_31=s_max[30]
    s_32=s_max[31]
    s_33=s_max[32]
    s_34=s_max[33]
    s_35=s_max[34]
    s_36=s_max[35]
    s_37=s_max[36]
    s_38=s_max[37]
    s_39=s_max[38]
    s_40=s_max[39]
    s_41=s_max[40]
    s_42=s_max[41]
    s_43=s_max[42]
    s_44=s_max[43]
    s_45=s_max[44]
    s_46=s_max[45]
    s_47=s_max[46]
    
    ###################################
    #Miscellaneous input data/variables
    ###################################
    
    #MCD_fctarget  #Target daily storage value at Mica
    #ICFs = pd.read_excel('TDA5ARF_daily.xlsx','syntheticICFs')
    ICFs=pd.read_csv('PNW_hydro/FCRPS/ICFcal.csv',header=None)
    ICFs = np.array(ICFs)
    #floodyear  #Flood control year (spring)
    #fillstart  #First day of refill period
    sim_days = no_days - 365  #has to be 1 year shorter because of reliance on forecasts in system operations
    
    #One water year contains 14 periods
    p1=np.arange(213,228)   #Aug 1 - Agu 15
    p2=np.arange(228,244)   #Aug 16 - Aug 31
    p3=np.arange(244,274)   #Sep
    p4=np.arange(274,305)  #Oct
    p5=np.arange(305,335)  #Nov
    p6=np.arange(335,366)  #Dec
    p7=np.arange(1,32)      #Jan
    p8=np.arange(32,60)     #Feb
    p9=np.arange(60,91)    #Mar
    p10=np.arange(91,106)   #Apr 1 - Apr 15
    p11=np.arange(106,121)  #Apr 16 - Apr 30
    p12=np.arange(121,152) #May
    p13=np.arange(152,182) #Jun
    p14=np.arange(191,213) #Jul
    
    ###############
    #Output buckets
    ###############
    spokane_flow = np.zeros((sim_days,1))
    storage = np.zeros((sim_days,47))
    discharge = np.zeros((sim_days,47))
    powerflow = np.zeros((sim_days,47))
    spill = np.zeros((sim_days,47))
    generation = np.zeros((sim_days,48))
    Spillheads = np.zeros((sim_days,11))
    heads = np.zeros((sim_days,10))
    inflow = np.zeros((sim_days,1))
    stor = np.zeros((sim_days,1))
    Storage_left = np.zeros((sim_days,1))
    
    ##########
    #ORC arrays#
    ###########
    ALB_ORC = np.zeros((365,1))
    ARD_ORC = np.zeros((365,1))
    BRN_ORC = np.zeros((365,1))
    DNC_ORC = np.zeros((365,1))
    DWR_ORC = np.zeros((365,1))
    GCL_ORC = np.zeros((365,1))
    HHO_ORC = np.zeros((365,1))
    LIB_ORC = np.zeros((365,1))
    MCD_ORC = np.zeros((365,1))
    
    #########
    #sfore arrays#
    #########
    ALB_sfore = np.zeros((sim_days,1))
    ARD_sfore = np.zeros((sim_days,1))
    BRN_sfore = np.zeros((sim_days,1))
    DNC_sfore = np.zeros((sim_days,1))
    DWR_sfore = np.zeros((sim_days,1))
    GCL_sfore = np.zeros((sim_days,1))
    HHO_sfore = np.zeros((sim_days,1))
    LIB_sfore = np.zeros((sim_days,1))
    MCD_sfore = np.zeros((sim_days,1))
    
    ###########
    CHJ_head = np.zeros((sim_days,1))
    DWR_head = np.zeros((sim_days,1))
    GCL_head = np.zeros((sim_days,1))
    HHO_head = np.zeros((sim_days,1))
    IHR_head = np.zeros((sim_days,1))
    JDA_head = np.zeros((sim_days,1))
    LGO_head = np.zeros((sim_days,1))
    LIB_head = np.zeros((sim_days,1))
    LIM_head = np.zeros((sim_days,1))
    LWG_head = np.zeros((sim_days,1))
    MCD_head = np.zeros((sim_days,1))
    MCN_head = np.zeros((sim_days,1))
    LMN_head = np.zeros((sim_days,1))
    
    ###########
    GCL_VRC = np.zeros((365,1))
    MCD_Julian = np.zeros((sim_days,1))
    VAQR_LIB = np.zeros((sim_days,1))
    VAQRnew_LIB = np.zeros((sim_days,1))
    VAQR_HHO = np.zeros((sim_days,1))
    VAQRnew_HHO = np.zeros((sim_days,1))
    FCDend_LIB = np.zeros((no_years,1))
    
    
    ###########
    #Daily Loop
    ###########
    for i in range(0,sim_days):
    
        #First: what julian day and year is it? (need this for all sorts of stuff)
        julian = int(julians[i])
        year = int(years[i])
    
        #When does the initial controlled flood (ICF) occur? This refers to the
        #first instance of simulated unregulated flows at The Dalles reaching
        #450,000cfs. 20 days prior to the ICF marks the start of refill period for storage projects.
        if julian<182:
            floodyear = year
        else:
            floodyear = int(min(year+1,no_years))
    
        ICF = ICFs[floodyear-1]
        fillstart = max(ICF - 20,0)
    
        ##############################
        #############################
        #Add new fillstart day
        #
        fillstart_ARD = max(ICF-2,0)  #Arrow
        fillstart_DNC = max(ICF-10,0)  #Duncan
        fillstart_LIB = max(ICF-10,0) #Libby
        ############################
        ############################
        #Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182
    
        #Calculate "forecasted" unregulated flows at The Dalles (April -
        #August)
        if spring == True:
            TDA_for = TDA_unreg[(year-2)*365+212:(year-2)*365+365].sum()
        else:
            TDA_for = TDA_unreg[(year-1)*365+212:(year-1)*365+365].sum()
    
    
        #Convert forecast to kAF
        TDA_for = TDA_for*.001987
    
        ########################
        #SPOKANE RIVER PROJECTS#
        #Post Falls, Upper Falls, Monroe St.,Nine Mile, Long Lake, and Little
        #Falls#
        #Note: No information regarding storage, release constraints or other
        #operational characteristics is availabe for these dams. As such, they are
        #all modeled as run-of-river (outflows = inflows).
    
    
        #Post Falls - run of river project
        discharge[i,8] = local.iloc[i,8]
        powerflow[i,8] = min(f_max[8],discharge[i,8]*0.001987)
        spill[i,8] = max(0,discharge[i,8]*.001987-f_max[8])
        storage[i,8] = s_9
    
        #Power production
        #Relies on equation P = nphrgk
        #where, P - power (W)
        #p = density of water (1000kg/m^3)
        #h = hydraulic head
        #r = flow rate in m^3/s
        #g = acceleration due to gravity (9.81m/s^2)
        #k = coefficient of efficiency
    
        #Convert powerflow to m^3/s.
        pf_trans = powerflow[i,8]*14.27641
        #Averagy hourly power output (MWh)
        generation[i,8] = max(0,((1000*19.812*pf_trans*9.81*.86)/1000000)*24)
    
        #Upper Falls - run of river project
        discharge[i,23] = local.iloc[i,23] + local.iloc[i,8]
        powerflow[i,23] = min(f_max[23],discharge[i,23]*.001987)
        spill[i,23] = max(0,discharge[i,23]*.001987-f_max[23])
        storage[i,23] = s_24
        generation[i,23] = max(0,((1000*19.812*powerflow[i,23]*14.27641*9.81*.73)/1000000)*24)
    
        #Monroe Street - run of river project
        discharge[i,24] = local.iloc[i,24] + local.iloc[i,23] + local.iloc[i,8]
        powerflow[i,24] = min(f_max[24],discharge[i,24]*.001987)
        spill[i,24] = max(0,discharge[i,24]*.001987-f_max[24])
        storage[i,24] = s_25
        generation[i,24] = max(0,((1000*23.1648*powerflow[i,24]*14.27641*9.81*.82)/1000000)*24)
    
        #Nine Mile - run of river project
        discharge[i,25] = local.iloc[i,25] + local.iloc[i,24] + local.iloc[i,23] + local.iloc[i,8]
        powerflow[i,25] = min(f_max[25],discharge[i,25]*.001987)
        spill[i,25] = max(0,discharge[i,25]*.001987-f_max[25])
        storage[i,25] = s_26
        generation[i,25] = max(0,((1000*20.42*powerflow[i,25]*14.27641*9.81*.71)/1000000)*24)
    
        #Long Lake - run of river project
        discharge[i,26] = local.iloc[i,26] + local.iloc[i,25] + local.iloc[i,24] + local.iloc[i,23] + local.iloc[i,8]
        powerflow[i,26] = min(f_max[26],discharge[i,26]*.001987)
        spill[i,26] = max(0,discharge[i,26]*.001987-f_max[26])
        storage[i,26] = s_26
        generation[i,26] = max(0,((1000*53.34*powerflow[i,26]*14.26641*9.81*.76)/1000000)*24)
    
        #Litle Falls - run of river project
        discharge[i,27] = local.iloc[i,27] + local.iloc[i,26] + local.iloc[i,25] + local.iloc[i,24] + local.iloc[i,23] + local.iloc[i,8]
        powerflow[i,27] = min(f_max[27],discharge[i,27]*.001987)
        spill[i,27] = max(0,discharge[i,27]*.001987-f_max[27])
        storage[i,27] = s_27
        generation[i,27] = max(0,((1000*19.812*powerflow[i,27]*14.27641*9.81*.8)/1000000)*24)
    
        spokane_flow[i] = local.iloc[i,8] + local.iloc[i,23] + local.iloc[i,24] + local.iloc[i,25] + local.iloc[i,26] + local.iloc[i,27]
    
        #########################
        #UPPER COLUMBIA PROJECTS#
        #Mica, Revelstoke, Arrow
    
        ######################################################
        #Mica - storage reservor with flood control rule curve
        ######################################################
        #MCD_sfore = np.zeros((sim_days,1))
        #Are we in evacuation or refill?
        #If ICF exists, then fill start date is ICF - 20.
        if fillstart>0:
            evac = julian<fillstart or julian>243
        #Otherwise just use schedule.
        else:
            evac = julian<182 or julian>243
    
    
    
    
           #Calculate PDR
        if julian>=151 and julian <= 181:
              VPDR_MCD=22000
        elif julian >181 and julian <=212:
              VPDR_MCD = 30000
    
        else:
              VPDR_MCD=3000
    
        if i==0:
              #MCD's storage forecaste
    
              MCD_sfore[i]=min((local.iloc[i,0]-VPDR_MCD)*.001987+s_1,s_max[0])
        else:
              MCD_sfore[i]=min((local.iloc[i,0]-VPDR_MCD)*.001987+ storage[i-1,0],s_max[0])
    
    
        MCD_VRC= MCD_sfore[i] #this is in kAF
    
               #Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182
    
            # Calculate "forecasted" inflows to Mica (April - August)
        if spring == True:
            MCD_for = local.iloc[(year-2)*365+212:(year-2)*365+365,0].sum()
        else:
            MCD_for = local.iloc[(year-1)*365+212:(year-1)*365+365,0].sum()
    
    
            #Convert forecast to kAF
        MCD_for = MCD_for*.001987
    
            #Identify target reservoir storage. A number of flood control curves
            #are publically available. They are based on forecasted flows at The
            #Dalles and Mica Dam (April - August). Some interpolation is
            #necessary when the forecasted flows are in-between those specifiec by
            #USACE.
    
        if TDA_for <= 62000:
            MCD_fctarget = MCD_fc.iloc[julian-1,0]
        elif TDA_for > 62000 and TDA_for <= 65000:
            MCD_fctarget = MCD_fc.iloc[julian-1,0] + ((TDA_for - 62000)/(65000-62000))*(MCD_fc.iloc[julian-1,1] - MCD_fc.iloc[julian-1,0])
        elif TDA_for > 65000 and TDA_for <= 70000:
            MCD_fctarget = MCD_fc.iloc[julian-1,1] + ((TDA_for - 65000)/(70000-65000))*(MCD_fc.iloc[julian-1,2] - MCD_fc.iloc[julian-1,1])
        elif TDA_for > 70000 and TDA_for <= 75000:
            MCD_fctarget = MCD_fc.iloc[julian-1,2] + ((TDA_for - 70000)/(75000-7000))*(MCD_fc.iloc[julian-1,3] - MCD_fc.iloc[julian-1,2])
        elif TDA_for > 75000 and TDA_for <= 80000:
            MCD_fctarget = MCD_fc.iloc[julian-1,3] + ((TDA_for - 75000)/(80000-75000))*(MCD_fc.iloc[julian-1,4] - MCD_fc.iloc[julian-1,3])
        elif TDA_for > 80000 and TDA_for <= 105000:
            MCD_fctarget = MCD_fc.iloc[julian-1,4]
        elif TDA_for > 105000: #This is called "On Call" storage
            if MCD_for <= 8000:
                MCD_fctarget = MCD_fc.iloc[julian-1,5]
            elif MCD_for > 8000 and MCD_for <= 10000:
                MCD_fctarget = MCD_fc.iloc[julian-1,5] + ((MCD_for - 8000)/(10000-8000))*(MCD_fc.iloc[julian-1,6] - MCD_fc.iloc[julian-1,5])
            elif MCD_for > 10000 and MCD_for <= 12000:
                MCD_fctarget = MCD_fc.iloc[julian-1,6] + ((MCD_for - 10000)/(12000-10000))*(MCD_fc.iloc[julian-1,7] - MCD_fc.iloc[julian-1,6])
            elif MCD_for > 12000 and MCD_for <= 14000:
                MCD_fctarget = MCD_fc.iloc[julian-1,7] + ((MCD_for - 12000)/(14000-12000))*(MCD_fc.iloc[julian-1,8] - MCD_fc.iloc[julian-1,7])
            elif MCD_for > 14000 and MCD_for <= 16000:
                MCD_fctarget = MCD_fc.iloc[julian-1,8] + ((MCD_for - 14000)/(16000-14000))*(MCD_fc.iloc[julian-1,9] - MCD_fc.iloc[julian-1,8])
            elif MCD_for > 16000 and MCD_for <= 18000:
                MCD_fctarget = MCD_fc.iloc[julian-1,9] + ((MCD_for - 16000)/(18000-16000))*(MCD_fc.iloc[julian-1,10] - MCD_fc.iloc[julian-1,9])
            elif MCD_for > 18000:
                MCD_fctarget = MCD_fc.iloc[julian-1,11]
    
    
    
            #Calculate MCD's ORC
        #MCD_ORC = np.zeros((365,1))
        if julian>=213 and julian <=365:
           MCD_ORC[julian-1]= max(MCD_CRC[julian-1,1],MCD_ARC[julian-1,1])
           MCD_ORC[julian-1]= max(0,min(MCD_ORC[julian-1],MCD_fctarget))
        elif julian >=1 and julian <= 212:
           MCD_ORC[julian-1]= min(MCD_VRC,max(MCD_CRC[julian-1,1],MCD_ARC[julian-1,1]))
           MCD_ORC[julian-1]= max(0,min(MCD_ORC[julian-1],MCD_fctarget))
        else:
           MCD_ORC[julian-1]=MCD_fctarget
    
        #MCD_Julian = np.zeros((sim_days,1))
        MCD_Julian[julian-1]=MCD_fctarget
        if julian>=121 and julian<152:
            APDR_MCD=3478
        elif julian>= 152 and julian <182:
            APDR_MCD=6834
        elif julian >= 182 and julian <213:
            APDR_MCD=42766
        else:
            APDR_MCD=3000
    
    
            #Which PDR are we using
        if julian>=213 and julian <=365:
            MCD_PDR=APDR_MCD
        elif julian >=1 and julian <= 181:
            if MCD_VRC<= max(MCD_CRC[julian-1,1],MCD_ARC[julian-1,1]):
                MCD_PDR=VPDR_MCD
    
        else:
            MCD_PDR=0
    
    
    
    
        if evac == True:
        #Evacuation mode
    
            #Calculate daily reservoir discharge and end-of-day storage. Have to
            #convert project inflows ("local") to kAF. Note there is a seasonal
            #minimum flow value (MCD_min) associated with Mica Dam in order to
            #create adequate flows into Arrow Lake.
    
            #Mica's operating target based on Arrow's content
            if ismember(julian,p1)== 1:
                if s_2>3300*3:
                    MCD_min=15000*.001987
                    if s_1<3379.2*3:
                        MCD_max=34000*.001987
    
                        MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                elif s_2<=3300*3 and s_2>=1450*3:
                    MCD_dg = 25000*.001987
                elif s_2<1450*3:
                    MCD_dg = 32000*.001987
    
            elif ismember(julian,p2)==1:
                  if s_2>3060*3:
                      MCD_min=15000*.001987
                      if s_1<3529.2*3:
                          MCD_max=34000*.001987
    
                          MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                  elif s_2<=3060*3 and s_2>=1300*3:
                      MCD_dg = 25000*.001987
                  elif s_2<1300*3:
                      MCD_dg = 32000*.001987
    
            elif ismember(julian,p3)==1:
                 if s_2>3570*3:
                     MCD_min=10000*.001987
                     if s_1<3529.2*3:
                         MCD_max=34000*.001987
    
                         MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                 elif s_2<=3570*3 and s_2>=3480*3:
                    MCD_dg = 25000*.001987
                 elif s_2<=3480*3 and s_2>=2140*3:
                    MCD_dg = 27000*.001987
                 elif s_2<1450*3:
                    MCD_dg = 32000*.001987
    
            elif ismember(julian,p4)==1:
                if s_2>3450*3:
                    MCD_min=10000*.001987
                    if s_1<3428.4*3:
                        MCD_max=34000*.001987
    
                        MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                elif s_2<=3450*3 and s_2>=2860*3:
                    MCD_dg = 21000*.001987
                elif s_2<=2860*3 and s_2>=1360*3:
                    MCD_dg = 25000*.001987
                elif s_2<1360*3:
                    MCD_dg = 32000*.001987
    
    
            elif ismember(julian,p5)==1:
                if s_2>3400*3:
                    MCD_min=10000*.001987
    
                    MCD_dg = 22000*.001987
                elif s_2<=3400*3 and s_2>=3030*3:
                    MCD_dg = 19000*.001987
                elif s_2<=3030*3 and s_2>=1100*3:
                    MCD_dg = 25000*.001987
                elif s_2<1100*3:
                    MCD_dg = 32000*.001987
    
    
            elif ismember(julian,p6)==1:
                if s_2>3240*3:
                    if s_1<204.1*3:
                        MCD_dg = 10000*.001987
                    else:
    
                        MCD_dg = 22000*.001987
    
                elif s_2<=3240*3 and s_2>=2400*3:
                    if s_1<204.1*3:
                        MCD_dg = 10000*.001987
                    else:
                        MCD_dg = 25000*.001987
    
                elif s_2<=2400*3 and s_2>=690*3:
                    if s_1<204.1*3:
                        MCD_dg = 10000*.001987
                    else:
                        MCD_dg = 26000*.001987
    
                elif s_2<690*3:
                    if s_1<204.1*3:
                        MCD_dg = 10000*.001987
                    else:
    
                        MCD_dg = 32000*.001987
    
    
            elif ismember(julian,p7)==1:
                if s_2>2250*3:
                    if s_1<204.1*3:
                        MCD_dg = 12000*.001987
                    else:
                        MCD_dg = 24000*.001987
    
                elif s_2<=2500*3 and s_2>=2210*3:
                    if s_1<204.1*3:
                        MCD_dg = 12000*.001987
                    else:
                        MCD_dg = 26000*.001987
    
                elif s_2<=2210*3 and s_2>=1560*3:
                    if s_1<204.1*3:
                        MCD_dg = 12000*.001987
                    else:
                        MCD_dg = 28000*.001987
    
                elif s_2<1560*3:
                    if s_1<204.1*3:
                        MCD_dg = 12000*.001987
                    else:
                        MCD_dg = 29000*.001987
    
    
            elif ismember(julian,p8)==1:
                if s_2>1370*3:
                    MCD_dg = 21000*.001987
                elif s_2<=1370*3 and s_2>=940*3:
                    MCD_dg = 26000*.001987
                elif s_2<=940*3 and s_2>=850*3:
                    MCD_dg = 22000*.001987
                elif s_2<850*3:
                    MCD_dg = 26000*.001987
    
    
    
            elif ismember(julian,p9)==1:
                if s_2>570*3:
                    MCD_dg = 25000*.001987
                elif s_2<=570*3 and s_2>=440*3:
                    MCD_dg = 17000*.001987
                elif s_2<=440*3 and s_2>=160*3:
                    MCD_dg = 21000*.001987
                elif s_2<160*3:
                    MCD_dg = 26000*.001987
    
    
    
            elif ismember(julian,p10)==1:
                if s_2>520*3:
                    MCD_dg = 17000*.001987
                elif s_2<=520*3 and s_2>=400*3:
                    MCD_dg = 12000*.001987
                elif s_2<=400*3 and s_2>=20*3:
                    MCD_dg = 15000*.001987
                elif s_2<20*3:
                    MCD_dg = 21000*.001987
    
    
    
            elif ismember(julian,p11)==1:
                if s_2>890*3:
                    MCD_dg = 10000*.001987
                elif s_2<=890*3 and s_2>=490*3:
                    MCD_dg = 12000*.001987
                elif s_2<=490*3 and s_2>=40*3:
                    MCD_dg = 10000*.001987
                elif s_2<40*3:
                    MCD_dg = 15000*.001987
    
    
            elif ismember(julian,p12)==1:
                if s_2>160*3:
                    MCD_dg = 8000*.001987
                elif s_2<=160*3 and s_2>=20*3:
                    MCD_dg = 10000*.001987
                elif s_2<20*3:
                    MCD_dg = 12000*.001987
    
    
    
            elif ismember(julian,p13)==1:
                if s_2>2140*3:
                    MCD_dg =10000*.001987
                elif s_2<=2140*3 and s_2>=1450*3:
                    MCD_dg = 8000*.001987
                elif s_2<=1450*3 and s_2>=1140*3:
                    MCD_dg = 10000*.001987
                elif s_2<1140*3:
                    MCD_dg = 16000*.001987
    
    
            elif ismember(julian,p14)==1:
                if s_2>3110*3:
                    MCD_min=10000*.001987
                    if s_1<3467.2*3:
                       MCD_max=34000*.001987
    
                       MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                elif s_2<=3110*3 and s_2>=2880*3:
                    MCD_min=10000*.001987
                    if s_1<3405.2*3:
                       MCD_max=34000*.001987
    
                       MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                elif s_2<=2880*3 and s_2>=1650*3:
                    MCD_dg = 22000*.001987
                elif s_2<1650*3:
                    MCD_dg = 24000*.001987
    
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,MCD_dg - f_max[0])
    
            #Is any storage space available?
            stor_avail = MCD_ORC[julian-1] - s_1
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,0] = f_max[0]
                spill[i,0] = MCD_dg - f_max[0]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                MCD_dg = max(MCD_dg - stor_avail,f_max[0])
                powerflow[i,0] = f_max[0]
                spill[i,0] = max(0,MCD_dg - f_max[0])
            else:
                powerflow[i,0] = MCD_dg
    
    
            s_1 = s_1 + local.iloc[i,0]*.001987 - MCD_dg
            discharge[i,0] = MCD_dg*(1/.001987)  #Convert back to cfs
            storage[i,0] = s_1
    
        else:
        #Refill mode - this is when the reservoir fills back up during spring
        #floods. Only storage target is maximum reservoir storage (spillway
        #threshold).
    
            if ismember(julian,p1)==1:
                if s_2>3300*3:
                    MCD_min=15000*.001987
                    if s_1<3379.2*3:
                       MCD_max=34000*.001987
                       MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                elif s_2<=3300*3 and s_2>=1450*3:
                    MCD_dg = 25000*.001987
                elif s_2<1450*3:
                    MCD_dg = 32000*.001987
    
            elif ismember(julian,p2)==1:
                if s_2>3060*3:
                    MCD_min=15000*.001987
                    if s_1<3529.2*3:
                        MCD_max=34000*.001987
                        MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                elif s_2<=3060*3 and s_2>=1300*3:
                    MCD_dg = 25000*.001987
                elif s_2<1300*3:
                    MCD_dg = 32000*.001987
    
    
            elif ismember(julian,p3)==1:
                 if s_2>3570*3:
                     MCD_min=10000*.001987
                     if s_1<3529.2*3:
                         MCD_max=34000*.001987
                         MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                 elif s_2<=3570*3 and s_2>=3480*3:
                     MCD_dg = 25000*.001987
                 elif s_2<=3480*3 and s_2>=2140*3:
                    MCD_dg = 27000*.001987
                 elif s_2<1450*3:
                    MCD_dg = 32000*.001987
    
            elif ismember(julian,p4)==1:
                 if s_2>3450*3:
                     MCD_min=10000*.001987
                     if s_1<3428.4*3:
                         MCD_max=34000*.001987
                         MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                 elif s_2<=3450*3 and s_2>=2860*3:
                     MCD_dg = 21000*.001987
                 elif s_2<=2860*3 and s_2>=1360*3:
                     MCD_dg = 25000*.001987
                 elif s_2<1360*3:
                     MCD_dg = 32000*.001987
    
    
            elif ismember(julian,p5)==1:
                 if s_2>3400*3:
                     MCD_min=10000*.001987
                     MCD_dg = 22000*.001987
                 elif s_2<=3400*3 and s_2>=3030*3:
                     MCD_dg = 19000*.001987
                 elif s_2<=3030*3 and s_2>=1100*3:
                     MCD_dg = 25000*.001987
                 elif s_2<1100*3:
                     MCD_dg = 32000*.001987
    
    
            elif ismember(julian,p6)==1:
               if s_2>3240*3:
                   if s_1<204.1*3:
                       MCD_dg = 10000*.001987
                   else:
                       MCD_dg = 22000*.001987
    
               elif s_2<=3240*3 and s_2>=2400*3:
                   if s_1<204.1*3:
                       MCD_dg = 10000*.001987
                   else:
                       MCD_dg = 25000*.001987
    
               elif s_2<=2400*3 and s_2>=690*3:
                   if s_1<204.1*3:
                       MCD_dg = 10000*.001987
                   else:
                       MCD_dg = 26000*.001987
               elif s_2<690*3:
                   if s_1<204.1*3:
                       MCD_dg = 10000*.001987
                   else:
                       MCD_dg = 32000*.001987
    
    
            elif ismember(julian,p7)==1:
                if s_2>2250*3:
                    if s_1<204.1*3:
                        MCD_dg = 12000*.001987
                    else:
                        MCD_dg = 24000*.001987
    
                elif s_2<=2500*3 and s_2>=2210*3:
                    if s_1<204.1*3:
                        MCD_dg = 12000*.001987
                    else:
                        MCD_dg = 26000*.001987
    
                elif s_2<=2210*3 and s_2>=1560*3:
                   if s_1<204.1*3:
                       MCD_dg = 12000*.001987
                   else:
                       MCD_dg = 28000*.001987
    
                elif s_2<1560*3:
                   if s_1<204.1*3:
                       MCD_dg = 12000*.001987
                   else:
                       MCD_dg = 29000*.001987
    
    
            elif ismember(julian,p8)==1:
                 if s_2>1370*3:
                     MCD_dg = 21000*.001987
                 elif s_2<=1370*3 and s_2>=940*3:
                     MCD_dg = 26000*.001987
                 elif s_2<=940*3 and s_2>=850*3:
                     MCD_dg = 22000*.001987
                 elif s_2<850*3:
                     MCD_dg = 26000*.001987
    
    
    
            elif ismember(julian,p9)==1:
                if s_2>570*3:
                    MCD_dg = 25000*.001987
                elif s_2<=570*3 and s_2>=440*3:
                    MCD_dg = 17000*.001987
                elif s_2<=440*3 and s_2>=160*3:
                    MCD_dg = 21000*.001987
                elif s_2<160*3:
                    MCD_dg = 26000*.001987
    
    
            elif ismember(julian,p10)==1:
                if s_2>520*3:
                    MCD_dg = 17000*.001987
                elif s_2<=520*3 and s_2>=400*3:
                    MCD_dg = 12000*.001987
                elif s_2<=400*3 and s_2>=20*3:
                    MCD_dg = 15000*.001987
                elif s_2<20*3:
                    MCD_dg = 21000*.001987
    
    
            elif ismember(julian,p11)==1:
                if s_2>890*3:
                    MCD_dg = 10000*.001987
                elif s_2<=890*3 and s_2>=490*3:
                    MCD_dg = 12000*.001987
                elif s_2<=490*3 and s_2>=40*3:
                    MCD_dg = 10000*.001987
                elif s_2<40*3:
                    MCD_dg = 15000*.001987
    
    
            elif ismember(julian,p12)==1:
                if s_2>160*3:
                    MCD_dg = 8000*.001987
                elif s_2<=160*3 and s_2>=20*3:
                    MCD_dg = 10000*.001987
                elif s_2<20*3:
                    MCD_dg = 12000*.001987
    
    
            elif ismember(julian,p13)==1:
                if s_2>2140*3:
                    MCD_dg =10000*.001987
                elif s_2<=2140*3 and s_2>=1450*3:
                    MCD_dg = 8000*.001987
                elif s_2<=1450*3 and s_2>=1140*3:
                    MCD_dg = 10000*.001987
                elif s_2<1140*3:
                    MCD_dg = 16000*.001987
    
    
            elif ismember(julian,p14)==1:
                if s_2>3110*3:
                    MCD_min=10000*.001987
                    if s_1<3467.2*3:
                       MCD_max=34000*.001987
                       MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                elif s_2<=3110*3 and s_2>=2880*3:
                    MCD_min=10000*.001987
                    if s_1<3405.2*3:
                       MCD_max=34000*.001987
                       MCD_dg = min(MCD_max,max(max(max(MCD_min - local.iloc[i,15],local.iloc[i,15]),MCD_PDR)*.001987, s_1 + local.iloc[i,0]*.001987 - MCD_ORC[julian-1]))
                elif s_2<=2880*3 and s_2>=1650*3:
                    MCD_dg = 22000*.001987
                elif s_2<1650*3:
                    MCD_dg = 24000*.001987
    
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,MCD_dg - f_max[0])
    
            #Is any storage space available?
            stor_avail = s_max[0] - s_1
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,0] = f_max[0]
                spill[i,0] = MCD_dg - f_max[0]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                MCD_dg = max(MCD_dg - stor_avail,f_max[0])
                powerflow[i,0] = f_max[0]
                spill[i,0] = max(0,MCD_dg - f_max[0])
            else:
                powerflow[i,0] = MCD_dg
    
    
            s_1 = s_1 + local.iloc[i,0]*.001987 - MCD_dg
            discharge[i,0] = MCD_dg*(1/.001987)
            storage[i,0] = s_1
    
        generation[i,0] = ((1000*240.1824*powerflow[i,0]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Revelstoke Dam - run-of-river project
        ######################################
    
        RVC_dg = max(0,MCD_dg + local.iloc[i,15]*.001987)
        s_16 = s_16 + MCD_dg + local.iloc[i,15]*.001987 - RVC_dg
        powerflow[i,15] = min(RVC_dg,f_max[15])
        spill[i,15] = max(0,RVC_dg - f_max[15])
        discharge[i,15] = RVC_dg*(1/.001987)
        storage[i,15] = s_16
        generation[i,15] = ((1000*174.9552*powerflow[i,15]*14.27641*9.81*.875)/1000000)*24
    
        #############################################
        #Arrow (H. Keenleyside) Dam - storage project
        #############################################
    
        #Are we in evacuation or refill?
        #If ICF exists, then fill start date is ICF - 20.
        if fillstart>0:
            evac = julian<fillstart or julian>243
        #Otherwise just use schedule.
        else:
            evac = julian<182 or julian>243
    
    
    
    
            #A wide range of TDA forecast that will be used in later modelling
        if spring == True:
            TDA_for_ARD_Feb=TDA_unreg[(year-2)*365+153:(year-2)*365+334].sum()
            TDA_for_ARD_Mar=TDA_unreg[(year-2)*365+181:(year-2)*365+334].sum()
            TDA_for_ARD_Apr=TDA_unreg[(year-2)*365+212:(year-2)*365+334].sum()
            TDA_for_ARD_May=TDA_unreg[(year-2)*365+242:(year-2)*365+334].sum()
            TDA_for_ARD_Jun=TDA_unreg[(year-2)*365+273:(year-2)*365+334].sum()
            TDA_for_ARD=TDA_unreg[(year-2)*365+122:(year-2)*365+334].sum()
        else:
            TDA_for_ARD_Feb=TDA_unreg[(year-1)*365+153:(year-1)*365+334].sum()
            TDA_for_ARD_Mar=TDA_unreg[(year-1)*365+181:(year-1)*365+334].sum()
            TDA_for_ARD_Apr=TDA_unreg[(year-1)*365+212:(year-1)*365+334].sum()
            TDA_for_ARD_May=TDA_unreg[(year-1)*365+242:(year-1)*365+334].sum()
            TDA_for_ARD_Jun=TDA_unreg[(year-1)*365+273:(year-1)*365+334].sum()
            TDA_for_ARD=TDA_unreg[(year-1)*365+122:(year-1)*365+334].sum()
    
        TDA_for_ARD= TDA_for_ARD*1.9835/1000000
    
        #Set boundries
        if TDA_for_ARD <= 80:
            TDA_for_ARD = 80
        elif TDA_for_ARD >= 110:
            TDA_for_ARD =110
    
    
         #Minimun flow for Arrow
        if julian>=1 and julian <=31:
            ARD_min=10001
        elif julian >=32 and julian <=90:
            ARD_min=19998
        elif julian >=91 and julian <=105:
            ARD_min=15001
        elif julian >= 106 and julian <=120:
            ARD_min=11999
        elif julian >=121 and julian <= 151:
            ARD_min=10001
        elif julian >=152 and julian <=181:
            ARD_min=5000
        else:
            ARD_min=10001
    
    
         #Calculate PDR
        if julian>=151 and julian <= 181:
            VPDR_ARD=42000
        elif julian >181 and julian <=212:
            VPDR_ARD = 53000
          #Above is liner extrapolation from data
        else:
            VPDR_ARD=5000
    
    
      #Calculate VRC
      #inflow is RVC_dg + local.iloc[i,1] out flow is VPDR or APDR
        #ARD_sfore = np.zeros((sim_days,1))
        if i==0:
          #ARD's storage forecaste
          ARD_sfore[i]=min((local.iloc[i,1]-VPDR_ARD)*.001987+s_2,s_max[1])
        else:
            ARD_sfore[i]=min(RVC_dg +(local.iloc[i,1]-VPDR_ARD)*.001987+ storage[i-1,1],s_max[1])
    
        ARD_VRC = ARD_sfore[i] #this is in kAF
    
        #Identify target reservoir storage. A number of flood control curves
        #are publically available. They are based on forecasted flows at The
        #Dalles. Some interpolation is
        #necessary when the forecasted flows are in-between those specifiec by
        #USACE.
    
        if TDA_for <= 64000:
            ARD_fctarget = ARD_fc.iloc[julian-1,0]
        elif TDA_for > 64000 and TDA_for <= 65000:
            ARD_fctarget = ARD_fc.iloc[julian-1,0] + ((TDA_for - 64000)/(65000-64000))*(ARD_fc.iloc[julian-1,1] - ARD_fc.iloc[julian-1,0])
        elif TDA_for > 65000 and TDA_for <= 70000:
            ARD_fctarget = ARD_fc.iloc[julian-1,1] + ((TDA_for - 65000)/(70000-65000))*(ARD_fc.iloc[julian-1,2] - ARD_fc.iloc[julian-1,1])
        elif TDA_for > 70000 and TDA_for <= 75000:
            ARD_fctarget = ARD_fc.iloc[julian-1,2] + ((TDA_for - 70000)/(75000-7000))*(ARD_fc.iloc[julian-1,3] - ARD_fc.iloc[julian-1,2])
        elif TDA_for > 75000 and TDA_for <= 80000:
            ARD_fctarget = ARD_fc.iloc[julian-1,3] + ((TDA_for - 75000)/(80000-75000))*(ARD_fc.iloc[julian-1,4] - ARD_fc.iloc[julian-1,3])
        elif TDA_for > 80000 and TDA_for <= 111000:
            ARD_fctarget = ARD_fc.iloc[julian-1,4] + ((TDA_for - 80000)/(111000-80000))*(ARD_fc.iloc[julian-1,5] - ARD_fc.iloc[julian-1,4])
        else:
            ARD_fctarget = ARD_fc.iloc[julian-1,5]
    
    
        #Calculate ORC
        #ARD_ORC = np.zeros((365,1))
        if julian>=213 and julian <=365:
           ARD_ORC[julian-1]= max(ARD_CRC[julian-1,1],ARD_ARC[julian-1,1])
           ARD_ORC[julian-1]= min(ARD_ORC[julian-1],ARD_fctarget)
        elif julian >=1 and julian <= 212:
           ARD_ORC[julian-1]= min(ARD_VRC,max(ARD_CRC[julian-1,1],ARD_ARC[julian-1,1]))
           ARD_ORC[julian-1]= min(ARD_ORC[julian-1],ARD_fctarget)
        else:
           ARD_ORC[julian-1]=ARD_fctarget
    
    
        if evac==True:
        #Evacuation mode
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
            ARD_dg = max(ARD_min*.001987, s_2 + RVC_dg + local.iloc[i,1]*.001987 - ARD_ORC[julian-1])
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,ARD_dg - f_max[1])
    
            #Is any storage space available?
            stor_avail = ARD_ORC[julian-1] - s_2
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,1] = f_max[1]
                spill[i,1] = ARD_dg - f_max[1]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                ARD_dg = max(ARD_dg - stor_avail,f_max[1])
                powerflow[i,1] = f_max[1]
                spill[i,1] = max(0,ARD_dg - f_max[1])
            else:
                powerflow[i,1] = ARD_dg
    
    
            s_2 = s_2 + RVC_dg + local.iloc[i,1]*.001987 - ARD_dg
            discharge[i,1] = ARD_dg*(1/.001987)  #Convert back to cfs
            storage[i,1] = s_2
    
        else:
        #Refill mode - this is when the reservoir fills back up during spring
        #floods. Only storage target is maximum reservoir storage (spillway
        #threshold).
    
            ARD_dg = max(ARD_min*.001987, s_2 + RVC_dg + local.iloc[i,1]*.001987 - s_max[1])
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,ARD_dg - f_max[1])
    
            #Is any storage space available?
            stor_avail = s_max[1] - s_2
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,1] = f_max[1]
                spill[i,1] = ARD_dg - f_max[1]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                ARD_dg = max(ARD_dg - stor_avail,f_max[1])
                powerflow[i,1] = f_max[1]
                spill[i,1] = max(0,ARD_dg - f_max[1])
            else:
                powerflow[i,1] = ARD_dg
    
    
            s_2 = s_2 + RVC_dg + local.iloc[i,1]*.001987 - ARD_dg
            discharge[i,1] = ARD_dg*(1/.001987)
            storage[i,1] = s_2
    
    
    
        generation[i,1] = ((1000*52.1208*powerflow[i,1]*14.27641*9.81*.875)/1000000)*24
    
        ###################
        #KOOTENAI PROJECTS#
        #Libby, Bonner's Ferry, Duncan, Corra Linn, and Brilliant
    
        ######################################################
        #Duncan - storage reservoir with flood control rule curve
        ######################################################
        #Note: Duncan has no hydroelectric generation capability.
    
        #Are we in evacuation or refill?
        #If ICF exists, then fill start date is ICF - 20.
        if fillstart>0:
            evac = julian<fillstart_LIB or julian>243
        #Otherwise just use schedule.
        else:
            evac = julian<182 or julian>243
    
        #Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182
    
        if spring == True:
            TDA_for_DNC= TDA_unreg[(year-2)*365+122:(year-2)*365+334].sum()
            DNC_for = local.iloc[(year-2)*365+212:(year-2)*365+365,3].sum()
        else:
            DNC_for = local.iloc[(year-1)*365+212:(year-1)*365+365,3].sum()
            TDA_for_DNC= TDA_unreg[(year-1)*365+122:(year-1)*365+334].sum()
    
          #Convert from cfs to mAF
        TDA_for_DNC= TDA_for_DNC*1.9835/1000000
    
        if evac == True:
        #Evacuation mode
    
    
        #Calculate PDR
            if TDA_for_DNC <= 80:
                TDA_for_DNC = 80
            elif TDA_for_DNC >= 110:
                TDA_for_DNC =110
    
    
        #from Jan 1 to May 30 the value is all 100 cfs
            if julian>=1 and julian <= 151:
                VPDR_DNC=100
            elif julian >151 and julian <=181:
                VPDR_DNC = 1200- (1/3)*(TDA_for_DNC-80)
              #Above is liner extrapolation from data
            elif julian >181 and julian <=212:
                VPDR_DNC=2400
            else:
                VPDR_DNC=0
    
    
          #Calculate VRC
          #inflow is just local.iloc[i,4) out flow is VPDR or APDR
            #DNC_sfore = np.zeros((sim_days,1))
            if i==0:
              #DNC's storage forecaste
              DNC_sfore[i]=min((local.iloc[i,3]-VPDR_DNC)*.001987+s_4,s_max[3])
            else:
              DNC_sfore[i]=min((local.iloc[i,3]-VPDR_DNC)*.001987+ storage[i-1,3],s_max[3])
    
            DNC_VRC= DNC_sfore[i] #this is in kAF
    
            #Identify target reservoir storage. A number of flood control curves
            #are publically available. They are based on forecasted inflows. Some interpolation is
            #necessary when the forecasted flows are in-between those specifiec by
            #USACE.
    
            if DNC_for <= 1400:
                DNC_fctarget = DNC_fc.iloc[julian-1,0]
            elif DNC_for > 1400 and DNC_for <= 1600:
                DNC_fctarget = DNC_fc.iloc[julian-1,0] + ((DNC_for - 1400)/(1600-1400))*(DNC_fc.iloc[julian-1,1] - DNC_fc.iloc[julian-1,0])
            elif DNC_for > 1600 and DNC_for <= 1800:
                DNC_fctarget = DNC_fc.iloc[julian-1,1] + ((DNC_for - 1600)/(1800-1600))*(DNC_fc.iloc[julian-1,2] - DNC_fc.iloc[julian-1,1])
            elif DNC_for > 1800 and DNC_for <= 2000:
                DNC_fctarget = DNC_fc.iloc[julian-1,2] + ((DNC_for - 1800)/(2000-1800))*(DNC_fc.iloc[julian-1,3] - DNC_fc.iloc[julian-1,2])
            elif DNC_for > 2000 and DNC_for <= 2200:
                DNC_fctarget = DNC_fc.iloc[julian-1,3] + ((DNC_for - 2000)/(2200-2000))*(DNC_fc.iloc[julian-1,4] - DNC_fc.iloc[julian-1,3])
            elif DNC_for > 2200:
                DNC_fctarget = DNC_fc.iloc[julian-1,4]
    
            #DNC_ORC = np.zeros((365,1)) #this may need to be 365,1
            if julian>=213 and julian <=365:
               DNC_ORC[julian-1]= max(DNC_CRC[julian-1,1],DNC_ARC[julian-1,1])
               DNC_ORC[julian-1]= min(DNC_ORC[julian-1],DNC_fctarget)
            elif julian >=1 and julian <= 212:
                DNC_ORC[julian-1]= min(DNC_VRC,max(DNC_CRC[julian-1,1],DNC_ARC[julian-1,1]))
                DNC_ORC[julian-1]= min(DNC_ORC[julian-1],DNC_fctarget)
            else:
               DNC_ORC[julian-1]=DNC_fctarget
    
    
            #Calculate daily reservoir discharge and end-of-day storage. Have to
            #convert project inflows ("local") to kAF.
            DNC_dg = max(0, s_4 + local.iloc[i,3]*.001987 - DNC_ORC[julian-1])
            s_4 = s_4 + local.iloc[i,3]*.001987 - DNC_dg
            discharge[i,3] = DNC_dg*(1/.001987)  #Convert back to cfs
            storage[i,3] = s_4
    
        else:
        #Refill mode - this is when the reservoir fills back up during spring
        #floods. Only storage target is maximum reservoir storage (spillway
        #threshold).
    
            DNC_dg = max(0, s_4 + local.iloc[i,3]*.001987 - s_max[3])
            s_4 = s_4 + local.iloc[i,3]*.001987 - DNC_dg
            discharge[i,3] = DNC_dg*(1/.001987)
            storage[i,3] = s_4
    
    
    
    
        ######################################################
        #Libby - storage reservor with flood control rule curve
        ######################################################
    
        #Are we in evacuation or refill?
        #If ICF exists, then fill start date is ICF - 20.
        if fillstart_LIB>0:
            evac = julian<fillstart_LIB or julian>244
        #Otherwise just use schedule.
        else:
            evac = julian<120 or julian>244  #I changed this from 180 to 120 and 273 to 304
    
    
         #Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182
    
            # Calculate "forecasted" inflows to Libby (April - August)
        if spring == True:
             LIB_for = local.iloc[(year-2)*365+212:(year-2)*365+365,2].sum()
             if fillstart_LIB>0:
                 ICF_D=TDA_unreg[(year-2)*365 + fillstart_LIB[0] + 131]/1000 # this is cfs
             else:
                 ICF_D=TDA_unreg[(year-2)*365 + 110 + 131]/1000
    
               #below is used to check which curve needs to be applied
             TDA_for_LIB_B= TDA_unreg[(year-2)*365+212:(year-2)*365+365].sum()
        else:
             LIB_for = local.iloc[(year-1)*365+212:(year-1)*365+365,2].sum()
             if fillstart_LIB>0:
                 ICF_D=TDA_unreg[(year-1)*365 + fillstart_LIB[0] + 131]/1000 # this is cfs
             else:
                 ICF_D=TDA_unreg[(year-1)*365 + 110 + 131]/1000
               #ICF_D=TDA_unreg((year-1)*365+120)/1000
    
             TDA_for_LIB_B =TDA_unreg[(year-1)*365+212:(year-1)*365+365].sum()
    
            #Convert forecast to kAF
        LIB_for = LIB_for*.001987
    
           #Calculate PDR Can use Duncan's value
        if TDA_for_DNC <= 80:
             TDA_for_DNC = 80
        elif TDA_for_DNC >= 110:
             TDA_for_DNC =110
    
    
         #from Jan 1 to May 30 the value is all 4000 cfs
        if julian>=1 and julian <= 151:
              VPDR_LIB=4000
        elif julian >151 and julian <=181:
              VPDR_LIB = 9000
              #Above is liner extrapolation from data
        elif julian >181 and julian <=212:
              VPDR_LIB=10000
        else:
              VPDR_LIB=0
    
        #LIB_sfore = np.zeros((sim_days,1))
         #Calculate VRC
         #inflow is just local.iloc[i,3) out flow is VPDR or APDR
        if i==0:
         #DNC's storage forecaste
             LIB_sfore[i]=min((local.iloc[i,2]-VPDR_LIB)*.001987+s_3,s_max[2])
        else:
              LIB_sfore[i]=min((local.iloc[i,2]-VPDR_LIB)*.001987+ storage[i-1,2],s_max[2])
    
        LIB_VRC= LIB_sfore[i] #this is in kAF
         #Identify target reservoir storage. A number of flood control curves
            #are publically available. They are based on forecasted inflows. Some interpolation is
            #necessary when the forecasted flows are in-between those specifiec by
            #USACE.
    
        if LIB_for <= 4500:
             LIB_fctarget = LIB_fc.iloc[julian-1,0]
        elif LIB_for > 4500 and LIB_for <= 5500:
                LIB_fctarget = LIB_fc.iloc[julian-1,0] + ((LIB_for - 4500)/(5500-4500))*(LIB_fc.iloc[julian-1,1] - LIB_fc.iloc[julian-1,0])
        elif LIB_for > 5500 and LIB_for <= 6500:
                LIB_fctarget = LIB_fc.iloc[julian-1,1] + ((LIB_for - 5500)/(6500-5500))*(LIB_fc.iloc[julian-1,2] - LIB_fc.iloc[julian-1,1])
        elif LIB_for > 6500 and LIB_for <= 7500:
                LIB_fctarget = LIB_fc.iloc[julian-1,2] + ((LIB_for - 6500)/(7500-6500))*(LIB_fc.iloc[julian-1,3] - LIB_fc.iloc[julian-1,2])
        elif LIB_for > 7500 and LIB_for <= 8000:
                LIB_fctarget = LIB_fc.iloc[julian-1,3] + ((LIB_for - 7500)/(8000-7500))*(LIB_fc.iloc[julian-1,4] - LIB_fc.iloc[julian-1,3])
        elif LIB_for > 8000:
                LIB_fctarget = LIB_fc.iloc[julian-1,4]
    
        #LIB_ORC = np.zeros((365,1))
        if julian>=213 and julian <=365:
             LIB_ORC[julian-1]= max(LIB_CRC[julian-1,1],LIB_ARC[julian-1,1])
             LIB_ORC[julian-1]= min(LIB_ORC[julian-1],LIB_fctarget)
        elif julian >=1 and julian <= 212:
             LIB_ORC[julian-1]= min(LIB_VRC,max(LIB_CRC[julian-1,1],LIB_ARC[julian-1,1]))
             LIB_ORC[julian-1]= min(LIB_ORC[julian-1],LIB_fctarget)
        else:
             LIB_ORC[julian-1]=LIB_fctarget
    
    
    
        LIB_ORC[julian-1]=max(0,LIB_ORC[julian-1])
    
    
        TDA_for_LIB_B = TDA_for_LIB_B * .001987  #in kAF
    
         #Calculate initial controlled flow at Dalls
        if ICF_D<350:
             ICF_D=350
    
         #Calculate Libby flood control duration
        if ICF_D>=350 and ICF_D<400:  #Use curve 1
             TDA_for_LIB_B =max(TDA_for_LIB_B,70000)
             if TDA_for_LIB_B >= 70000 and TDA_for_LIB_B<= 100000:
                 FCD_LIB=0.00233333*(TDA_for_LIB_B-70000)
             elif TDA_for_LIB_B > 100000 and TDA_for_LIB_B <=110000:
                 FCD_LIB = 70+ (0.001*(TDA_for_LIB_B-100000))
             elif TDA_for_LIB_B > 110000 and TDA_for_LIB_B <=140000:
                 FCD_LIB = 80+ (0.005*(TDA_for_LIB_B-110000))
             elif TDA_for_LIB_B > 140000 and TDA_for_LIB_B <=200000:
                 FCD_LIB = 95+ (0.0025*(TDA_for_LIB_B-110000))
    
        elif ICF_D>=400 and ICF_D<450: #Use curve 2
              if TDA_for_LIB_B>= 80000 and TDA_for_LIB_B<= 100000:
                  FCD_LIB=0.003*(TDA_for_LIB_B-80000)
              elif TDA_for_LIB_B >100000 and TDA_for_LIB_B <=145000:
                  FCD_LIB = 60 + (0.00556*(TDA_for_LIB_B-100000))
              elif TDA_for_LIB_B >145000 and TDA_for_LIB_B <=200000:
                  FCD_LIB = 85+ (0.001818*(TDA_for_LIB_B-145000))
                  #FCD is flood control duration
        elif ICF_D >=450: #Use curve 3
              if TDA_for_LIB_B>= 80000 and TDA_for_LIB_B <= 100000:
                  FCD_LIB=0.0025*(TDA_for_LIB_B-80000)
              elif TDA_for_LIB_B >100000 and TDA_for_LIB_B <=150000:
                  FCD_LIB = 50 + (0.0005*(TDA_for_LIB_B-100000))
              elif TDA_for_LIB_B >150000 and TDA_for_LIB_B <=200000:
                  FCD_LIB = 75+ (0.0002*(TDA_for_LIB_B-150000))
    
         # KAF
        if LIB_for >= 5600 and LIB_for <= 7500:
              LIB_FL = (25000- (10.52*(LIB_for-5600)))
        elif LIB_for >= 8600:
              LIB_FL= (5000+ (10*(LIB_for-8600)))
        elif LIB_for>7500 and LIB_for <8600:
              LIB_FL=5000
        else:
              LIB_FL=0
    
    #    FCDend_LIB = np.zeros((years,1))
        if fillstart_LIB>0:
              Dur_LIB=FCD_LIB
              FCDend_LIB[year-1]=fillstart_LIB+Dur_LIB
        else:
              Dur_LIB=FCD_LIB
              FCDend_LIB[year-1]=120+Dur_LIB
    
    
    
    
    
    
    
        if evac == True:
        #Evacuation mode
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF. Note: Libby Dam has a
        #minimum flow value of 4000cfs-d.
        #Flow target
    
            LIB_dg = max(4000*.001987, s_3 + local.iloc[i,2]*.001987 - LIB_ORC[julian-1])
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,LIB_dg - f_max[2])
    
            #Is any storage space available?
            stor_avail = LIB_ORC[julian-1] - s_3
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,2] = f_max[2]
                spill[i,2] = LIB_dg - f_max[2]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                LIB_dg = max(LIB_dg - stor_avail,f_max[2])
                powerflow[i,2] = f_max[2]
                spill[i,2] = max(0,LIB_dg - f_max[2])
            else:
                powerflow[i,2] = LIB_dg
    
    
            s_3 = max(0,s_3 + local.iloc[i,2]*.001987 - LIB_dg)
            discharge[i,2] = LIB_dg*(1/.001987)  #Convert back to cfs
            storage[i,2] = s_3
    
        else:
        #Refill mode - this is when the reservoir fills back up during spring
        #floods. Only storage target is maximum reservoir storage (spillway
        #threshold).
             #Alright lets cheat
                      #GOD VIEW!!!!!
                      #What is coming?
    #        VARQ_LIB = np.zeros((sim_days,1))
    #        VARQnew_LIB = np.zeros((sim_days,1))
            if year >1:
                VAQR_LIB[i]= LIB_FL
                LIB_dg = max(max(4000*.001987, VAQR_LIB[i]*.001987),s_3 + local.iloc[i,2]*.001987 - LIB_ORC[julian-1]+ VAQR_LIB[i]*.001987*1.5)
            else:
                LIB_dg = max(4000*.001987,s_3 + local.iloc[i,2]*.001987 - LIB_ORC[julian-1])
    
            VAQR_LIB[i]= LIB_FL
            VAQRnew_LIB[i]=VAQR_LIB[i]  #+ ADJ_LIB(year)
    
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,LIB_dg - f_max[2])
    
            #Is any storage space available?
            stor_avail = LIB_ORC[julian-1] - s_3
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,2] = f_max[2]
                spill[i,2] = LIB_dg - f_max[2]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                LIB_dg = max(LIB_dg - stor_avail,f_max[2])
                powerflow[i,2] = f_max[2]
                spill[i,2] = max(0,LIB_dg - f_max[2])
            else:
                powerflow[i,2] = LIB_dg
    
    
            s_3 = max(0,s_3 + local.iloc[i,2]*.001987 - LIB_dg)
            discharge[i,2] = LIB_dg*(1/.001987)
            storage[i,2] = s_3
    
    
    
        #Convert storage to AF
        LIB_stor = s_3*1000
        #LIB_dg = max(0,LIB_dg)
        #What is forebay elevation?
        LIB_forebay = StorEq.iloc[2,1]*LIB_stor**4 + StorEq.iloc[2,2]*LIB_stor**3 + StorEq.iloc[2,3]*LIB_stor**2 + StorEq.iloc[2,4]*LIB_stor + StorEq.iloc[2,5]
        #What is tailwater elevation?
        LIB_tailwater = TailEq.iloc[2,1]*discharge[i,2]**4 + TailEq.iloc[2,2]*discharge[i,2]**3 + TailEq.iloc[2,3]*discharge[i,2]**2 + TailEq.iloc[2,4]*discharge[i,2] + TailEq.iloc[2,5]
        #Convert head to meters.
        #LIB_head = np.zeros((sim_days,1))
        LIB_head[i] = (LIB_forebay - LIB_tailwater)*.3048
        generation[i,2] = max(0,((1000*LIB_head[i]*powerflow[i,2]*14.27641*9.81*.865)/1000000)*24)
    
        ######################################
        #Bonner's Ferry - run-of-river project
        ######################################
    
        BFE_dg = max(0,LIB_dg + local.iloc[i,46]*.001987)
        powerflow[i,46] = min(BFE_dg,f_max[46])
        spill[i,46] = max(0,BFE_dg - f_max[46])
        s_47 = s_47 + LIB_dg + local.iloc[i,46]*.001987 - BFE_dg
        discharge[i,46] = BFE_dg*(1/.001987)
        storage[i,46] = s_47
        generation[i,46] = ((1000*28.0416*powerflow[i,46]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Corra Linn - run-of-river project
        ######################################
    
        CLN_dg = max(0,BFE_dg + DNC_dg + local.iloc[i,4]*.001987)
        powerflow[i,4] = min(CLN_dg,f_max[4])
        spill[i,4] = max(0,CLN_dg - f_max[4])
        s_5 = s_5 + BFE_dg + DNC_dg + local.iloc[i,4]*.001987 - CLN_dg
        discharge[i,4] = CLN_dg*(1/.001987)
        storage[i,4] = s_5
        generation[i,4] = ((1000*16.1544*powerflow[i,4]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Brilliant - run-of-river project
        ######################################
    
        BRI_dg = max(0,CLN_dg + local.iloc[i,17]*.001987)
        powerflow[i,17] = min(BRI_dg,f_max[17])
        spill[i,17] = max(0,BRI_dg - f_max[17])
        s_18 = s_18 + CLN_dg + local.iloc[i,17]*.001987 - BRI_dg
        discharge[i,17] = BRI_dg*(1/.001987)
        storage[i,17] = s_18
        generation[i,17] = ((1000*28.0416*powerflow[i,17]*14.27641*9.81*.875)/1000000)*24
    
        ###################
        #FLATHEAD PROJECTS#
        #Hungry Horse, Kerr, Thompson Falls, Noxon, Cabinet Gorge, Priest Lake,
        #Albeni Falls, Box Canyon, Boundary, Seven Mile, Waneta
    
        ######################################################
        #Hungry Horse - storage reservoir with flood control rule curve
        ######################################################
    
        #Are we in evacuation or refill?
        #If ICF exists, then fill start date is ICF - 20.
        if fillstart>0:
            evac = julian<fillstart or julian>243
        #Otherwise just use schedule.
        else:
            evac = julian<120 or julian>304
    
    #I changed this from 180 to 120 and 273 to 304
    
         #Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182
    
        #Calculate "forecasted" inflows to Hungry Horse (May - August)
        if spring == True:
            HHO_for = local.iloc[(year-2)*365+242:(year-2)*365+365,5].sum()
        else:
            HHO_for = local.iloc[(year-1)*365+242:(year-1)*365+365,5].sum()
        #Convert forecast to kAF
        HHO_for = HHO_for*.001987
    
        if julian>=1 and julian <= 151:
              VPDR_HHO=400
        elif julian >151 and julian <=181:
              VPDR_HHO = 2000
              #Above is liner extrapolation from data
        elif julian >181 and julian <=212:
              VPDR_HHO=2300
        else:
              VPDR_HHO=0
    
        #Identify target reservoir storage. A number of flood control curves
        #are publically available. They are based on forecasted inflows. Some interpolation is
        #necessary when the forecasted flows are in-between those specifiec by
        #USACE.
    
        #Calculate VRC
        #inflow is just local.iloc[i,6) out flow is VPDR or APDR
        #HHO_sfore = np.zeros((sim_days,1))
        if i==0:
            #DNC's storage forecaste
            HHO_sfore[i]=min((local.iloc[i,5]-VPDR_HHO)*.001987+s_6,s_max[5])
        else:
            HHO_sfore[i]=min((local.iloc[i,5]-VPDR_HHO)*.001987+ storage[i-1,5],s_max[5])
    
        HHO_VRC= HHO_sfore[i] #this is in kAF
    
        if HHO_for <= 1000:
            HHO_fctarget = HHO_fc.iloc[julian-1,0]
        elif HHO_for > 1000 and HHO_for <= 1400:
            HHO_fctarget = HHO_fc.iloc[julian-1,0] + ((HHO_for - 1000)/(1400-1000))*(HHO_fc.iloc[julian-1,1] - HHO_fc.iloc[julian-1,0])
        elif HHO_for > 1400 and HHO_for <= 1600:
            HHO_fctarget = HHO_fc.iloc[julian-1,1] + ((HHO_for - 1400)/(1600-1400))*(HHO_fc.iloc[julian-1,2] - HHO_fc.iloc[julian-1,1])
        elif HHO_for > 1600 and HHO_for <= 2000:
            HHO_fctarget = HHO_fc.iloc[julian-1,2] + ((HHO_for - 1600)/(2000-1600))*(HHO_fc.iloc[julian-1,3] - HHO_fc.iloc[julian-1,2])
        elif HHO_for > 2000 and HHO_for <= 2200:
            HHO_fctarget = HHO_fc.iloc[julian-1,3] + ((HHO_for - 2000)/(2200-2000))*(HHO_fc.iloc[julian-1,4] - HHO_fc.iloc[julian-1,3])
        elif HHO_for > 2200 and HHO_for <= 2500:
            HHO_fctarget = HHO_fc.iloc[julian-1,4] + ((HHO_for - 2200)/(2500-2200))*(HHO_fc.iloc[julian-1,5] - HHO_fc.iloc[julian-1,4])
        elif HHO_for > 2500 and HHO_for <= 2800:
            HHO_fctarget = HHO_fc.iloc[julian-1,5] + ((HHO_for - 2500)/(2800-2500))*(HHO_fc.iloc[julian-1,6] - HHO_fc.iloc[julian-1,5])
        elif HHO_for > 2800 and HHO_for <= 3680:
            HHO_fctarget = HHO_fc.iloc[julian-1,6] + ((HHO_for - 2800)/(3680-2800))*(HHO_fc.iloc[julian-1,7] - HHO_fc.iloc[julian-1,6])
        else:
            HHO_fctarget = HHO_fc.iloc[julian-1,7]
    
        #HHO_ORC = np.zeros((365,1))
        if julian>=213 and julian <=365:
            HHO_ORC[julian-1]= max(HHO_CRC[julian-1,1],HHO_ARC[julian-1,1])
            HHO_ORC[julian-1]= min(HHO_ORC[julian-1],HHO_fctarget)
        elif julian >=1 and julian <= 212:
            HHO_ORC[julian-1]= min(HHO_VRC,max(HHO_CRC[julian-1,1],HHO_ARC[julian-1,1]))
            HHO_ORC[julian-1]= min(HHO_ORC[julian-1],LIB_fctarget)
        else:
            HHO_ORC[julian-1]=HHO_fctarget
    
    ############################################################################
            #This section is the same as LIB's this repilication is to make
            #sure that nothing goes wrong
    
        if ICF_D<350:
             ICF_D=350
    
         #Calculate Libby flood control duration
        if ICF_D>=350 and ICF_D<400:  #Use curve 1
             TDA_for_LIB_B =max(TDA_for_LIB_B,70000)
             if TDA_for_LIB_B >= 70000 and TDA_for_LIB_B<= 100000:
                 FCD_LIB=0.00233333*(TDA_for_LIB_B-70000)
             elif TDA_for_LIB_B > 100000 and TDA_for_LIB_B <=110000:
                 FCD_LIB = 70+ (0.001*(TDA_for_LIB_B-100000))
             elif TDA_for_LIB_B > 110000 and TDA_for_LIB_B <=140000:
                 FCD_LIB = 80+ (0.005*(TDA_for_LIB_B-110000))
             elif TDA_for_LIB_B > 140000 and TDA_for_LIB_B <=200000:
                 FCD_LIB = 95+ (0.0025*(TDA_for_LIB_B-110000))
    
        elif ICF_D>=400 and ICF_D<450: #Use curve 2
              if TDA_for_LIB_B>= 80000 and TDA_for_LIB_B<= 100000:
                  FCD_LIB=0.003*(TDA_for_LIB_B-80000)
              elif TDA_for_LIB_B >100000 and TDA_for_LIB_B <=145000:
                  FCD_LIB = 60 + (0.00556*(TDA_for_LIB_B-100000))
              elif TDA_for_LIB_B >145000 and TDA_for_LIB_B <=200000:
                  FCD_LIB = 85+ (0.001818*(TDA_for_LIB_B-145000))
                  #FCD is flood control duration
        elif ICF_D >=450: #Use curve 3
              if TDA_for_LIB_B>= 80000 and TDA_for_LIB_B <= 100000:
                  FCD_LIB=0.0025*(TDA_for_LIB_B-80000)
              elif TDA_for_LIB_B >100000 and TDA_for_LIB_B <=150000:
                  FCD_LIB = 50 + (0.0005*(TDA_for_LIB_B-100000))
              elif TDA_for_LIB_B >150000 and TDA_for_LIB_B <=200000:
                  FCD_LIB = 75+ (0.0002*(TDA_for_LIB_B-150000))
      ########################################################################
    
        if  HHO_for >= 3000:
              HHO_FL=0
        elif HHO_for>1000 and LIB_for <3000:
              HHO_FL=12000- (6*(HHO_for-1000))
        else:
              HHO_FL=0
    
    
        if fillstart>0:
              Dur_LIB=FCD_LIB
              FCDend_LIB[year-1]=fillstart+Dur_LIB
        else:
               Dur_LIB=FCD_LIB
               FCDend_LIB[year-1]=120+Dur_LIB
    
    
    
        if evac == True:
        #Evacuation mode
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF. Note: there is a minimum flow release of 3500cfs associated with this dam.
            HHO_dg = max(max(0,3500-local.iloc[i,6])*.001987, s_6 + local.iloc[i,5]*.001987 - HHO_ORC[julian-1])
            #If reservoir storage is low
            if HHO_dg>s_6 + local.iloc[i,5]*.001987:
                HHO_dg=s_6 + local.iloc[i,5]*.001987
    
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,HHO_dg - f_max[5])
    
            #Is any storage space available?
            stor_avail = HHO_ORC[julian-1] - s_6
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,5] = f_max[5]
                spill[i,5] = HHO_dg - f_max[5]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                HHO_dg = max(HHO_dg - stor_avail,f_max[5])
                powerflow[i,5] = f_max[5]
                spill[i,5] = max(0,HHO_dg - f_max[5])
            else:
                powerflow[i,5] = HHO_dg
    
    
            s_6 = s_6 + local.iloc[i,5]*.001987 - HHO_dg
            discharge[i,5] = HHO_dg*(1/.001987)  #Convert back to cfs
            storage[i,5] = s_6
    
        else:
        #Refill mode - this is when the reservoir fills back up during spring
        #floods. Only storage target is maximum reservoir storage (spillway
        #threshold).
    #        VAQR_HHO = np.zeros((sim_days,1))
    #        VAQRnew_HHO = np.zeros((sim_days,1))
            if year >1:
                VAQR_HHO[i]= HHO_FL
                VAQRnew_HHO[i]=VAQR_HHO[i]  #+ ADJ_LIB(year)
                HHO_dg = max(max(0,3500-local.iloc[i,6])*.001987, s_6 + local.iloc[i,5]*.001987 - HHO_ORC[julian-1]+ VAQR_HHO[i]*.001987*1.5)
            else:
                HHO_dg = max(max(0,3500-local.iloc[i,6])*.001987, s_6 + local.iloc[i,5]*.001987 - HHO_ORC[julian-1])
    
            #If reservoir storage is low
            if HHO_dg>s_6 + local.iloc[i,5]*.001987:
               HHO_dg=s_6 + local.iloc[i,5]*.001987
    
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,HHO_dg - f_max[5])
    
            #Is any storage space available?
            stor_avail = HHO_ORC[julian-1] - s_6
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,5] = f_max[5]
                spill[i,5] = HHO_dg - f_max[5]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                HHO_dg = max(HHO_dg - stor_avail,f_max[5])
                powerflow[i,5] = f_max[5]
                spill[i,5] = max(0,HHO_dg - f_max[5])
            else:
                powerflow[i,5] = HHO_dg
    
    
            s_6 = s_6 + local.iloc[i,5]*.001987 - HHO_dg
            discharge[i,5] = HHO_dg*(1/.001987)
            storage[i,5] = s_6
    
    
    
        #Convert storage to AF
        HHO_stor = s_6*1000
        #What is forebay elevation?
        HHO_forebay = StorEq.iloc[5,1]*HHO_stor**4 + StorEq.iloc[5,2]*HHO_stor**3 + StorEq.iloc[5,3]*HHO_stor**2 + StorEq.iloc[5,4]*HHO_stor + StorEq.iloc[5,5]
        #What is tailwater elevation?
        HHO_tailwater = TailEq.iloc[5,1]*discharge[i,5]**4 + TailEq.iloc[5,2]*discharge[i,5]**3 + TailEq.iloc[5,3]*discharge[i,5]**2 + TailEq.iloc[5,4]*discharge[i,5] + TailEq.iloc[5,5]
        #Convert head to meters.
        #HHO_head = np.zeros((sim_days,1))
        HHO_head[i] = (HHO_forebay - HHO_tailwater)*.3048
        generation[i,5] = max(0,((1000*HHO_head[i]* powerflow[i,5] *14.27641*9.81*.84)/1000000)*24)
    
        ######################################
        #Kerr - run-of-river project
        ######################################
        #Note: There is a 1-day travel delay between Hungry Horse and Kerr.
        if i > 0:
            KER_dg = max(0,discharge[i-1,5]*.001987 + + CFM5L.iloc[i]*.001987+ local.iloc[i,6]*.001987)
            s_7 = s_7 + discharge[i-1,5]*.001987 + local.iloc[i,6]*.001987 + CFM5L.iloc[i]*.001987 - KER_dg
        else:
            KER_dg = max(0,HHO_dg + local.iloc[i,6]*.001987+ CFM5L.iloc[i]*.001987)
            s_7 = s_7 + HHO_dg + local.iloc[i,6]*.001987 + CFM5L.iloc[i]*.001987 - KER_dg
    
        powerflow[i,6] = min(KER_dg,f_max[6])
        spill[i,6] = max(0,KER_dg - f_max[6])
        discharge[i,6] = KER_dg*(1/.001987)
        storage[i,6] = s_7
        #Convert storage to AF
        KER_stor = s_7*1000
        smax = s_max[6]*1000
        #What is forebay elevation?
        KER_forebay = StorEq.iloc[6,1]*KER_stor**4 + StorEq.iloc[6,2]*KER_stor**3 + StorEq.iloc[6,3]*KER_stor**2 + StorEq.iloc[6,4]*KER_stor + StorEq.iloc[6,5]
        #What is tailwater elevation?
        KER_tailwater = (StorEq.iloc[6,1]*smax**4 + StorEq.iloc[6,2]*smax**3 + StorEq.iloc[6,3]*smax**2 + StorEq.iloc[6,4]*smax + StorEq.iloc[6,5]) - 206
        #Convert head to meters.
        KER_head = (KER_forebay - KER_tailwater)*.3048
        generation[i,6] = ((1000*62.7888*powerflow[i,6]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Thompson Falls - run-of-river project
        ######################################
    
        THF_dg = max(0,KER_dg + local.iloc[i,18]*.001987)
        s_19 = s_19 + KER_dg + local.iloc[i,18]*.001987 - THF_dg
        powerflow[i,18] = min(THF_dg,f_max[18])
        spill[i,18] = max(0,THF_dg - f_max[18])
        discharge[i,18] = THF_dg*(1/.001987)
        storage[i,18] = s_19
        generation[i,18] = ((1000*19.5072*powerflow[i,18]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Noxon - run-of-river project
        ######################################
        #Note: There is a 1-day travel delay between Thompson Falls and Noxon.
    
        if i > 0:
            NOX_dg = max(0,discharge[i-1,18]*.001987 + local.iloc[i,13]*.001987)
            s_14 = s_14 + discharge[i-1,18]*.001987 + local.iloc[i,13]*.001987 - NOX_dg
        else:
            NOX_dg = max(0,THF_dg + local.iloc[i,13]*.001987)
            s_14 = s_14 + THF_dg + local.iloc[i,13]*.001987 - NOX_dg
    
        powerflow[i,13] = min(NOX_dg,f_max[13])
        spill[i,13] = max(0,NOX_dg - f_max[13])
        discharge[i,13] = NOX_dg*(1/.001987)
        storage[i,13] = s_14
        #Convert storage to AF
        NOX_stor = s_14*1000
        smax = s_max[13]*1000
        #What is forebay elevation?
        NOX_forebay = StorEq.iloc[13,1]*NOX_stor**4 + StorEq.iloc[13,2]*NOX_stor**3 + StorEq.iloc[13,3]*NOX_stor**2 + StorEq.iloc[13,4]*NOX_stor + StorEq.iloc[13,5]
        #What is tailwater elevation?
        NOX_tailwater = (StorEq.iloc[13,1]*smax**4 + StorEq.iloc[13,2]*smax**3 + StorEq.iloc[13,3]*smax**2 + StorEq.iloc[13,4]*smax + StorEq.iloc[13,5]) - 179
        #Convert head to meters.
        NOX_head = (NOX_forebay - NOX_tailwater)*.3048
        generation[i,13] = ((1000*54.5592*powerflow[i,13]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Cabinet Gorge - run-of-river project
        ######################################
    
        CBG_dg = max(0,NOX_dg + local.iloc[i,19]*.001987)
        s_19 = s_19 + NOX_dg + local.iloc[i,19]*.001987 - CBG_dg
        powerflow[i,19] = min(CBG_dg,f_max[19])
        spill[i,19] = max(0,CBG_dg - f_max[19])
        discharge[i,19] = CBG_dg*(1/.001987)
        storage[i,19] = s_19
        generation[i,19] = ((1000*33.8328*powerflow[i,19]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Priest Lake - run-of-river project
        ######################################
    
        PSL_dg = max(0,local.iloc[i,45]*.001987)
        s_45 = s_45 + local.iloc[i,45]*.001987 - PSL_dg
        powerflow[i,45] = min(PSL_dg,f_max[45])
        spill[i,45] = max(0,PSL_dg - f_max[45])
        discharge[i,45] = PSL_dg*(1/.001987)
        storage[i,45] = s_45
        generation[i,45] = ((1000*84.1428*powerflow[i,45]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Albeni Falls - storage project
        ######################################
    
        #Note. This project has upper and lower rule curves and minimum flows.
        ALB_upper = ALB_fc.iloc[julian-1,0]
        ALB_lower = ALB_fc.iloc[julian-1,1]
    
    #         #If reservoir storage is near lower curve
    #         if s_8 - ALB_dg < ALB_lower
    #           ALB_dg = 0
    #         end
    #    ALB_sfore = np.zeros((sim_days,1))
        if i==0:
        #DNC's storage forecaste
            ALB_sfore[i]=min((local.iloc[i,7]-4000)*.001987+ PSL_dg + CBG_dg+s_8,s_max[7])
        else:
            ALB_sfore[i]=min((local.iloc[i,7]-4000)*.001987+ PSL_dg + CBG_dg+ storage[i-1,7],s_max[7])
    
        ALB_VRC= ALB_sfore[i]
        #ALB_ORC = np.zeros((365,1))
        if julian>=213 and julian <=365:
            ALB_ORC[julian-1]= max(ALB_CRC[julian-1,1],ALB_ARC[julian-1,1])
            ALB_ORC[julian-1]= min(ALB_ORC[julian-1],ALB_upper)
            ALB_ORC[julian-1]= max(ALB_ORC[julian-1],ALB_lower)
        elif julian >=1 and julian <= 212:
            ALB_ORC[julian-1]= min(ALB_VRC,max(ALB_CRC[julian-1,1],ALB_ARC[julian-1,1]))
            ALB_ORC[julian-1]= min(ALB_ORC[julian-1],ALB_upper)
            ALB_ORC[julian-1]= max(ALB_ORC[julian-1],ALB_lower)
    
    
        ALB_dg = max(4000*.001987, s_8 + local.iloc[i,7]*.001987 + PSL_dg + CBG_dg - ALB_ORC[julian-1])
            #Do flows exceed hydraulic capacity of dam?
        overflow = max(0,ALB_dg - f_max[7])
    
            #Is any storage space available?
        stor_avail = ALB_upper - s_8
    
        #If flows exceed dam's hydraulic capacity.
        if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
            powerflow[i,7] = f_max[7]
            spill[i,7] = ALB_dg - f_max[7]
        elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
            ALB_dg = max(ALB_dg - stor_avail,f_max[7])
            powerflow[i,7] = f_max[7]
            spill[i,7] = max(0,ALB_dg - f_max[7])
        else:
            powerflow[i,7] = ALB_dg
    
    
        s_8 = s_8 + local.iloc[i,7]*.001987 + PSL_dg + CBG_dg - ALB_dg
        discharge[i,7] = ALB_dg*(1/.001987)
        storage[i,7] = s_8
    
        #Convert storage to AF
        ALB_stor = s_8*1000
        #What is forebay elevation?
        ALB_forebay = StorEq.iloc[7,1]*ALB_stor**4 + StorEq.iloc[7,2]*ALB_stor**3 + StorEq.iloc[7,3]*ALB_stor**2 + StorEq.iloc[7,4]*ALB_stor + StorEq.iloc[7,5]
        #What is tailwater elevation?
        ALB_tailwater = TailEq.iloc[7,1]*discharge[i,7]**4 + TailEq.iloc[7,2]*discharge[i,7]**3 + TailEq.iloc[7,3]*discharge[i,7]**2 + TailEq.iloc[7,4]*discharge[i,7] + TailEq.iloc[7,5]
        #Convert head to meters.
        ALB_head = (ALB_forebay - ALB_tailwater)*.3048
        generation[i,7] = max(0,((1000*ALB_head*powerflow[i,7]*14.27641*9.81*.71)/1000000)*24)
    
        ######################################
        #Box Canyon - run-of-river project
        ######################################
    
        BOX_dg = max(0,local.iloc[i,20]*.001987 + ALB_dg)
        s_21 = s_21 + local.iloc[i,20]*.001987 + ALB_dg - BOX_dg
        powerflow[i,20] = min(BOX_dg,f_max[20])
        spill[i,20] = max(0,BOX_dg - f_max[20])
        discharge[i,20] = BOX_dg*(1/.001987)
        storage[i,20] = s_21
        generation[i,20] = ((1000*14.0208*powerflow[i,20]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Boundary - run-of-river project
        ######################################
    
        BOU_dg = max(0,local.iloc[i,21]*.001987 + BOX_dg)
        s_22 = s_22 + local.iloc[i,21]*.001987  + BOX_dg - BOU_dg
        powerflow[i,21] = min(BOU_dg,f_max[21])
        spill[i,21] = max(0,BOU_dg - f_max[21])
        discharge[i,21] = BOU_dg*(1/.001987)
        storage[i,21] = s_22
        generation[i,21] = ((1000*103.632*powerflow[i,21]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Seven Mile - run-of-river project
        ######################################
    
        SVN_dg = max(0,local.iloc[i,16]*.001987 + BOU_dg)
        s_17 = s_17 + local.iloc[i,16]*.001987 + BOU_dg - SVN_dg
        powerflow[i,16] = min(SVN_dg,f_max[16])
        spill[i,16] = max(0,SVN_dg - f_max[16])
        discharge[i,16] = SVN_dg*(1/.001987)
        storage[i,16] = s_17
        generation[i,16] = ((1000*64.92*powerflow[i,16]*14.27641*9.81*.875)/1000000)*24
    
        ######################################
        #Waneta - run-of-river project
        ######################################
    
        WNT_dg = max(0,local.iloc[i,22]*.001987 + SVN_dg)
        s_23 = s_23 + local.iloc[i,22]*.001987 + SVN_dg - WNT_dg
        powerflow[i,22] = min(WNT_dg,f_max[22])
        spill[i,22] = max(0,WNT_dg - f_max[22])
        discharge[i,22] = WNT_dg*(1/.001987)
        storage[i,22] = s_23
        generation[i,22] = ((1000*23.1648*powerflow[i,22]*14.27641*9.81*.875)/1000000)*24
    
        #########################
        #MID COLUMBIA PROJECTS#
        #Grand Coulee, Chief Joseph, Wells, Chelan, Rocky Reach, Rock Island,
        #Wanapum, Priest Rapids
    
        #########################
        #Grand Coulee - storage project
        #########################
    
        #Are we in evacuation or refill?
        #If ICF exists, then fill start date is ICF - 20.
        if fillstart>0:
            evac = julian<fillstart or julian>334
        #Otherwise just use schedule.
        else:
            evac = julian<182 or julian>334
    
    
        if TDA_for <= 57000:
                GCL_fctarget = GCL_fc.iloc[julian-1,0]
        elif TDA_for > 57000 and TDA_for <= 60000:
                GCL_fctarget = GCL_fc.iloc[julian-1,0] + ((TDA_for - 57000)/(60000-57000))*(GCL_fc.iloc[julian-1,1] - GCL_fc.iloc[julian-1,0])
        elif TDA_for > 60000 and TDA_for <= 63250:
                GCL_fctarget = GCL_fc.iloc[julian-1,1] + ((TDA_for - 60000)/(63250-60000))*(GCL_fc.iloc[julian-1,2] - GCL_fc.iloc[julian-1,1])
        elif TDA_for > 63250 and TDA_for <= 65000:
                GCL_fctarget = GCL_fc.iloc[julian-1,2] + ((TDA_for - 63250)/(65000-63250))*(GCL_fc.iloc[julian-1,3] - GCL_fc.iloc[julian-1,2])
        elif TDA_for > 65000 and TDA_for <= 67660:
                GCL_fctarget = GCL_fc.iloc[julian-1,3] + ((TDA_for - 65000)/(67660-65000))*(GCL_fc.iloc[julian-1,4] - GCL_fc.iloc[julian-1,3])
        elif TDA_for > 67660 and TDA_for <= 71000:
                GCL_fctarget = GCL_fc.iloc[julian-1,4] + ((TDA_for - 67660)/(71000-67660))*(GCL_fc.iloc[julian-1,5] - GCL_fc.iloc[julian-1,4])
        elif TDA_for > 71000 and TDA_for <= 75000:
                GCL_fctarget = GCL_fc.iloc[julian-1,5] + ((TDA_for - 71000)/(75000-71000))*(GCL_fc.iloc[julian-1,6] - GCL_fc.iloc[julian-1,5])
        elif TDA_for > 75000 and TDA_for <= 87500:
                GCL_fctarget = GCL_fc.iloc[julian-1,6] + ((TDA_for - 75000)/(87500-75000))*(GCL_fc.iloc[julian-1,7] - GCL_fc.iloc[julian-1,6])
        elif TDA_for > 87500 and TDA_for <= 100000:
                GCL_fctarget = GCL_fc.iloc[julian-1,7] + ((TDA_for - 87500)/(100000-87500))*(GCL_fc.iloc[julian-1,8] - GCL_fc.iloc[julian-1,7])
        elif TDA_for > 100000:
                GCL_fctarget = GCL_fc.iloc[julian-1,8]
    
        VPDR_GCL=30000*.001987
        #GCL_sfore = np.zeros((sim_days,1))
        #GCL_VRC = np.zeros((365,1))
        if i==0:
              #DNC's storage forecaste
              GCL_sfore[i]=min(local.iloc[i,9]*.001987 + spokane_flow[i]*.001987 + discharge[i,1]*.001987 + discharge[i,17]*.001987 + discharge[i,22]*.001987+s_10 - VPDR_GCL,s_max[9])
        else:
              GCL_sfore[i]=min(local.iloc[i,9]*.001987 + spokane_flow[i-1]*.001987 + discharge[i-1,1]*.001987 + discharge[i-1,17]*.001987 + discharge[i-1,22]*.001987+ storage[i-1,9] - VPDR_GCL,s_max[9])
    
        GCL_VRC[julian-1]= GCL_sfore[i] #this is in kAF
    
    
        #set VRCLL for GCL
        if julian >=1 and julian <=31:
               GCL_VRCLL=1778.9*2.4466
        elif julian >=32 and julian<=59:
               GCL_VRCLL=1054.5*2.4466
        elif julian >=60 and julian <=90:
               GCL_VRCLL=418.7*2.4466
        elif julian >=91 and julian <=120:
               GCL_VRCLL=418.7*2.4466
        elif julian >=121 and julian <=151:
               GCL_VRCLL=843.7*2.4466
        elif julian >=152 and julian <=181:
               GCL_VRCLL=2411.3*2.4466
        elif julian >=182 and julian <=212:
               GCL_VRCLL=2614.3*2.4466
    
    
        if julian>=213 and julian <=365:
            GCL_ORC[julian-1]= max(GCL_CRC[julian-1,1],GCL_ARC[julian-1,1])
            GCL_ORC[julian-1]= min(GCL_ORC[julian-1],GCL_fctarget)
    
        elif julian >=1 and julian <= 212:
                GCL_ORC[julian-1]= min(GCL_VRC[julian-1],max(GCL_CRC[julian-1,1],GCL_ARC[julian-1,1]))
                GCL_ORC[julian-1]= min(GCL_ORC[julian-1],GCL_fctarget)
                GCL_ORC[julian-1]= max(GCL_ORC[julian-1],GCL_VRCLL)
        else:
               GCL_ORC[julian-1]=GCL_fctarget
    #    Storage_left = np.zeros((sim_days,1))
        Storage_left[i]=GCL_fctarget-GCL_ORC[julian-1]
    
        if evac == True:
        #Evacuation mode
    
            #Identify target reservoir storage. A number of flood control curves
            #are publically available. They are based on forecasted flows at The Dalles. Some interpolation is
            #necessary when the forecasted flows are in-between those specifiec by
            #USACE.
    
    
            #Calculate dail
            #Calculate daily reservoir discharge and end-of-day storage. Have to
            #convert project inflows ("local") to kAF. Note: there is a minimum flow release of 30000cfs associated with this dam.
            #There is also a 1-day travel delay between upstream sources and
            #Grand Coulee.
            if i>0:
                GCL_dg = max(30000*.001987, s_10 + local.iloc[i,9]*.001987 + spokane_flow[i-1]*.001987 + discharge[i-1,1]*.001987 + discharge[i-1,17]*.001987 + discharge[i-1,22]*.001987 -  GCL_ORC[julian-1])
    
            #Do flows exceed hydraulic capacity of dam?
                overflow = max(0,GCL_dg - f_max[9])
    
            #Is any storage space available?
                stor_avail = GCL_fctarget - s_10
    
            #If flows exceed dam's hydraulic capacity.
                if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                    powerflow[i,9] = f_max[9]
                    spill[i,9] = GCL_dg - f_max[9]
                elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                    GCL_dg = max(GCL_dg - stor_avail,f_max[9])
                    powerflow[i,9] = f_max[9]
                    spill[i,9] = max(0,GCL_dg - f_max[9])
                else:
                    powerflow[i,9] = GCL_dg
    
    
                s_10 = s_10 + local.iloc[i,9]*.001987 + spokane_flow[i-1]*.001987 + discharge[i-1,1]*.001987 + discharge[i-1,17]*.001987 + discharge[i-1,22]*.001987 - GCL_dg
    
            else:
    
                GCL_dg = max(30000*.001987, s_10 + local.iloc[i,9]*.001987 + spokane_flow[i]*.001987 + discharge[i,1]*.001987 + discharge[i,17]*.001987 + discharge[i,22]*.001987 -  GCL_ORC[julian-1])
    
            #Do flows exceed hydraulic capacity of dam?
                overflow = max(0,GCL_dg - f_max[9])
    
            #Is any storage space available?
                stor_avail = GCL_fctarget - s_10
    
            #If flows exceed dam's hydraulic capacity.
                if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                    powerflow[i,9] = f_max[9]
                    spill[i,9] = GCL_dg - f_max[9]
                elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                    GCL_dg = max(GCL_dg - stor_avail,f_max[9])
                    powerflow[i,9] = f_max[9]
                    spill[i,9] = max(0,GCL_dg - f_max[9])
                else:
                    powerflow[i,9] = GCL_dg
    
    
                s_10 = s_10 + local.iloc[i,9]*.001987 + spokane_flow[i]*.001987 + discharge[i,1]*.001987 + discharge[i,17]*.001987 + discharge[i,22]*.001987 - GCL_dg
    
    
            discharge[i,9] = GCL_dg*(1/.001987)  #Convert back to cfs
            storage[i,9] = s_10
    
    
        else:
        #Refill mode - this is when the reservoir fills back up during spring
        #floods. Only storage target is maximum reservoir storage (spillway
        #threshold).
    
            if i>0:
                GCL_dg = max(30000*.001987, s_10 + local.iloc[i,9]*.001987 + spokane_flow[i-1]*.001987 + discharge[i-1,1]*.001987 + discharge[i-1,17]*.001987 + discharge[i-1,22]*.001987 -  GCL_ORC[julian-1])
    
            #Do flows exceed hydraulic capacity of dam?
                overflow = max(0,GCL_dg - f_max[9])
    
            #Is any storage space available?
                stor_avail = s_max[9] - s_10
    
            #If flows exceed dam's hydraulic capacity.
                if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                    powerflow[i,9] = f_max[9]
                    spill[i,9] = GCL_dg - f_max[9]
                elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                    GCL_dg = max(GCL_dg - stor_avail,f_max[9])
                    powerflow[i,9] = f_max[9]
                    spill[i,9] = max(0,GCL_dg - f_max[9])
                else:
                    powerflow[i,9] = GCL_dg
    
    
                s_10 = s_10 + local.iloc[i,9]*.001987 + spokane_flow[i-1]*.001987 + discharge[i-1,1]*.001987 + discharge[i-1,17]*.001987 + discharge[i-1,22]*.001987 - GCL_dg
    
            else:
                GCL_dg = max(30000*.001987, s_10 + local.iloc[i,9]*.001987 + spokane_flow[i]*.001987 + discharge[i,1]*.001987 + discharge[i,17]*.001987 + discharge[i,22]*.001987 -  GCL_ORC[julian-1])
    
            #Do flows exceed hydraulic capacity of dam?
                overflow = max(0,GCL_dg - f_max[9])
    
            #Is any storage space available?
                stor_avail = s_max[9] - s_10
    
            #If flows exceed dam's hydraulic capacity.
                if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                    powerflow[i,9] = f_max[9]
                    spill[i,9] = GCL_dg - f_max[9]
                elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                    GCL_dg = max(GCL_dg - stor_avail,f_max[9])
                    powerflow[i,9] = f_max[9]
                    spill[i,9] = max(0,GCL_dg - f_max[9])
                else:
                    powerflow[i,9] = GCL_dg
    
    
    
                s_10 = s_10 + local.iloc[i,9]*.001987 + spokane_flow[i]*.001987 + discharge[i,1]*.001987 + discharge[i,17]*.001987 + discharge[i,22]*.001987 - GCL_dg
    
    
            discharge[i,9] = GCL_dg*(1/.001987)  #Convert back to cfs
            storage[i,9] = s_10
    
    
    
    
        #Convert storage to AF
        GCL_stor = s_10*1000
        #What is forebay elevation?
        GCL_forebay = StorEq.iloc[9,1]*GCL_stor**4 + StorEq.iloc[9,2]*GCL_stor**3 + StorEq.iloc[9,3]*GCL_stor**2 + StorEq.iloc[9,4]*GCL_stor + StorEq.iloc[9,5]
        #What is tailwater elevation?
        GCL_tailwater = TailEq.iloc[9,1]*discharge[i,9]**4 + TailEq.iloc[9,2]*discharge[i,9]**3 + TailEq.iloc[9,3]*discharge[i,9]**2 + TailEq.iloc[9,4]*discharge[i,9] + TailEq.iloc[9,5]
        #Convert head to meters.
        #GCL_head = np.zeros((sim_days,1))
        GCL_head[i] = (GCL_forebay - GCL_tailwater)*.3048
        generation[i,9] = ((1000*GCL_head[i]*powerflow[i,9]*14.27641*9.81*.9)/1000000)*24
        #heads = np.zeros((sim_days,10))
    #    Spillheads = np.zeros((sim_days,11))
        heads[i,0]=GCL_head[i]
        Spillheads[i,0]=GCL_head[i]
        #stor = np.zeros((sim_days,1))
        #inflow = stor = np.zeros((sim_days,1))
        stor[i]=GCL_stor
        if i>0:
            inflow[i,0]=(local.iloc[i,9]*.001987 + spokane_flow[i-1]*.001987 + discharge[i-1,1]*.001987 + discharge[i-1,17]*.001987 + discharge[i-1,22]*.001987)/0.001987
    
        #########################
        #Chief Joseph - run-of-river
        #########################
    
        CHJ_dg = max(0,local.iloc[i,28]*.001987 + GCL_dg)
        s_29 = s_29 + local.iloc[i,28]*.001987 + GCL_dg - CHJ_dg
        powerflow[i,28] = min(CHJ_dg,f_max[28])
        spill[i,28] = max(0,CHJ_dg - f_max[28])
        discharge[i,28] = CHJ_dg*(1/.001987)
        storage[i,28] = s_29
        #Convert storage to AF
        CHJ_stor = s_29*1000
        #What is forebay elevation?
        CHJ_forebay = StorEq.iloc[28,1]*CHJ_stor**4 + StorEq.iloc[28,2]*CHJ_stor**3 + StorEq.iloc[28,3]*CHJ_stor**2 + StorEq.iloc[28,4]*CHJ_stor + StorEq.iloc[28,5]
        #What is tailwater elevation?
        CHJ_tailwater = TailEq.iloc[28,1]*discharge[i,28]**4 + TailEq.iloc[28,2]*discharge[i,28]**3 + TailEq.iloc[28,3]*discharge[i,28]**2 + TailEq.iloc[28,4]*discharge[i,28] + TailEq.iloc[28,5]
        #Convert head to meters.
        #CHJ_head = np.zeros((sim_days,1))
        CHJ_head[i] = max(0,(CHJ_forebay - CHJ_tailwater)*.3048)
        generation[i,28] = max(0,((1000*CHJ_head[i]*powerflow[i,28]*14.27641*9.81*.84)/1000000)*24)
        heads[i,1]=CHJ_head[i]
        Spillheads[i,1]=CHJ_head[i]
    
        #########################
        #Wells - run-of-river
        #########################
    
        WLL_dg = max(0,local.iloc[i,29]*.001987 + CHJ_dg)
        s_30 = s_30 + local.iloc[i,29]*.001987 + CHJ_dg - WLL_dg
        powerflow[i,29] = min(WLL_dg,f_max[29])
        spill[i,29] = max(0,WLL_dg - f_max[29])
        discharge[i,29] = WLL_dg*(1/.001987)
        storage[i,29] = s_30
        generation[i,29] = ((1000*15.9142*powerflow[i,29]*14.27641*9.81*.87)/1000000)*24
    
        #########################
        #Chelan - run-of-river
        #########################
    
        CHL_dg = max(0,local.iloc[i,10]*.001987)
        s_11 = s_11 + local.iloc[i,10]*.001987 - CHL_dg
        powerflow[i,10] = min(CHL_dg,f_max[10])
        spill[i,10] = max(0,CHL_dg - f_max[10])
        discharge[i,10] = CHL_dg*(1/.001987)
        storage[i,10] = s_11
        generation[i,10] = ((1000*121.92*powerflow[i,10]*14.27641*9.81*.848)/1000000)*24
    
        #########################
        #Rocky Reach - run-of-river
        #########################
    
        RRH_dg = max(0,local.iloc[i,30]*.001987 + CHL_dg + WLL_dg)
        s_31 = s_31 + local.iloc[i,30]*.001987 + CHL_dg + WLL_dg - RRH_dg
        powerflow[i,30] = min(RRH_dg,f_max[30])
        spill[i,30] = max(0,RRH_dg - f_max[30])
        discharge[i,30] = RRH_dg*(1/.001987)
        storage[i,30] = s_31
        generation[i,30] = ((1000*24.3108*powerflow[i,30]*14.27641*9.81*.873)/1000000)*24
    
        #########################
        #Rock Island - run-of-river
        #########################
    
        RIS_dg = max(0,local.iloc[i,31]*.001987 + RRH_dg)
        s_32 = s_32 + local.iloc[i,31]*.001987 + RRH_dg - RIS_dg
        powerflow[i,31] = min(RIS_dg,f_max[31])
        spill[i,31] = max(0,RIS_dg - f_max[31])
        discharge[i,31] = RIS_dg*(1/.001987)
        storage[i,31] = s_32
        generation[i,31] = ((1000*11.5640*powerflow[i,31]*14.27641*9.81*.874)/1000000)*24
    
        #########################
        #Wanapum - run-of-river
        #########################
    
        WPM_dg = max(0,local.iloc[i,32]*.001987 + RIS_dg)
        s_33 = s_33 + local.iloc[i,32]*.001987 + RIS_dg - WPM_dg
        powerflow[i,32] = min(WPM_dg,f_max[32])
        spill[i,32] = max(0,WPM_dg - f_max[32])
        discharge[i,32] = WPM_dg*(1/.001987)
        storage[i,32] = s_33
        generation[i,32] = ((1000*19.2734*powerflow[i,32]*14.27641*9.81*.873)/1000000)*24
    
        #########################
        #Priest Rapids - run-of-river
        #########################
    
        PRD_dg = max(0,local.iloc[i,33]*.001987 + WPM_dg)
        s_34 = s_34 + local.iloc[i,33]*.001987 + WPM_dg - PRD_dg
        powerflow[i,33] = min(PRD_dg,f_max[33])
        spill[i,33] = max(0,PRD_dg - f_max[33])
        discharge[i,33] = PRD_dg*(1/.001987)
        storage[i,33] = s_34
        generation[i,33] = ((1000*17.698*powerflow[i,33]*14.27641*9.81*.873)/1000000)*24
    
        #########################
        #SNAKE RIVER PROJECTS#
        #Brownlee, Oxbow, Hell's Canyon, Dworshak, Lower Granite, Little Goose
        #Lower Monumental, Ice Harbor
    
        #########################
        #Brownlee - storage project
        #########################
    
        #Are we in evacuation or refill?
        #If ICF exists, then fill start date is ICF - 20.
        if fillstart>0:
            evac = julian<fillstart or julian>243
        #Otherwise just use schedule.
        else:
            evac = julian<182 or julian>243
    
    
          #Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182
    
            # Calculate "forecasted" inflows to Brownlee (April - July)
        if spring == True:
               BRN_for = local.iloc[(year-2)*365+212:(year-2)*365+334,11].sum()
        else:
               BRN_for = local.iloc[(year-1)*365+212:(year-1)*365+334,11].sum()
    
    
        #Convert forecast to kAF
        BRN_for = BRN_for*.001987
    
            #Identify target reservoir storage. A number of flood control curves
            #are publically available. They are based on forecasted inflows. Some interpolation is
            #necessary when the forecasted flows are in-between those specifiec by
            #USACE.
    
        if TDA_for <= 75000:
            if BRN_for <= 3000:
                BRN_fctarget = BRN_fc.iloc[julian-1,0]
            elif BRN_for > 3000 and BRN_for <= 4000:
                BRN_fctarget = BRN_fc.iloc[julian-1,0] + ((BRN_for - 3000)/(4000-3000))*(BRN_fc.iloc[julian-1,1] - BRN_fc.iloc[julian-1,0])
            elif BRN_for > 4000 and BRN_for < 5000:
                BRN_fctarget = BRN_fc.iloc[julian-1,1] + ((BRN_for - 4000)/(5000-4000))*(BRN_fc.iloc[julian-1,2] - BRN_fc.iloc[julian-1,1])
            elif BRN_for > 5000 and BRN_for < 6000:
                BRN_fctarget = BRN_fc.iloc[julian-1,2] + ((BRN_for - 5000)/(6000-5000))*(BRN_fc.iloc[julian-1,3] - BRN_fc.iloc[julian-1,2])
            elif BRN_for > 6000:
                BRN_fctarget = BRN_fc.iloc[julian-1,3]
    
        elif TDA_for > 75000 and TDA_for <= 85000:
            if BRN_for <= 3000:
                BRN_fctarget = BRN_fc.iloc[julian-1,4]
            elif BRN_for > 3000 and BRN_for <= 4000:
                BRN_fctarget = BRN_fc.iloc[julian-1,4] + ((BRN_for - 3000)/(4000-3000))*(BRN_fc.iloc[julian-1,5] - BRN_fc.iloc[julian-1,4])
            elif BRN_for > 4000 and BRN_for < 5000:
                BRN_fctarget = BRN_fc.iloc[julian-1,5] + ((BRN_for - 4000)/(5000-4000))*(BRN_fc.iloc[julian-1,6] - BRN_fc.iloc[julian-1,5])
            elif BRN_for > 5000 and BRN_for < 6000:
                BRN_fctarget = BRN_fc.iloc[julian-1,6] + ((BRN_for - 5000)/(6000-5000))*(BRN_fc.iloc[julian-1,7] - BRN_fc.iloc[julian-1,6])
            elif BRN_for > 6000:
                BRN_fctarget = BRN_fc.iloc[julian-1,7]
    
        elif TDA_for > 85000 and TDA_for <= 95000:
            if BRN_for <= 3000:
                BRN_fctarget = BRN_fc.iloc[julian-1,8]
            elif BRN_for > 3000 and BRN_for <= 4000:
                BRN_fctarget = BRN_fc.iloc[julian-1,8] + ((BRN_for - 3000)/(4000-3000))*(BRN_fc.iloc[julian-1,9] - BRN_fc.iloc[julian-1,8])
            elif BRN_for > 4000 and BRN_for < 5000:
                BRN_fctarget = BRN_fc.iloc[julian-1,9]+ ((BRN_for - 4000)/(5000-4000))*(BRN_fc.iloc[julian-1,10] - BRN_fc.iloc[julian-1,9])
            elif BRN_for > 5000 and BRN_for < 6000:
                BRN_fctarget = BRN_fc.iloc[julian-1,10] + ((BRN_for - 5000)/(6000-5000))*(BRN_fc.iloc[julian-1,11] - BRN_fc.iloc[julian-1,10])
            elif BRN_for > 6000:
                BRN_fctarget = BRN_fc.iloc[julian-1,11]
    
        elif TDA_for > 95000 and TDA_for <= 105000:
            if BRN_for <= 3000:
                BRN_fctarget = BRN_fc.iloc[julian-1,12]
            elif BRN_for > 3000 and BRN_for <= 4000:
                BRN_fctarget = BRN_fc.iloc[julian-1,12] + ((BRN_for - 3000)/(4000-3000))*(BRN_fc.iloc[julian-1,13] - BRN_fc.iloc[julian-1,12])
            elif BRN_for > 4000 and BRN_for < 5000:
                BRN_fctarget = BRN_fc.iloc[julian-1,13] + ((BRN_for - 4000)/(5000-4000))*(BRN_fc.iloc[julian-1,14] - BRN_fc.iloc[julian-1,13])
            elif BRN_for > 5000 and BRN_for < 6000:
                BRN_fctarget = BRN_fc.iloc[julian-1,14] + ((BRN_for - 5000)/(6000-5000))*(BRN_fc.iloc[julian-1,15] - BRN_fc.iloc[julian-1,14])
            elif BRN_for > 6000:
                BRN_fctarget = BRN_fc.iloc[julian-1,15]
    
        elif TDA_for > 105000 and TDA_for <= 115000:
            if BRN_for <= 3000:
                BRN_fctarget = BRN_fc.iloc[julian-1,16]
            elif BRN_for > 3000 and BRN_for <= 4000:
                BRN_fctarget = BRN_fc.iloc[julian-1,16] + ((BRN_for - 3000)/(4000-3000))*(BRN_fc.iloc[julian-1,17] - BRN_fc.iloc[julian-1,16])
            elif BRN_for > 4000 and BRN_for < 5000:
                BRN_fctarget = BRN_fc.iloc[julian-1,17] + ((BRN_for - 4000)/(5000-4000))*(BRN_fc.iloc[julian-1,18] - BRN_fc.iloc[julian-1,17])
            elif BRN_for > 5000 and BRN_for < 6000:
                BRN_fctarget = BRN_fc.iloc[julian-1,18] + ((BRN_for - 5000)/(6000-5000))*(BRN_fc.iloc[julian-1,19] - BRN_fc.iloc[julian-1,18])
            elif BRN_for > 6000:
                BRN_fctarget = BRN_fc.iloc[julian-1,19]
    
        elif TDA_for > 115000:
            BRN_fctarget = BRN_fc.iloc[julian-1,19]
        #BRN_sfore = np.zeros((sim_days,1))
        if i==0:
        #DNC's storage forecast
            BRN_sfore[i]=min((local.iloc[i,11]-3500)*.001987+s_12,s_max[11])
        else:
            BRN_sfore[i]=min((local.iloc[i,11]-3500)*.001987+ storage[i-1,11],s_max[11])
    
        BRN_VRC= BRN_sfore[i]
        #BRN_ORC = np.zeros((365,1))
        if julian>=213 and julian <=365:
               BRN_ORC[julian-1]= max(BRN_CRC[julian-1,1],BRN_ARC[julian-1,1])
               BRN_ORC[julian-1]= min(BRN_ORC[julian-1],BRN_fctarget)
    
        elif julian >=1 and julian <= 212:
               BRN_ORC[julian-1]= min(BRN_VRC,max(BRN_CRC[julian-1,1],BRN_ARC[julian-1,1]))
               BRN_ORC[julian-1]= min(BRN_ORC[julian-1],BRN_fctarget)
    
    
    
    
        if evac == True:
        #Evacuation mode
    
    
            #Calculate daily reservoir discharge and end-of-day storage. Have to
            #convert project inflows ("local") to kAF. Note: there is a minimum flow release of 3500cfs associated with this dam.
            BRN_dg = max(0,s_12 + local.iloc[i,11]*.001987 - BRN_ORC[julian-1])
            #If reservoir storage is low
            if BRN_dg > s_12 + local.iloc[i,11]*.001987:
                BRN_dg = s_12 + local.iloc[i,11]*.001987
    
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,BRN_dg - f_max[11])
    
            #Is any storage space available?
            stor_avail = BRN_fctarget - s_12
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,11] = f_max[11]
                spill[i,11] = BRN_dg - f_max[11]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                BRN_dg = max(BRN_dg - stor_avail,f_max[11])
                powerflow[i,11] = f_max[11]
                spill[i,11] = max(0,BRN_dg - f_max[11])
            else:
                powerflow[i,11] = BRN_dg
    
    
            s_12 = s_12 + local.iloc[i,11]*.001987 - BRN_dg
            discharge[i,11] = BRN_dg*(1/.001987)  #Convert back to cfs
            storage[i,11] = s_12
    
        else:
        #Refill mode - this is when the reservoir fills back up during spring
        #floods. Only storage target is maximum reservoir storage (spillway
        #threshold).
    
            BRN_dg = max(0,s_12 + local.iloc[i,11]*.001987 - BRN_ORC[julian-1])
            #If reservoir storage is low
            if BRN_dg > s_12 + local.iloc[i,11]*.001987:
                BRN_dg = s_12 + local.iloc[i,11]*.001987
    
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,BRN_dg - f_max[11])
    
            #Is any storage space available?
            stor_avail = s_max[11] - s_12
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,11] = f_max[11]
                spill[i,11] = BRN_dg - f_max[11]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                BRN_dg = max(BRN_dg - stor_avail,f_max[11])
                powerflow[i,11] = f_max[11]
                spill[i,11] = max(0,BRN_dg - f_max[11])
            else:
                powerflow[i,11] = BRN_dg
    
    
            s_12 = s_12 + local.iloc[i,11]*.001987 - BRN_dg
            discharge[i,11] = BRN_dg*(1/.001987)
            storage[i,11] = s_12
    
    
    
        #Convert storage to AF
        BRN_stor = s_12*1000
        smax = s_max[11]*1000
        #What is forebay elevation?
        BRN_forebay = StorEq.iloc[11,1]*BRN_stor**4 + StorEq.iloc[11,2]*BRN_stor**3 + StorEq.iloc[11,3]*BRN_stor**2 + StorEq.iloc[11,4]*BRN_stor + StorEq.iloc[11,5]
        #What is tailwater elevation?
        BRN_tailwater = (StorEq.iloc[11,1]*smax**4 + StorEq.iloc[11,2]*smax**3 + StorEq.iloc[11,3]*smax**2 + StorEq.iloc[11,4]*smax + StorEq.iloc[11,5]-229)
        #Convert head to meters.
        BRN_head = (BRN_forebay - BRN_tailwater)*.3048
        generation[i,11] = ((1000*BRN_head*powerflow[i,11]*14.27641*9.81*.87)/1000000)*24
    
        #########################
        #Oxbow - run-of-river
        #########################
    
        OXB_dg = max(0,local.iloc[i,34]*.001987 + BRN_dg)
        s_35 = s_35 + local.iloc[i,34]*.001987 + BRN_dg - OXB_dg
        powerflow[i,34] = min(OXB_dg,f_max[34])
        spill[i,34] = max(0,OXB_dg - f_max[34])
        discharge[i,34] = OXB_dg*(1/.001987)
        storage[i,34] = s_35
        generation[i,34] = ((1000*31.2674*powerflow[i,34]*14.27641*9.81*.875)/1000000)*24
    
        #########################
        #Hell's Canyon - run-of-river
        #########################
    
        HLC_dg = max(0,local.iloc[i,43]*.001987 + OXB_dg)
        s_44 = s_44 + local.iloc[i,43]*.001987 + OXB_dg - HLC_dg
        powerflow[i,43] = min(HLC_dg,f_max[43])
        spill[i,43] = max(0,HLC_dg - f_max[43])
        discharge[i,43] = HLC_dg*(1/.001987)
        storage[i,43] = s_44
        generation[i,43] = ((1000*53.62*powerflow[i,43]*14.27641*9.81*.875)/1000000)*24
    
        #########################
        #Dworshak - storage project
        #########################
    
        #Are we in evacuation or refill?
        #If ICF exists, then fill start date is ICF - 20.
        if fillstart>0:
            evac = julian<fillstart or julian>243
        #Otherwise just use schedule.
        else:
            evac = julian<182 or julian>243
    
    
        #Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182
        # Calculate "forecasted" inflows to Dworshak (April - July)
        if spring == True:
              DWR_for = local.iloc[(year-2)*365+212:(year-2)*365+334,12].sum()
        else:
              DWR_for = local.iloc[(year-1)*365+212:(year-1)*365+334,12].sum()
    
    
        #Convert forecast to kAF
        DWR_for = DWR_for*.001987
    
            #Identify target reservoir storage. A number of flood control curves
            #are publically available. They are based on forecasted inflows. Some interpolation is
            #necessary when the forecasted flows are in-between those specifiec by
            #USACE.
    
        if DWR_for <= 1200:
            DWR_fctarget = DWR_fc.iloc[julian-1,0]
        elif DWR_for > 1200 and DWR_for <= 1400:
            DWR_fctarget = DWR_fc.iloc[julian-1,0] + ((DWR_for - 1200)/(1400-1200))*(DWR_fc.iloc[julian-1,1] - DWR_fc.iloc[julian-1,0])
        elif DWR_for > 1400 and DWR_for <= 1800:
            DWR_fctarget = DWR_fc.iloc[julian-1,1] + ((DWR_for - 1400)/(1800-1400))*(DWR_fc.iloc[julian-1,2] - DWR_fc.iloc[julian-1,1])
        elif DWR_for > 1800 and DWR_for <= 2200:
            DWR_fctarget = DWR_fc.iloc[julian-1,2] + ((DWR_for - 1800)/(2200-1800))*(DWR_fc.iloc[julian-1,3] - DWR_fc.iloc[julian-1,2])
        elif DWR_for > 2200 and DWR_for <= 2600:
            DWR_fctarget = DWR_fc.iloc[julian-1,3] + ((DWR_for - 2200)/(2600-2200))*(DWR_fc.iloc[julian-1,4] - DWR_fc.iloc[julian-1,3])
        elif DWR_for > 2600 and DWR_for <= 3000:
            DWR_fctarget = DWR_fc.iloc[julian-1,4] + ((DWR_for - 2600)/(3000-2600))*(DWR_fc.iloc[julian-1,5] - DWR_fc.iloc[julian-1,4])
        elif DWR_for > 3000 and DWR_for <= 3200:
            DWR_fctarget = DWR_fc.iloc[julian-1,5] + ((DWR_for - 3000)/(3200-3000))*(DWR_fc.iloc[julian-1,6] - DWR_fc.iloc[julian-1,5])
        elif DWR_for > 3200 and DWR_for <= 3400:
            DWR_fctarget = DWR_fc.iloc[julian-1,6] + ((DWR_for - 3200)/(3400-3200))*(DWR_fc.iloc[julian-1,7] - DWR_fc.iloc[julian-1,6])
        elif DWR_for > 3400 and DWR_for <= 3600:
            DWR_fctarget = DWR_fc.iloc[julian-1,7] + ((DWR_for - 3600)/(3600-3400))*(DWR_fc.iloc[julian-1,8] - DWR_fc.iloc[julian-1,7])
        elif DWR_for > 3600 and DWR_for <= 3800:
            DWR_fctarget = DWR_fc.iloc[julian-1,8] + ((DWR_for - 3800)/(3800-3600))*(DWR_fc.iloc[julian-1,9] - DWR_fc.iloc[julian-1,8])
        elif DWR_for > 3800:
            DWR_fctarget = DWR_fc.iloc[julian-1,9]
    
        #DWR_sfore = np.zeros((sim_days,1))
        if i==0:
              #DNC's storage forecaste
              DWR_sfore[i]=min((local.iloc[i,12]-1600)*.001987+s_13,s_max[12])
        else:
              DWR_sfore[i]=min((local.iloc[i,12]-1600)*.001987+ storage[i-1,12],s_max[12])
    
        DWR_VRC= DWR_sfore[i]
        #DWR_ORC = np.zeros((365,1))
    
        if julian>=213 and julian <=365:
               DWR_ORC[julian-1]= max(DWR_CRC[julian-1,1],DWR_ARC[julian-1,1])
               DWR_ORC[julian-1]= min(DWR_ORC[julian-1],DWR_fctarget)
    
        elif julian >=1 and julian <= 212:
               DWR_ORC[julian-1]= min(DWR_VRC,max(DWR_CRC[julian-1,1],DWR_ARC[julian-1,1]))
               DWR_ORC[julian-1]= min(DWR_ORC[julian-1],DWR_fctarget)
    
    
        if evac == True:
        #Evacuation mode
    
    
    
    
            #Calculate daily reservoir discharge and end-of-day storage. Have to
            #convert project inflows ("local") to kAF.
            DWR_dg = max(1600*.001987, s_13 + local.iloc[i,12]*.001987 -  DWR_ORC[julian-1])
            #If reservoir is low
            if DWR_dg > s_13 + local.iloc[i,12]*.001987:
                DWR_dg = s_13 + local.iloc[i,12]*.001987
    
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,DWR_dg - f_max[12])
    
            #Is any storage space available?
            stor_avail = DWR_fctarget - s_13
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,12] = f_max[12]
                spill[i,12] = DWR_dg - f_max[12]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                DWR_dg = max(DWR_dg - stor_avail,f_max[12])
                powerflow[i,12] = f_max[12]
                spill[i,12] = max(0,DWR_dg - f_max[12])
            else:
                powerflow[i,12] = DWR_dg
    
    
            s_13 = s_13 + local.iloc[i,12]*.001987 - DWR_dg
            discharge[i,12] = DWR_dg*(1/.001987)  #Convert back to cfs
            storage[i,12] = s_13
    
        else:
        #Refill mode - this is when the reservoir fills back up during spring
        #floods. Only storage target is maximum reservoir storage (spillway
        #threshold).
    
            DWR_dg = max(1600*.001987, s_13 + local.iloc[i,12]*.001987 -  DWR_ORC[julian-1])
            if DWR_dg > s_13 + local.iloc[i,12]*.001987:
               DWR_dg = s_13 + local.iloc[i,12]*.001987
    
    
            #Do flows exceed hydraulic capacity of dam?
            overflow = max(0,DWR_dg - f_max[12])
    
            #Is any storage space available?
            stor_avail = s_max[12] - s_13
    
            #If flows exceed dam's hydraulic capacity.
            if overflow>0 and stor_avail<=0:
                #If there is no storage available,then total discharge remains
                #the same, and anything beyond hydraulic capacity of dam is
                #spilled.
                powerflow[i,12] = f_max[12]
                spill[i,12] = DWR_dg - f_max[12]
            elif overflow>0 and stor_avail>0:
                #If there is some storage available, total release must be revised down and additional water
                #stored.
                DWR_dg = max(DWR_dg - stor_avail,f_max[12])
                powerflow[i,12] = f_max[12]
                spill[i,12] = max(0,DWR_dg - f_max[12])
            else:
                powerflow[i,12] = DWR_dg
    
    
    
            s_13 = s_13 + local.iloc[i,12]*.001987 - DWR_dg
            discharge[i,12] = DWR_dg*(1/.001987)
            storage[i,12] = s_13
    
    
    
        #Convert storage to AF
        DWR_stor = s_13*1000
        #What is forebay elevation?
        DWR_forebay = StorEq.iloc[12,1]*DWR_stor**4 + StorEq.iloc[12,2]*DWR_stor**3 + StorEq.iloc[12,3]*DWR_stor**2 + StorEq.iloc[12,4]*DWR_stor + StorEq.iloc[12,5]
        #What is tailwater elevation?
        DWR_tailwater = TailEq.iloc[12,1]*discharge[i,12]**4 + TailEq.iloc[12,2]*discharge[i,12]**3 + TailEq.iloc[12,3]*discharge[i,12]**2 + TailEq.iloc[12,4]*discharge[i,12] + TailEq.iloc[12,5]
        #Convert head to meters.
        #DWR_head = np.zeros((sim_days,1))
        DWR_head[i] = (DWR_forebay - DWR_tailwater)*.3048
        generation[i,12] = ((1000*DWR_head[i]*powerflow[i,12]*14.27641*9.81*.83)/1000000)*24
        Spillheads[i,2]=DWR_head[i]
    
        #########################
        #Lower Granite - run-of-river project
        #########################
    
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
        #Note: There is a 1-day travel delay between Hell's Canyon and Dworshak
        #and Lower Granite.
        if i>0:
            LWG_dg = max(0,local.iloc[i,35]*.001987 + discharge[i-1,12]*.001987 + discharge[i-1,43]*.001987 + ORF5H[i]* .001987 + SPD5L[i]*.001987 + ANA5L[i]*.001987 + LIM5L[i]*.001987 + WHB5H[i]*.001987)
            s_36 = s_36 + local.iloc[i,35]*.001987 + discharge[i-1,12]*.001987 + discharge[i-1,43]*.001987+ ORF5H[i]* .001987 + SPD5L[i]*.001987 + ANA5L[i]*.001987 + LIM5L[i]*.001987 + WHB5H[i]*.001987 - LWG_dg
        else:
            LWG_dg = max(0,local.iloc[i,35]*.001987 + discharge[i,12]*.001987 + discharge[i,43]*.001987+ ORF5H[i]* .001987 + SPD5L[i]*.001987 + ANA5L[i]*.001987 + LIM5L[i]*.001987 + WHB5H[i]*.001987)
            s_36 = s_36 + local.iloc[i,35]*.001987 + discharge[i,12]*.001987 + discharge[i,43]*.001987 + ORF5H[i]*.001987 + SPD5L[i]*.001987 + ANA5L[i]*.001987 + LIM5L[i]*.001987 + WHB5H[i]*.001987 - LWG_dg
    
        powerflow[i,35] = min(LWG_dg,f_max[35])
        spill[i,35] = max(0,LWG_dg - f_max[35])
        discharge[i,35] = LWG_dg*(1/.001987)  #Convert back to cfs
        storage[i,35] = s_36
        #Convert storage to AF
        LWG_stor = s_36*1000
        #What is forebay elevation?
        LWG_forebay = StorEq.iloc[35,1]*LWG_stor**4 + StorEq.iloc[35,2]*LWG_stor**3 + StorEq.iloc[35,3]*LWG_stor**2 + StorEq.iloc[35,4]*LWG_stor + StorEq.iloc[35,5]
        #What is tailwater elevation?
        LWG_tailwater = TailEq.iloc[35,1]*discharge[i,35]**4 + TailEq.iloc[35,2]*discharge[i,35]**3 + TailEq.iloc[35,3]*discharge[i,35]**2 + TailEq.iloc[35,4]*discharge[i,35] + TailEq.iloc[35,5]
        #Convert head to meters.
        LWG_head[i] = (LWG_forebay - LWG_tailwater)*.3048
        generation[i,35] = ((1000*LWG_head[i]*powerflow[i,35]*14.27641*9.81*.86)/1000000)*24
        heads[i,2]=LWG_head[i]
        Spillheads[i,3]=LWG_head[i]
    
    
    
        #########################
        #Little Goose - run-of-river project
        #########################
    
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
        LGO_dg = max(0,local.iloc[i,36]*.001987 + LWG_dg)
        s_37 = s_37 + local.iloc[i,36]*.001987 + LWG_dg - LGO_dg
        powerflow[i,36] = min(LGO_dg,f_max[36])
        spill[i,36] = max(0,LGO_dg - f_max[36])
        discharge[i,36] = LGO_dg*(1/.001987)  #Convert back to cfs
        storage[i,36] = s_37
        #Convert storage to AF
        LGO_stor = s_37*1000
        #What is forebay elevation?
        LGO_forebay = StorEq.iloc[36,1]*LGO_stor**4 + StorEq.iloc[36,2]*LGO_stor**3 + StorEq.iloc[36,3]*LGO_stor**2 + StorEq.iloc[36,4]*LGO_stor + StorEq.iloc[36,5]
        #What is tailwater elevation?
        LGO_tailwater = TailEq.iloc[36,1]*discharge[i,36]**4 + TailEq.iloc[36,2]*discharge[i,36]**3 + TailEq.iloc[36,3]*discharge[i,36]**2 + TailEq.iloc[36,4]*discharge[i,36] + TailEq.iloc[36,5]
        #Convert head to meters.
        LGO_head[i] = (LGO_forebay - LGO_tailwater)*.3048
        generation[i,36] = ((1000*LGO_head[i]*powerflow[i,36]*14.27641*9.81*.86)/1000000)*24
        heads[i,3]=LGO_head[i]
        Spillheads[i,4]=LGO_head[i]
    
    
        #########################
        #Lower Monumental - run-of-river project
        #########################
    
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
        LMN_dg = max(0,local.iloc[i,37]*.001987 + LGO_dg)
        s_38 = s_38 + local.iloc[i,37]*.001987 + LGO_dg - LMN_dg
        powerflow[i,37] = min(LMN_dg,f_max[37])
        spill[i,37] = max(0,LMN_dg - f_max[37])
        discharge[i,37] = LMN_dg*(1/.001987)  #Convert back to cfs
        storage[i,37] = s_38
        #Convert storage to AF
        LMN_stor = s_38*1000
        #What is forebay elevation?
        LMN_forebay = StorEq.iloc[37,1]*LMN_stor**4 + StorEq.iloc[37,2]*LMN_stor**3 + StorEq.iloc[37,3]*LMN_stor**2 + StorEq.iloc[37,4]*LMN_stor + StorEq.iloc[37,5]
        #What is tailwater elevation?
        LMN_tailwater = TailEq.iloc[37,1]*discharge[i,37]**4 + TailEq.iloc[37,2]*discharge[i,37]**3 + TailEq.iloc[37,3]*discharge[i,37]**2 + TailEq.iloc[37,4]*discharge[i,37] + TailEq.iloc[37,5]
        #Convert head to meters.
        LMN_head[i] = (LMN_forebay - LMN_tailwater)*.3048
        generation[i,37] = max(0,((1000*LMN_head[i]*powerflow[i,37]*14.27641*9.81*.83)/1000000)*24)
        heads[i,4]=LMN_head[i]
        Spillheads[i,5]=LMN_head[i]
    
        #########################
        #Ice Harbor - run-of-river project
        #########################
    
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
        IHR_dg = max(0,local.iloc[i,38]*.001987 + LMN_dg)
        s_39 = s_39 + local.iloc[i,38]*.001987 + LMN_dg - IHR_dg
        powerflow[i,38] = min(IHR_dg,f_max[38])
        spill[i,38] = max(0,IHR_dg - f_max[38])
        discharge[i,38] = IHR_dg*(1/.001987)  #Convert back to cfs
        storage[i,38] = s_39
        #Convert storage to AF
        IHR_stor = s_39*1000
        #What is forebay elevation?
        IHR_forebay = StorEq.iloc[38,1]*IHR_stor**4 + StorEq.iloc[38,2]*IHR_stor**3 + StorEq.iloc[38,3]*IHR_stor**2 + StorEq.iloc[38,4]*IHR_stor + StorEq.iloc[38,5]
        #What is tailwater elevation?
        IHR_tailwater = TailEq.iloc[38,1]*discharge[i,38]**4 + TailEq.iloc[38,2]*discharge[i,38]**3 + TailEq.iloc[38,3]*discharge[i,38]**2 + TailEq.iloc[38,4]*discharge[i,38] + TailEq.iloc[38,5]
        #Convert head to meters.
        IHR_head[i] = (IHR_forebay - IHR_tailwater)*.3048
        generation[i,38] = ((1000*IHR_head[i]*powerflow[i,38]*14.27641*9.81*.83)/1000000)*24
        heads[i,5]=IHR_head[i]
        Spillheads[i,6]=IHR_head[i]
    
    
        #########################
        #LOWER COLUMBIA RIVER PROJECTS
        #McNary, Round Butte, Pelton, John Day, The Dalles, and Bonneville
    
        #########################
        #Round Butte - run-of-river
        #########################
    
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
        RBU_dg = max(0,local.iloc[i,14]*.001987)
        s_15 = s_15 + local.iloc[i,14]*.001987 - RBU_dg
        powerflow[i,14] = min(RBU_dg,f_max[14])
        spill[i,14] = max(0,RBU_dg - f_max[14])
        discharge[i,14] = RBU_dg*(1/.001987)  #Convert back to cfs
        storage[i,14] = s_15
        generation[i,14] = ((1000*134*powerflow[i,14]*14.27641*9.81*.83)/1000000)*24
    
        #########################
        #Pelton - run-of-river
        #########################
    
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
        PLT_dg = max(0,local.iloc[i,44]*.001987 + RBU_dg)
        s_44 = s_44 + local.iloc[i,44]*.001987 + RBU_dg - PLT_dg
        powerflow[i,44] = min(PLT_dg,f_max[44])
        spill[i,44] = max(0,PLT_dg - f_max[44])
        discharge[i,44] = PLT_dg*(1/.001987)  #Convert back to cfs
        storage[i,44] = s_44
        generation[i,44] = ((1000*62.1792*powerflow[i,44]*14.27641*9.81*.87)/1000000)*24
    
        #########################
        #McNary - run-of-river
        #########################
    
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
        MCN_dg = max(0,local.iloc[i,39]*.001987 + PRD_dg +IHR_dg + YAK5H[i]*.001987)
        s_40 = s_40 + local.iloc[i,39]*.001987 + PRD_dg +IHR_dg + YAK5H[i]*.001987 - MCN_dg
        powerflow[i,39] = min(MCN_dg,f_max[39])
        spill[i,39] = max(0,MCN_dg - f_max[39])
        discharge[i,39] = MCN_dg*(1/.001987)  #Convert back to cfs
        storage[i,39] = s_40
        #Convert storage to AF
        MCN_stor = s_40*1000
        #What is forebay elevation?
        MCN_forebay = StorEq.iloc[39,1]*MCN_stor**4 + StorEq.iloc[39,2]*MCN_stor**3 + StorEq.iloc[39,3]*MCN_stor**2 + StorEq.iloc[39,4]*MCN_stor + StorEq.iloc[39,5]
        #What is tailwater elevation?
        MCN_tailwater = TailEq.iloc[39,1]*discharge[i,39]**4 + TailEq.iloc[39,2]*discharge[i,39]**3 + TailEq.iloc[39,3]*discharge[i,39]**2 + TailEq.iloc[39,4]*discharge[i,39] + TailEq.iloc[39,5]
        #Convert head to meters.
        MCN_head[i] = (MCN_forebay - MCN_tailwater)*.3048
        generation[i,39] = ((1000*MCN_head[i]*powerflow[i,39]*14.27641*9.81*.76)/1000000)*24
        heads[i,6]=MCN_head[i]
        Spillheads[i,7]=MCN_head[i]
    
    
        #########################
        #John Day - run-of-river
        #########################
    
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
        JDA_dg = max(0,local.iloc[i,40]*.001987 + MCN_dg)
        s_41 = s_41 + local.iloc[i,40]*.001987 + MCN_dg - JDA_dg
        powerflow[i,40] = min(JDA_dg,f_max[40])
        spill[i,40] = max(0,JDA_dg - f_max[40])
        discharge[i,40] = JDA_dg*(1/.001987)  #Convert back to cfs
        storage[i,40] = s_41
        #Convert storage to AF
        JDA_stor = s_41*1000
        #What is forebay elevation?
        JDA_forebay = StorEq.iloc[40,1]*JDA_stor**4 + StorEq.iloc[40,2]*JDA_stor**3 + StorEq.iloc[40,3]*JDA_stor**2 + StorEq.iloc[40,4]*JDA_stor + StorEq.iloc[40,5]
        #What is tailwater elevation?
        JDA_tailwater = TailEq.iloc[40,1]*discharge[i,40]**4 + TailEq.iloc[40,2]*discharge[i,40]**3 + TailEq.iloc[40,3]*discharge[i,40]**2 + TailEq.iloc[40,4]*discharge[i,40] + TailEq.iloc[40,5]
        #Convert head to meters.
        JDA_head[i] = max(0,(JDA_forebay - JDA_tailwater)*.3048)
        generation[i,40] = max(0,((1000*JDA_head[i]*powerflow[i,40]*14.27641*9.81*.87)/1000000)*24)
        heads[i,7]=JDA_head[i]
        Spillheads[i,8]=JDA_head[i]
    
        #########################
        #The Dalles - run-of-river
        #########################
    
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
        TDA_dg = max(0,local.iloc[i,41]*.001987 + JDA_dg + PLT_dg)
        s_42 = s_42 + local.iloc[i,41]*.001987 + JDA_dg + PLT_dg - TDA_dg
        powerflow[i,41] = min(TDA_dg,f_max[41])
        spill[i,41] = max(0,TDA_dg - f_max[41])
        discharge[i,41] = TDA_dg*(1/.001987)  #Convert back to cfs
        storage[i,41] = s_42
        #Convert storage to AF
        TDA_stor = s_42*1000
        #What is forebay elevation?
        TDA_forebay = 13.891*np.log(TDA_stor) - 20.692
        #What is tailwater elevation?
        TDA_tailwater = TailEq.iloc[41,1]*discharge[i,41]**4 + TailEq.iloc[41,2]*discharge[i,41]**3 + TailEq.iloc[41,3]*discharge[i,41]**2 + TailEq.iloc[41,4]*discharge[i,41] + TailEq.iloc[41,5]
        #Convert head to meters.
        TDA_head = max(0,(TDA_forebay - TDA_tailwater)*.3048)
        generation[i,41] = max(0,((1000*TDA_head*powerflow[i,41]*14.27641*9.81*.86)/1000000)*24)
        heads[i,8]=TDA_head
        Spillheads[i,9]=TDA_head
    
    
        #########################
        #Bonneville - run-of-river
        #########################
    
        #Calculate daily reservoir discharge and end-of-day storage. Have to
        #convert project inflows ("local") to kAF.
        BNN_dg = max(0,local.iloc[i,42]*.001987 + TDA_dg)
        s_43 = s_43 + local.iloc[i,42]*.001987 + TDA_dg - BNN_dg
        powerflow[i,42] = min(BNN_dg,f_max[42])
        spill[i,42] = max(0,BNN_dg - f_max[42])
        discharge[i,42] = BNN_dg*(1/.001987)  #Convert back to cfs
        storage[i,42] = s_43
        #Convert storage to AF
        BNN_stor = s_43*1000
        #What is forebay elevation?
        BNN_forebay = StorEq.iloc[42,1]*BNN_stor**4 + StorEq.iloc[42,2]*BNN_stor**3 + StorEq.iloc[42,3]*BNN_stor**2 + StorEq.iloc[42,4]*BNN_stor + StorEq.iloc[42,5]
        #What is tailwater elevation?
        BNN_tailwater = TailEq.iloc[42,1]*discharge[i,42]**4 + TailEq.iloc[42,2]*discharge[i,42]**3 + TailEq.iloc[42,3]*discharge[i,42]**2 + TailEq.iloc[42,4]*discharge[i,42] + TailEq.iloc[42,5]
        #Convert head to meters.
        BNN_head = (BNN_forebay - BNN_tailwater)*.3048
        generation[i,42] = max(0,((1000*BNN_head*powerflow[i,42]*14.27641*9.81*.92)/1000000)*24)
        heads[i,9]=BNN_head
        Spillheads[i,10]=BNN_head
    
    
    
    
    
    
    
    ############
    #Data Output
    ############
    np.savetxt('PNW_hydro/FCRPS/discharge.csv',discharge,delimiter=',')
    np.savetxt('PNW_hydro/FCRPS/storage.csv',storage,delimiter=',')
    np.savetxt('PNW_hydro/FCRPS/powerflow.csv',powerflow,delimiter=',')
    np.savetxt('PNW_hydro/FCRPS/spill.csv',spill,delimiter=',')
    np.savetxt('PNW_hydro/FCRPS/heads.csv',heads,delimiter=',')
    
    
    generation[0,:]=generation[2,:]
    generation[1,:]=generation[2,:]
    
    # bias correction
    generation = generation*0.94
    
    total=np.sum((generation),axis=1)
    
    #BPA owned dams
    BPA_own = np.zeros((sim_days,22))
    BPA_own[:,0]=generation[:,9] #Grand Culee
    BPA_own[:,1]=generation[:,28] #Chief Joseph
    BPA_own[:,2]=generation[:,12] #Dworshak
    BPA_own[:,3]=generation[:,35] #Lower Granite
    BPA_own[:,4]=generation[:,36] #Little Goose
    BPA_own[:,5]=generation[:,37] #Lower Monumental
    BPA_own[:,6]=generation[:,38] #Ice Harbor
    BPA_own[:,7]=generation[:,39] #McNary
    BPA_own[:,8]=generation[:,40] #John Day
    BPA_own[:,9]=generation[:,41] #Dalles
    BPA_own[:,10]=generation[:,42] #Bonneville
    BPA_own[:,11]=generation[:,7] #Albeni Falls
    BPA_own[:,12]=generation[:,2] #Libby
    BPA_own[:,13]=generation[:,5] #Hungry Horse
    
    
    Unmodeled = np.zeros((sim_days,47))
    Unmodeled[:,0]=generation[:,9]*0.0038 #Main Canal #1
    Unmodeled[:,1]=generation[:,23]*1.77 #Upriver
    Unmodeled[:,2]=generation[:,20]*0.017 #Meyers Falls
    Unmodeled[:,3]=generation[:,39]*0.0621 #Cowlitz
    Unmodeled[:,4]=total*0.0015 #Smith Creek
    Unmodeled[:,5]=generation[:,41]*0.019 #Dalles N Fishway
    Unmodeled[:,6]=generation[:,39]*0.024 #Packwood
    Unmodeled[:,7]=generation[:,39]*0.012 # Tieton
    Unmodeled[:,8]=generation[:,32]*0.012 #Roza
    Unmodeled[:,9]=generation[:,33]*0.0126 #Chandler
    Unmodeled[:,10]=generation[:,39]*0.0089 #McNary Fishway
    Unmodeled[:,11]=total*0.00022 #Lower No1
    Unmodeled[:,12]=total*0.00022 #Upper Pow3
    Unmodeled[:,13]=generation[:,19]*0.0196 #Lake Creek
    Unmodeled[:,14]=generation[:,39]*0.0036 #Yakama Drop
    Unmodeled[:,15]=generation[:,19]*0.0169 #Moyie River
    Unmodeled[:,16]=generation[:,41]*0.0018 #Middle Fork
    Unmodeled[:,17]=generation[:,21]*0.0012 #Sheep Creek
    Unmodeled[:,18]=generation[:,38]*0.00159 #Esquatzel
    Unmodeled[:,19]=total*0.0000139 #Mill Creek
    Unmodeled[:,20]=generation[:,39]*0.000426 #Burton Creek
    Unmodeled[:,21]=total*0.000011 #Hellroaring
    Unmodeled[:,22]=total*0.000083 #Lower No2
    Unmodeled[:,23]=generation[:,31]*0.015 #Quincy
    Unmodeled[:,24]=generation[:,31]*0.0106 #Pec Headworks
    Unmodeled[:,25]=generation[:,31]*0.497 #Swift
    Unmodeled[:,26]=generation[:,31]*0.216 #Merwin
    Unmodeled[:,27]=generation[:,31]*0.2148 #Yale
    Unmodeled[:,28]=generation[:,42]*0.034 #North Fork
    Unmodeled[:,29]=generation[:,42]*0.0308 # Faraday
    Unmodeled[:,30]=generation[:,42]*0.0299 #Portland
    Unmodeled[:,31]=generation[:,31]*0.179 #Lower Baker
    Unmodeled[:,32]=generation[:,31]*0.168 #Upper Baker
    Unmodeled[:,33]=generation[:,39]*0.036 #Snoqualmie
    Unmodeled[:,34]=generation[:,31]*0.019 #Koma Kulshan
    Unmodeled[:,35]=generation[:,31]*0.0024 #Nooksack
    Unmodeled[:,36]=generation[:,31]*0.0016 #Hutchinson
    Unmodeled[:,37]=generation[:,31]*0.72 #Ross
    Unmodeled[:,38]=generation[:,31]*0.33 #Gorge
    Unmodeled[:,39]=generation[:,31]*0.266 #Diablo
    Unmodeled[:,40]=generation[:,33]*0.0176 #South Fork Tolt
    Unmodeled[:,41]=generation[:,37]*0.0065 #Russel D Smith
    Unmodeled[:,42]=generation[:,39]*0.266 #Mossyrock
    Unmodeled[:,43]=generation[:,39]*0.144 #Mayfield
    Unmodeled[:,44]=generation[:,9]*0.13 #Summer Falls
    Unmodeled[:,45]=generation[:,39]*0.057 #Lagrande
    Unmodeled[:,46]=generation[:,39]*0.044 #Alder
    
    #Sum all of the unmodeled dams
    total_unmodeled=np.sum((Unmodeled),axis=1)
    
    
    BPA_own[:,14]=Unmodeled[:,9]  #Chandler
    BPA_own[:,15]=Unmodeled[:,3]  #Cowlitz
    BPA_own[:,16]=Unmodeled[:,8]  #Roza
    #Upper Sanke River dams:
    BPA_own[:,17]=generation[:,35]*0.011 #Black Canyon
    BPA_own[:,18]=generation[:,35]*0.002 #Boise River Diversion
    BPA_own[:,19]=generation[:,35]*0.043 #Anderson Ranch
    BPA_own[:,20]=generation[:,35]*0.030 #Minidoka
    BPA_own[:,21]=generation[:,35]*0.190 #Palisades
    
    #Path dams
    Path_dams = np.zeros((sim_days,26))
    Path_dams[:,0] = generation[:,7] #Albeni Falls
    Path_dams[:,1] = generation[:,42] #Bonneville
    Path_dams[:,2] = Unmodeled[:,9]  #Chandler
    Path_dams[:,3] = generation[:,28] #Chief Joseph
    Path_dams[:,4] = Unmodeled[:,3]  #Cowlitz
    Path_dams[:,5] = generation[:,12] #Dworshak
    Path_dams[:,6] = generation[:,38]*0.00159 #Esquatzel
    Path_dams[:,7] = generation[:,9] #Grand Culee
    Path_dams[:,8] = generation[:,5] #Hungry Horse
    Path_dams[:,9] = generation[:,38] #Ice Harbor
    Path_dams[:,10] = generation[:,40] #John Day
    Path_dams[:,11] = generation[:,19]*0.0196 #Lake Creek
    Path_dams[:,12] = generation[:,2] #Libby
    Path_dams[:,13] = generation[:,36] #Little Goose
    Path_dams[:,14] = generation[:,35] #Lower Granite
    Path_dams[:,15] = generation[:,37] #Lower Monumental
    Path_dams[:,16] = generation[:,39] #McNary
    Path_dams[:,17] = generation[:,39]*0.0089 #McNary Fishway
    Path_dams[:,18] = generation[:,39]*0.024 #Packwood
    Path_dams[:,19] = generation[:,32]*0.012 #Roza
    Path_dams[:,20] = Unmodeled[:,16]  #Middle Fork
    Path_dams[:,21] = total*0.0015 #Smith Creek
    Path_dams[:,22] = generation[:,41] #Dalles
    Path_dams[:,23] = generation[:,41]*0.019 #Dalles N Fishway
    Path_dams[:,24] =generation[:,39]*0.0036 #Yakama Drop
    
    generation[:,47]=total_unmodeled
    Total_generation=generation
    Total_generation=np.delete(Total_generation,[0,1,3,4,6,11,15,16,17,18,22,34,43,45,46] ,axis=1)
    
    #BPA owned dams
    BPA_own=BPA_own[122:len(BPA_own)-243,:]
    BPA_own=pd.DataFrame(np.sum(BPA_own,axis=1))
    #Path dams
    Path_dams=Path_dams[122:len(Path_dams)-243,:]
    #Total Generation
    Total_generation=Total_generation[122:len(Total_generation)-243,:]
    
    #Load Willamette
    df_Willamette = pd.read_excel('Willamette/Output/WillametteDAMS_hydropower.xlsx', usecols=np.arange(1,9))
    Willamette=pd.DataFrame(24*df_Willamette.sum(axis=1),columns=['tot_Willamette_dailySum'])
    #cut first two years and last year 
    Willamette = Willamette.iloc[365:len(Willamette)-(2*365),:]
    Willamette= Willamette.reset_index(drop=True)
    
    #Add Willamette and Willamette missing dams to BPA own file
    LC=Willamette*0.12 #Lost Creek
    GP=Willamette*0.03 #Green Springs
    BPA=pd.DataFrame(BPA_own.values + Willamette.values +LC.values +GP.values,columns=['BPA_tot'])
    
    #Add Willamette and Willamette missing to Path generation 
    WILL_total = Willamette*(1+331/411)
    Path_dams[:,25] = WILL_total.values[:,0]
    
    #Add Willamette and Willamette missing to Total PNW dams
    Will_PNW=Willamette*(1+514/411)
    Total_generation=np.hstack([Total_generation, Will_PNW.values])
    
    Total_sum = pd.DataFrame(np.sum(Total_generation,axis=1), columns = ['PNW'])
    
    Total_sum.to_excel('PNW_hydro/PNW_hydro_daily.xlsx') #to be used in the dispatch
    np.savetxt('PNW_hydro/FCRPS/BPA_owned_dams.csv',BPA,delimiter=',') #to be used for BPA revenue
    np.savetxt('PNW_hydro/FCRPS/Path_dams.csv',Path_dams,delimiter=',') #to be used for path transmission estimation
    np.savetxt('PNW_hydro/FCRPS/Total_PNW_dams.csv',Total_generation,delimiter=',') #same as dispatch but single dams
    np.savetxt('PNW_hydro/FCRPS/generation.csv',generation,delimiter=',') #all modeled dams and unmodeled sum

    return None