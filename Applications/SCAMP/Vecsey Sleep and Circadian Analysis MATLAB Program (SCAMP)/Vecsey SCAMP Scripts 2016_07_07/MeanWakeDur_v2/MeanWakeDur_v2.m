function [MeanWakeningsDur]=MeanWakeDur_v2(file,n,t)


[a,s30]=fly_sleepthresh(file,n);

[x y]= size(a);
for j=1:y                    
    for i=1:(x/t)           
        stdur(i,j)=sum(a((1+(i-1)*t):i*t,j));
    end
end
stdur;
TotTimeActive=t-stdur;

[C,s30]=fly_sleepthresh(file,n);   
[x y]= size(C);
for j=1:y                   
    for i=1:(x/t)  
        try
        [S(i,j)]=find(C((1+(i-1)*t):i*t,j),1,'first');
        catch
        S(i,j)=t;
        end
    end 
end

S;
wakeningsDur=TotTimeActive-(S-1);

Z2=fly_acthisto(file,n);
B=Z2>0;

[x y]= size(B);
for j=1:y                   
    for i=1:(x/t)          
        afreq(i,j)=sum(B((1+(i-1)*t):i*t,j));
    end
end
afreq;
MeanWakeningsDur=wakeningsDur./afreq;

MeanWakeningsDur(find(isnan(MeanWakeningsDur)))=0;
MeanWakeningsDur(find(isinf(MeanWakeningsDur)))=0;
MeanWakeningsDur;