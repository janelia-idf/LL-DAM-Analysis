function CalcObject= sleepcalc2EDIT(file,n,t)
%Calculates multiple sleep parameters from raw beam-cross DAM data.
%file=data file
%n=sleep definition (usually 5 minutes)
%t=time interval, i.e., bin length in minutes (720 = 12 hours)

%It is important to be aware that a wake bout that
%starts in bin 1 and continues into bin 2 will be counted in bin 1. This
%can be problematic in the case of sleep deprivation, when a wake bout may
%begin just before the sleep deprivation period, and continue through the
%entire sleep deprivation period. This massive wake bout will be counted in
%the bin before the deprivation, thus artificially boosting its mean and
%max wake bout duration.

% On 2-9-10 changed output to CalcObject from the following:
% [amean,sfreq,stdur,s30,smedian,smax,smeandur,oamean,atcounts,namean,ameandur,afreq,atdur,latency,MeanWakeningsDur,wmax,WSdiff]


% m=file.f;
% [x y]= size(m);
% for j=1:y                   
%     for i=1:(x/30)          
%         amean(i,j)=nanmean(m((1+(i-1)*30):i*30,j));
%     end
% end
% Commented code above and replaced with that below, which takes the sum
% of activity counts across 30-minute bins, instead of finding the average activity
% counts/minute across the 30-minute bin.
m=file.f;
[x y]= size(m);
for j=1:y                   
    for i=1:(x/30)          
        amean(i,j)=sum(m((1+(i-1)*30):i*30,j));
    end
end

% Z is the output of fly_histo, which has a number wherever a non-active
% bout began, and the # indicates the length in minutes of that bout. All
% other data points are NaN. In "B" below, only points in Z that are
% greater than or equal to the sleep threshold (usually 5) are transferred
% to B as 1s. Then sfreq counts the number of 1s to determine the number of
% sleep bouts in each bin.
Z=fly_histo(file);
B=(Z>=n);

[x y]= size(B);
for j=1:y                   
    for i=1:(x/t)          
        sfreq(i,j)=sum(B((1+(i-1)*t):i*t,j));
    end
end

%Z2 is the output from fly_acthisto, which has a number wherever a wake
%bout began, and the # indicates the length in minutes of that bout. All
%other data points are NaN. In "B" below, all NaN values therefore become zeros,
%and the numbers become 1s. So even if there was a 50-minute wake bout
%starting at i,j, there will now be a 1 at i,j. afreq therefore sums the
%number of ones across the chosen bin length to count the number of wake
%bouts in each bin. 
Z2=fly_acthisto(file,n);
B2=Z2>0;
[x y]= size(B2);
for j=1:y                   
    for i=1:(x/t)          
        afreq(i,j)=sum(B2((1+(i-1)*t):i*t,j));
    end
end

%Z is the output from fly_histo above. H replaces all values lower than the
%sleep threshold with NaN. Then smedian2 takes the median of all non-NaN
%values, thus getting the median length of all sleep episodes during each
%bin. smeandur2 and smax2 repeat the process for those measurements.
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
        smedian2(i,j)=nanmedian(H((1+(i-1)*t):i*t,j));
    end
end
smedian=smedian2;
% If there was a bin with no sleep bouts, the following code will replace
% that bin's NaN value with a 0.
smedian(find(isnan(smedian)))=0;

[x y]= size(H);
for j=1:y                   
    for i=1:(x/t)          
        smeandur2(i,j)=nanmean(H((1+(i-1)*t):i*t,j));
    end
end
smeandur=smeandur2;
% If there was a bin with no sleep bouts, the following code will replace
% that bin's NaN value with a 0.
smeandur(find(isnan(smeandur)))=0;

[x y]= size(Z2);
for j=1:y                   
    for i=1:(x/t)          
        ameandur2(i,j)=nanmean(Z2((1+(i-1)*t):i*t,j));
    end
end

ameandur=ameandur2;
% If there was a bin with no active bouts, the following code will replace
% that bin's NaN value with a 0.
ameandur(find(isnan(ameandur)))=0;

[x y]= size(H);
for j=1:y                   
    for i=1:(x/t)          
        smax2(i,j)=nanmax(H((1+(i-1)*t):i*t,j));
    end
end

smax=smax2;
smax(find(isnan(smax)))=0;

[x y]= size(B2);
for j=1:y                   
    for i=1:(x/t)          
        wmax(i,j)=nanmax(Z2((1+(i-1)*t):i*t,j));
    end
end

wmax(find(isnan(wmax)))=0;

WSdiff=wmax-smax;

[a,s30]=fly_sleepthresh(file,n);

[x y]= size(a);
for j=1:y                    
    for i=1:(x/t)           
        stdur(i,j)=sum(a((1+(i-1)*t):i*t,j));
    end
end

a2=a<1;
[x y]= size(a2);
for j=1:y                    
    for i=1:(x/t)           
        atdur(i,j)=sum(a2((1+(i-1)*t):i*t,j));
    end
end

% The following code turns any 0 value into NaN. Then, by taking nanmean of
% the resulting matrix, you find the average number of crosses during any
% minute in which there was at least one cross, excluding the NaNs from the
% average. This average is taken across whatever bin length is specified
% (default is to calculate over both 12 and 24 hour periods).

b=file.f;

[x,y]=size(b);
for i=1:x
    for j=1:y
       if b(i,j)==0;
       b(i,j)=NaN;
   else H(i,j)=1;
       end
    end
end

[x y]= size(b);
for j=1:y                   
    for i=1:(x/t)  
         
        namean(i,j)=nanmean(b((1+(i-1)*t):i*t,j));
    end
end

H=a;
[x,y]=size(H);
for i=1:x
    for j=1:y
        if H(i,j)==1;
            H(i,j)=NaN;
        else H(i,j)=1;
        end
    end
end

b=file.f.*H;

[x y]= size(b);
for j=1:y                   
    for i=1:(x/t)          
        oamean2(i,j)=nanmean(b((1+(i-1)*t):i*t,j));
    end
end
oamean=oamean2;
oamean(find(isnan(oamean)))=0;

b=file.f;

[x y]= size(b);
for j=1:y                   
    for i=1:(x/t)          
        atcounts(i,j)=nansum(b((1+(i-1)*t):i*t,j));
    end
end

% New Material 2-9-10 - Added fset_v2, which outputs latency,...
% added MeanWakeDur, which outputs MeanWakeningsDur
% Then added CalcObject, function of which is to lump all sleepcalc2 data
% into a single cell object

% fset_v2
% Latency tries to find the first minute of sleep in a bin, but if there is
% no sleep in that bin, it simply records the latency as the full length of the bin.
[x y]= size(a);
for j=1:y                   
    for i=1:(x/t)  
        try
        latency(i,j)=find(a((1+(i-1)*t):i*t,j),1,'first');
        catch
        latency(i,j)=t;
        end
    end 
end

% MeanWakeDur_v2
% -(latency-1)

%Following code first subtracts minutes of sleep from bin length in
%minutes. Resulting TotTimeActive is a matrix the size of stdur (r bins x c
%animals). The latency (-1) is subtracted, which essentially removes any
%period of wakefulness that leads off at the beginning of a bin. Then this
%data is divided by the number of wake bouts (afreq) in each bin. Because
%there may be 0 bouts in a bin, some values may become INF. In this
%situation, the last code replaces all NaN (I'm not sure when, if ever, a NaN 
%value will appear) and INF values with zeros.

wakeDur=atdur-(latency-1);
MeanWakeningsDur=wakeDur./afreq;

MeanWakeningsDur(find(isnan(MeanWakeningsDur)))=0;
MeanWakeningsDur(find(isinf(MeanWakeningsDur)))=0;
MeanWakeningsDur;

% CalcObject

CalcObject={amean,s30,stdur,sfreq,smax,smeandur,smedian,oamean,atcounts,...
    namean,ameandur,afreq,atdur,latency,MeanWakeningsDur,wmax,WSdiff};
