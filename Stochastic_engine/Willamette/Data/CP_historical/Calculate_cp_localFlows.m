
% Load historical control point daily inflow data downloaded from USGS and aggregated to daily 
% cut to 12/31/1988 - 12/31/2007
ALBin = xlsread('Control point historical discharge 1989_2007',1);
SALin = xlsread('Control point historical discharge 1989_2007',2);
HARin = xlsread('Control point historical discharge 1989_2007',3);
HARin_shift = [8838.367347; HARin(1:end-1)]; %shifted to 12/30/1988
VIDin = xlsread('Control point historical discharge 1989_2007',4);
JEFin = xlsread('Control point historical discharge 1989_2007',5);
MEHin = xlsread('Control point historical discharge 1989_2007',6);
MONin = xlsread('Control point historical discharge 1989_2007',7);
MONin_shift = [1854.583333; MONin(1:end-1)]; %shifted to 12/30/1988
WATin = xlsread('Control point historical discharge 1989_2007',8);
JASin = xlsread('Control point historical discharge 1989_2007',9);
GOSin = xlsread('Control point historical discharge 1989_2007',10);

% plot 
figure; ax1=subplot(2,5,1);plot(ALBin);title('Albany');ylabel('ft^3/s') 
hold on; ax2=subplot(2,5,2);plot(GOSin);title('Goshen');ylabel('ft^3/s')
ax3=subplot(2,5,3);plot(HARin);title('Harrisburg');ylabel('ft^3/s')
ax4=subplot(2,5,4);plot(JASin);title('Jasper');ylabel('ft^3/s') 
% 
ax5=subplot(2,5,5);plot(MEHin);title('Mehama');ylabel('ft^3/s')
ax6=subplot(2,5,6);plot(MONin);title('Monroe');ylabel('ft^3/s')
ax7=subplot(2,5,7);plot(SALin);title('Salem');ylabel('ft^3/s')
ax8=subplot(2,5,8);plot(VIDin);title('Vida');ylabel('ft^3/s')
ax9=subplot(2,5,9);plot(WATin);title('Waterloo');ylabel('ft^3/s')
ax10=subplot(2,5,10);plot(JEFin);title('Jefferson');ylabel('ft^3/s')
linkaxes([ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10],'xy')
suptitle('Historic streamflow at control points (USGS stations)')

% Load historical reservoirs daily outflow data downloaded from BPA modified streamflow page 
% 01/07/1928 - 09/30/2008 cut to 1/1/1989 - 12/31/2007
[DEXout,~, raw] = xlsread('../Res_historical/Res_out/\DEX5M_daily.xls');
ind(1)=find (strcmp(raw(:,1),'12/31/1988'));ind(2)=find(strcmp(raw(:,1),'12/31/2007'));
DEXout=DEXout(ind(1):ind(2));
[FALout,~, raw] = xlsread('../Res_historical/Res_out/\FAL5H_daily.xls');
ind(1)=find (strcmp(raw(:,1),'12/31/1988'));ind(2)=find(strcmp(raw(:,1),'12/31/2007'));
FALout=FALout(ind(1):ind(2));
[DORout, ~, raw] = xlsread('../Res_historical/Res_out/\DOR5H_daily.xls');
ind(1)=find (strcmp(raw(:,1),'12/31/1988'));ind(2)=find(strcmp(raw(:,1),'12/31/2007'));
DORout=DORout(ind(1):ind(2));
[CGRout, ~, raw] = xlsread('../Res_historical/Res_out/\CGR5H_daily.xls');
ind(1)=find (strcmp(raw(:,1),'12/31/1988'));ind(2)=find(strcmp(raw(:,1),'12/31/2007'));
CGRout=CGRout(ind(1):ind(2));
[BLUout, ~, raw] = xlsread('../Res_historical/Res_out/\BLU5H_daily.xls');
ind(1)=find (strcmp(raw(:,1),'12/31/1988'));ind(2)=find(strcmp(raw(:,1),'12/31/2007'));
BLUout=BLUout(ind(1):ind(2));
[FRNout, ~, raw] = xlsread('../Res_historical/Res_out/\FRN5H_daily.xls');
ind(1)=find (strcmp(raw(:,1),'12/31/1988'));ind(2)=find(strcmp(raw(:,1),'12/31/2007'));
FRNout=FRNout(ind(1):ind(2));
[FOSout, ~, raw]= xlsread('../Res_historical/Res_out/\FOS5H_daily.xls');
ind(1)=find (strcmp(raw(:,1),'12/31/1988'));ind(2)=find(strcmp(raw(:,1),'12/31/2007'));
FOSout=FOSout(ind(1):ind(2));
[BCLout, ~, raw] = xlsread('../Res_historical/Res_out/\BCL5H_daily.xls');
ind(1)=find (strcmp(raw(:,1),'12/31/1988'));ind(2)=find(strcmp(raw(:,1),'12/31/2007'));
BCLout=BCLout(ind(1):ind(2));
[COTout, ~, raw] = xlsread('../Res_historical/Res_out/\COT5H_daily.xls');
ind(1)=find (strcmp(raw(:,1),'12/31/1988'));ind(2)=find(strcmp(raw(:,1),'12/31/2007'));
COTout=COTout(ind(1):ind(2));

%plot
figure; ax1=subplot(2,5,1);plot(DEXout);title('Dexter');ylabel('ft^3/s') 
hold on; ax2=subplot(2,5,2);plot(FALout);title('Fall Creek');ylabel('ft^3/s')
ax3=subplot(2,5,3);plot(DORout);title('Dorena');ylabel('ft^3/s')
ax4=subplot(2,5,4);plot(CGRout);title('Cougar');ylabel('ft^3/s') 
ax5=subplot(2,5,5);plot(BLUout);title('Blue River');ylabel('ft^3/s')
ax6=subplot(2,5,6);plot(FRNout);title('Fern Ridge');ylabel('ft^3/s')
ax7=subplot(2,5,7);plot(FOSout);title('Foster');ylabel('ft^3/s')
ax8=subplot(2,5,8);plot(BCLout);title('Big Cliff');ylabel('ft^3/s')
ax9=subplot(2,5,9);plot(COTout);title('Cottage Grove');ylabel('ft^3/s')
%linkaxes([ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9],'xy')
suptitle('Historic reservoirs releases(BPA modified streamflow)')

% Apply balance equations and calculate local flows
SALloc = SALin - ALBin - JEFin;
JEFloc = JEFin - WATin - MEHin;
MEHloc = MEHin - BCLout;
WATloc = WATin - FOSout;
ALBloc = ALBin - MONin_shift - HARin_shift;
MONloc = MONin - FRNout;
HARloc = HARin - VIDin - GOSin - JASin;
VIDloc = VIDin - CGRout - BLUout;
JASloc = JASin - DEXout - FALout;
GOSloc = GOSin - COTout - DORout;

%plot
figure; ax1=subplot(2,5,1);plot(ALBloc);title('Albany');ylabel('ft^3/s') 
hold on; ax2=subplot(2,5,2);plot(GOSloc);title('Goshen');ylabel('ft^3/s')
ax3=subplot(2,5,3);plot(HARloc);title('Harrisburg');ylabel('ft^3/s')
ax4=subplot(2,5,4);plot(JASloc);title('Jasper');ylabel('ft^3/s') 
ax5=subplot(2,5,5);plot(MEHloc);title('Mehama');ylabel('ft^3/s')
ax6=subplot(2,5,6);plot(MONloc);title('Monroe');ylabel('ft^3/s')
ax7=subplot(2,5,7);plot(SALloc);title('Salem');ylabel('ft^3/s')
ax8=subplot(2,5,8);plot(VIDloc);title('Vida');ylabel('ft^3/s')
ax9=subplot(2,5,9);plot(WATloc);title('Waterloo');ylabel('ft^3/s')
ax10=subplot(2,5,10);plot(JEFloc);title('Jefferson');ylabel('ft^3/s')
suptitle('Derived control points local flows')

% Save results
date=datetime(1988,12,31):datetime(2007,12,31);
cfs_to_cms = 0.0283168;
filename='Controlpoints_local_flows';
T=table(date',ALBloc.*cfs_to_cms,'VariableNames',{'date','local_flows_cms'});
writetable(T, filename, 'FileType','spreadsheet','Sheet','Albany');
T=table(date',SALloc.*cfs_to_cms,'VariableNames',{'date','local_flows_cms'});
writetable(T, filename, 'FileType','spreadsheet','Sheet','Salem');
T=table(date',HARloc.*cfs_to_cms,'VariableNames',{'date','local_flows_cms'});
writetable(T, filename, 'FileType','spreadsheet','Sheet','Harrisburg');
T=table(date',VIDloc.*cfs_to_cms,'VariableNames',{'date','local_flows_cms'});
writetable(T, filename, 'FileType','spreadsheet','Sheet','Vida');
T=table(date',JEFloc.*cfs_to_cms,'VariableNames',{'date','local_flows_cms'});
writetable(T, filename, 'FileType','spreadsheet','Sheet','Jefferson');
T=table(date',MEHloc.*cfs_to_cms,'VariableNames',{'date','local_flows_cms'});
writetable(T, filename, 'FileType','spreadsheet','Sheet','Mehama');
T=table(date',MONloc.*cfs_to_cms,'VariableNames',{'date','local_flows_cms'});
writetable(T, filename, 'FileType','spreadsheet','Sheet','Monroe');
T=table(date',WATloc.*cfs_to_cms,'VariableNames',{'date','local_flows_cms'});
writetable(T, filename, 'FileType','spreadsheet','Sheet','Waterloo');
T=table(date',JASloc.*cfs_to_cms,'VariableNames',{'date','local_flows_cms'});
writetable(T, filename, 'FileType','spreadsheet','Sheet','Jasper');
T=table(date',GOSloc.*cfs_to_cms,'VariableNames',{'date','local_flows_cms'});
writetable(T, filename, 'FileType','spreadsheet','Sheet','Goshen');
