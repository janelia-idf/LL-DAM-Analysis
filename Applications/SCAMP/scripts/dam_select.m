function u=dam_select(o,wells)
% o=dam_select(o,wells)
% chooses only a list of wells out of dam object o
% example
% o=dam_load('Z32M062');  % load monitor 62
% o1=dam_select(o,22:32)  % only interested in channels 22 thru 32.
%
% see also: dam_truncate

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
u.data=o.data(:,wells);
u.boards=o.boards(wells);
u.channels=o.channels(wells);
u.start=o.start;
u.int=o.int;
u.len=o.len;
u.headers=o.headers(wells);
u.names=o.names(wells);
u.daylight=o.daylight(wells);
u.f=o.f(:,wells);
u.x=o.x;
u.lights=o.lights;
u.first=o.first;
