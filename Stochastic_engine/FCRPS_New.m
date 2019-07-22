

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Federal Columbia River Power System Model developed from HYSSR
%This version operates on a daily time step. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Data input - select flows september 1 (244 julian date)
d=csvread('Synthetic_streamflows/synthetic_streamflows_FCRPS.csv');
d = d(244:length(d)-122,:);
[r, c]=size(d);

for i = 1:r
    for j = 1:c
        if isnan(d(i,j))>0
            d(i,j) = 0;
        end
    end
end

no_days = length(d);
no_years = no_days/365;

 %d = xlsread('daily_streamflows.xlsx');
calender=xlsread('PNW_hydro/FCRPS/daily_streamflows.xlsx','Calender');
c=zeros(no_days,4);

for i = 1:no_years
    c((i-1)*365+1:(i-1)*365+365,1) = calender(:,1);
    c((i-1)*365+1:(i-1)*365+365,2) = calender(:,2);
    c((i-1)*365+1:(i-1)*365+365,3) = calender(:,3);
    c((i-1)*365+1:(i-1)*365+365,4) = calender(:,4)+(i-1);
end

% month, day, year of simulation data
months = c(:,1); 
days = c(:,2);
julians = c(:,3);
no_days = length(c);
years = c(:,4);

%Simulated Runoff ("local" flow accretions defined by USACE and BPA)
local = d;

%Project indices (consistent with HYSSR)
% No. Name	HYSSR ID
% 1 MICA	1
% 2 ARROW	2
% 3 LIBBY	3
% 4 DUNCAN	5
% 5 CORRA LINN	6
% 6 HUNGRY HORSE	10
% 7 KERR	11
% 8 ALBENI FALLS	16
% 9 POST FALLS	18
% 10 GRAND COULEE	19
% 11 CHELAN	20
% 12 BROWNLEE	21
% 13 DWORSHAK	31
% 14 NOXON	38
% 15 ROUND BUTTE	40
% 16 REVELSTOKE	41
% 17 SEVEN MILE	46
% 18 BRILLIANT	50
% 19 THOMPSON FALLS	54
% 20 CABINET GRGE	56
% 21 BOX CANYON	57
% 22 BOUNDARY	58
% 23 WANETA	59
% 24 UPPER FALLS	61
% 25 MONROE ST	62
% 26 NINE MILE	63
% 27 LONG LAKE	64
% 28 LITTLE FALLS	65
% 29 CHIEF JOSEPH	66
% 30 WELLS	67
% 31 ROCKY REACH	68
% 32 ROCK ISLAND	69
% 33 WANAPUM	70
% 34 PRIEST RAPIDS	71
% 35 OXBOW	72
% 36 LOWER GRANITE	76
% 37 LITTLE GOOSE	77
% 38 LOWER MONUMENTAL	78
% 39 ICE HARBOR	79
% 40 MCNARY	80
% 41 JOHN DAY	81
% 42 DALLES	82
% 43 BONNEVILLE	83
% 44 HELLS CANYON	84
% 45 PELTON	95
% 46 PRIEST LAKE	146
% 47 BONNERS FERRY	400

%Simulated unregulated flows for The Dalles. These flows are used to
%adjust rule curves for storage reservoirs. In reality, ESP FORECASTS are
%used-- but for now, the model assumes that BPA/USACE gets the forecast
%exactly right.
TDA_unreg = d(:,48);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Additional input to fix the model
%
%Fix No.1 Kerr Dam lack of input from CFM
CFM5L= d(:,49);%add to Kerr
%
%Fix No.2 Lower Granite lack of input from 5 sources
%Following will be add ti LWG
ORF5H= d(:,50);
SPD5L= d(:,51);
ANA5L= d(:,52);
LIM5L= d(:,53);
WHB5H= d(:,54);
%
%Fix No.3 lack of input McNary
%
YAK5H= d(:,55);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Flood control curves
MCD_fc = xlsread('PNW_hydro/FCRPS/res_specs2.xlsx','Mica_Daily','B4:M368');
ARD_fc = xlsread('PNW_hydro/FCRPS/res_specs2.xlsx','Arrow_Daily','B4:G368');
LIB_fc = xlsread('PNW_hydro/FCRPS/res_specs2.xlsx','Libby_Daily','B4:F368');
DNC_fc = xlsread('PNW_hydro/FCRPS/res_specs2.xlsx','Duncan_Daily','B4:F368');
HHO_fc = xlsread('PNW_hydro/FCRPS/res_specs2.xlsx','HungryHorse_Daily','B4:I368');
ALB_fc = xlsread('PNW_hydro/FCRPS/res_specs2.xlsx','Albeni_Daily','B4:C368');
GCL_fc = xlsread('PNW_hydro/FCRPS/res_specs2.xlsx','GrandCoulee_Daily','B4:J368');
BRN_fc = xlsread('PNW_hydro/FCRPS/res_specs2.xlsx','Brownlee_Daily','B4:U368');
DWR_fc = xlsread('PNW_hydro/FCRPS/res_specs2.xlsx','Dworshak_Daily','B4:K368');


%Read Other CRCs
LIB_CRC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','LIB_CRC', 'A1:B365');
LIB_ARC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','LIB_ARC', 'A1:B365');
% COR_CRC_hm3 = xlsread('ORC.xlsx','COR_CRC', 'A1:B365');
HHO_CRC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','HHO_CRC', 'A1:B365');
HHO_ARC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','HHO_ARC', 'A1:B365');
% KER_CRC_hm3 = xlsread('ORC.xlsx','KER_CRC', 'A1:B365');
ALF_CRC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','ALF_CRC', 'A1:B365');
ALF_ARC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','ALF_ARC', 'A1:B365');
GCL_CRC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','GCL_CRC', 'A1:B365');
GCL_ARC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','GCL_ARC', 'A1:B365');
% CHL_CRC_hm3 = xlsread('ORC.xlsx','CHL_CRC', 'A1:B365');
BRN_CRC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','BRN_CRC', 'A1:B365');
BRN_ARC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','BRN_ARC', 'A1:B365');
DWR_CRC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','DWR_CRC', 'A1:B365');
DWR_ARC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','DWR_ARC', 'A1:B365');
%convert to kAF
%Read Duncan's ARC and CRC (in hm3)

DNC_ARC_hm3= xlsread('PNW_hydro/FCRPS/ORC.xlsx','Duncan_ARC', 'A1:B365');
DNC_CRC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','Duncan_CRC', 'A1:B365');

DNC_ARC(:,2) =1.23*DNC_ARC_hm3(:,2) ;
DNC_CRC(:,2) =1.23*DNC_CRC_hm3(:,2) ;

%Read Arror's ARC and CRC (in hm3)

ARD_ARC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','ARD_ARC', 'A1:B365');
ARD_CRC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','ARD_CRC', 'A1:B365');
%Read Mica's ARC and CRC (in hm3)
MCD_ARC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','MCD_ARC', 'A1:B365');
MCD_CRC_hm3 = xlsread('PNW_hydro/FCRPS/ORC.xlsx','MCD_CRC', 'A1:B365');

%convert to kAF
DNC_ARC(:,1) =DNC_ARC_hm3(:,1) ;
DNC_CRC(:,1) =DNC_CRC_hm3(:,1) ;

ARD_ARC(:,1) =ARD_ARC_hm3(:,1) ;
ARD_CRC(:,1) =ARD_CRC_hm3(:,1) ;

MCD_ARC(:,1) =MCD_ARC_hm3(:,1) ;
MCD_CRC(:,1) =MCD_CRC_hm3(:,1) ;

DNC_ARC(:,2) =1.23*DNC_ARC_hm3(:,2) ;
DNC_CRC(:,2) =1.23*DNC_CRC_hm3(:,2) ;

ARD_ARC(:,2) =1.23*ARD_ARC_hm3(:,2) ;
ARD_CRC(:,2) =1.23*ARD_CRC_hm3(:,2) ;

MCD_ARC(:,2) =1.23*MCD_ARC_hm3(:,2) ;
MCD_CRC(:,2) =1.23*MCD_CRC_hm3(:,2) ;


 LIB_CRC(:,1) =LIB_CRC_hm3(:,1) ;
 LIB_ARC(:,1) =LIB_ARC_hm3(:,1) ;
 
% COR_CRC(:,1) =COR_CRC_hm3(:,1) ;
 HHO_CRC(:,1) =HHO_CRC_hm3(:,1) ;
 HHO_ARC(:,1) =HHO_ARC_hm3(:,1) ;
 
% KER_CRC(:,1) =KER_CRC_hm3(:,1) ;
 ALB_CRC(:,1) =ALF_CRC_hm3(:,1) ;
 ALB_ARC(:,1) =ALF_ARC_hm3(:,1) ;
 
 GCL_CRC(:,1) =GCL_CRC_hm3(:,1) ;
 GCL_ARC(:,1) =GCL_ARC_hm3(:,1) ;
 
 BRN_CRC(:,1) =BRN_CRC_hm3(:,1) ;
 BRN_ARC(:,1) =BRN_ARC_hm3(:,1) ;
 
DWR_CRC(:,1) =DWR_CRC_hm3(:,1) ;
DWR_ARC(:,1) =DWR_ARC_hm3(:,1) ;
% 
 LIB_CRC(:,2) =1.23*LIB_CRC_hm3(:,2) ;
 LIB_ARC(:,2) =1.23*LIB_ARC_hm3(:,2) ;
 
% COR_CRC(:,2) =1.23*COR_CRC_hm3(:,2) ;
 HHO_CRC(:,2) =1.23*HHO_CRC_hm3(:,2) ;
 HHO_ARC(:,2) =1.23*HHO_ARC_hm3(:,2) ;
% KER_CRC(:,2) =1.23*KER_CRC_hm3(:,2) ;
 ALB_CRC(:,2) =1.23*ALF_CRC_hm3(:,2) ;
 ALB_ARC(:,2) =1.23*ALF_ARC_hm3(:,2) ;
GCL_CRC(:,2) =1.23*GCL_CRC_hm3(:,2) ;
BRN_CRC(:,2) =1.23*BRN_CRC_hm3(:,2) ;
GCL_ARC(:,2) =1.23*GCL_ARC_hm3(:,2) ;
BRN_ARC(:,2) =1.23*BRN_ARC_hm3(:,2) ;
DWR_CRC(:,2) =1.23*DWR_CRC_hm3(:,2) ;
DWR_ARC(:,2) =1.23*DWR_ARC_hm3(:,2) ;
%Spillway storage levels (kAF). 

d=xlsread('PNW_hydro/FCRPS/res_specs3.xlsx');
s_max = d(:,2);

%Maximum Hydraulic Capacity
d=xlsread('PNW_hydro/FCRPS/res_specs2.xlsx','HydraulicMax');
f_max = d(:,4)*0.8;

%Storage-elevation curves
d = xlsread('PNW_hydro/FCRPS/res_specs.xlsx','StorEq');
StorEq = d;

%Outflow-tailwater elevation curves
d = xlsread('PNW_hydro/FCRPS/res_specs.xlsx','TailEq');
TailEq = d;

%Starting storage levels(kAF).
%Note: model starts August 1, 1928, so reservoirs are assumed full to start.
s_1= s_max(1);
s_2=s_max(2);
s_3=s_max(3);
s_4=s_max(4);
s_5=s_max(5);
s_6=s_max(6);
s_7=s_max(7);
s_8=s_max(8);
s_9=s_max(9);
s_10=s_max(10);
s_11=s_max(11);
s_12=s_max(12);
s_13=s_max(13);
s_14=s_max(14);
s_15=s_max(15);
s_16=s_max(16);
s_17=s_max(17);
s_18=s_max(18);
s_19=s_max(19);
s_20=s_max(20);
s_21=s_max(21);
s_22=s_max(22);
s_23=s_max(23);
s_24=s_max(24);
s_25=s_max(25);
s_26=s_max(26);
s_27=s_max(27);
s_28=s_max(28);
s_29=s_max(29);
s_30=s_max(30);
s_31=s_max(31);
s_32=s_max(32);
s_33=s_max(33);
s_34=s_max(34);
s_35=s_max(35);
s_36=s_max(36);
s_37=s_max(37);
s_38=s_max(38);
s_39=s_max(39);
s_40=s_max(40);
s_41=s_max(41);
s_42=s_max(42);
s_43=s_max(43);
s_44=s_max(44);
s_45=s_max(45);
s_46=s_max(46);
s_47=s_max(47);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Miscellaneous input data/variables
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%MCD_fctarget; %Target daily storage value at Mica
%ICFs = xlsread('TDA5ARF_daily.xlsx','syntheticICFs');
ICFs=csvread('PNW_hydro/FCRPS/ICFcal.csv');
%floodyear; %Flood control year (spring)
%fillstart; %First day of refill period
sim_days = no_days - 365; %has to be 1 year shorter because of reliance on forecasts in system operations

%One water year contains 14 periods
p1=213:227;  %Aug 1 - Agu 15
p2=228:243;  %Aug 16 - Aug 31
p3=244:273;  %Sep
p4=274:304;  %Oct
p5=305:334;  %Nov
p6=335:365;  %Dec
p7=1:31;     %Jan
p8=32:59;    %Feb
p9=60:90;    %Mar
p10=91:105;  %Apr 1 - Apr 15
p11=106:120; %Apr 16 - Apr 30 
p12=121:151; %May
p13=152:181; %Jun
p14=191:212; %Jul

%%%%%%%%%%%%%%%
%Output buckets
%%%%%%%%%%%%%%%
spokane_flow = zeros(sim_days,1);
storage = zeros(sim_days,47);
discharge = zeros(sim_days,47);
powerflow = zeros(sim_days,47);
spill = zeros(sim_days,47);
generation = zeros(sim_days,47);

%%%%%%%%%%%
%Daily Loop
%%%%%%%%%%%
for i = 1: sim_days
    
    %First: what julian day and year is it? (need this for all sorts of stuff)
    julian = julians(i);
    year = years(i);

    %When does the initial controlled flood (ICF) occur? This refers to the
    %first instance of simulated unregulated flows at The Dalles reaching
    %450,000cfs. 20 days prior to the ICF marks the start of refill period for storage projects. 
    if julian<182
        floodyear = year;
    else
        floodyear = min(year+1,no_years);
    end
    ICF = ICFs(floodyear);
    fillstart = max(ICF - 20,0);

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Add new fillstart day
    %
    fillstart_ARD = max(ICF-2,0); %Arrow
    fillstart_DNC = max(ICF-10,0); %Duncan
    fillstart_LIB = max(ICF-10,0);%Libby
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Is it spring (January 1 - June 30) or fall (September 1 - December 31)
    spring = julian<182;

    %Calculate "forecasted" unregulated flows at The Dalles (April -
    %August)
    if spring>0
        TDA_for = sum(TDA_unreg((year-2)*365+213:(year-2)*365+365));
    else
        TDA_for = sum(TDA_unreg((year-1)*365+213:(year-1)*365+365));
    end

    %Convert forecast to kAF
    TDA_for = TDA_for*.001987;

    %%%%%%%%%%%%%%%%%%%%%%%%
    %SPOKANE RIVER PROJECTS%
    %Post Falls, Upper Falls, Monroe St.,Nine Mile, Long Lake, and Little
    %Falls%
    %Note: No information regarding storage, release constraints or other
    %operational characteristics is availabe for these dams. As such, they are
    %all modeled as run-of-river (outflows = inflows).

            
    %Post Falls - run of river project
    discharge(i,9) = local(i,9);
    powerflow(i,9) = min(f_max(9),discharge(i,9)*.001987);
    spill(i,9) = max(0,discharge(i,9)*.001987-f_max(9));
    storage(i,9) = s_9;
    
    %Power production
    %Relies on equation P = nphrgk
    %where, P - power (W)
    %p = density of water (1000kg/m^3)
    %h = hydraulic head
    %r = flow rate in m^3/s
    %g = acceleration due to gravity (9.81m/s^2)
    %k = coefficient of efficiency 
    
    %Convert powerflow to m^3/s.
    pf_trans = powerflow(i,9)*14.27641;
    %Averagy hourly power output (MWh)
    generation(i,9) = ((1000*19.812*pf_trans*9.81*.86)/1000000)*24;
    
    %Upper Falls - run of river project
    discharge(i,24) = local(i,24) + local(i,9);
    powerflow(i,24) = min(f_max(24),discharge(i,24)*.001987);
    spill(i,24) = max(0,discharge(i,24)*.001987-f_max(24));
    storage(i,24) = s_24;
    generation(i,24) = ((1000*19.812*powerflow(i,24)*14.27641*9.81*.73)/1000000)*24;
    
    %Monroe Street - run of river project
    discharge(i,25) = local(i,25) + local(i,24) + local(i,9);
    powerflow(i,25) = min(f_max(25),discharge(i,25)*.001987);
    spill(i,25) = max(0,discharge(i,25)*.001987-f_max(25));
    storage(i,25) = s_25;
    generation(i,25) = ((1000*23.1648*powerflow(i,25)*14.27641*9.81*.82)/1000000)*24;
    
    %Nine Mile - run of river project
    discharge(i,26) = local(i,26) + local(i,25) + local(i,24) + local(i,9);
    powerflow(i,26) = min(f_max(26),discharge(i,26)*.001987);
    spill(i,26) = max(0,discharge(i,26)*.001987-f_max(26));
    storage(i,26) = s_26;
    generation(i,26) = ((1000*20.42*powerflow(i,26)*14.27641*9.81*.71)/1000000)*24;
    
    %Long Lake - run of river project
    discharge(i,27) = local(i,27) + local(i,26) + local(i,25) + local(i,24) + local(i,9);
    powerflow(i,27) = min(f_max(27),discharge(i,27)*.001987);
    spill(i,27) = max(0,discharge(i,27)*.001987-f_max(27));
    storage(i,27) = s_27;
    generation(i,27) = ((1000*53.34*powerflow(i,27)*14.27641*9.81*.76)/1000000)*24;
    
    %Litle Falls - run of river project
    discharge(i,28) = local(i,28) + local(i,27) + local(i,26) + local(i,25) + local(i,24) + local(i,9);
    powerflow(i,28) = min(f_max(28),discharge(i,28)*.001987);
    spill(i,28) = max(0,discharge(i,28)*.001987-f_max(28));
    storage(i,28) = s_28; 
    generation(i,28) = ((1000*19.812*powerflow(i,28)*14.27641*9.81*.8)/1000000)*24;
    
    spokane_flow(i) = local(i,9) + local(i,24) + local(i,25) + local(i,26) + local(i,27) + local(i,28);

    %%%%%%%%%%%%%%%%%%%%%%%%%
    %UPPER COLUMBIA PROJECTS%
    %Mica, Revelstoke, Arrow

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Mica - storage reservor with flood control rule curve
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %Are we in evacuation or refill?
    %If ICF exists, then fill start date is ICF - 20.
    if fillstart>0
        evac = julian<fillstart || julian>243;
    %Otherwise just use schedule.
    else
        evac = julian<182 || julian>243;
    end

  
        
       %Calculate PDR
    if julian>=151 && julian <= 181;
          VPDR_MCD=22000;
         elseif julian >181 && julian <=212;
          VPDR_MCD = 30000;
         
       else
          VPDR_MCD=3000;
    end
     if i==1
          %MCD's storage forecaste
          MCD_sfore(i)=min((local(i,1)-VPDR_MCD)*.001987+s_1,s_max(1));
      else
          MCD_sfore(i)=min((local(i,1)-VPDR_MCD)*.001987+ storage(i-1,1),s_max(1));
     end
     
          MCD_VRC= MCD_sfore(i);%this is in kAF
          
           %Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182;

        % Calculate "forecasted" inflows to Mica (April - August)
        if spring>0
           MCD_for = sum(local((year-2)*365+213:(year-2)*365+365,1));
        else
           MCD_for = sum(local((year-1)*365+213:(year-1)*365+365,1));
        end

        %Convert forecast to kAF
        MCD_for = MCD_for*.001987;

        %Identify target reservoir storage. A number of flood control curves
        %are publically available. They are based on forecasted flows at The
        %Dalles and Mica Dam (April - August). Some interpolation is
        %necessary when the forecasted flows are in-between those specifiec by
        %USACE.

        if TDA_for <= 62000
            MCD_fctarget = MCD_fc(julian,1);
        elseif TDA_for > 62000 && TDA_for <= 65000
            MCD_fctarget = MCD_fc(julian,1) + ((TDA_for - 62000)/(65000-62000))*(MCD_fc(julian,2) - MCD_fc(julian,1));
        elseif TDA_for > 65000 && TDA_for <= 70000
            MCD_fctarget = MCD_fc(julian,2) + ((TDA_for - 65000)/(70000-65000))*(MCD_fc(julian,3) - MCD_fc(julian,2));
        elseif TDA_for > 70000 && TDA_for <= 75000
            MCD_fctarget = MCD_fc(julian,3) + ((TDA_for - 70000)/(75000-7000))*(MCD_fc(julian,4) - MCD_fc(julian,3));
        elseif TDA_for > 75000 && TDA_for <= 80000
            MCD_fctarget = MCD_fc(julian,4) + ((TDA_for - 75000)/(80000-75000))*(MCD_fc(julian,5) - MCD_fc(julian,4));
        elseif TDA_for > 80000 && TDA_for <= 105000
            MCD_fctarget = MCD_fc(julian,5);
        elseif TDA_for > 105000 %This is called "On Call" storage
            if MCD_for <= 8000
                MCD_fctarget = MCD_fc(julian,6);
            elseif MCD_for > 8000 && MCD_for <= 10000
                MCD_fctarget = MCD_fc(julian,6) + ((MCD_for - 8000)/(10000-8000))*(MCD_fc(julian,7) - MCD_fc(julian,6));
            elseif MCD_for > 10000 && MCD_for <= 12000
                MCD_fctarget = MCD_fc(julian,7) + ((MCD_for - 10000)/(12000-10000))*(MCD_fc(julian,8) - MCD_fc(julian,7));
            elseif MCD_for > 12000 && MCD_for <= 14000
                MCD_fctarget = MCD_fc(julian,8) + ((MCD_for - 12000)/(14000-12000))*(MCD_fc(julian,9) - MCD_fc(julian,8));
            elseif MCD_for > 14000 && MCD_for <= 16000
                MCD_fctarget = MCD_fc(julian,9) + ((MCD_for - 14000)/(16000-14000))*(MCD_fc(julian,10) - MCD_fc(julian,9));
            elseif MCD_for > 16000 && MCD_for <= 18000
                MCD_fctarget = MCD_fc(julian,10) + ((MCD_for - 16000)/(18000-16000))*(MCD_fc(julian,11) - MCD_fc(julian,10));
            elseif MCD_for > 18000
                MCD_fctarget = MCD_fc(julian,11);
            end    
        end
        
        %Calculate MCD's ORC
        if julian>=213 && julian <=365
           MCD_ORC(julian)= max(MCD_CRC(julian,2),MCD_ARC(julian,2));
           MCD_ORC(julian)= max(0,min(MCD_ORC(julian),MCD_fctarget));
       elseif julian >=1 && julian <= 212
           MCD_ORC(julian)= min(MCD_VRC,max(MCD_CRC(julian,2),MCD_ARC(julian,2)));
           MCD_ORC(julian)= max(0,min(MCD_ORC(julian),MCD_fctarget));
       else
           MCD_ORC(julian)=MCD_fctarget;
        end
       
        MCD_Julian(julian)=MCD_fctarget;
            if julian>=121 && julian<152;
                APDR_MCD=3478;
            elseif julian>= 152 && julian <182;
                APDR_MCD=6834;
            elseif julian >= 182 && julian <213
                APDR_MCD=42766;
            else
                APDR_MCD=3000;
            end
            
            %Which PDR are we using
       if julian>=213 && julian <=365
            MCD_PDR=APDR_MCD;
        elseif julian >=1 && julian <= 181
            if MCD_VRC<= max(MCD_CRC(julian,2),MCD_ARC(julian,2))
            MCD_PDR=VPDR_MCD;
            end
        else
            MCD_PDR=0;
        end
        
             
          
    if evac>0 
    %Evacuation mode
                          
        %Calculate daily reservoir discharge and end-of-day storage. Have to
        %convert project inflows ("local") to kAF. Note there is a seasonal
        %minimum flow value (MCD_min) associated with Mica Dam in order to
        %create adequate flows into Arrow Lake.
       
        %Mica's operating target based on Arrow's content
        if ismember(julian,p1)==1;
            if s_2>3300*3;
        MCD_min=15000*.001987;
               if s_1<3379.2*3
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=3300*3 && s_2>=1450*3;
         MCD_dg = 25000*.001987;
            elseif s_2<1450*3;
          MCD_dg = 32000*.001987;
            end
        elseif ismember(julian,p2)==1;
              if s_2>3060*3;
        MCD_min=15000*.001987;
               if s_1<3529.2*3
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=3060*3 && s_2>=1300*3;
         MCD_dg = 25000*.001987;
            elseif s_2<1300*3;
          MCD_dg = 32000*.001987;
              end
        elseif ismember(julian,p3)==1;
             if s_2>3570*3;
        MCD_min=10000*.001987;
               if s_1<3529.2*3
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=3570*3 && s_2>=3480*3;
        MCD_dg = 25000*.001987;
            elseif s_2<=3480*3 && s_2>=2140*3;
        MCD_dg = 27000*.001987;       
            elseif s_2<1450*3;
        MCD_dg = 32000*.001987;
             end
       elseif ismember(julian,p4)==1;
             if s_2>3450*3;
        MCD_min=10000*.001987;
               if s_1<3428.4*3;
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=3450*3 && s_2>=2860*3;
        MCD_dg = 21000*.001987;
            elseif s_2<=2860*3 && s_2>=1360*3;
        MCD_dg = 25000*.001987;       
            elseif s_2<1360*3;
        MCD_dg = 32000*.001987;
            end
       elseif ismember(julian,p5)==1;
             if s_2>3400*3;
        MCD_min=10000*.001987;
             
        MCD_dg = 22000*.001987;   
            elseif s_2<=3400*3 && s_2>=3030*3;
        MCD_dg = 19000*.001987;
            elseif s_2<=3030*3 && s_2>=1100*3;
        MCD_dg = 25000*.001987;       
            elseif s_2<1100*3;
        MCD_dg = 32000*.001987;
             end 
        elseif ismember(julian,p6)==1;
           if s_2>3240*3;
        if s_1<204.1*3;
              MCD_dg = 10000*.001987;
        else
             
        MCD_dg = 22000*.001987;   
        end
            elseif s_2<=3240*3 && s_2>=2400*3;
             if s_1<204.1*3;
              MCD_dg = 10000*.001987;
        else
             
        MCD_dg = 25000*.001987;   
        end
            elseif s_2<=2400*3 && s_2>=690*3;
               if s_1<204.1*3;
              MCD_dg = 10000*.001987;
        else
             
        MCD_dg = 26000*.001987;   
        end      
            elseif s_2<690*3;
               if s_1<204.1*3;
              MCD_dg = 10000*.001987;
        else
             
        MCD_dg = 32000*.001987;   
        end
           end 
        elseif ismember(julian,p7)==1;
         if s_2>2250*3;
        if s_1<204.1*3;
              MCD_dg = 12000*.001987;
        else
             
        MCD_dg = 24000*.001987;   
        end
            elseif s_2<=2500*3 && s_2>=2210*3;
             if s_1<204.1*3;
              MCD_dg = 12000*.001987;
        else
             
        MCD_dg = 26000*.001987;   
        end
            elseif s_2<=2210*3 && s_2>=1560*3;
               if s_1<204.1*3;
              MCD_dg = 12000*.001987;
        else
             
        MCD_dg = 28000*.001987;   
        end      
            elseif s_2<1560*3;
               if s_1<204.1*3;
              MCD_dg = 12000*.001987;
        else
             
        MCD_dg = 29000*.001987;   
        end
         end 
        elseif ismember(julian,p8)==1;
             if s_2>1370*3;
        
             
        MCD_dg = 21000*.001987;   
            elseif s_2<=1370*3 && s_2>=940*3;
        MCD_dg = 26000*.001987;
            elseif s_2<=940*3 && s_2>=850*3;
        MCD_dg = 22000*.001987;       
            elseif s_2<850*3;
        MCD_dg = 26000*.001987;
             end 
        elseif ismember(julian,p9)==1;
            if s_2>570*3;
        
             
        MCD_dg = 25000*.001987;   
            elseif s_2<=570*3 && s_2>=440*3;
        MCD_dg = 17000*.001987;
            elseif s_2<=440*3 && s_2>=160*3;
        MCD_dg = 21000*.001987;       
            elseif s_2<160*3;
        MCD_dg = 26000*.001987;
            end   
        elseif ismember(julian,p10)==1;
        if s_2>520*3;
        
             
        MCD_dg = 17000*.001987;   
            elseif s_2<=520*3 && s_2>=400*3;
        MCD_dg = 12000*.001987;
            elseif s_2<=400*3 && s_2>=20*3;
        MCD_dg = 15000*.001987;       
            elseif s_2<20*3;
        MCD_dg = 21000*.001987;
        end
        elseif ismember(julian,p11)==1;
        if s_2>890*3;
        
             
        MCD_dg = 10000*.001987;   
            elseif s_2<=890*3 && s_2>=490*3;
        MCD_dg = 12000*.001987;
            elseif s_2<=490*3 && s_2>=40*3;
        MCD_dg = 10000*.001987;       
            elseif s_2<40*3;
        MCD_dg = 15000*.001987;
        end    
        elseif ismember(julian,p12)==1;
        if s_2>160*3;
        
             
        MCD_dg = 8000*.001987;   
            elseif s_2<=160*3 && s_2>=20*3;
        MCD_dg = 10000*.001987;  
            elseif s_2<20*3;
        MCD_dg = 12000*.001987;
        end     
        elseif ismember(julian,p13)==1;
        if s_2>2140*3;
        
        MCD_dg =10000*.001987;   
            elseif s_2<=2140*3 && s_2>=1450*3;
        MCD_dg = 8000*.001987;  
            elseif s_2<=1450*3 && s_2>=1140*3;
        MCD_dg = 10000*.001987;  
            elseif s_2<1140*3;
        MCD_dg = 16000*.001987;
        end  
        elseif ismember(julian,p14)==1;
        if s_2>3110*3;
        MCD_min=10000*.001987;
               if s_1<3467.2*3;
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=3110*3 && s_2>=2880*3;
      MCD_min=10000*.001987;
               if s_1<3405.2*3;
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=2880*3 && s_2>=1650*3;
        MCD_dg = 22000*.001987;       
            elseif s_2<1650*3;
        MCD_dg = 24000*.001987;
            end
        end
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,MCD_dg - f_max(1));
        
        %Is any storage space available?
        stor_avail = MCD_ORC(julian) - s_1;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,1) = f_max(1);
            spill(i,1) = MCD_dg - f_max(1);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            MCD_dg = max(MCD_dg - stor_avail,f_max(1));
            powerflow(i,1) = f_max(1);
            spill(i,1) = max(0,MCD_dg - f_max(1));
        else 
            powerflow(i,1) = MCD_dg;
        end
        
        s_1 = s_1 + local(i,1)*.001987 - MCD_dg;
        discharge(i,1) = MCD_dg*(1/.001987); %Convert back to cfs
        storage(i,1) = s_1;

    else
    %Refill mode - this is when the reservoir fills back up during spring
    %floods. Only storage target is maximum reservoir storage (spillway
    %threshold).
    
           if ismember(julian,p1)==1;
            if s_2>3300*3;
        MCD_min=15000*.001987;
               if s_1<3379.2*3
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=3300*3 && s_2>=1450*3;
         MCD_dg = 25000*.001987;
            elseif s_2<1450*3;
          MCD_dg = 32000*.001987;
            end
        elseif ismember(julian,p2)==1;
              if s_2>3060*3;
        MCD_min=15000*.001987;
               if s_1<3529.2*3
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=3060*3 && s_2>=1300*3;
         MCD_dg = 25000*.001987;
            elseif s_2<1300*3;
          MCD_dg = 32000*.001987;
              end
        elseif ismember(julian,p3)==1;
             if s_2>3570*3;
        MCD_min=10000*.001987;
               if s_1<3529.2*3
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=3570*3 && s_2>=3480*3;
        MCD_dg = 25000*.001987;
            elseif s_2<=3480*3 && s_2>=2140*3;
        MCD_dg = 27000*.001987;       
            elseif s_2<1450*3;
        MCD_dg = 32000*.001987;
             end
       elseif ismember(julian,p4)==1;
             if s_2>3450*3;
        MCD_min=10000*.001987;
               if s_1<3428.4*3;
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=3450*3 && s_2>=2860*3;
        MCD_dg = 21000*.001987;
            elseif s_2<=2860*3 && s_2>=1360*3;
        MCD_dg = 25000*.001987;       
            elseif s_2<1360*3;
        MCD_dg = 32000*.001987;
            end
       elseif ismember(julian,p5)==1;
             if s_2>3400*3;
        MCD_min=10000*.001987;
             
        MCD_dg = 22000*.001987;   
            elseif s_2<=3400*3 && s_2>=3030*3;
        MCD_dg = 19000*.001987;
            elseif s_2<=3030*3 && s_2>=1100*3;
        MCD_dg = 25000*.001987;       
            elseif s_2<1100*3;
        MCD_dg = 32000*.001987;
             end 
        elseif ismember(julian,p6)==1;
           if s_2>3240*3;
        if s_1<204.1*3;
              MCD_dg = 10000*.001987;
        else
             
        MCD_dg = 22000*.001987;   
        end
            elseif s_2<=3240*3 && s_2>=2400*3;
             if s_1<204.1*3;
              MCD_dg = 10000*.001987;
        else
             
        MCD_dg = 25000*.001987;   
        end
            elseif s_2<=2400*3 && s_2>=690*3;
               if s_1<204.1*3;
              MCD_dg = 10000*.001987;
        else
             
        MCD_dg = 26000*.001987;   
        end      
            elseif s_2<690*3;
               if s_1<204.1*3;
              MCD_dg = 10000*.001987;
        else
             
        MCD_dg = 32000*.001987;   
        end
           end 
        elseif ismember(julian,p7)==1;
         if s_2>2250*3;
        if s_1<204.1*3;
              MCD_dg = 12000*.001987;
        else
             
        MCD_dg = 24000*.001987;   
        end
            elseif s_2<=2500*3 && s_2>=2210*3;
             if s_1<204.1*3;
              MCD_dg = 12000*.001987;
        else
             
        MCD_dg = 26000*.001987;   
        end
            elseif s_2<=2210*3 && s_2>=1560*3;
               if s_1<204.1*3;
              MCD_dg = 12000*.001987;
        else
             
        MCD_dg = 28000*.001987;   
        end      
            elseif s_2<1560*3;
               if s_1<204.1*3;
              MCD_dg = 12000*.001987;
        else
             
        MCD_dg = 29000*.001987;   
        end
         end 
        elseif ismember(julian,p8)==1;
             if s_2>1370*3;
        
             
        MCD_dg = 21000*.001987;   
            elseif s_2<=1370*3 && s_2>=940*3;
        MCD_dg = 26000*.001987;
            elseif s_2<=940*3 && s_2>=850*3;
        MCD_dg = 22000*.001987;       
            elseif s_2<850*3;
        MCD_dg = 26000*.001987;
             end 
        elseif ismember(julian,p9)==1;
            if s_2>570*3;
        
             
        MCD_dg = 25000*.001987;   
            elseif s_2<=570*3 && s_2>=440*3;
        MCD_dg = 17000*.001987;
            elseif s_2<=440*3 && s_2>=160*3;
        MCD_dg = 21000*.001987;       
            elseif s_2<160*3;
        MCD_dg = 26000*.001987;
            end   
        elseif ismember(julian,p10)==1;
        if s_2>520*3;
        
             
        MCD_dg = 17000*.001987;   
            elseif s_2<=520*3 && s_2>=400*3;
        MCD_dg = 12000*.001987;
            elseif s_2<=400*3 && s_2>=20*3;
        MCD_dg = 15000*.001987;       
            elseif s_2<20*3;
        MCD_dg = 21000*.001987;
        end
        elseif ismember(julian,p11)==1;
        if s_2>890*3;
        
             
        MCD_dg = 10000*.001987;   
            elseif s_2<=890*3 && s_2>=490*3;
        MCD_dg = 12000*.001987;
            elseif s_2<=490*3 && s_2>=40*3;
        MCD_dg = 10000*.001987;       
            elseif s_2<40*3;
        MCD_dg = 15000*.001987;
        end    
        elseif ismember(julian,p12)==1;
        if s_2>160*3;
        
             
        MCD_dg = 8000*.001987;   
            elseif s_2<=160*3 && s_2>=20*3;
        MCD_dg = 10000*.001987;  
            elseif s_2<20*3;
        MCD_dg = 12000*.001987;
        end     
        elseif ismember(julian,p13)==1;
        if s_2>2140*3;            
        MCD_dg =10000*.001987;   
            elseif s_2<=2140*3 && s_2>=1450*3;
        MCD_dg = 8000.001987;  
            elseif s_2<=1450*3 && s_2>=1140*3;
        MCD_dg = 10000*.001987;  
            elseif s_2<1140*3;
        MCD_dg = 16000*.001987;
        end  
        elseif ismember(julian,p14)==1;
        if s_2>3110*3;
        MCD_min=10000*.001987;
               if s_1<3467.2*3;
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=3110*3 && s_2>=2880*3;
      MCD_min=10000*.001987;
               if s_1<3405.2*3;
                   MCD_max=34000*.001987;
               end
        MCD_dg = min(MCD_max,max(max(max(MCD_min - local(i,16),local(i,16)),MCD_PDR)*.001987, s_1 + local(i,1)*.001987 - MCD_ORC(julian)));   
            elseif s_2<=2880*3 && s_2>=1650*3;
        MCD_dg = 22000*.001987;       
            elseif s_2<1650*3;
        MCD_dg = 24000*.001987;
            end
        end
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,MCD_dg - f_max(1));
        
        %Is any storage space available?
        stor_avail = s_max(1) - s_1;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,1) = f_max(1);
            spill(i,1) = MCD_dg - f_max(1);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            MCD_dg = max(MCD_dg - stor_avail,f_max(1));
            powerflow(i,1) = f_max(1);
            spill(i,1) = max(0,MCD_dg - f_max(1));
        else 
            powerflow(i,1) = MCD_dg;
        end
    
    s_1 = s_1 + local(i,1)*.001987 - MCD_dg;
    discharge(i,1) = MCD_dg*(1/.001987);
    storage(i,1) = s_1;     

    end
    
    generation(i,1) = ((1000*240.1824*powerflow(i,1)*14.27641*9.81*.875)/1000000)*24;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Revelstoke Dam - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    RVC_dg = MCD_dg + local(i,16)*.001987;
    s_16 = s_16 + MCD_dg + local(i,16)*.001987 - RVC_dg;
    powerflow(i,16) = min(RVC_dg,f_max(16));
    spill(i,16) = max(0,RVC_dg - f_max(16));
    discharge(i,16) = RVC_dg*(1/.001987);
    storage(i,16) = s_16; 
    generation(i,16) = ((1000*174.9552*powerflow(i,16)*14.27641*9.81*.875)/1000000)*24;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Arrow (H. Keenleyside) Dam - storage project 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %Are we in evacuation or refill?
    %If ICF exists, then fill start date is ICF - 20.
    if fillstart>0
        evac = julian<fillstart || julian>243;
    %Otherwise just use schedule.
    else
        evac = julian<182 || julian>243;
    end
    
    
      
        %A wide range of TDA forecast that will be used in later modelling
         if spring>0
           TDA_for_ARD_Feb=sum(TDA_unreg((year-2)*365+154:(year-2)*365+334));
           TDA_for_ARD_Mar=sum(TDA_unreg((year-2)*365+182:(year-2)*365+334));
           TDA_for_ARD_Apr=sum(TDA_unreg((year-2)*365+213:(year-2)*365+334));
           TDA_for_ARD_May=sum(TDA_unreg((year-2)*365+243:(year-2)*365+334));
           TDA_for_ARD_Jun=sum(TDA_unreg((year-2)*365+274:(year-2)*365+334));
           TDA_for_ARD=sum(TDA_unreg((year-2)*365+123:(year-2)*365+334));
        else
           TDA_for_ARD_Feb=sum(TDA_unreg((year-1)*365+154:(year-1)*365+334));
           TDA_for_ARD_Mar=sum(TDA_unreg((year-1)*365+182:(year-1)*365+334));
           TDA_for_ARD_Apr=sum(TDA_unreg((year-1)*365+213:(year-1)*365+334));
           TDA_for_ARD_May=sum(TDA_unreg((year-1)*365+243:(year-1)*365+334));
           TDA_for_ARD_Jun=sum(TDA_unreg((year-1)*365+274:(year-1)*365+334));
           TDA_for_ARD=sum(TDA_unreg((year-1)*365+123:(year-1)*365+334));
         end
          TDA_for_ARD= TDA_for_ARD*1.9835/1000000;
          
            %Set boundries
         if TDA_for_ARD <= 80;
          TDA_for_ARD = 80;
      elseif TDA_for_ARD >= 110;
          TDA_for_ARD =110;
         end
         
         %Minimun flow for Arrow
         if julian>=1 && julian <=31;
             ARD_min=10001;
         elseif julian >=32 && julian <=90;
             ARD_min=19998;
         elseif julian >=91 && julian <=105;
             ARD_min=15001;
         elseif julian >= 106 && julian <=120;
             ARD_min=11999;
         elseif julian >=121 && julian <= 151;
             ARD_min=10001;
         elseif julian >=152 && julian <=181;
             ARD_min=5000;
         else
             ARD_min=10001;
         end
         
         %Calculate PDR
      if julian>=151 && julian <= 181;
          VPDR_ARD=42000;
      elseif julian >181 && julian <=212;
          VPDR_ARD = 53000;
          %Above is liner extrapolation from data
       else
          VPDR_ARD=5000;
      end
      %Calculate VRC
      %inflow is RVC_dg + local(i,2) out flow is VPDR or APDR
      if i==1
          %ARD's storage forecaste
          ARD_sfore(i)=min((local(i,2)-VPDR_ARD)*.001987+s_2,s_max(2));
      else
          ARD_sfore(i)=min(RVC_dg +(local(i,2)-VPDR_ARD)*.001987+ storage(i-1,2),s_max(2));
      end
      
         ARD_VRC= ARD_sfore(i);%this is in kAF
      
        %Identify target reservoir storage. A number of flood control curves
        %are publically available. They are based on forecasted flows at The
        %Dalles. Some interpolation is
        %necessary when the forecasted flows are in-between those specifiec by
        %USACE.

        if TDA_for <= 64000
            ARD_fctarget = ARD_fc(julian,1);
        elseif TDA_for > 64000 && TDA_for <= 65000
            ARD_fctarget = ARD_fc(julian,1) + ((TDA_for - 64000)/(65000-64000))*(ARD_fc(julian,2) - ARD_fc(julian,1));
        elseif TDA_for > 65000 && TDA_for <= 70000
            ARD_fctarget = ARD_fc(julian,2) + ((TDA_for - 65000)/(70000-65000))*(ARD_fc(julian,3) - ARD_fc(julian,2));
        elseif TDA_for > 70000 && TDA_for <= 75000
            ARD_fctarget = ARD_fc(julian,3) + ((TDA_for - 70000)/(75000-7000))*(ARD_fc(julian,4) - ARD_fc(julian,3));
        elseif TDA_for > 75000 && TDA_for <= 80000
            ARD_fctarget = ARD_fc(julian,4) + ((TDA_for - 75000)/(80000-75000))*(ARD_fc(julian,5) - ARD_fc(julian,4));
        elseif TDA_for > 80000 && TDA_for <= 111000
            ARD_fctarget = ARD_fc(julian,5) + ((TDA_for - 80000)/(111000-80000))*(ARD_fc(julian,6) - ARD_fc(julian,5));
        else
            ARD_fctarget = ARD_fc(julian,6);    
        end
       
        %Calculate ORC
       if julian>=213 && julian <=365
           ARD_ORC(julian)= max(ARD_CRC(julian,2),ARD_ARC(julian,2));
           ARD_ORC(julian)= min(ARD_ORC(julian),ARD_fctarget);
       elseif julian >=1 && julian <= 212
           ARD_ORC(julian)= min(ARD_VRC,max(ARD_CRC(julian,2),ARD_ARC(julian,2)));
           ARD_ORC(julian)= min(ARD_ORC(julian),ARD_fctarget);
       else
           ARD_ORC(julian)=ARD_fctarget;
       end
    if evac>0 
    %Evacuation mode

     
        %Calculate daily reservoir discharge and end-of-day storage. Have to
        %convert project inflows ("local") to kAF.
        ARD_dg = max(ARD_min*.001987, s_2 + RVC_dg + local(i,2)*.001987 - ARD_ORC(julian));
        
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,ARD_dg - f_max(2));
        
        %Is any storage space available?
        stor_avail = ARD_ORC(julian) - s_2;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,2) = f_max(2);
            spill(i,2) = ARD_dg - f_max(2);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            ARD_dg = max(ARD_dg - stor_avail,f_max(2));
            powerflow(i,2) = f_max(2);
            spill(i,2) = max(0,ARD_dg - f_max(2));
        else 
            powerflow(i,2) = ARD_dg;
        end
        
        s_2 = s_2 + RVC_dg + local(i,2)*.001987 - ARD_dg;
        discharge(i,2) = ARD_dg*(1/.001987); %Convert back to cfs
        storage(i,2) = s_2;

    else
    %Refill mode - this is when the reservoir fills back up during spring
    %floods. Only storage target is maximum reservoir storage (spillway
    %threshold).

    ARD_dg = max(ARD_min*.001987, s_2 + RVC_dg + local(i,2)*.001987 - s_max(2));
    
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,ARD_dg - f_max(2));
        
        %Is any storage space available?
        stor_avail = s_max(2) - s_2;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,2) = f_max(2);
            spill(i,2) = ARD_dg - f_max(2);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            ARD_dg = max(ARD_dg - stor_avail,f_max(2));
            powerflow(i,2) = f_max(2);
            spill(i,2) = max(0,ARD_dg - f_max(2));
        else 
            powerflow(i,2) = ARD_dg;
        end
    
    s_2 = s_2 + RVC_dg + local(i,2)*.001987 - ARD_dg;
    discharge(i,2) = ARD_dg*(1/.001987);
    storage(i,2) = s_2;     

    end
    
    generation(i,2) = ((1000*52.1208*powerflow(i,2)*14.27641*9.81*.875)/1000000)*24;

    %%%%%%%%%%%%%%%%%%%
    %KOOTENAI PROJECTS%
    %Libby, Bonner's Ferry, Duncan, Corra Linn, and Brilliant

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Duncan - storage reservoir with flood control rule curve
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Note: Duncan has no hydroelectric generation capability.

    %Are we in evacuation or refill?
    %If ICF exists, then fill start date is ICF - 20.
    if fillstart>0
        evac = julian<fillstart_LIB || julian>243;
    %Otherwise just use schedule.
    else
        evac = julian<182 || julian>243;
    end
    %Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182;

       if spring>0
           TDA_for_DNC=sum(TDA_unreg((year-2)*365+123:(year-2)*365+334));
           DNC_for = sum(local((year-2)*365+213:(year-2)*365+365,4));
        else
           DNC_for = sum(local((year-1)*365+213:(year-1)*365+365,4));
           TDA_for_DNC=sum(TDA_unreg((year-1)*365+123:(year-1)*365+334));
        end
      %Convert from cfs to mAF
      TDA_for_DNC= TDA_for_DNC*1.9835/1000000;
     
    if evac>0 
    %Evacuation mode

    
      %Calculate PDR
      if TDA_for_DNC <= 80;
          TDA_for_DNC = 80;
      elseif TDA_for_DNC >= 110;
          TDA_for_DNC =110;
      end
        
          %from Jan 1 to May 30 the value is all 100 cfs
      if julian>=1 && julian <= 151;
          VPDR_DNC=100;
      elseif julian >151 && julian <=181;
          VPDR_DNC = 1200- (1/3)*(TDA_for_DNC-80);
          %Above is liner extrapolation from data
      elseif julian >181 && julian <=212
          VPDR_DNC=2400;
      else
          VPDR_DNC=0;
      end
      
      %Calculate VRC
      %inflow is just local(i,4) out flow is VPDR or APDR
      if i==1
          %DNC's storage forecaste
          DNC_sfore(i)=min((local(i,4)-VPDR_DNC)*.001987+s_4,s_max(4));
      else
          DNC_sfore(i)=min((local(i,4)-VPDR_DNC)*.001987+ storage(i-1,4),s_max(4));
      end
          DNC_VRC= DNC_sfore(i);%this is in kAF

        %Identify target reservoir storage. A number of flood control curves
        %are publically available. They are based on forecasted inflows. Some interpolation is
        %necessary when the forecasted flows are in-between those specifiec by
        %USACE.

        if DNC_for <= 1400
            DNC_fctarget = DNC_fc(julian,1);
        elseif DNC_for > 1400 && DNC_for <= 1600
            DNC_fctarget = DNC_fc(julian,1) + ((DNC_for - 1400)/(1600-1400))*(DNC_fc(julian,2) - DNC_fc(julian,1));
        elseif DNC_for > 1600 && DNC_for <= 1800
            DNC_fctarget = DNC_fc(julian,2) + ((DNC_for - 1600)/(1800-1600))*(DNC_fc(julian,3) - DNC_fc(julian,2));
        elseif DNC_for > 1800 && DNC_for <= 2000
            DNC_fctarget = DNC_fc(julian,3) + ((DNC_for - 1800)/(2000-1800))*(DNC_fc(julian,4) - DNC_fc(julian,3));
        elseif DNC_for > 2000 && DNC_for <= 2200
            DNC_fctarget = DNC_fc(julian,4) + ((DNC_for - 2000)/(2200-2000))*(DNC_fc(julian,5) - DNC_fc(julian,4));
        elseif DNC_for > 2200 
            DNC_fctarget = DNC_fc(julian,5); 
        end
        
     if julian>=213 && julian <=365
           DNC_ORC(julian)= max(DNC_CRC(julian,2),DNC_ARC(julian,2));
           DNC_ORC(julian)= min(DNC_ORC(julian),DNC_fctarget);
        elseif julian >=1 && julian <= 212
            DNC_ORC(julian)= min(DNC_VRC,max(DNC_CRC(julian,2),DNC_ARC(julian,2)));
            DNC_ORC(julian)= min(DNC_ORC(julian),DNC_fctarget);
       else
           DNC_ORC(julian)=DNC_fctarget;
       end
        %Calculate daily reservoir discharge and end-of-day storage. Have to
        %convert project inflows ("local") to kAF.
        DNC_dg = max(0, s_4 + local(i,4)*.001987 - DNC_ORC(julian));
        s_4 = s_4 + local(i,4)*.001987 - DNC_dg;
        discharge(i,4) = DNC_dg*(1/.001987); %Convert back to cfs
        storage(i,4) = s_4;

    else
    %Refill mode - this is when the reservoir fills back up during spring
    %floods. Only storage target is maximum reservoir storage (spillway
    %threshold).

    DNC_dg = max(0, s_4 + local(i,4)*.001987 - s_max(4));
    s_4 = s_4 + local(i,4)*.001987 - DNC_dg;
    discharge(i,4) = DNC_dg*(1/.001987);
    storage(i,4) = s_4;     

    end
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Libby - storage reservor with flood control rule curve
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %Are we in evacuation or refill?
    %If ICF exists, then fill start date is ICF - 20.
    if fillstart_LIB>0
        evac = julian<fillstart_LIB || julian>244;
    %Otherwise just use schedule.
    else
        evac = julian<120 || julian>244; %I changed this from 180 to 120 and 273 to 304
    end
       
     %Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182;

        % Calculate "forecasted" inflows to Libby (April - August)
        if spring>0
           LIB_for = sum(local((year-2)*365+213:(year-2)*365+365,3));
           if fillstart_LIB>0
           ICF_D=TDA_unreg((year-2)*365 + fillstart_LIB + 132)/1000;% this is cfs
           else
           ICF_D=TDA_unreg((year-2)*365 + 110 + 132)/1000;
           end
           %below is used to check which curve needs to be applied
           TDA_for_LIB_B= sum(TDA_unreg((year-2)*365+213:(year-2)*365+365));
        else
           LIB_for = sum(local((year-1)*365+213:(year-1)*365+365,3));
           if fillstart_LIB>0
           ICF_D=TDA_unreg((year-1)*365 + fillstart_LIB + 132)/1000;% this is cfs
           else
           ICF_D=TDA_unreg((year-1)*365 + 110 + 132)/1000;
           %ICF_D=TDA_unreg((year-1)*365+120)/1000;
           end
           TDA_for_LIB_B =sum(TDA_unreg((year-1)*365+213:(year-1)*365+365));
        end
        %Convert forecast to kAF
         LIB_for = LIB_for*.001987;
         
       %Calculate PDR Can use Duncan's value
      if TDA_for_DNC <= 80;
          TDA_for_DNC = 80;
      elseif TDA_for_DNC >= 110;
          TDA_for_DNC =110;
      end
        
          %from Jan 1 to May 30 the value is all 4000 cfs
      if julian>=1 && julian <= 151;
          VPDR_LIB=4000;
      elseif julian >151 && julian <=181;
          VPDR_LIB = 9000;
          %Above is liner extrapolation from data
      elseif julian >181 && julian <=212
          VPDR_LIB=10000;
      else
          VPDR_LIB=0;
      end
      
      %Calculate VRC
      %inflow is just local(i,3) out flow is VPDR or APDR
      if i==1
          %DNC's storage forecaste
          LIB_sfore(i)=min((local(i,3)-VPDR_LIB)*.001987+s_3,s_max(3));
      else
          LIB_sfore(i)=min((local(i,3)-VPDR_LIB)*.001987+ storage(i-1,3),s_max(3));
      end
          LIB_VRC= LIB_sfore(i);%this is in kAF
    %Identify target reservoir storage. A number of flood control curves
        %are publically available. They are based on forecasted inflows. Some interpolation is
        %necessary when the forecasted flows are in-between those specifiec by
        %USACE.
       
        if LIB_for <= 4500
            LIB_fctarget = LIB_fc(julian,1);
        elseif LIB_for > 4500 && LIB_for <= 5500
            LIB_fctarget = LIB_fc(julian,1) + ((LIB_for - 4500)/(5500-4500))*(LIB_fc(julian,2) - LIB_fc(julian,1));
        elseif LIB_for > 5500 && LIB_for <= 6500
            LIB_fctarget = LIB_fc(julian,2) + ((LIB_for - 5500)/(6500-5500))*(LIB_fc(julian,3) - LIB_fc(julian,2));
        elseif LIB_for > 6500 && LIB_for <= 7500
            LIB_fctarget = LIB_fc(julian,3) + ((LIB_for - 6500)/(7500-6500))*(LIB_fc(julian,4) - LIB_fc(julian,3));
        elseif LIB_for > 7500 && LIB_for <= 8000
            LIB_fctarget = LIB_fc(julian,4) + ((LIB_for - 7500)/(8000-7500))*(LIB_fc(julian,5) - LIB_fc(julian,4));
        elseif LIB_for > 8000 
            LIB_fctarget = LIB_fc(julian,5); 
        end
   
        if julian>=213 && julian <=365
           LIB_ORC(julian)= max(LIB_CRC(julian,2),LIB_ARC(julian,2));
           LIB_ORC(julian)= min(LIB_ORC(julian),LIB_fctarget);
        elseif julian >=1 && julian <= 212
            LIB_ORC(julian)= min(LIB_VRC,max(LIB_CRC(julian,2),LIB_ARC(julian,2)));
            LIB_ORC(julian)= min(LIB_ORC(julian),LIB_fctarget);
       else
           LIB_ORC(julian)=LIB_fctarget;
        end
         
           LIB_ORC(julian)=max(0,LIB_ORC(julian));


           TDA_for_LIB_B = TDA_for_LIB_B * .001987; %in kAF
           %Calculate initial controlled flow at Dalls
           
                    
           if ICF_D<350 
               ICF_D=350;
           end
           %Calculate Libby flood control duration
           if ICF_D>=350 &&ICF_D<400  %Use curve 1
              TDA_for_LIB_B =max(TDA_for_LIB_B,70000);
              if TDA_for_LIB_B >= 70000 && TDA_for_LIB_B<= 100000;
                  FCD_LIB=0.00233333*(TDA_for_LIB_B-70000);
              elseif TDA_for_LIB_B > 100000 && TDA_for_LIB_B <=110000
                  FCD_LIB = 70+ (0.001*(TDA_for_LIB_B-100000));
              elseif TDA_for_LIB_B > 110000 && TDA_for_LIB_B <=140000
                  FCD_LIB = 80+ (0.005*(TDA_for_LIB_B-110000));
              elseif TDA_for_LIB_B > 140000 && TDA_for_LIB_B <=200000
                  FCD_LIB = 95+ (0.0025*(TDA_for_LIB_B-110000));
              end
           elseif ICF_D>=400 && ICF_D<450 %Use curve 2
               if TDA_for_LIB_B>= 80000 && TDA_for_LIB_B<= 100000;
                  FCD_LIB=0.003*(TDA_for_LIB_B-80000);
              elseif TDA_for_LIB_B >100000 && TDA_for_LIB_B <=145000
                  FCD_LIB = 60 + (0.00556*(TDA_for_LIB_B-100000));
              elseif TDA_for_LIB_B >145000 && TDA_for_LIB_B <=200000
                  FCD_LIB = 85+ (0.001818*(TDA_for_LIB_B-145000));
               end
           
              %FCD is flood control duration
           elseif ICF_D >=450 %Use curve 3
               if TDA_for_LIB_B>= 80000 && TDA_for_LIB_B <= 100000;
                  FCD_LIB=0.0025*(TDA_for_LIB_B-80000);
              elseif TDA_for_LIB_B >100000 && TDA_for_LIB_B <=150000
                  FCD_LIB = 50 + (0.0005*(TDA_for_LIB_B-100000));
              elseif TDA_for_LIB_B >150000 && TDA_for_LIB_B <=200000
                  FCD_LIB = 75+ (0.0002*(TDA_for_LIB_B-150000));
               end
           end
     
        
     % KAF
           if LIB_for >= 5600 && LIB_for <= 7500;
            LIB_FL = (25000- (10.52*(LIB_for-5600)));
        elseif LIB_for >= 8600 ;
            LIB_FL= (5000+ (10*(LIB_for-8600)));
           elseif LIB_for>7500 && LIB_for <8600;
               LIB_FL=5000;
           else
               LIB_FL=0;
           end
          
       if fillstart_LIB>0
           Dur_LIB=FCD_LIB;
           FCDend_LIB(year)=fillstart_LIB+Dur_LIB;
       else
           Dur_LIB=FCD_LIB;
           FCDend_LIB(year)=120+Dur_LIB;
       end
       

      
 
        
  
    if evac>0 
    %Evacuation mode

         
    
        
        

        %Calculate daily reservoir discharge and end-of-day storage. Have to
        %convert project inflows ("local") to kAF. Note: Libby Dam has a
        %minimum flow value of 4000cfs-d.  
        
        %Flow target

            LIB_dg = max(4000*.001987, s_3 + local(i,3)*.001987 - LIB_ORC(julian));

        
       
        
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,LIB_dg - f_max(3));
        
        %Is any storage space available?
        stor_avail = LIB_ORC(julian) - s_3;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,3) = f_max(3);
            spill(i,3) = LIB_dg - f_max(3);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            LIB_dg = max(LIB_dg - stor_avail,f_max(3));
            powerflow(i,3) = f_max(3);
            spill(i,3) = max(0,LIB_dg - f_max(3));
        else 
            powerflow(i,3) = LIB_dg;
        end
        
        s_3 = max(0,s_3 + local(i,3)*.001987 - LIB_dg);
        discharge(i,3) = LIB_dg*(1/.001987); %Convert back to cfs
        storage(i,3) = s_3;

    else
    %Refill mode - this is when the reservoir fills back up during spring
    %floods. Only storage target is maximum reservoir storage (spillway
    %threshold).
         %Alright lets cheat
                  %GOD VIEW!!!!!
                  %What is coming?
               if year >1
               VAQR_LIB(i)= LIB_FL;
               LIB_dg = max(max(4000*.001987, VAQR_LIB(i)*.001987),s_3 + local(i,3)*.001987 - LIB_ORC(julian)+ VAQR_LIB(i)*.001987*1.5);
               else
                   LIB_dg = max(4000*.001987,s_3 + local(i,3)*.001987 - LIB_ORC(julian));
               end

                      VAQR_LIB(i)= LIB_FL;
                      VAQRnew_LIB(i)=VAQR_LIB(i); %+ ADJ_LIB(year);
 
   
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,LIB_dg - f_max(3));
        
        %Is any storage space available?
        stor_avail = LIB_ORC(julian) - s_3;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,3) = f_max(3);
            spill(i,3) = LIB_dg - f_max(3);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            LIB_dg = max(LIB_dg - stor_avail,f_max(3));
            powerflow(i,3) = f_max(3);
            spill(i,3) = max(0,LIB_dg - f_max(3));
        else 
            powerflow(i,3) = LIB_dg;
        end
    
    s_3 = max(0,s_3 + local(i,3)*.001987 - LIB_dg);
    discharge(i,3) = LIB_dg*(1/.001987);
    storage(i,3) = s_3;     

    end
    
    %Convert storage to AF
    LIB_stor = s_3*1000;
  
    %What is forebay elevation?
    LIB_forebay = StorEq(3,2)*LIB_stor^4 + StorEq(3,3)*LIB_stor^3 + StorEq(3,4)*LIB_stor^2 + StorEq(3,5)*LIB_stor + StorEq(3,6);  
    %What is tailwater elevation?
    LIB_tailwater = TailEq(3,2)*discharge(i,3)^4 + TailEq(3,3)*discharge(i,3)^3 + TailEq(3,4)*discharge(i,3)^2 + TailEq(3,5)*discharge(i,3) + TailEq(3,6); 
    %Convert head to meters.
    LIB_head(i) = (LIB_forebay - LIB_tailwater)*.3048;
    generation(i,3) = ((1000*LIB_head(i)*powerflow(i,3)*14.27641*9.81*.865)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Bonner's Ferry - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    BFE_dg = LIB_dg + local(i,47)*.001987;
    powerflow(i,47) = min(BFE_dg,f_max(47));
    spill(i,47) = max(0,BFE_dg - f_max(47));
    s_47 = s_47 + LIB_dg + local(i,47)*.001987 - BFE_dg;
    discharge(i,47) = BFE_dg*(1/.001987);
    storage(i,47) = s_47; 
    generation(i,47) = ((1000*28.0416*powerflow(i,47)*14.27641*9.81*.875)/1000000)*24;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Corra Linn - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    CLN_dg = BFE_dg + DNC_dg + local(i,5)*.001987;
    powerflow(i,5) = min(CLN_dg,f_max(5));
    spill(i,5) = max(0,CLN_dg - f_max(5));
    s_5 = s_5 + BFE_dg + DNC_dg + local(i,5)*.001987 - CLN_dg;
    discharge(i,5) = CLN_dg*(1/.001987);
    storage(i,5) = s_5; 
    generation(i,5) = ((1000*16.1544*powerflow(i,5)*14.27641*9.81*.875)/1000000)*24;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Brilliant - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    BRI_dg = CLN_dg + local(i,18)*.001987;
    powerflow(i,18) = min(BRI_dg,f_max(18));
    spill(i,18) = max(0,BRI_dg - f_max(18));
    s_18 = s_18 + CLN_dg + local(i,18)*.001987 - BRI_dg;
    discharge(i,18) = BRI_dg*(1/.001987);
    storage(i,18) = s_18; 
    generation(i,18) = ((1000*28.0416*powerflow(i,18)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%
    %FLATHEAD PROJECTS%
    %Hungry Horse, Kerr, Thompson Falls, Noxon, Cabinet Gorge, Priest Lake,
    %Albeni Falls, Box Canyon, Boundary, Seven Mile, Waneta

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Hungry Horse - storage reservoir with flood control rule curve
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Are we in evacuation or refill?
    %If ICF exists, then fill start date is ICF - 20.
    if fillstart>0
        evac = julian<fillstart || julian>243;
    %Otherwise just use schedule.
    else
        evac = julian<120 || julian>304;
    end
%I changed this from 180 to 120 and 273 to 304
    
     %Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182;

        % Calculate "forecasted" inflows to Hungry Horse (May - August)
        if spring>0
           HHO_for = sum(local((year-2)*365+243:(year-2)*365+365,6));
        else
           HHO_for = sum(local((year-1)*365+243:(year-1)*365+365,6));
        end

        %Convert forecast to kAF
        HHO_for = HHO_for*.001987;
      
        if julian>=1 && julian <= 151;
          VPDR_HHO=400;
      elseif julian >151 && julian <=181;
          VPDR_HHO = 2000;
          %Above is liner extrapolation from data
      elseif julian >181 && julian <=212
          VPDR_HHO=2300;
      else
          VPDR_HHO=0;
      end
        %Identify target reservoir storage. A number of flood control curves
        %are publically available. They are based on forecasted inflows. Some interpolation is
        %necessary when the forecasted flows are in-between those specifiec by
        %USACE.
     
        %Calculate VRC
      %inflow is just local(i,6) out flow is VPDR or APDR
      if i==1
          %DNC's storage forecaste
          HHO_sfore(i)=min((local(i,6)-VPDR_HHO)*.001987+s_6,s_max(6));
      else
          HHO_sfore(i)=min((local(i,6)-VPDR_HHO)*.001987+ storage(i-1,6),s_max(6));
      end
          HHO_VRC= HHO_sfore(i);%this is in kAF
          
        if HHO_for <= 1000
            HHO_fctarget = HHO_fc(julian,1);
        elseif HHO_for > 1000 && HHO_for <= 1400
            HHO_fctarget = HHO_fc(julian,1) + ((HHO_for - 1000)/(1400-1000))*(HHO_fc(julian,2) - HHO_fc(julian,1));
        elseif HHO_for > 1400 && HHO_for <= 1600
            HHO_fctarget = HHO_fc(julian,2) + ((HHO_for - 1400)/(1600-1400))*(HHO_fc(julian,3) - HHO_fc(julian,2));
        elseif HHO_for > 1600 && HHO_for <= 2000
            HHO_fctarget = HHO_fc(julian,3) + ((HHO_for - 1600)/(2000-1600))*(HHO_fc(julian,4) - HHO_fc(julian,3));
        elseif HHO_for > 2000 && HHO_for <= 2200
            HHO_fctarget = HHO_fc(julian,4) + ((HHO_for - 2000)/(2200-2000))*(HHO_fc(julian,5) - HHO_fc(julian,4));
        elseif HHO_for > 2200 && HHO_for <= 2500
            HHO_fctarget = HHO_fc(julian,5) + ((HHO_for - 2200)/(2500-2200))*(HHO_fc(julian,6) - HHO_fc(julian,5));
        elseif HHO_for > 2500 && HHO_for <= 2800
            HHO_fctarget = HHO_fc(julian,6) + ((HHO_for - 2500)/(2800-2500))*(HHO_fc(julian,7) - HHO_fc(julian,6));
        elseif HHO_for > 2800 && HHO_for <= 3680
            HHO_fctarget = HHO_fc(julian,7) + ((HHO_for - 2800)/(3680-2800))*(HHO_fc(julian,8) - HHO_fc(julian,7));
        else
            HHO_fctarget = HHO_fc(julian,8);
        end
        
          if julian>=213 && julian <=365
           HHO_ORC(julian)= max(HHO_CRC(julian,2),HHO_ARC(julian,2));
           HHO_ORC(julian)= min(HHO_ORC(julian),HHO_fctarget);
        elseif julian >=1 && julian <= 212
            HHO_ORC(julian)= min(HHO_VRC,max(HHO_CRC(julian,2),HHO_ARC(julian,2)));
            HHO_ORC(julian)= min(HHO_ORC(julian),LIB_fctarget);
       else
           HHO_ORC(julian)=HHO_fctarget;
          end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %This section is the same as LIB's this repilication is to make
        %sure that nothing goes wrong

           if ICF_D<350 
               ICF_D=350;
           end
           %Calculate Libby flood control duration
           if ICF_D>=350 &&ICF_D<400  %Use curve 1
              TDA_for_LIB_B =max(TDA_for_LIB_B,70000);
              if TDA_for_LIB_B >= 70000 && TDA_for_LIB_B<= 100000;
                  FCD_LIB=0.00233333*(TDA_for_LIB_B-70000);
              elseif TDA_for_LIB_B > 100000 && TDA_for_LIB_B <=110000
                  FCD_LIB = 70+ (0.001*(TDA_for_LIB_B-100000));
              elseif TDA_for_LIB_B > 110000 && TDA_for_LIB_B <=140000
                  FCD_LIB = 80+ (0.005*(TDA_for_LIB_B-110000));
              elseif TDA_for_LIB_B > 140000 && TDA_for_LIB_B <=200000
                  FCD_LIB = 95+ (0.0025*(TDA_for_LIB_B-110000));
              end
           elseif ICF_D>=400 && ICF_D<450 %Use curve 2
               if TDA_for_LIB_B>= 80000 && TDA_for_LIB_B<= 100000;
                  FCD_LIB=0.003*(TDA_for_LIB_B-80000);
              elseif TDA_for_LIB_B >100000 && TDA_for_LIB_B <=145000
                  FCD_LIB = 60 + (0.00556*(TDA_for_LIB_B-100000));
              elseif TDA_for_LIB_B >145000 && TDA_for_LIB_B <=200000
                  FCD_LIB = 85+ (0.001818*(TDA_for_LIB_B-145000));
               end
           
              %FCD is flood control duration
           elseif ICF_D >=450 %Use curve 3
               if TDA_for_LIB_B>= 80000 && TDA_for_LIB_B <= 100000;
                  FCD_LIB=0.0025*(TDA_for_LIB_B-80000);
              elseif TDA_for_LIB_B >100000 && TDA_for_LIB_B <=150000
                  FCD_LIB = 50 + (0.0005*(TDA_for_LIB_B-100000));
              elseif TDA_for_LIB_B >150000 && TDA_for_LIB_B <=200000
                  FCD_LIB = 75+ (0.0002*(TDA_for_LIB_B-150000));
               end
           end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
           if  HHO_for >= 3000;
            HHO_FL=0;
     
           elseif HHO_for>1000 && LIB_for <3000;
               HHO_FL=12000- (6*(HHO_for-1000));
           else
               HHO_FL=0;
           end
           
            if fillstart>0
           Dur_LIB=FCD_LIB;
           FCDend_LIB(year)=fillstart+Dur_LIB;
       else
           Dur_LIB=FCD_LIB;
           FCDend_LIB(year)=120+Dur_LIB;
       end
    if evac>0 
    %Evacuation mode

   
        %Calculate daily reservoir discharge and end-of-day storage. Have to
        %convert project inflows ("local") to kAF. Note: there is a minimum flow release of 3500cfs associated with this dam.  
        HHO_dg = max(max(0,3500-local(i,7))*.001987, s_6 + local(i,6)*.001987 - HHO_ORC(julian));
        %If reservoir storage is low
        if HHO_dg>s_6 + local(i,6)*.001987
            HHO_dg=s_6 + local(i,6)*.001987;
        end
        
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,HHO_dg - f_max(6));
        
        %Is any storage space available?
        stor_avail = HHO_ORC(julian) - s_6;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,6) = f_max(6);
            spill(i,6) = HHO_dg - f_max(6);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            HHO_dg = max(HHO_dg - stor_avail,f_max(6));
            powerflow(i,6) = f_max(6);
            spill(i,6) = max(0,HHO_dg - f_max(6));
        else 
            powerflow(i,6) = HHO_dg;
        end
        
        s_6 = s_6 + local(i,6)*.001987 - HHO_dg;
        discharge(i,6) = HHO_dg*(1/.001987); %Convert back to cfs
        storage(i,6) = s_6;

    else
    %Refill mode - this is when the reservoir fills back up during spring
    %floods. Only storage target is maximum reservoir storage (spillway
    %threshold).

    if year >1
               
                      VAQR_HHO(i)= HHO_FL;
                      VAQRnew_HHO(i)=VAQR_HHO(i); %+ ADJ_LIB(year);
                 
                  HHO_dg = max(max(0,3500-local(i,7))*.001987, s_6 + local(i,6)*.001987 - HHO_ORC(julian)+ VAQR_HHO(i)*.001987*1.5);
    else
        
                   HHO_dg = max(max(0,3500-local(i,7))*.001987, s_6 + local(i,6)*.001987 - HHO_ORC(julian));
    end
    
        
        %If reservoir storage is low
        if HHO_dg>s_6 + local(i,6)*.001987
           HHO_dg=s_6 + local(i,6)*.001987;
        end
        
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,HHO_dg - f_max(6));
        
        %Is any storage space available?
        stor_avail = HHO_ORC(julian) - s_6;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,6) = f_max(6);
            spill(i,6) = HHO_dg - f_max(6);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            HHO_dg = max(HHO_dg - stor_avail,f_max(6));
            powerflow(i,6) = f_max(6);
            spill(i,6) = max(0,HHO_dg - f_max(6));
        else 
            powerflow(i,6) = HHO_dg;
        end
        
        s_6 = s_6 + local(i,6)*.001987 - HHO_dg;
        discharge(i,6) = HHO_dg*(1/.001987);
        storage(i,6) = s_6;     
 
    end
    
    %Convert storage to AF
    HHO_stor = s_6*1000;
    %What is forebay elevation?
    HHO_forebay = StorEq(6,2)*HHO_stor^4 + StorEq(6,3)*HHO_stor^3 + StorEq(6,4)*HHO_stor^2 + StorEq(6,5)*HHO_stor + StorEq(6,6);  
    %What is tailwater elevation?
    HHO_tailwater = TailEq(6,2)*discharge(i,6)^4 + TailEq(6,3)*discharge(i,6)^3 + TailEq(6,4)*discharge(i,6)^2 + TailEq(6,5)*discharge(i,6) + TailEq(6,6); 
    %Convert head to meters.
    HHO_head(i) = (HHO_forebay - HHO_tailwater)*.3048;
    generation(i,6) = ((1000*HHO_head(i)* powerflow(i,6) *14.27641*9.81*.84)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Kerr - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Note: There is a 1-day travel delay between Hungry Horse and Kerr.
    if i > 1
    KER_dg = discharge(i-1,6)*.001987 + + CFM5L(i)*.001987+ local(i,7)*.001987;
    s_7 = s_7 + discharge(i-1,6)*.001987 + local(i,7)*.001987 + CFM5L(i)*.001987 - KER_dg;
    else
    KER_dg = HHO_dg + local(i,7)*.001987+ CFM5L(i)*.001987;
    s_7 = s_7 + HHO_dg + local(i,7)*.001987 + CFM5L(i)*.001987 - KER_dg;
    end
    powerflow(i,7) = min(KER_dg,f_max(7));
    spill(i,7) = max(0,KER_dg - f_max(7));
    discharge(i,7) = KER_dg*(1/.001987);
    storage(i,7) = s_7; 
    %Convert storage to AF
    KER_stor = s_7*1000;
    smax = s_max(7)*1000;
    %What is forebay elevation?
    KER_forebay = StorEq(7,2)*KER_stor^4 + StorEq(7,3)*KER_stor^3 + StorEq(7,4)*KER_stor^2 + StorEq(7,5)*KER_stor + StorEq(7,6);  
    %What is tailwater elevation?
    KER_tailwater = (StorEq(7,2)*smax^4 + StorEq(7,3)*smax^3 + StorEq(7,4)*smax^2 + StorEq(7,5)*smax + StorEq(7,6)) - 206; 
    %Convert head to meters.
    KER_head = (KER_forebay - KER_tailwater)*.3048; 
    generation(i,7) = ((1000*62.7888*powerflow(i,7)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Thompson Falls - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    THF_dg = KER_dg + local(i,19)*.001987;
    s_19 = s_19 + KER_dg + local(i,19)*.001987 - THF_dg;
    powerflow(i,19) = min(THF_dg,f_max(19));
    spill(i,19) = max(0,THF_dg - f_max(19));
    discharge(i,19) = THF_dg*(1/.001987);
    storage(i,19) = s_19; 
    generation(i,19) = ((1000*19.5072*powerflow(i,19)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Noxon - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Note: There is a 1-day travel delay between Thompson Falls and Noxon.
    
    if i > 1
    NOX_dg = discharge(i-1,19)*.001987 + local(i,14)*.001987;
    s_14 = s_14 + discharge(i-1,19)*.001987 + local(i,14)*.001987 - NOX_dg;
    else
    NOX_dg = THF_dg + local(i,14)*.001987;
    s_14 = s_14 + THF_dg + local(i,14)*.001987 - NOX_dg;
    end
    powerflow(i,14) = min(NOX_dg,f_max(14));
    spill(i,14) = max(0,NOX_dg - f_max(14));
    discharge(i,14) = NOX_dg*(1/.001987);
    storage(i,14) = s_14; 
    %Convert storage to AF
    NOX_stor = s_14*1000;
    smax = s_max(14)*1000;
    %What is forebay elevation?
    NOX_forebay = StorEq(14,2)*NOX_stor^4 + StorEq(14,3)*NOX_stor^3 + StorEq(14,4)*NOX_stor^2 + StorEq(14,5)*NOX_stor + StorEq(14,6);  
    %What is tailwater elevation?
    NOX_tailwater = (StorEq(14,2)*smax^4 + StorEq(14,3)*smax^3 + StorEq(14,4)*smax^2 + StorEq(14,5)*smax + StorEq(14,6)) - 179; 
    %Convert head to meters.
    NOX_head = (NOX_forebay - NOX_tailwater)*.3048; 
    generation(i,14) = ((1000*54.5592*powerflow(i,14)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Cabinet Gorge - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    CBG_dg = NOX_dg + local(i,20)*.001987;
    s_20 = s_20 + NOX_dg + local(i,20)*.001987 - CBG_dg;
    powerflow(i,20) = min(CBG_dg,f_max(20));
    spill(i,20) = max(0,CBG_dg - f_max(20));
    discharge(i,20) = CBG_dg*(1/.001987);
    storage(i,20) = s_20;    
    generation(i,20) = ((1000*33.8328*powerflow(i,20)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Priest Lake - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    PSL_dg = local(i,46)*.001987;
    s_46 = s_46 + local(i,46)*.001987 - PSL_dg;
    powerflow(i,46) = min(PSL_dg,f_max(46));
    spill(i,46) = max(0,PSL_dg - f_max(46));
    discharge(i,46) = PSL_dg*(1/.001987);
    storage(i,46) = s_46;    
    generation(i,46) = ((1000*84.1428*powerflow(i,46)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Albeni Falls - storage project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Note. This project has upper and lower rule curves and minimum flows.
    ALB_upper = ALB_fc(julian,1);
    ALB_lower = ALB_fc(julian,2);
   
%         %If reservoir storage is near lower curve
%         if s_8 - ALB_dg < ALB_lower 
%           ALB_dg = 0;
%         end
   if i==1
          %DNC's storage forecaste
          ALB_sfore(i)=min((local(i,8)-4000)*.001987+ PSL_dg + CBG_dg+s_8,s_max(8));
      else
          ALB_sfore(i)=min((local(i,8)-4000)*.001987+ PSL_dg + CBG_dg+ storage(i-1,8),s_max(8));
      end
          ALB_VRC= ALB_sfore(i);
        if julian>=213 && julian <=365
           ALB_ORC(julian)= max(ALB_CRC(julian,2),ALB_ARC(julian,2));
           ALB_ORC(julian)= min(ALB_ORC(julian),ALB_upper);
           ALB_ORC(julian)= max(ALB_ORC(julian),ALB_lower);
        elseif julian >=1 && julian <= 212
           ALB_ORC(julian)= min(ALB_VRC,max(ALB_CRC(julian,2),ALB_ARC(julian,2)));
           ALB_ORC(julian)= min(ALB_ORC(julian),ALB_upper);
           ALB_ORC(julian)= max(ALB_ORC(julian),ALB_lower);
       
        end
         ALB_dg = max(4000*.001987, s_8 + local(i,8)*.001987 + PSL_dg + CBG_dg - ALB_ORC(julian));
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,ALB_dg - f_max(8));
        
        %Is any storage space available?
        stor_avail = ALB_upper - s_8;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,8) = f_max(8);
            spill(i,8) = ALB_dg - f_max(8);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            ALB_dg = max(ALB_dg - stor_avail,f_max(8));
            powerflow(i,8) = f_max(8);
            spill(i,8) = max(0,ALB_dg - f_max(8));
        else 
            powerflow(i,8) = ALB_dg;
        end
        
    s_8 = s_8 + local(i,8)*.001987 + PSL_dg + CBG_dg - ALB_dg;
    discharge(i,8) = ALB_dg*(1/.001987);
    storage(i,8) = s_8;  
    
    %Convert storage to AF
    ALB_stor = s_8*1000;
    %What is forebay elevation?
    ALB_forebay = StorEq(8,2)*ALB_stor^4 + StorEq(8,3)*ALB_stor^3 + StorEq(8,4)*ALB_stor^2 + StorEq(8,5)*ALB_stor + StorEq(8,6);  
    %What is tailwater elevation?
    ALB_tailwater = TailEq(8,2)*discharge(i,8)^4 + TailEq(8,3)*discharge(i,8)^3 + TailEq(8,4)*discharge(i,8)^2 + TailEq(8,5)*discharge(i,8) + TailEq(8,6); 
    %Convert head to meters.
    ALB_head = (ALB_forebay - ALB_tailwater)*.3048;
    generation(i,8) = ((1000*ALB_head*powerflow(i,8)*14.27641*9.81*.71)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Box Canyon - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    BOX_dg = local(i,21)*.001987 + ALB_dg;
    s_21 = s_21 + local(i,21)*.001987 + ALB_dg - BOX_dg;
    powerflow(i,21) = min(BOX_dg,f_max(21));
    spill(i,21) = max(0,BOX_dg - f_max(21));
    discharge(i,21) = BOX_dg*(1/.001987);
    storage(i,21) = s_21;  
    generation(i,21) = ((1000*14.0208*powerflow(i,21)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Boundary - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    BOU_dg = local(i,22)*.001987 + BOX_dg;
    s_22 = s_22 + local(i,22)*.001987  + BOX_dg - BOU_dg;
    powerflow(i,22) = min(BOU_dg,f_max(22));
    spill(i,22) = max(0,BOU_dg - f_max(22));
    discharge(i,22) = BOU_dg*(1/.001987);
    storage(i,22) = s_22;
    generation(i,22) = ((1000*103.632*powerflow(i,22)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Seven Mile - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    SVN_dg = local(i,17)*.001987 + BOU_dg;
    s_17 = s_17 + local(i,17)*.001987 + BOU_dg - SVN_dg;
    powerflow(i,17) = min(SVN_dg,f_max(17));
    spill(i,17) = max(0,SVN_dg - f_max(17));
    discharge(i,17) = SVN_dg*(1/.001987);
    storage(i,17) = s_17;
    generation(i,17) = ((1000*64.92*powerflow(i,17)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Waneta - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    WNT_dg = local(i,23)*.001987 + SVN_dg;
    s_23 = s_23 + local(i,23)*.001987 + SVN_dg - WNT_dg;
    powerflow(i,23) = min(WNT_dg,f_max(23));
    spill(i,23) = max(0,WNT_dg - f_max(23));
    discharge(i,23) = WNT_dg*(1/.001987);
    storage(i,23) = s_23;
    generation(i,23) = ((1000*23.1648*powerflow(i,23)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %MID COLUMBIA PROJECTS%
    %Grand Coulee, Chief Joseph, Wells, Chelan, Rocky Reach, Rock Island, 
    %Wanapum, Priest Rapids
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Grand Coulee - storage project
    %%%%%%%%%%%%%%%%%%%%%%%%%
      
    %Are we in evacuation or refill?
    %If ICF exists, then fill start date is ICF - 20.
    if fillstart>0
        evac = julian<fillstart || julian>334;
    %Otherwise just use schedule.
    else
        evac = julian<182 || julian>334;
    end
    
     if TDA_for <= 57000
            GCL_fctarget = GCL_fc(julian,1);
        elseif TDA_for > 57000 && TDA_for <= 60000
            GCL_fctarget = GCL_fc(julian,1) + ((TDA_for - 57000)/(60000-57000))*(GCL_fc(julian,2) - GCL_fc(julian,1));
        elseif TDA_for > 60000 && TDA_for <= 63250
            GCL_fctarget = GCL_fc(julian,2) + ((TDA_for - 60000)/(63250-60000))*(GCL_fc(julian,3) - GCL_fc(julian,2));
        elseif TDA_for > 63250 && TDA_for <= 65000
            GCL_fctarget = GCL_fc(julian,3) + ((TDA_for - 63250)/(65000-63250))*(GCL_fc(julian,4) - GCL_fc(julian,3));
        elseif TDA_for > 65000 && TDA_for <= 67660
            GCL_fctarget = GCL_fc(julian,4) + ((TDA_for - 65000)/(67660-65000))*(GCL_fc(julian,5) - GCL_fc(julian,4));
        elseif TDA_for > 67660 && TDA_for <= 71000
            GCL_fctarget = GCL_fc(julian,5) + ((TDA_for - 67660)/(71000-67660))*(GCL_fc(julian,6) - GCL_fc(julian,5));
        elseif TDA_for > 71000 && TDA_for <= 75000
            GCL_fctarget = GCL_fc(julian,6) + ((TDA_for - 71000)/(75000-71000))*(GCL_fc(julian,7) - GCL_fc(julian,6));
        elseif TDA_for > 75000 && TDA_for <= 87500
            GCL_fctarget = GCL_fc(julian,7) + ((TDA_for - 75000)/(87500-75000))*(GCL_fc(julian,8) - GCL_fc(julian,7));
        elseif TDA_for > 87500 && TDA_for <= 100000
            GCL_fctarget = GCL_fc(julian,8) + ((TDA_for - 87500)/(100000-87500))*(GCL_fc(julian,9) - GCL_fc(julian,8));
        elseif TDA_for > 100000
            GCL_fctarget = GCL_fc(julian,9);
        end
            VPDR_GCL=30000*.001987 ;
            
        if i==1
          %DNC's storage forecaste
          GCL_sfore(i)=min(local(i,10)*.001987 + spokane_flow(i)*.001987 + discharge(i,2)*.001987 + discharge(1,18)*.001987 + discharge(i,23)*.001987+s_10 - VPDR_GCL,s_max(10));
      else
          GCL_sfore(i)=min(local(i,10)*.001987 + spokane_flow(i-1)*.001987 + discharge(i-1,2)*.001987 + discharge(i-1,18)*.001987 + discharge(i-1,23)*.001987+ storage(i-1,10) - VPDR_GCL,s_max(10));
      end
          GCL_VRC(julian)= GCL_sfore(i);%this is in kAF
       %set VRCLL for GCL
       if julian >=1 && julian <=31;
           GCL_VRCLL=1778.9*2.4466;
       elseif julian >=32 && julian<=59;
           GCL_VRCLL=1054.5*2.4466;  
       elseif julian >=60 && julian <=90;
           GCL_VRCLL=418.7*2.4466;
       elseif julian >=91 && julian <=120;
           GCL_VRCLL=418.7*2.4466;
       elseif julian >=121 && julian <=151;
           GCL_VRCLL=843.7*2.4466;
       elseif julian >=152 && julian <=181;
           GCL_VRCLL=2411.3*2.4466;
       elseif julian >=182 && julian <=212;
           GCL_VRCLL=2614.3*2.4466;
       end
       
       if julian>=213 && julian <=365
           GCL_ORC(julian)= max(GCL_CRC(julian,2),GCL_ARC(julian,2));
           GCL_ORC(julian)= min(GCL_ORC(julian),GCL_fctarget);
          
        elseif julian >=1 && julian <= 212
            GCL_ORC(julian)= min(GCL_VRC(julian),max(GCL_CRC(julian,2),GCL_ARC(julian,2)));
            GCL_ORC(julian)= min(GCL_ORC(julian),GCL_fctarget);
            GCL_ORC(julian)= max(GCL_ORC(julian),GCL_VRCLL);
       else
           GCL_ORC(julian)=GCL_fctarget;
       end
           Storage_left(i,1)=GCL_fctarget-GCL_ORC(julian);
    if evac>0 
    %Evacuation mode

        %Identify target reservoir storage. A number of flood control curves
        %are publically available. They are based on forecasted flows at The Dalles. Some interpolation is
        %necessary when the forecasted flows are in-between those specifiec by
        %USACE.

       
        %Calculate dail
        %Calculate daily reservoir discharge and end-of-day storage. Have to
        %convert project inflows ("local") to kAF. Note: there is a minimum flow release of 30000cfs associated with this dam.
        %There is also a 1-day travel delay between upstream sources and
        %Grand Coulee. 
        if i>1
        GCL_dg = max(30000*.001987, s_10 + local(i,10)*.001987 + spokane_flow(i-1)*.001987 + discharge(i-1,2)*.001987 + discharge(i-1,18)*.001987 + discharge(i-1,23)*.001987 -  GCL_ORC(julian));
        
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,GCL_dg - f_max(10));
        
        %Is any storage space available?
        stor_avail = GCL_fctarget - s_10;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,10) = f_max(10);
            spill(i,10) = GCL_dg - f_max(10);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            GCL_dg = max(GCL_dg - stor_avail,f_max(10));
            powerflow(i,10) = f_max(10);
            spill(i,10) = max(0,GCL_dg - f_max(10));
        else 
            powerflow(i,10) = GCL_dg;
        end
        
        s_10 = s_10 + local(i,10)*.001987 + spokane_flow(i-1)*.001987 + discharge(i-1,2)*.001987 + discharge(i-1,18)*.001987 + discharge(i-1,23)*.001987 - GCL_dg;
        
        else
            
        GCL_dg = max(30000*.001987, s_10 + local(i,10)*.001987 + spokane_flow(i)*.001987 + discharge(i,2)*.001987 + discharge(i,18)*.001987 + discharge(i,23)*.001987 -  GCL_ORC(julian));
        
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,GCL_dg - f_max(10));
        
        %Is any storage space available?
        stor_avail = GCL_fctarget - s_10;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,10) = f_max(10);
            spill(i,10) = GCL_dg - f_max(10);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            GCL_dg = max(GCL_dg - stor_avail,f_max(10));
            powerflow(i,10) = f_max(10);
            spill(i,10) = max(0,GCL_dg - f_max(10));
        else 
            powerflow(i,10) = GCL_dg;
        end
        
        s_10 = s_10 + local(i,10)*.001987 + spokane_flow(i)*.001987 + discharge(i,2)*.001987 + discharge(i,18)*.001987 + discharge(i,23)*.001987 - GCL_dg;
        
        end
        discharge(i,10) = GCL_dg*(1/.001987); %Convert back to cfs
        storage(i,10) = s_10;
    

    else
    %Refill mode - this is when the reservoir fills back up during spring
    %floods. Only storage target is maximum reservoir storage (spillway
    %threshold).

        if i>1
        GCL_dg = max(30000*.001987, s_10 + local(i,10)*.001987 + spokane_flow(i-1)*.001987 + discharge(i-1,2)*.001987 + discharge(i-1,18)*.001987 + discharge(i-1,23)*.001987 -  GCL_ORC(julian));
        
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,GCL_dg - f_max(10));
        
        %Is any storage space available?
        stor_avail = s_max(10) - s_10;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,10) = f_max(10);
            spill(i,10) = GCL_dg - f_max(10);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            GCL_dg = max(GCL_dg - stor_avail,f_max(10));
            powerflow(i,10) = f_max(10);
            spill(i,10) = max(0,GCL_dg - f_max(10));
        else 
            powerflow(i,10) = GCL_dg;
        end
        
        s_10 = s_10 + local(i,10)*.001987 + spokane_flow(i-1)*.001987 + discharge(i-1,2)*.001987 + discharge(i-1,18)*.001987 + discharge(i-1,23)*.001987 - GCL_dg;
        
        else 
        GCL_dg = max(30000*.001987, s_10 + local(i,10)*.001987 + spokane_flow(i)*.001987 + discharge(i,2)*.001987 + discharge(i,18)*.001987 + discharge(i,23)*.001987 -  GCL_ORC(julian));
        
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,GCL_dg - f_max(10));
        
        %Is any storage space available?
        stor_avail = s_max(10) - s_10;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,10) = f_max(10);
            spill(i,10) = GCL_dg - f_max(10);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            GCL_dg = max(GCL_dg - stor_avail,f_max(10));
            powerflow(i,10) = f_max(10);
            spill(i,10) = max(0,GCL_dg - f_max(10));
        else 
            powerflow(i,10) = GCL_dg;
        end

        
        s_10 = s_10 + local(i,10)*.001987 + spokane_flow(i)*.001987 + discharge(i,2)*.001987 + discharge(i,18)*.001987 + discharge(i,23)*.001987 - GCL_dg;
        
        end
        discharge(i,10) = GCL_dg*(1/.001987); %Convert back to cfs
        storage(i,10) = s_10;   
        
 
    end
    
    %Convert storage to AF
    GCL_stor = s_10*1000;
    %What is forebay elevation?
    GCL_forebay = StorEq(10,2)*GCL_stor^4 + StorEq(10,3)*GCL_stor^3 + StorEq(10,4)*GCL_stor^2 + StorEq(10,5)*GCL_stor + StorEq(10,6);  
    %What is tailwater elevation?
    GCL_tailwater = TailEq(10,2)*discharge(i,10)^4 + TailEq(10,3)*discharge(i,10)^3 + TailEq(10,4)*discharge(i,10)^2 + TailEq(10,5)*discharge(i,10) + TailEq(10,6); 
    %Convert head to meters.
    GCL_head(i) = (GCL_forebay - GCL_tailwater)*.3048;
    generation(i,10) = ((1000*GCL_head(i)*powerflow(i,10)*14.27641*9.81*.9)/1000000)*24;
    heads(i,1)=GCL_head(i);
    Spillheads(i,1)=GCL_head(i);
    stor(i)=GCL_stor;
        if i>1;
        inflow(i,1)=(local(i,10)*.001987 + spokane_flow(i-1)*.001987 + discharge(i-1,2)*.001987 + discharge(i-1,18)*.001987 + discharge(i-1,23)*.001987)/0.001987;
        end
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Chief Joseph - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    CHJ_dg = local(i,29)*.001987 + GCL_dg;
    s_29 = s_29 + local(i,29)*.001987 + GCL_dg - CHJ_dg;
    powerflow(i,29) = min(CHJ_dg,f_max(29));
    spill(i,29) = max(0,CHJ_dg - f_max(29));
    discharge(i,29) = CHJ_dg*(1/.001987);
    storage(i,29) = s_29;
    %Convert storage to AF
    CHJ_stor = s_29*1000;
    %What is forebay elevation?
    CHJ_forebay = StorEq(29,2)*CHJ_stor^4 + StorEq(29,3)*CHJ_stor^3 + StorEq(29,4)*CHJ_stor^2 + StorEq(29,5)*CHJ_stor + StorEq(29,6);  
    %What is tailwater elevation?
    CHJ_tailwater = TailEq(29,2)*discharge(i,29)^4 + TailEq(29,3)*discharge(i,29)^3 + TailEq(29,4)*discharge(i,29)^2 + TailEq(29,5)*discharge(i,29) + TailEq(29,6); 
    %Convert head to meters.
    CHJ_head(i) = (CHJ_forebay - CHJ_tailwater)*.3048;
    generation(i,29) = ((1000*CHJ_head(i)*powerflow(i,29)*14.27641*9.81*.84)/1000000)*24;
    heads(i,2)=CHJ_head(i);
    Spillheads(i,2)=CHJ_head(i);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Wells - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    WLL_dg = local(i,30)*.001987 + CHJ_dg;
    s_30 = s_30 + local(i,30)*.001987 + CHJ_dg - WLL_dg;
    powerflow(i,30) = min(WLL_dg,f_max(30));
    spill(i,30) = max(0,WLL_dg - f_max(30));
    discharge(i,30) = WLL_dg*(1/.001987);
    storage(i,30) = s_30;   
    generation(i,30) = ((1000*15.9142*powerflow(i,30)*14.27641*9.81*.87)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Chelan - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    CHL_dg = local(i,11)*.001987;
    s_11 = s_11 + local(i,11)*.001987 - CHL_dg;
    powerflow(i,11) = min(CHL_dg,f_max(11));
    spill(i,11) = max(0,CHL_dg - f_max(11));
    discharge(i,11) = CHL_dg*(1/.001987);
    storage(i,11) = s_11; 
    generation(i,11) = ((1000*121.92*powerflow(i,11)*14.27641*9.81*.848)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Rocky Reach - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    RRH_dg = local(i,31)*.001987 + CHL_dg + WLL_dg;
    s_31 = s_31 + local(i,31)*.001987 + CHL_dg + WLL_dg - RRH_dg;
    powerflow(i,31) = min(RRH_dg,f_max(31));
    spill(i,31) = max(0,RRH_dg - f_max(31));
    discharge(i,31) = RRH_dg*(1/.001987);
    storage(i,31) = s_31;
    generation(i,31) = ((1000*24.3108*powerflow(i,31)*14.27641*9.81*.873)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Rock Island - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    RIS_dg = local(i,32)*.001987 + RRH_dg;
    s_32 = s_32 + local(i,32)*.001987 + RRH_dg - RIS_dg;
    powerflow(i,32) = min(RIS_dg,f_max(32));
    spill(i,32) = max(0,RIS_dg - f_max(32));
    discharge(i,32) = RIS_dg*(1/.001987);
    storage(i,32) = s_32;
    generation(i,32) = ((1000*11.5640*powerflow(i,32)*14.27641*9.81*.874)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Wanapum - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    WPM_dg = local(i,33)*.001987 + RIS_dg;
    s_33 = s_33 + local(i,33)*.001987 + RIS_dg - WPM_dg;
    powerflow(i,33) = min(WPM_dg,f_max(33));
    spill(i,33) = max(0,WPM_dg - f_max(33));
    discharge(i,33) = WPM_dg*(1/.001987);
    storage(i,33) = s_33;
    generation(i,33) = ((1000*19.2734*powerflow(i,33)*14.27641*9.81*.873)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Priest Rapids - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    PRD_dg = local(i,34)*.001987 + WPM_dg;
    s_34 = s_34 + local(i,34)*.001987 + WPM_dg - PRD_dg;
    powerflow(i,34) = min(PRD_dg,f_max(34));
    spill(i,34) = max(0,PRD_dg - f_max(34));
    discharge(i,34) = PRD_dg*(1/.001987);
    storage(i,34) = s_34;
    generation(i,34) = ((1000*17.698*powerflow(i,34)*14.27641*9.81*.873)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %SNAKE RIVER PROJECTS%
    %Brownlee, Oxbow, Hell's Canyon, Dworshak, Lower Granite, Little Goose
    %Lower Monumental, Ice Harbor
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Brownlee - storage project
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Are we in evacuation or refill?
    %If ICF exists, then fill start date is ICF - 20.
    if fillstart>0
        evac = julian<fillstart || julian>243;
    %Otherwise just use schedule.
    else
        evac = julian<182 || julian>243;
    end
    
      %Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182;

        % Calculate "forecasted" inflows to Brownlee (April - July)
        if spring>0
           BRN_for = sum(local((year-2)*365+213:(year-2)*365+334,12));
        else
           BRN_for = sum(local((year-1)*365+213:(year-1)*365+334,12));
        end

        %Convert forecast to kAF
        BRN_for = BRN_for*.001987;

        %Identify target reservoir storage. A number of flood control curves
        %are publically available. They are based on forecasted inflows. Some interpolation is
        %necessary when the forecasted flows are in-between those specifiec by
        %USACE.

        if TDA_for <= 75000
            if BRN_for <= 3000        
                BRN_fctarget = BRN_fc(julian,1);
            elseif BRN_for > 3000 && BRN_for <= 4000
                BRN_fctarget = BRN_fc(julian,1) + ((BRN_for - 3000)/(4000-3000))*(BRN_fc(julian,2) - BRN_fc(julian,1));
            elseif BRN_for > 4000 && BRN_for < 5000
                BRN_fctarget = BRN_fc(julian,2) + ((BRN_for - 4000)/(5000-4000))*(BRN_fc(julian,3) - BRN_fc(julian,2));
            elseif BRN_for > 5000 && BRN_for < 6000
                BRN_fctarget = BRN_fc(julian,3) + ((BRN_for - 5000)/(6000-5000))*(BRN_fc(julian,4) - BRN_fc(julian,3));
            elseif BRN_for > 6000
                BRN_fctarget = BRN_fc(julian,4); 
            end
        elseif TDA_for > 75000 && TDA_for <= 85000
            if BRN_for <= 3000        
                BRN_fctarget = BRN_fc(julian,5);
            elseif BRN_for > 3000 && BRN_for <= 4000
                BRN_fctarget = BRN_fc(julian,5) + ((BRN_for - 3000)/(4000-3000))*(BRN_fc(julian,6) - BRN_fc(julian,5));
            elseif BRN_for > 4000 && BRN_for < 5000
                BRN_fctarget = BRN_fc(julian,6) + ((BRN_for - 4000)/(5000-4000))*(BRN_fc(julian,7) - BRN_fc(julian,6));
            elseif BRN_for > 5000 && BRN_for < 6000
                BRN_fctarget = BRN_fc(julian,7) + ((BRN_for - 5000)/(6000-5000))*(BRN_fc(julian,8) - BRN_fc(julian,7));
            elseif BRN_for > 6000
                BRN_fctarget = BRN_fc(julian,8);
            end
        elseif TDA_for > 85000 && TDA_for <= 95000
            if BRN_for <= 3000        
                BRN_fctarget = BRN_fc(julian,9);
            elseif BRN_for > 3000 && BRN_for <= 4000
                BRN_fctarget = BRN_fc(julian,9) + ((BRN_for - 3000)/(4000-3000))*(BRN_fc(julian,10) - BRN_fc(julian,9));
            elseif BRN_for > 4000 && BRN_for < 5000
                BRN_fctarget = BRN_fc(julian,10)+ ((BRN_for - 4000)/(5000-4000))*(BRN_fc(julian,11) - BRN_fc(julian,10));
            elseif BRN_for > 5000 && BRN_for < 6000
                BRN_fctarget = BRN_fc(julian,11) + ((BRN_for - 5000)/(6000-5000))*(BRN_fc(julian,12) - BRN_fc(julian,11));
            elseif BRN_for > 6000
                BRN_fctarget = BRN_fc(julian,12); 
            end
        elseif TDA_for > 95000 && TDA_for <= 105000
            if BRN_for <= 3000        
                BRN_fctarget = BRN_fc(julian,13);
            elseif BRN_for > 3000 && BRN_for <= 4000
                BRN_fctarget = BRN_fc(julian,13) + ((BRN_for - 3000)/(4000-3000))*(BRN_fc(julian,14) - BRN_fc(julian,13));
            elseif BRN_for > 4000 && BRN_for < 5000
                BRN_fctarget = BRN_fc(julian,14) + ((BRN_for - 4000)/(5000-4000))*(BRN_fc(julian,15) - BRN_fc(julian,14));
            elseif BRN_for > 5000 && BRN_for < 6000
                BRN_fctarget = BRN_fc(julian,15) + ((BRN_for - 5000)/(6000-5000))*(BRN_fc(julian,16) - BRN_fc(julian,15));
            elseif BRN_for > 6000
                BRN_fctarget = BRN_fc(julian,16); 
            end
        elseif TDA_for > 105000 && TDA_for <= 115000
            if BRN_for <= 3000        
                BRN_fctarget = BRN_fc(julian,17);
            elseif BRN_for > 3000 && BRN_for <= 4000
                BRN_fctarget = BRN_fc(julian,17) + ((BRN_for - 3000)/(4000-3000))*(BRN_fc(julian,18) - BRN_fc(julian,17));
            elseif BRN_for > 4000 && BRN_for < 5000
                BRN_fctarget = BRN_fc(julian,18) + ((BRN_for - 4000)/(5000-4000))*(BRN_fc(julian,19) - BRN_fc(julian,18));
            elseif BRN_for > 5000 && BRN_for < 6000
                BRN_fctarget = BRN_fc(julian,19) + ((BRN_for - 5000)/(6000-5000))*(BRN_fc(julian,20) - BRN_fc(julian,19));
            elseif BRN_for > 6000
                BRN_fctarget = BRN_fc(julian,20); 
            end
        elseif TDA_for > 115000
            BRN_fctarget = BRN_fc(julian,20);
        end
            if i==1
          %DNC's storage forecaste
          BRN_sfore(i)=min((local(i,12)-3500)*.001987+s_12,s_max(12));
      else
          BRN_sfore(i)=min((local(i,12)-3500)*.001987+ storage(i-1,12),s_max(12));
      end
          BRN_VRC= BRN_sfore(i);
          
        if julian>=213 && julian <=365
           BRN_ORC(julian)= max(BRN_CRC(julian,2),BRN_ARC(julian,2));
           BRN_ORC(julian)= min(BRN_ORC(julian),BRN_fctarget);
          
        elseif julian >=1 && julian <= 212
           BRN_ORC(julian)= min(BRN_VRC,max(BRN_CRC(julian,2),BRN_ARC(julian,2)));
           BRN_ORC(julian)= min(BRN_ORC(julian),BRN_fctarget);
        
       
        end

    if evac>0 
    %Evacuation mode

  
        %Calculate daily reservoir discharge and end-of-day storage. Have to
        %convert project inflows ("local") to kAF. Note: there is a minimum flow release of 3500cfs associated with this dam.  
        BRN_dg = max(0,s_12 + local(i,12)*.001987 - BRN_ORC(julian));
        %If reservoir storage is low
        if BRN_dg > s_12 + local(i,12)*.001987
            BRN_dg = s_12 + local(i,12)*.001987;
        end
        
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,BRN_dg - f_max(12));
        
        %Is any storage space available?
        stor_avail = BRN_fctarget - s_12;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,12) = f_max(12);
            spill(i,12) = BRN_dg - f_max(12);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            BRN_dg = max(BRN_dg - stor_avail,f_max(12));
            powerflow(i,12) = f_max(12);
            spill(i,12) = max(0,BRN_dg - f_max(12));
        else 
            powerflow(i,12) = BRN_dg;
        end
        
        s_12 = s_12 + local(i,12)*.001987 - BRN_dg;
        discharge(i,12) = BRN_dg*(1/.001987); %Convert back to cfs
        storage(i,12) = s_12;

    else
    %Refill mode - this is when the reservoir fills back up during spring
    %floods. Only storage target is maximum reservoir storage (spillway
    %threshold).

        BRN_dg = max(0,s_12 + local(i,12)*.001987 - BRN_ORC(julian));
        %If reservoir storage is low
        if BRN_dg > s_12 + local(i,12)*.001987
            BRN_dg = s_12 + local(i,12)*.001987;
        end
               
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,BRN_dg - f_max(12));
        
        %Is any storage space available?
        stor_avail = s_max(12) - s_12;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,12) = f_max(12);
            spill(i,12) = BRN_dg - f_max(12);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            BRN_dg = max(BRN_dg - stor_avail,f_max(12));
            powerflow(i,12) = f_max(12);
            spill(i,12) = max(0,BRN_dg - f_max(12));
        else 
            powerflow(i,12) = BRN_dg;
        end
        
        s_12 = s_12 + local(i,12)*.001987 - BRN_dg;
        discharge(i,12) = BRN_dg*(1/.001987);
        storage(i,12) = s_12;     
 
    end
    
    %Convert storage to AF
    BRN_stor = s_12*1000;
    smax = s_max(12)*1000;
    %What is forebay elevation?
    BRN_forebay = StorEq(12,2)*BRN_stor^4 + StorEq(12,3)*BRN_stor^3 + StorEq(12,4)*BRN_stor^2 + StorEq(12,5)*BRN_stor + StorEq(12,6);  
    %What is tailwater elevation?
    BRN_tailwater = (StorEq(12,2)*smax^4 + StorEq(12,3)*smax^3 + StorEq(12,4)*smax^2 + StorEq(12,5)*smax + StorEq(12,6)-229); 
    %Convert head to meters.
    BRN_head = (BRN_forebay - BRN_tailwater)*.3048;
    generation(i,12) = ((1000*BRN_head*powerflow(i,12)*14.27641*9.81*.87)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Oxbow - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    OXB_dg = local(i,35)*.001987 + BRN_dg;
    s_35 = s_35 + local(i,35)*.001987 + BRN_dg - OXB_dg;
    powerflow(i,35) = min(OXB_dg,f_max(35));
    spill(i,35) = max(0,OXB_dg - f_max(35));
    discharge(i,35) = OXB_dg*(1/.001987);
    storage(i,35) = s_35;
    generation(i,35) = ((1000*31.2674*powerflow(i,35)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Hell's Canyon - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    HLC_dg = local(i,44)*.001987 + OXB_dg;
    s_44 = s_44 + local(i,44)*.001987 + OXB_dg - HLC_dg;
    powerflow(i,44) = min(HLC_dg,f_max(44));
    spill(i,44) = max(0,HLC_dg - f_max(44));
    discharge(i,44) = HLC_dg*(1/.001987);
    storage(i,44) = s_44;
    generation(i,44) = ((1000*53.62*powerflow(i,44)*14.27641*9.81*.875)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Dworshak - storage project
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Are we in evacuation or refill?
    %If ICF exists, then fill start date is ICF - 20.
    if fillstart>0
        evac = julian<fillstart || julian>243;
    %Otherwise just use schedule.
    else
        evac = julian<182 || julian>243;
    end
    
     %Is it spring (January 1 - June 30) or fall (September 1 - December 31)
        spring = julian<182;
      % Calculate "forecasted" inflows to Dworshak (April - July)
        if spring>0
           DWR_for = sum(local((year-2)*365+213:(year-2)*365+334,13));
        else
           DWR_for = sum(local((year-1)*365+213:(year-1)*365+334,13));
        end

        %Convert forecast to kAF
        DWR_for = DWR_for*.001987;

        %Identify target reservoir storage. A number of flood control curves
        %are publically available. They are based on forecasted inflows. Some interpolation is
        %necessary when the forecasted flows are in-between those specifiec by
        %USACE.

        if DWR_for <= 1200
            DWR_fctarget = DWR_fc(julian,1);
        elseif DWR_for > 1200 && DWR_for <= 1400
            DWR_fctarget = DWR_fc(julian,1) + ((DWR_for - 1200)/(1400-1200))*(DWR_fc(julian,2) - DWR_fc(julian,1));
        elseif DWR_for > 1400 && DWR_for <= 1800
            DWR_fctarget = DWR_fc(julian,2) + ((DWR_for - 1400)/(1800-1400))*(DWR_fc(julian,3) - DWR_fc(julian,2));
        elseif DWR_for > 1800 && DWR_for <= 2200
            DWR_fctarget = DWR_fc(julian,3) + ((DWR_for - 1800)/(2200-1800))*(DWR_fc(julian,4) - DWR_fc(julian,3));
        elseif DWR_for > 2200 && DWR_for <= 2600
            DWR_fctarget = DWR_fc(julian,4) + ((DWR_for - 2200)/(2600-2200))*(DWR_fc(julian,5) - DWR_fc(julian,4));
        elseif DWR_for > 2600 && DWR_for <= 3000
            DWR_fctarget = DWR_fc(julian,5) + ((DWR_for - 2600)/(3000-2600))*(DWR_fc(julian,6) - DWR_fc(julian,5));
        elseif DWR_for > 3000 && DWR_for <= 3200
            DWR_fctarget = DWR_fc(julian,6) + ((DWR_for - 3000)/(3200-3000))*(DWR_fc(julian,7) - DWR_fc(julian,6));
        elseif DWR_for > 3200 && DWR_for <= 3400
            DWR_fctarget = DWR_fc(julian,7) + ((DWR_for - 3200)/(3400-3200))*(DWR_fc(julian,8) - DWR_fc(julian,7));
        elseif DWR_for > 3400 && DWR_for <= 3600
            DWR_fctarget = DWR_fc(julian,8) + ((DWR_for - 3600)/(3600-3400))*(DWR_fc(julian,9) - DWR_fc(julian,8));
        elseif DWR_for > 3600 && DWR_for <= 3800
            DWR_fctarget = DWR_fc(julian,9) + ((DWR_for - 3800)/(3800-3600))*(DWR_fc(julian,10) - DWR_fc(julian,9));
        elseif DWR_for > 3800
            DWR_fctarget = DWR_fc(julian,10); 
        end

    if i==1
          %DNC's storage forecaste
          DWR_sfore(i)=min((local(i,13)-1600)*.001987+s_13,s_max(13));
      else
          DWR_sfore(i)=min((local(i,13)-1600)*.001987+ storage(i-1,13),s_max(13));
      end
          DWR_VRC= DWR_sfore(i);
          
        if julian>=213 && julian <=365
           DWR_ORC(julian)= max(DWR_CRC(julian,2),DWR_ARC(julian,2));
           DWR_ORC(julian)= min(DWR_ORC(julian),DWR_fctarget);
          
        elseif julian >=1 && julian <= 212
           DWR_ORC(julian)= min(DWR_VRC,max(DWR_CRC(julian,2),DWR_ARC(julian,2)));
           DWR_ORC(julian)= min(DWR_ORC(julian),DWR_fctarget);
        end
        
    if evac>0 
    %Evacuation mode

   

      
        %Calculate daily reservoir discharge and end-of-day storage. Have to
        %convert project inflows ("local") to kAF.
        DWR_dg = max(1600*.001987, s_13 + local(i,13)*.001987 -  DWR_ORC(julian));
        %If reservoir is low
        if DWR_dg > s_13 + local(i,13)*.001987
            DWR_dg = s_13 + local(i,13)*.001987;
        end
        
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,DWR_dg - f_max(13));
        
        %Is any storage space available?
        stor_avail = DWR_fctarget - s_13;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,13) = f_max(13);
            spill(i,13) = DWR_dg - f_max(13);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            DWR_dg = max(DWR_dg - stor_avail,f_max(13));
            powerflow(i,13) = f_max(13);
            spill(i,13) = max(0,DWR_dg - f_max(13));
        else 
            powerflow(i,13) = DWR_dg;
        end
        
        s_13 = s_13 + local(i,13)*.001987 - DWR_dg;
        discharge(i,13) = DWR_dg*(1/.001987); %Convert back to cfs
        storage(i,13) = s_13;

    else
    %Refill mode - this is when the reservoir fills back up during spring
    %floods. Only storage target is maximum reservoir storage (spillway
    %threshold).

    DWR_dg = max(1600*.001987, s_13 + local(i,13)*.001987 -  DWR_ORC(julian));
        if DWR_dg > s_13 + local(i,13)*.001987
           DWR_dg = s_13 + local(i,13)*.001987;
        end
    
        %Do flows exceed hydraulic capacity of dam? 
        overflow = max(0,DWR_dg - f_max(13));
        
        %Is any storage space available?
        stor_avail = s_max(13) - s_13;
        
        %If flows exceed dam's hydraulic capacity.
        if overflow>0 && stor_avail<=0
            %If there is no storage available,then total discharge remains
            %the same, and anything beyond hydraulic capacity of dam is
            %spilled. 
            powerflow(i,13) = f_max(13);
            spill(i,13) = DWR_dg - f_max(13);
        elseif overflow>0 && stor_avail>0
            %If there is some storage available, total release must be revised down and additional water
            %stored.
            DWR_dg = max(DWR_dg - stor_avail,f_max(13));
            powerflow(i,13) = f_max(13);
            spill(i,13) = max(0,DWR_dg - f_max(13));
        else 
            powerflow(i,13) = DWR_dg;
        end

        
    s_13 = s_13 + local(i,13)*.001987 - DWR_dg;
    discharge(i,13) = DWR_dg*(1/.001987);
    storage(i,13) = s_13;     

    end
    
    %Convert storage to AF
    DWR_stor = s_13*1000;
    %What is forebay elevation?
    DWR_forebay = StorEq(13,2)*DWR_stor^4 + StorEq(13,3)*DWR_stor^3 + StorEq(13,4)*DWR_stor^2 + StorEq(13,5)*DWR_stor + StorEq(13,6);  
    %What is tailwater elevation?
    DWR_tailwater = TailEq(13,2)*discharge(i,13)^4 + TailEq(13,3)*discharge(i,13)^3 + TailEq(13,4)*discharge(i,13)^2 + TailEq(13,5)*discharge(i,13) + TailEq(13,6); 
    %Convert head to meters.
    DWR_head(i) = (DWR_forebay - DWR_tailwater)*.3048;
    generation(i,13) = ((1000*DWR_head(i)*powerflow(i,13)*14.27641*9.81*.83)/1000000)*24;
    Spillheads(i,3)=DWR_head(i);

    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Lower Granite - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Calculate daily reservoir discharge and end-of-day storage. Have to
    %convert project inflows ("local") to kAF.
    %Note: There is a 1-day travel delay between Hell's Canyon and Dworshak
    %and Lower Granite. 
    if i>1
    LWG_dg = local(i,36)*.001987 + discharge(i-1,13)*.001987 + discharge (i-1,44)*.001987 + ORF5H(i)* .001987 + SPD5L(i)*.001987 + ANA5L(i)*.001987 + LIM5L(i)*.001987 + WHB5H(i)*.001987;
    s_36 = s_36 + local(i,36)*.001987 + discharge(i-1,13)*.001987 + discharge (i-1,44)*.001987+ ORF5H(i)* .001987 + SPD5L(i)*.001987 + ANA5L(i)*.001987 + LIM5L(i)*.001987 + WHB5H(i)*.001987 - LWG_dg;
    else
    LWG_dg = local(i,36)*.001987 + discharge(i,13)*.001987 + discharge (i,44)*.001987+ ORF5H(i)* .001987 + SPD5L(i)*.001987 + ANA5L(i)*.001987 + LIM5L(i)*.001987 + WHB5H(i)*.001987;
    s_36 = s_36 + local(i,36)*.001987 + discharge(i,13)*.001987 + discharge (i,44)*.001987 + ORF5H(i)* .001987 + SPD5L(i)*.001987 + ANA5L(i)*.001987 + LIM5L(i)*.001987 + WHB5H(i)*.001987 - LWG_dg;
    end
    powerflow(i,36) = min(LWG_dg,f_max(36));
    spill(i,36) = max(0,LWG_dg - f_max(36));
    discharge(i,36) = LWG_dg*(1/.001987); %Convert back to cfs
    storage(i,36) = s_36;
    %Convert storage to AF
    LWG_stor = s_36*1000;
    %What is forebay elevation?
    LWG_forebay = StorEq(36,2)*LWG_stor^4 + StorEq(36,3)*LWG_stor^3 + StorEq(36,4)*LWG_stor^2 + StorEq(36,5)*LWG_stor + StorEq(36,6);  
    %What is tailwater elevation?
    LWG_tailwater = TailEq(36,2)*discharge(i,36)^4 + TailEq(36,3)*discharge(i,36)^3 + TailEq(36,4)*discharge(i,36)^2 + TailEq(36,5)*discharge(i,36) + TailEq(36,6); 
    %Convert head to meters.
    LWG_head(i) = (LWG_forebay - LWG_tailwater)*.3048;
    generation(i,36) = ((1000*LWG_head(i)*powerflow(i,36)*14.27641*9.81*.86)/1000000)*24;
    heads(i,3)=LWG_head(i);
    Spillheads(i,4)=LWG_head(i);

    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Little Goose - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Calculate daily reservoir discharge and end-of-day storage. Have to
    %convert project inflows ("local") to kAF.
    LGO_dg = local(i,37)*.001987 + LWG_dg;
    s_37 = s_37 + local(i,37)*.001987 + LWG_dg - LGO_dg;
    powerflow(i,37) = min(LGO_dg,f_max(37));
    spill(i,37) = max(0,LGO_dg - f_max(37));
    discharge(i,37) = LGO_dg*(1/.001987); %Convert back to cfs
    storage(i,37) = s_37;
    %Convert storage to AF
    LGO_stor = s_37*1000;
    %What is forebay elevation?
    LGO_forebay = StorEq(37,2)*LGO_stor^4 + StorEq(37,3)*LGO_stor^3 + StorEq(37,4)*LGO_stor^2 + StorEq(37,5)*LGO_stor + StorEq(37,6);  
    %What is tailwater elevation?
    LGO_tailwater = TailEq(37,2)*discharge(i,37)^4 + TailEq(37,3)*discharge(i,37)^3 + TailEq(37,4)*discharge(i,37)^2 + TailEq(37,5)*discharge(i,37) + TailEq(37,6); 
    %Convert head to meters.
    LGO_head(i) = (LGO_forebay - LGO_tailwater)*.3048;
    generation(i,37) = ((1000*LGO_head(i)*powerflow(i,37)*14.27641*9.81*.86)/1000000)*24;
    heads(i,4)=LGO_head(i);
    Spillheads(i,5)=LGO_head(i);

    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Lower Monumental - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Calculate daily reservoir discharge and end-of-day storage. Have to
    %convert project inflows ("local") to kAF.
    LMN_dg = local(i,38)*.001987 + LGO_dg;
    s_38 = s_38 + local(i,38)*.001987 + LGO_dg - LMN_dg;
    powerflow(i,38) = min(LMN_dg,f_max(38));
    spill(i,38) = max(0,LMN_dg - f_max(38));
    discharge(i,38) = LMN_dg*(1/.001987); %Convert back to cfs
    storage(i,38) = s_38;
    %Convert storage to AF
    LMN_stor = s_38*1000;
    %What is forebay elevation?
    LMN_forebay = StorEq(38,2)*LMN_stor^4 + StorEq(38,3)*LMN_stor^3 + StorEq(38,4)*LMN_stor^2 + StorEq(38,5)*LMN_stor + StorEq(38,6);  
    %What is tailwater elevation?
    LMN_tailwater = TailEq(38,2)*discharge(i,38)^4 + TailEq(38,3)*discharge(i,38)^3 + TailEq(38,4)*discharge(i,38)^2 + TailEq(38,5)*discharge(i,38) + TailEq(38,6); 
    %Convert head to meters.
    LMN_head(i) = (LMN_forebay - LMN_tailwater)*.3048;
    generation(i,38) = ((1000*LMN_head(i)*powerflow(i,38)*14.27641*9.81*.83)/1000000)*24;
    heads(i,5)=LMN_head(i);
    Spillheads(i,6)=LMN_head(i);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Ice Harbor - run-of-river project
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Calculate daily reservoir discharge and end-of-day storage. Have to
    %convert project inflows ("local") to kAF.
    IHR_dg = local(i,39)*.001987 + LMN_dg;
    s_39 = s_39 + local(i,39)*.001987 + LMN_dg - IHR_dg;
    powerflow(i,39) = min(IHR_dg,f_max(39));
    spill(i,39) = max(0,IHR_dg - f_max(39));
    discharge(i,39) = IHR_dg*(1/.001987); %Convert back to cfs
    storage(i,39) = s_39;
    %Convert storage to AF
    IHR_stor = s_39*1000;
    %What is forebay elevation?
    IHR_forebay = StorEq(39,2)*IHR_stor^4 + StorEq(39,3)*IHR_stor^3 + StorEq(39,4)*IHR_stor^2 + StorEq(39,5)*IHR_stor + StorEq(39,6);  
    %What is tailwater elevation?
    IHR_tailwater = TailEq(39,2)*discharge(i,39)^4 + TailEq(39,3)*discharge(i,39)^3 + TailEq(39,4)*discharge(i,39)^2 + TailEq(39,5)*discharge(i,39) + TailEq(39,6); 
    %Convert head to meters.
    IHR_head(i) = (IHR_forebay - IHR_tailwater)*.3048;
    generation(i,39) = ((1000*IHR_head(i)*powerflow(i,39)*14.27641*9.81*.83)/1000000)*24;
    heads(i,6)=IHR_head(i);
    Spillheads(i,7)=IHR_head(i);

    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %LOWER COLUMBIA RIVER PROJECTS
    %McNary, Round Butte, Pelton, John Day, The Dalles, and Bonneville
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Round Butte - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Calculate daily reservoir discharge and end-of-day storage. Have to
    %convert project inflows ("local") to kAF.
    RBU_dg = local(i,15)*.001987;
    s_15 = s_15 + local(i,15)*.001987 - RBU_dg;
    powerflow(i,15) = min(RBU_dg,f_max(15));
    spill(i,15) = max(0,RBU_dg - f_max(15));
    discharge(i,15) = RBU_dg*(1/.001987); %Convert back to cfs
    storage(i,15) = s_15; 
    generation(i,15) = ((1000*134*powerflow(i,15)*14.27641*9.81*.83)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Pelton - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Calculate daily reservoir discharge and end-of-day storage. Have to
    %convert project inflows ("local") to kAF.
    PLT_dg = local(i,45)*.001987 + RBU_dg;
    s_45 = s_45 + local(i,45)*.001987 - PLT_dg;
    powerflow(i,45) = min(PLT_dg,f_max(45));
    spill(i,45) = max(0,PLT_dg - f_max(45));
    discharge(i,45) = PLT_dg*(1/.001987); %Convert back to cfs
    storage(i,45) = s_45; 
    generation(i,45) = ((1000*62.1792*powerflow(i,45)*14.27641*9.81*.87)/1000000)*24;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %McNary - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Calculate daily reservoir discharge and end-of-day storage. Have to
    %convert project inflows ("local") to kAF.
    MCN_dg = local(i,40)*.001987 + PRD_dg +IHR_dg + YAK5H(i)*.001987;
    s_40 = s_40 + local(i,40)*.001987 + PRD_dg +IHR_dg + YAK5H(i)*.001987 - MCN_dg;
    powerflow(i,40) = min(MCN_dg,f_max(40));
    spill(i,40) = max(0,MCN_dg - f_max(40));
    discharge(i,40) = MCN_dg*(1/.001987); %Convert back to cfs
    storage(i,40) = s_40; 
    %Convert storage to AF
    MCN_stor = s_40*1000;
    %What is forebay elevation?
    MCN_forebay = StorEq(40,2)*MCN_stor^4 + StorEq(40,3)*MCN_stor^3 + StorEq(40,4)*MCN_stor^2 + StorEq(40,5)*MCN_stor + StorEq(40,6);  
    %What is tailwater elevation?
    MCN_tailwater = TailEq(40,2)*discharge(i,40)^4 + TailEq(40,3)*discharge(i,40)^3 + TailEq(40,4)*discharge(i,40)^2 + TailEq(40,5)*discharge(i,40) + TailEq(40,6); 
    %Convert head to meters.
    MCN_head(i) = (MCN_forebay - MCN_tailwater)*.3048;
    generation(i,40) = ((1000*MCN_head(i)*powerflow(i,40)*14.27641*9.81*.76)/1000000)*24;
    heads(i,7)=MCN_head(i);
    Spillheads(i,8)=MCN_head(i);

    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %John Day - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Calculate daily reservoir discharge and end-of-day storage. Have to
    %convert project inflows ("local") to kAF.
    JDA_dg = local(i,41)*.001987 + MCN_dg;
    s_41 = s_41 + local(i,41)*.001987 + MCN_dg - JDA_dg;
    powerflow(i,41) = min(JDA_dg,f_max(41));
    spill(i,41) = max(0,JDA_dg - f_max(41));
    discharge(i,41) = JDA_dg*(1/.001987); %Convert back to cfs
    storage(i,41) = s_41; 
    %Convert storage to AF
    JDA_stor = s_41*1000;
    %What is forebay elevation?
    JDA_forebay = StorEq(41,2)*JDA_stor^4 + StorEq(41,3)*JDA_stor^3 + StorEq(41,4)*JDA_stor^2 + StorEq(41,5)*JDA_stor + StorEq(41,6);  
    %What is tailwater elevation?
    JDA_tailwater = TailEq(41,2)*discharge(i,41)^4 + TailEq(41,3)*discharge(i,41)^3 + TailEq(41,4)*discharge(i,41)^2 + TailEq(41,5)*discharge(i,41) + TailEq(41,6); 
    %Convert head to meters.
    JDA_head(i) = (JDA_forebay - JDA_tailwater)*.3048;
    generation(i,41) = ((1000*JDA_head(i)*powerflow(i,41)*14.27641*9.81*.87)/1000000)*24;
    heads(i,8)=JDA_head(i);
    Spillheads(i,9)=JDA_head(i);

    %%%%%%%%%%%%%%%%%%%%%%%%%
    %The Dalles - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Calculate daily reservoir discharge and end-of-day storage. Have to
    %convert project inflows ("local") to kAF.
    TDA_dg = local(i,42)*.001987 + JDA_dg + PLT_dg;
    s_42 = s_42 + local(i,42)*.001987 + JDA_dg + PLT_dg - TDA_dg;
    powerflow(i,42) = min(TDA_dg,f_max(42));
    spill(i,42) = max(0,TDA_dg - f_max(42));
    discharge(i,42) = TDA_dg*(1/.001987); %Convert back to cfs
    storage(i,42) = s_42; 
    %Convert storage to AF
    TDA_stor = s_42*1000;
    %What is forebay elevation?
    TDA_forebay = 13.891*log(TDA_stor) - 20.692;  
    %What is tailwater elevation?
    TDA_tailwater = TailEq(42,2)*discharge(i,42)^4 + TailEq(42,3)*discharge(i,42)^3 + TailEq(42,4)*discharge(i,42)^2 + TailEq(42,5)*discharge(i,42) + TailEq(42,6); 
    %Convert head to meters.
    TDA_head = (TDA_forebay - TDA_tailwater)*.3048;
    generation(i,42) = ((1000*TDA_head*powerflow(i,42)*14.27641*9.81*.86)/1000000)*24;
    heads(i,9)=TDA_head;
    Spillheads(i,10)=TDA_head;

    
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Bonneville - run-of-river
    %%%%%%%%%%%%%%%%%%%%%%%%%
    
    %Calculate daily reservoir discharge and end-of-day storage. Have to
    %convert project inflows ("local") to kAF.
    BNN_dg = local(i,43)*.001987 + TDA_dg;
    s_43 = s_43 + local(i,43)*.001987 + TDA_dg - BNN_dg;
    powerflow(i,43) = min(BNN_dg,f_max(43));
    spill(i,43) = max(0,BNN_dg - f_max(43));
    discharge(i,43) = BNN_dg*(1/.001987); %Convert back to cfs
    storage(i,43) = s_43;
    %Convert storage to AF
    BNN_stor = s_43*1000;
    %What is forebay elevation?
    BNN_forebay = StorEq(43,2)*BNN_stor^4 + StorEq(43,3)*BNN_stor^3 + StorEq(43,4)*BNN_stor^2 + StorEq(43,5)*BNN_stor + StorEq(43,6);  
    %What is tailwater elevation?
    BNN_tailwater = TailEq(43,2)*discharge(i,43)^4 + TailEq(43,3)*discharge(i,43)^3 + TailEq(43,4)*discharge(i,43)^2 + TailEq(43,5)*discharge(i,43) + TailEq(43,6); 
    %Convert head to meters.
    BNN_head = (BNN_forebay - BNN_tailwater)*.3048;
    generation(i,43) = ((1000*BNN_head*powerflow(i,43)*14.27641*9.81*.92)/1000000)*24;
    heads(i,10)=BNN_head;
    Spillheads(i,11)=BNN_head;

    
    
end



%%%%%%%%%%%%
%Data Output
%%%%%%%%%%%%

%  xlswrite('Output.xlsx',storage,'Storage');
%  xlswrite('Output.xlsx',discharge,'Discharge');
%  xlswrite('Output2.xlsx',powerflow,'Powerflow');
%  xlswrite('Output2.xlsx',spill,'Spill');
%  xlswrite('Output3.xlsx',generation,'Generation');
csvwrite('PNW_hydro/FCRPS/discharge.csv',discharge);
csvwrite('PNW_hydro/FCRPS/storage.csv',storage);
csvwrite('PNW_hydro/FCRPS/powerflow.csv',powerflow);
csvwrite('PNW_hydro/FCRPS/spill.csv',spill);
csvwrite('PNW_hydro/FCRPS/generation.csv',generation);
csvwrite('PNW_hydro/FCRPS/heads.csv',heads);


generation(1,:)=generation(3,:);
generation(2,:)=generation(3,:);

total=sum(generation');
total=total';
% nature_spill(:,1)=spill(:,10);
% nature_spill(:,2)=spill(:,11);
% nature_spill(:,3)=spill(:,13);
% nature_spill(:,4)=spill(:,36);
% nature_spill(:,5)=spill(:,37);
% nature_spill(:,6)=spill(:,38);
% nature_spill(:,7)=spill(:,39);
% nature_spill(:,8)=spill(:,40);
% nature_spill(:,9)=spill(:,41);
% nature_spill(:,10)=spill(:,42);
% nature_spill(:,11)=spill(:,43);
% 
Modeled(:,1)=generation(:,10);
Modeled(:,2)=generation(:,11);
Modeled(:,3)=generation(:,13);
Modeled(:,4)=generation(:,36);
Modeled(:,5)=generation(:,37);
Modeled(:,6)=generation(:,38);
Modeled(:,7)=generation(:,39);
Modeled(:,8)=generation(:,40);
Modeled(:,9)=generation(:,41);
Modeled(:,10)=generation(:,42);
Modeled(:,11)=generation(:,43);
Modeled(:,12)=generation(:,8);
Modeled(:,13)=generation(:,3);



Modeled(1,:)=Modeled(3,:);
Modeled(2,:)=Modeled(3,:);



Unmodeled(:,1)=generation(:,10)*0.0038;
Unmodeled(:,2)=generation(:,24)*1.77;
Unmodeled(:,3)=generation(:,21)*0.017;
Unmodeled(:,4)=generation(:,40)*0.0621;
Unmodeled(:,5)=total*0.0015;
Unmodeled(:,6)=generation(:,42)*0.019;
Unmodeled(:,7)=generation(:,40)*0.024;
Unmodeled(:,8)=generation(:,40)*0.012;
Unmodeled(:,9)=generation(:,33)*0.012;
Unmodeled(:,10)=generation(:,34)*0.0126;
Unmodeled(:,11)=generation(:,40)*0.0089;
Unmodeled(:,12)=total*0.00022;
Unmodeled(:,13)=total*0.00022;
Unmodeled(:,14)=generation(:,20)*0.0196;
Unmodeled(:,15)=generation(:,40)*0.0036;
Unmodeled(:,16)=generation(:,20)*0.0169;
Unmodeled(:,17)=generation(:,42)*0.0018;
Unmodeled(:,18)=generation(:,22)*0.0012;
Unmodeled(:,19)=generation(:,39)*0.00159;
Unmodeled(:,20)=total*0.0000139;
Unmodeled(:,21)=generation(:,40)*0.000426;
Unmodeled(:,22)=total*0.000011;
Unmodeled(:,23)=total*0.000083;
Unmodeled(:,24)=generation(:,32)*0.015;
Unmodeled(:,25)=generation(:,32)*0.0106;
Unmodeled(:,26)=generation(:,32)*0.497;
Unmodeled(:,27)=generation(:,32)*0.216;
Unmodeled(:,28)=generation(:,32)*0.2148;
Unmodeled(:,29)=generation(:,43)*0.034;
Unmodeled(:,30)=generation(:,43)*0.0308;
Unmodeled(:,31)=generation(:,43)*0.0299;
Unmodeled(:,32)=generation(:,32)*0.179;
Unmodeled(:,33)=generation(:,32)*0.168;
Unmodeled(:,34)=generation(:,40)*0.036;
Unmodeled(:,35)=generation(:,32)*0.019;
Unmodeled(:,36)=generation(:,32)*0.0024;
Unmodeled(:,37)=generation(:,32)*0.0016;
Unmodeled(:,38)=generation(:,32)*0.72;
Unmodeled(:,39)=generation(:,32)*0.33;
Unmodeled(:,40)=generation(:,32)*0.266;
Unmodeled(:,41)=generation(:,34)*0.0176;
Unmodeled(:,42)=generation(:,38)*0.0065;
Unmodeled(:,43)=generation(:,40)*0.266;
Unmodeled(:,44)=generation(:,40)*0.144;
Unmodeled(:,45)=generation(:,10)*0.13;
Unmodeled(:,46)=generation(:,40)*0.057;
Unmodeled(:,47)=generation(:,40)*0.044;

%Modeled 14 is all of the unmodeled dams
total_unmodeled=sum(Unmodeled');
%Modeled(:,14)=total_unmodeled';




%BPAT dams
BPAT_modeled(:,1:13)=Modeled;
BPAT_modeled(:,14)=Unmodeled(:,10) ;%Chandler
BPAT_modeled(:,15)=Unmodeled(:,4) ;%Cowlitz
BPAT_modeled(:,16)=Unmodeled(:,17) ;%Middle Fork
BPAT_modeled(:,17)=Unmodeled(:,7) ;%Packwood
BPAT_modeled(:,18)=Unmodeled(:,9) ;%Roza
BPAT_modeled(:,19)=Unmodeled(:,5) ;%Smith Creek
BPAT_modeled(:,20)=Unmodeled(:,6) ;% Dalles N Fishway
BPAT_modeled(:,21)=Unmodeled(:,15); %Yakama Drop 

generation(:,48)=total_unmodeled;
Total_generation=generation;
Total_generation(:,[1,2,4,5,16])=[];
%BPA owned dams
Modeled=Modeled(123:length(Modeled)-243,:);
%BPAT dams
BPAT_modeled=BPAT_modeled(123:length(BPAT_modeled)-243,:);
%Total Generation
Total_generation=Total_generation(123:length(Total_generation)-243,:);

csvwrite('PNW_hydro/FCRPS/BPA_owned_dams.csv',Modeled)
csvwrite('PNW_hydro/FCRPS/Modeled_BPAT_dams.csv',BPAT_modeled)
csvwrite('PNW_hydro/FCRPS/Total_PNW_dams.csv',Total_generation)