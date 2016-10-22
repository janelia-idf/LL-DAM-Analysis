function [f,tau]=d_mesa(x,detr,lopas,mfl)
%D_MESA  Dusty's Mesa function
%[f,tau]=d_mesa(x,detr,lopas)
% 
%    d_mesa, Dusty's mesa adapted by pf'00 from joelmes.for
%    x: data ... a COLUMN vector , or many
%    detr: do (1) or not(0) a linear detrending first (default=1)
%    lopass: do (1) or not(0) a lopas filter first (default=1)
%    mfl: minimum filter length (default = 30)
%
%     subroutine to generate maximum entropy prediction
%    outputs: f(power) and tau (period). E.g., plot(tau,f).
%
% see: per_mesa.

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
  detr=1;
end
if nargin<3
  lopas=1;
end
nsamps=length(x);
%% functions lopass and detren are defined below
if (detr)
  x=detren(x);
end
if lopas
  x=lopass(x);
end
ncoef = floor(nsamps/2);
%
%
mfpe=0.0;
%mfl =  30; 
b=x;
p=dot(x,x);

p=p/nsamps;
fpe=(nsamps+1)/(nsamps-1)*p;
ftemp = fpe;
fpe=0.0;
%ao=zeros(size(x));
%a=ao;
a=zeros(size(x));
a(1)=-1;
%ao(1)=-1;
%no=floor(nsamps/2);

for m=1:(ncoef-1)
  i=1:(nsamps-m);
  xx=x(i)-a(m)*b(i);
  b(i)=b(i+1)-a(m)*x(i+1);
  x(i)=xx;
 
  nom=dot(x(i),b(i));
  denom=dot(x(i),x(i))+dot(b(i),b(i));

%  if denom ==0
%    a(m+1)=0;
%  else
if denom ~= 0
  a(m+1)=2*nom/denom;
else
  a(m+1)=0;
end
%  end
  p=p*(1-a(m+1)*a(m+1));
  if (~(m == 1 | m >= ncoef))
    fpe=(nsamps+m)/(nsamps-m)*p;
    if ftemp==0
      fpe=fpe*0;
    else
      fpe=fpe/ftemp;  
      fpe=log10(fpe);
    end
  end
%    fprintf(debug,'%d %14.7f\n',m,fpe);
  if (~(m==1))
    i=2:m;
    a(i)=a(i)-a(m+1)*a(m+2-i);
    %a(i)=ao(i);
  end
  %ao(m+1)=a(m+1);
  if (m==mfl) |  ~( (fpe >= mfpe) | (m <= mfl)) 
    lfilt=m+1;
    mfpe=fpe;
    po = p;
    j=1:lfilt;
    best=a(j);
  end
end

ncoef=lfilt;
%fprintf('NCOEF=%d\n',ncoef);
a(1) = -1;

i=1:ncoef;
best(i)=-best(i);
%fprintf(debug,'%f\n',best);

fmin=2.0/(nsamps);
fmax=0.5;
%fclose(debug);
[f,tau]=mesa(fmin,fmax,nsamps,ncoef,po,best);


function z=detren(y)
n=length(y);
x=(1:n)';
[m,b]=slope(x,y);
z=y-m*x-b;

function y=lopass(x)
a=[ 3.414213, 4.768372e-7, 0.5857863];
b=[1 2 1 ];
z=[(a(1)-b(1))*x(1)/a(1), ...
   ((a(1)-b(1))*x(2)+(a(2)-b(2))*x(1))/ a(1)];
y=filter(b,a,x,z);

function [f,tau]=mesa(fmin,fmax,nsamps,ncoef,po,best)
%
%     subroutine to compute samples of a mesa spectrum from a
%     prediction error filter
%
%     fmin,fmax   the range of frequencies to compute
%     (cycles per sample)
%     f  a real array at least nsamps long to contain
%     the sampled frequency values.
%     nsamps       the number of frequency values to compute
%     a  a real array of prediciton error filter coefficients
%     ncoef        the number of coefficients in the prediction error
%     filter.  the first coefficient is always one in a prediction
%     error filter.
%     p  the output power of the prediction error filter.

pi2=6.2831830717959;
f=zeros(1,nsamps*8);
tau=zeros(1,nsamps*8);
i=(1:nsamps*8)';
freq=fmin+(i-1).*(fmax-fmin)/(nsamps*8-1);
tau=1./freq;
j=1:ncoef; 

omega=-pi2*freq*j;

ream=cos(omega)*best(j);
imag=sin(omega)*best(j);
f=po./(ream.^2+imag.^2)./10;
