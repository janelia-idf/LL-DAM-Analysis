% function [m,b,esq,R]=slope(x,y)
% linear regression y=mx + b
% inputs: x independent var; y=dependent
% outputs: m=slope; b=intercept; esq=standar error (squared)
%          R=correlation coefficient (squared)

%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (C)Jeffrey Hall Lab, Brandeis University.             %%
% Use and distribution of this software is free for academic      %%
% purposes only, provided this copyright notice is not removed.   %%
% Not for commercial use.                                         %%
% Unless by explicit permission from the copyright holder.        %%
% Mailing address:                                                %%
% Jeff Hall Lab, Kalman Bldg, Brandeis Univ, Waltham MA 02454 USA %%
% Email: hall@brandeis.edu                                        %%
%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [m,b,esq,R]=slope(x,y)
n=length(x);
xavg=sum(x)/n;
yavg=sum(y)/n;
xx=x - xavg;
yy=y - yavg;
sst = dot(yy,yy) ;
q=dot(xx,xx);
m=dot(xx,yy)/q;
b=yavg-m*xavg;
sse=(sst-m^2*q);
esq=sse / n ;
if sst > 0
  R=1 - sse / sst ; 
else
  R=0;
end
