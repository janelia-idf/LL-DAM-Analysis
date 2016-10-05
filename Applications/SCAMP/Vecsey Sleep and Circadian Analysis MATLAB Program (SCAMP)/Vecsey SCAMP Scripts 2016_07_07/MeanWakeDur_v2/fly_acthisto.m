function data=fly_acthisto(file,n)
    
% Reads through "a" from fly_sleepthresh (which looks like this:
% 0;1;1;1;1;1;0;0, where 0s are minutes of non-sleep and 1s are minutes of
% sleep. Wherever there is a 0, this code replaces the 0 with a 1, and
% continues adding onto that point for however consecutive 0 data points
% there are. So the hypothetical data above would become 1;0;0;0;0;0;2;0.

[a,s30]=fly_sleepthresh(file,n);

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

% The following code replaces all zeros in "data" with NaN.


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

