function x = chisq(p, nu)
%CHISQ    Chi-square estimation
% 
%   X = CHISQ(P, NU) returns estimated chi-square value X based on
%   confidence level P and degrees of freedom NU.  Uses binary search
%   on the P->X mapping, computed via the GCF algorithm in
%
%   @Book{NRC,
%     author = 	 {W.H. Press and B.P. Flannery and S.A. Teukolsky and
%                 W.T. Vetterling},
%     title = 	 {Numerical Recipes in C: The Art of Scientific Computing},
%     publisher =  {Cambridge U.P.},
%     year = 	 {1988},
%     address =  {Cambridge, England},
%   }

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
% bozo filters
if p < eps | p > 1-eps, error('Argument P must be in range (0,1)'), end
if nu < 1 error('Argument NU must be positive'), end

PEPS = 0.0001;
ITMAX = 100;

xlo=1; xhi=100;

for i = 1:ITMAX
  x = (xlo+xhi) / 2;
  [q,gln] = gcf(nu/2, x/2);
  pp = 1 - q;
  if (pp < p)  % estimate too low 
      xlo = x; 
  else        % estimate too high
    xhi = x;
  end
  if (abs(p-pp) < PEPS) break, end
end

% Numerical Recipes GCF function
function [gammcf, gln] = gcf(a, x)

ITMAX = 100;
EPS = 3.0e-7;

gold=0.0;fac=1.0;b1=1.0;
b0=0.0;a0=1.0;
  
gln=gammln(a);
a1=x;
for n = 1:ITMAX
  ana=n-a;
  a0=(a1+a0*ana)*fac;
  b0=(b1+b0*ana)*fac;
  anf=n*fac;
  a1=x*a0+anf*a1;
  b1=x*b0+anf*b1;
  if (a1)
    fac=1.0/a1;
    g=b1*fac;
    if (abs((g-gold)/g) < EPS) 
        gammcf=exp(-x+a*log(x)-gln)*g;
        return;
    end
    gold = g;
   end
end    
fprintf('a too large, ITMAX too small in routine GCF\n')


% Numerical Recipes GAMMLN function
function g = gammln(xx)
  
  cof = [76.18009173,-86.50532033,24.01409822, ...
         -1.231739516,0.120858003e-2,-0.536382e-5];

  x = xx-1.0;
  tmp=x+5.5;
  tmp = tmp-(x+0.5)*log(tmp);
  ser=1.0;
  for j = 1:6  
    x = x + 1.0;
    ser = ser + cof(j)/x;
  end
  g = -tmp+log(2.50662827465*ser);

% LocalWords:  chisq GCF NRC Flannery Teukolsky Vetterling
