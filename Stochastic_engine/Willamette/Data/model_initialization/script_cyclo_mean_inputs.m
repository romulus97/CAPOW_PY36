% Calculate the cyclostationary filtered mean of historic cp discharge
% historic reservoirs release and volumes

%converters
cfs_to_cms = 0.0283168;
M3_PER_ACREFT = 1233.4;

%cp discharge (1989-2007)
cp_list={'Albany','Salem','Harrisburg','Vida','Jefferson','Mehama','Monroe','Waterloo','Jasper','Goshen','Foster_out','Foster_in'};
for cp=1:length(cp_list)
    %load the data
    [CP(cp).dis,txt] = xlsread('../CP_historical/Control point historical discharge 1989_2007.xlsx',cp_list{cp} );
    %prepare the data for calculating the filter
    CP(cp).dis(startsWith(txt,'2/29'))=[];
    CP(cp).dis=reshape(CP(cp).dis(2:end),365,[]);
    %calculate cyclostationary average
    CP(cp).filtered=cyclo_filter( CP(cp).dis,'mean', 3, 1); 
    CP(cp).filtered=CP(cp).filtered.*cfs_to_cms;
    CP(cp).names=cp_list{cp};
end


%Reservoirs releases (1929-2007)
res_list={'BCL5H','BLU5H','CGR5H','COT5H','DET5H','DEX5M','DOR5H','FAL5H','FOS5H','FRN5H','GPR5H','HCR5H' ,'LOP5H'};
for res=1:length(res_list)
    %load the data
    [RES(res).rel,txt,raw] = xlsread(['../Res_historical/Res_out/', res_list{res},'_daily.xls'],'','A186:B29039');
    %prepare the data for calculating the filter
    RES(res).rel(startsWith(txt,'2/29'))=[];
    RES(res).rel=reshape(RES(res).rel,365,[]);
    %calculate cyclostationary average
    RES(res).rel_filtered=cyclo_filter( RES(res).rel,'mean', 3, 1); 
    RES(res).rel_filtered=RES(res).rel_filtered.*cfs_to_cms;
end

%Reservoirs volumes (2005-2016)
res_list={'BCL','BLU','CGR','COT','DET','DEX','DOR','FAL','FOS','FRN','GPR','HCR' ,'LOP'};
for res=1:length(res_list)
    %load the data
    [RES(res).vol,txt,raw] = xlsread(['../Res_historical/Res_vol/', res_list{res},'.csv']);
    RES(res).vol=RES(res).vol(:,2);
    %eliminate outliers
    outl_id=RES(res).vol(isoutlier(RES(res).vol));
    RES(res).vol(isoutlier(RES(res).vol))=ones(length(outl_id),1)*mean(RES(res).vol);
    %prepare the data for calculating the filter
    dates=datetime(txt(2:end,1));
    doy = day(dates,'dayofyear');
    G=findgroups(doy);
    RES(res).vol_filtered=splitapply(@(x)mean(x,1), RES(res).vol,G);
    RES(res).vol_filtered=RES(res).vol_filtered(1:end-1,:).*M3_PER_ACREFT ;
    RES(res).names=res_list{res};
end

% Save results
doy=1:365;

filename='CP_hist_cyclo_discharge';
for cp=1:length(cp_list)
    T=table(doy',CP(cp).filtered,'VariableNames',{'doy','cyclo_mean_discharge_cms_1989_2007'});
    writetable(T, filename, 'FileType','spreadsheet','Sheet',CP(cp).names);
end

filename='RES_hist_cyclo_rel_vol';
for res=1:length(res_list)
    T=table(doy',RES(res).rel_filtered, RES(res).vol_filtered,'VariableNames',{'doy','cyclo_mean_release_cms_1929_2007','cyclo_mean_volume_m3_2005_2016'});
    writetable(T, filename, 'FileType','spreadsheet','Sheet',RES(res).names);
end