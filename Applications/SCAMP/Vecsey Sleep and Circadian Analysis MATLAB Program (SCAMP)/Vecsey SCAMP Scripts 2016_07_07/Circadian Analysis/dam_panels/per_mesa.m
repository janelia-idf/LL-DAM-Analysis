function [f,tau]=per_mesa(x,int,method,order)
%PER_MESA  Performs MESA analysis 
% [f,tau]=per_mesa(x,int[,method][,order])
% 
% Perform mesa analysis using one of several methods.
%
% x: input data
% int: interval between measures (in minutes)
% 
% outputs: f (strength) and tau (periods) (i.e., plot (tau,f))
%
% Methods available: 'dusty','pburg','pcov','pmcov',
% 'pyulear','pmtm','pmusic','peig'.
% 'dusty' uses D. Dowse's MESA code (help d_mesa),
% others use one of matlab's builtin mesa functions
% (see help pburg, help pcov, etc.)
% Order: Matlab's methods have an order (see help pburg, etc.)
% if not specified, order defaults to 48, unless using 'dusty'
% method, in which case it defaults to 30 (Dusty's MFL value, see
% help d_mesa). 
%
% Default: d_mesa
%
% No detrending or filtering are done.
%
% see also: mesa_compare, d_mesa, mesaplot, mesagraph

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
if nargin<3 | ~ ischar(method)
  method='dusty';
end
if nargin<4 | isempty(order)
  if strcmp(method,'dusty')==1
    order=30;
  else
    order=48;
  end
end

if strcmp('dusty',method)
  [f,tau]=d_mesa(x,0,0,order);
  tau=tau./60*int;
else
  mino=floor(length(x)/2);
  if order>mino
    fprintf('PER_MESA: ');
    fprintf('Insufficient data at order %d, order set to %d\n',order, mino);
    order=mino;
  end
  eval(sprintf('[f,freq]=%s(x,order,2^11,1);',method));  n=length(f);
  f=f(2:n);
  freq=freq(2:n);
  tau=(int/60)./freq; 
end
