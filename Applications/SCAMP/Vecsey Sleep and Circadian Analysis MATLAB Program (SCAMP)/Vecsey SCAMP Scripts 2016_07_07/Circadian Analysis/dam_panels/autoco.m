function [ac,x,ci]=autoco(a,bptu,detren)
%AUTOCO Compute autocorrelation
% [ac,x,ci]=autoco(a,bptu,detren)
%
% input:
% a: (column) vector(s) of data
% bptu: bins per time unit (i.e. bptu=2 for 30 min sampling
% interval). Default=1.
% detren: 0=no detrend; 1=linear (default); 2=loglog; 3=butterworth 
% 72 hour highpass detrending
%
% outputs:
% ac is autocorrelation matrix
% x are the x axis
% ci is confidence interval
%
% SEE ALSO: d_autoco, acplot,autocoplot.

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
dusty_code=0;

if nargin < 2
  bptu=1;
end

if nargin< 3
  detren=1;
end

ci=zeros(1,size(a,2));
n=size(a,1);
sqn=1.965/sqrt(size(a,1));
for i=1:size(a,2)
  switch (detren)
   case 0
    f=a(:,i);
   case 1
    f=notrend(a(:,i));
   case 2
    f=nologtrend(a(:,i));
   case 3
    f=butt_filter(a(:,i),0,72*bptu);
  end
  if (dusty_code)
    [r1,r2,sqn]=d_autoco(f,floor(n/2),bptu,0);
  else
    [r2,x]=xcorr(f,[ceil(72*bptu)],'coeff');
    if (size(r2,1)>1)
      r2=r2';
    end
  end
    ac(:,i)= r2';
    ci(i)=sqn;
end
if (dusty_code)
  if mod(n,2)==0
    x=-floor(1+n-(n/2)):floor(n-((n+1)/2));
  else
    x=-floor(n-(n/2)):floor(n-((n+1)/2));
  end
end
x=x' ./ bptu;
%n
%size(ac)
%size(x)
