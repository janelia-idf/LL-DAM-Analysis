function [S]= fset (file,n,t)

N=fly_histo(file);
[x,y]=size(N);
for i=1:x
    for j=1:y
       if N(i,j)<n
       N(i,j)=NaN;
       end
    end
end
C=N;
C(find(isnan(C)))=0;
[x y]= size(C);

%xi = zeros(1,y);
%C(1,:)=xi;

    
[x y]= size(C);
for j=1:y                   
    for i=1:(x/t)  
        try
        [S(i,j)]=find(C((1+(i-1)*t):i*t,j),1,'first');
        catch
        S(i,j)=0;
        end
    end 
end
