function [data1 data2]=fly_sleepthresh(file,n)
    
% Reads a raw data file, finds where there is a 0 (no beam crosses during
% that minute of data for that fly), and puts a 1 in a new matrix "data1". If the next minute is
% also 0, the first data point becomes a 2. So 1;0;0;0;0;0;5;3;0 would become
% 0;5;0;0;0;0;1.

[x y]= size(file.f);
data1=zeros(x,y);
for j = 1:y
    i=1;ii=0;
    while i<(x+1)   
        for ii= i:x
            if file.f(ii,j)==0            
                data1(i,j)= data1(i,j)+1; 
            else
% 'data' is created here, but is currently not used.
               data(ii)=0;
                break;
            end
        end 

        if (data1(i,j)>0)
            i=i+data1(i,j);
        else
            i=i+1;
        end
    end        
end 

% Finds in data1 where there are values greater or equal to the sleep threshold
% (usually set to 5 minutes). If the value at i,j = 8, e.g., i,j through i+7,j 
% will all become 1. All sub-threshold values will be changed to 0. So
% 0;5;0;0;0;0;1 will become 0;1;1;1;1;1;0.

for j=1:y 
    ii=0;
    for i=1:x
        if data1(i,j)>=n
            ii= data1(i,j);
            data1(i,j)=1; 
            ii=ii-1;                
        elseif ii>0;
            data1(i,j)=1;  
            ii=ii-1;
        else
            data1(i,j)=0;
        end
    end
end

% Sums the minutes of sleep from data1 in 30-minute blocks and puts the
% result into data2. This data parameter is called s30 elsewhere.

for j=1:y
    ii=0; 
    for i=1:(x/30)      %specifically applies to 1 min data
        data2(i,j)=sum(data1((1+(i-1)*30):i*30,j));
    end
end

% for m=1:y
%  for k= 1:x
%      if data(k,m)==0 
%          data(k,m)= nan; 
%      end
%  end
% end