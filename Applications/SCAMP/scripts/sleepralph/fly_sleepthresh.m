function [data1 data2]=fly_sleepthresh(file,n)
    
% Reads a DAM data file
% verifies interval between measurement
% concatenates inter-activity intervals for a single fly 
% generates IAI histogram
% generates activity histogram
% 
[x y]= size(file.f);
data1=zeros(x,y);
for j = 1:y
    i=1;ii=0;
    while i<(x+1)   
        for ii= i:x
            if file.f(ii,j)==0            
                data1(i,j)= data1(i,j)+1; 
            else

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