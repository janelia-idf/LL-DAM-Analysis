function [y,m,b,esq,R]=notrend(x,y)
%NOTREND  Remove linear trend
% y=notrend(x,y)
% deletes the linear trend from a data set y
% by running a linear regression
% and subtracting it 
% the new data has mean near zero
% optional outputs: [y,m,b,esq,R]=notrend(x,y)
% (see slope.m)
% (see also nologtrend.m)

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
if nargin<2
  y=x;
  x=1:length(x);
  if size(y,1)>1
    x=x';
  end
end
[m,b,esq,R]=slope(x,y);
line=m*x+b;
y=y-line;
