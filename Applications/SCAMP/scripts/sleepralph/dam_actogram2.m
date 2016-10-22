function dam_actogram2(o,well,mode,cutoff)
%DAM_ACTOGRAM  Plot actograms of DAM information
% dam_actogram(o,well(s),mode,cutoff)
%
% o: dam data, as read with dam_load.
% well: list of flies (columns), mean will be computed
% mode,cutoff: see actogram

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
if nargin<3
  mode=2;
end
if nargin<2
  well=(1:size(o.data,2));
end
if nargin<4
  cutoff=[];
end

%[f,h,first]=dam_cleanup(o.data(:,well),o.start,o.int,1);
f=o.f(:,well);
if length(well)>1
  f=mean(f,2);
end
% if ~isempty(o.daylight)
%   l=o.daylight{well(1)}.l;
%   l=l(first:length(l));
% else
%   l=[];
% end
actogram2(f,o.x(1),o.int,mode,o.lights,cutoff);
