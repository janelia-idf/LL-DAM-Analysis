function pgram(x, beghrs, endhrs, conf, int,quiet)
%PGRAM  Chi Square Periodogram computation and plotting.
%
% PGRAM(X, BEGHRS, ENDHRS, CONF, INT) computes and displays the chi
% square periodogram for periodic data X in the range [BEGHRS,ENDHRS}
% hours.  Also plots critical values of chi^2(P-1) at period P using
% the CHISQ function on confidence interval CONF.  Optional INT
% (default=60) is the number of minutes per interval (bin).  The
% periodogram is computed from equation (4) in:
%
%  
% Defaults: BEGHRS=15, ENDHRS=40, CONF=0.05; enter 0 or omit the 
% parameter to obtain the default [e.g. pgram(x,0,0,0,30)]
%
% 
% @Article{SokoloveBushell,
%   author = 	 {P. G. Sokolove and W.N. Bushell},
%   title = 	 {The Chi Square Periodogram: Its Utility for
%                 Analysis of Circadian Rhythms},
%   journal = 	 {Journal of Theoretical Biology},
%   year = 	 {1978},
%   volume = 	 {72},
%   pages = 	 {131-160},
% }
%
% See also CHISQ, dam_pgram.
%

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

% hidden parameter: quiet (for dam_analyze)
% print only location of peak instead of more verbose output

% default to 60 minutes between samples
if nargin < 5, int = 60; end

% defaults
if nargin<2 | beghrs==0
  beghrs = 15;
end
if nargin<3 | endhrs==0
  endhrs=40;
end
if nargin<4 | conf==0
  conf=0.05;
end

if nargin<6
  quiet=0;
end

% convert hours to bins
begbin = beghrs * (60/int);
endbin = endhrs * (60/int);


len = length(x);

% loop over bins, computing Qp at each bins
for p = begbin:endbin
 
  % number of rows in an array of P columns
  k = fix(len/p);
  
  % total number of hourly tallies 
  n = k * p;
  
  % bin-wise tally for the ith bin
  x_i = reshape(x(1:n), p, k)';

  % mean of the Xi's in column h of the array
  xbar_h = mean(x_i);
  
  % mean over entire array
  xbar = mean(xbar_h);

  % equation (4) from Sokolove & Bushell
  ssq= sum(sum(square(x_i - xbar)));
  if (ssq > 0)
    q(p) = (k * sum(square(xbar_h - xbar))) / ...
	   (1/n * ssq);
  else
    q(p)=0;
  end

  % chi-squared
  c(p) = chisq(1-conf, p-1);
  
end

% plot on hour scale
hrs = [int/60:int/60:endhrs];
plot(hrs, q)
hold on
plot(hrs, c, 'r')
if max(q) > 0
  axis([beghrs endhrs 0 max(q)])
end
xlabel('P (hours)')
ylabel('Qp')

% test for significance
if isempty(find(q>c))
  blurb('No significant peak')
  
else
  
  % clip values below confidence
  q(find(q<=c)) = 0;

  % width in hours, with an extra bin each for pre- and post-crossing 
  width = (length(find(q))+2) * int / 60;
  
  % get peak
  maxq = max(q);
  peakloc = find(q == maxq);
  height = maxq - c(peakloc);

  % report peak
  if (quiet)
      blurb(sprintf('peak=%2.1f\nw=%2.1f h=%2.1f',...
          peakloc*int/60,width,height))
  else
      blurb(sprintf('PEAK AT %2.1f HRS; WIDTH=%2.1f\n%2.1f ABOVE CONF=%2.2f',...
          peakloc*int/60, width, height, conf))
  end
end

% element-wise square of a vector or matrix
function y = square(x)
y = x.*x;




