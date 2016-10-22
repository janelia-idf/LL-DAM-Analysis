function period=mesaplot(x,int,peaklim,method,order,noplot)
%MESAPLOT  Run MESA analysis and graph it
% [rhythm=]mesaplot(x,int[,peaklim][,method][,order][,noplot])
%
% Peforms a mesa analysis of data x (previously detrended)
% and plots the results.
% Returns rhythm (see help mesagraph).
% 
% example: 
%     a=luc_read('.');
%     mesaplot(a(:,1),60);
%
% peaklim: if defined, this vector contains
% a range, min&max, to look for a peak 
%
% method,order: see help per_mesa
%
% noplot: Do not do any graphics, just return peak period
%
% example:  
%     mesaplot(a(:,1),60,[20 28])
% 
% see also: mesagraph, per_mesa, autocoplot.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
  int=60;
end
if nargin<3
  peaklim=[15 33];
end
if nargin<4
  method=[];
end
if nargin<5
  order=[];
end
if nargin<6
  noplot=0;
end

x=notrend(x);
[f,tau]=per_mesa(x,int,method,order);

% with the following, we were using Dusty's code
%dusty=0;
%if (dusty)
%  [f,tau]=d_mesa(x,1,0);
%  tau=tau/60*int;
%else
%  % this is an equivalent call with matlab code
%  % (use order 2^9 to reproduce Dusty's behavior, maybe)
%  [f,freq]=pyulear(notrend(x),48,2^12,1);
%  n=length(f);
%  f=f(2:n);
%  freq=freq(2:n);
%  tau=(int/60)./freq;
%end

period=mesagraph(f,tau,peaklim,noplot);