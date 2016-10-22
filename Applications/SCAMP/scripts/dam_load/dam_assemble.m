function o = dam_assemble(a,boards,channels,start,int,...
			  len,headers,names,direc,incubator, ...
			  use_daylight)
%DAM_ASSEMBLE  Assemble DAM data parts into single data structure
%
% This function is not usually called directly, use dam_load.

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

o.data=a;
o.boards=boards;
o.channels=channels;
o.start=start;
o.int=int;
o.len=len;
o.headers=headers;
o.names=names;
[o.f,o.x,o.first]=dam_cleanup(o.data,o.start,o.int,1);
if (nargin>2)
  wd=cd;
  cd(direc);
  o.daylight=dam_scan_daylight(o,incubator,use_daylight);
  cd(wd);
else
  o.daylight=dam_scan_daylight(o,incubator,use_daylight);
end
if isempty(o.daylight) | isempty(o.daylight{1}.l) | use_daylight==0
  o.lights=[];
else
  o.lights=o.daylight{1}.l;
  o.lights=o.lights(o.first:o.first-1+size(o.f,1));
end

function D=dam_scan_daylight(o,incubator,use_daylight)
last='@@@';
D={};
daylight=[];
for i=1:length(o.names);
  name=o.names{i};
  %pre=name(1:3);
  mletters=findstr('M',o.names{i});
  if isempty(mletters)
    error(['no M found on the filename, cannot determine DAYLIGHT' ...
	   ' file name']);
  end
  firstm=mletters(1);
  if (firstm==1 & length(mletters)>2)
    firstm=mletters(2);
  end
  pre=name(1:firstm-1);
  if strcmp(last,pre)==0
    daylightname=[pre,'DAYLIGHT'];
    if ischar(use_daylight)
      daylightname=use_daylight;
      use_daylight=1;
    end
    if use_daylight & exist(daylightname,'file');
      fprintf('found %s\n',daylightname);
      [y,m,d,h,lights]=dam_daylight(daylightname);
      daylight.y=y(1);
      daylight.m=m(1);
      daylight.d=d(1);
      daylight.h=h(1);
      n=length(y);
      tim=zeros(n,1);
      base=convert_to_hours(y(1),m(1),d(1),h(1));
      for j=1:n
	tim(j)=convert_to_hours(y(j),m(j),d(j),h(j))-base;
      end
      daylight.t=tim;
      if incubator>0
	incu=incubator;
      else
	incu=incubator_char(pre(1));
      end
      if incu > 0
        daylight.l=lights(:,incu);
      else
	daylight = empty_daylight;
      end
      last=pre;
    else
      if use_daylight
	fprintf('No Daylight file found (%s)\n',daylightname);
      end
      daylight = empty_daylight;
    end
  end
  D{i}=daylight;
end

function h=convert_to_hours(y,m,d,hh)
  h=24*datenum(y,m,d,floor(hh/100),mod(hh,100),0);

