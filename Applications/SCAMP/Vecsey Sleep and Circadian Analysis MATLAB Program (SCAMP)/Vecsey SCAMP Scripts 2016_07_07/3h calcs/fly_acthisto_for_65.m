function data=fly_acthisto_for_65(file,n)
    
% Reads a DAM data file
% verifies interval between measurement
% concatenates inter-activity intervals for a single fly 
% generates IAI histogram
% generates activity histogram
% 
[a,s30]=fly_sleepthresh_for_65_v2(file,n);
%Basically n= the duration of the interuptions i.e., if n=5, a wake period
%will end only if is interupted by a inactive period of 5min or more, so 
%a sequence like 1 1 1 1 1 0 0 0 0 1 1 1 1 will be change to a sequence
%like            1 1 1 1 1 1 1 1 1 1 1 1 1  and therefore the duration of the wake period will 
%be 13 min rather than 2 periods (one of 5 and another of 4) this is
%because the sleep definition is 5min.

% The code bellow keep counting zeros until they are interrupted. Because
% of the previus command, zeros are time awake.
[x y]= size(a);
data=zeros(x,y);
for j = 1:y
    i=1;ii=0;
    while i<(x+1)   
        for ii= i:x
            if a(ii,j)==0            
                data(i,j)= data(i,j)+1; 
            else

               %data(ii)=NaN;
                break;
            end
        end 

        if (data(i,j)>0)
            i=i+data(i,j);
        else
            i=i+1;
        end
        
    end        
end 




for m=1:y
 for k= 1:x
     if data(k,m)==0 
         data(k,m)= nan; 
     end
 end
end
% inter-activity interval: number of consecutive measurement intervals that recorded no
% activity 


% data.h= zeros(x*y,1);
% data.h(:)=nan;
% k=1;
% for j=1:y
%     for i=1:x
%         if data(i,j)~=nan
%             data.h(k)=data(i,j);
%             k=k+1;
%         end
%     end
% end
% 
% data.ah= zeros(x*y,1);
% data.ah(:)=nan;
% k=1;
% for j=1:y
%     for i=1:x
%         if file(i,j)~=0
%             data.ah(k)=file(i,j);
%             k=k+1;
%         end
%     end
% end

