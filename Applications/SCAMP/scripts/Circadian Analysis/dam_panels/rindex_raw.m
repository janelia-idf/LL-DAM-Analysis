function [ri,rs,px]=rindex_raw(ac,x,in,peakrange)
%RINDEX_RAW Compute rhytmicity index using autocorrelation data.
% [rindex,rstrength,peakx]=rindex_raw(ac,x,in,peakrange)
% function used by rindex & acplot. 
% see: help rindex

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
[peakf,peakx]=findpeaks(ac);
peaktau=x(peakx);
goodpeaks=find((peaktau>=peakrange(1)) &( peaktau<=peakrange(2)));
if isempty(goodpeaks)
  ri=[];
  rs=[];
  px=[];
else
  thapeak=goodpeaks(find(peakf(goodpeaks)==max(peakf(goodpeaks))));
  px=peaktau(thapeak);
  py=peakf(thapeak);
  rindex=py/in;
  peakx=px;
  ri=py;
  rs=rindex;
end
