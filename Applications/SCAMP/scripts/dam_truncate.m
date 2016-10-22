function o1=dam_truncate(o,first,last,what)
%DAM_TRUNCATE  Chop off days or bins from dam data
% o1=dam_truncate(o,first,last,what)
% 
% o: dam data as obtained from dam_load
% first: first day (or bin) you want included (0=day 1).
% last: last day (or bin) you want included (0=last day).
% what: 'days' or 'bins' or 'hours' (default: 'days').
% 
% example: 
% o1=dam_truncate(o,3,7,'days')
% extracts days 3 through 7 from o. 
%
% NOTE: use 'hours' to truncate wrt real time instead of 
%       bins/days from the beginning of the recorded data
%       eg. dam_truncate(o,16,0,'hours') deletes all entries
%       taken before 4pm
% SDL 19 JUL 2002 : Set o1.len to new value

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
  what='days';
end
if nargin<2
  first=0;
end
if nargin<3
  last=0;
end
if first==0 | isempty(first)
  first=1;
end
if last==0 | isempty(last)
  last=99999;
end
o1=o;
if strcmp(what,'days')
  firstbin=1+(first-1)*24*60/o.int;
  lastbin=(last)*24*60/o.int;
elseif strcmp(what,'hours')
  firstbin=min(find(o.x>=first));
  lastbin=max(find(o.x<=last));
else
  firstbin=first;
  lastbin=last;
end
lastbin=min(size(o1.f,1),lastbin);
if firstbin>lastbin
  o1.data=[];
  o1.daylight=[];
  o1.l=[];
  o1.x=[];
  o1.f=[];
  fprintf('ERROR: Not that many data days!');
else
  rawfirst=firstbin+o.first-1;
  rawlast=lastbin+o.first-1;
  o1.data=o1.data(rawfirst:rawlast,:);
  o1.first=1;
  %o1.start=o.start+(rawfirst-1)*o.int; modified by pf 5/6/03
  o1.start=o1.x(firstbin);
  o1.f=o1.f(firstbin:lastbin,:);
  if ~isempty(o1.lights)
    o1.lights=o1.lights(firstbin:lastbin);
  end
  o1.x=o1.x(firstbin:lastbin);
  for i=1:length(o.daylight)
    u=o1.daylight{i}.l;
    if ~isempty(u)
      o1.daylight{i}.l=u(rawfirst:rawlast);
      o1.daylight{i}.t=o1.daylight{i}.t(rawfirst:rawlast);
    end
  end
  o1.len = lastbin - firstbin + 1;
end
