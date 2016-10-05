function [Calc3Object]= sleepcalc3hr(file,n,t)

file=file.f;

Z=fly_histo_cut_180_new(file);
B=(Z>=n);

[x y]= size(B);
for j=1:y                   
    for i=1:(x/t)          
        sfreq(i,j)=sum(B((1+(i-1)*t):i*t,j));
    end
end

sfreq;


H=Z;
[x,y]=size(H);
for i=1:x
    for j=1:y
       if H(i,j)<n
       H(i,j)=NaN;
       end
    end
end

[x y]= size(H);
for j=1:y                   
    for i=1:(x/t)          
        smeandur(i,j)=nanmean(H((1+(i-1)*t):i*t,j));
    end
end

smeandur(find(isnan(smeandur)))=0;



[x y]= size(H);
for j=1:y                   
    for i=1:(x/t)          
        smax(i,j)=nanmax(H((1+(i-1)*t):i*t,j));
    end
end


smax(find(isnan(smax)))=0;



Z2=fly_acthisto_cut_180_new(file,n);
B2=Z2>0;

[x y]= size(B2);
for j=1:y                   
    for i=1:(x/t)          
        wmax(i,j)=nanmax(Z2((1+(i-1)*t):i*t,j));
    end
end

wmax(find(isnan(wmax)))=0;

WSdiff=wmax-smax;

Calc3Object={sfreq,smeandur,smax,WSdiff};