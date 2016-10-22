function [S]= fset_v2 (file,n,t)



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
