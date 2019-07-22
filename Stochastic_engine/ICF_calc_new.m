%ICF calculation


d=csvread('Synthetic_streamflows/synthetic_streamflows_FCRPS.csv');
d = d(244:length(d)-122,:);
years = length(d)/365;
ICFs = zeros(years,1);

for i = 1:years
    
    j = d((i-1)*365+1:(i-1)*365+365,1);
    a = d((i-1)*365+1:(i-1)*365+365,2);

    b = find(a>450000);
    if b>0
        
        ICFs(i) = min(j(b).*(j(b)>80)); 
    
    
    else
    ICFs(i) = 0;
    end
    
end
    

csvwrite('PNW_hydro/FCRPS/ICFcal.csv',ICFs);