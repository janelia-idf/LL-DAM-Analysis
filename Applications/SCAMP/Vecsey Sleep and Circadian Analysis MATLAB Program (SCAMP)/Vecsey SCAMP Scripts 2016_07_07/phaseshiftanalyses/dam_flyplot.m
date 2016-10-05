function dam_flyplot(o,wells)
%DAM_FLYPLOT  Plot activity of selected flies
% dam_flyplot(o,wells)
%
% o: dam data as obtained with dam_load
% wells: list of wells (default: all wells in o)
%
% Plots in one graph all activity of all flies
% Useful for a quick visualization of a lot of observations
% 
% see also: flyplot,fly_allplot

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
  wells=1:size(o.data,2);
end
if isfield(o,'f')
  f=o.f(:,wells);
  x=o.x;
  lights=o.lights;
else
  [f,x,first]=dam_cleanup(o.data(:,wells),o.start,o.int,1);
  %f=mean(o.f,2);
  if isfield(o,'daylight') & ~isempty(o.daylight) & ~isempty(o.daylight{wells(1)});
    lights=o.daylight{wells(1)}.l;
    lights=lights(first:length(lights));
  else
    lights=[];
  end
end

flyplot(f,x(1),o.int,lights);
if length(wells)>1
  title(sprintf('%s:%s',o.names{wells(1)}, ...
		o.names{wells(length(wells))}));
else
  title(o.names{wells});
end

