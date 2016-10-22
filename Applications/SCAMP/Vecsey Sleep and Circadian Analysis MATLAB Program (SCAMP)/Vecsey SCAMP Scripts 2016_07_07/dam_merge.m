function o=dam_merge(o1,o2) 
%DAM_MERGE merge two sets of DAM data
%
% o=dam_merge(o1,o2);

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
o=o1;
if (o2.x(1) ~= o1.x(1)) 
  fprintf('dam_merge WARNING: Starting times dont match (%g,%g)\n',o1.start, ...
	  o2.start);
  fprintf('new start time is %g\n',o1.start);
end
cols1=size(o1.f,2);
cols2=size(o2.f,2);
rows1=size(o1.f,1);
rows2=size(o2.f,1);
rows=min(rows1,rows2);
if (rows1 ~= rows2) 
  fprintf('WARNING: different numbers of bins (%d,%d)\n',rows1,rows2);
  fprintf('truncating to %d bins.\n',rows);
end
o.f=[o1.f(1:rows,:),o2.f(1:rows,:)];
o.x=o.x(1:rows);

if ~isempty(o1.lights) 
  l1=o1.lights(1:rows);
  o.lights=l1;
  if ~isempty(o2.lights)
    l2=o2.lights(1:rows);
    if sum(abs(l1-l2)) ~= 0
      fprintf('WARNING: daylight info does not match\n');
      fprintf('First sample shall prevail.\n');
    end
  else
    fprintf('WARNING: daylight info does not match\n');
    fprintf('First sample shall prevail.\n');
  end
else
  if ~isempty(o2.lights)  
    fprintf('WARNING: daylight info does not match\n');
    fprintf('daylight info lost.\n');
  end
end


rows1=size(o1.data,1);
rows2=size(o2.data,1);
rows=min(rows1,rows2);
  
o.len=rows;
if (rows1 ~= rows2) 
  fprintf('WARNING: different number of raw bins (%d,%d)\n',rows1,rows2);
  fprintf('truncating to %d bins.\n',rows);
end
o.data=[o1.data(1:rows,:),o2.data(1:rows,:)];
if o1.int ~= o2.int
  fprintf('ERROR: DIFFERENT SAMPLING INTERVALS (%d,%d)\n',o1.int, ...
	  o2.int);
end
if ~isempty(o1.daylight)
  if ~isempty(o2.daylight)
    for i=1:cols1
      if isfield(o1.daylight{i},'t')
	o.daylight{i}.t=o1.daylight{i}.t(1:rows);
	o.daylight{i}.l=o1.daylight{i}.l(1:rows);
      end
    end
    for i=1:cols2
	 o.daylight{i+cols1}=o2.daylight{i};
	 if isfield(o2.daylight{i},'t')
	 o.daylight{i+cols1}.t=o2.daylight{i}.t(1:rows);
	 o.daylight{i+cols1}.l=o2.daylight{i}.l(1:rows);
       end
    end
  else
    o.daylight=[];
  end
else
  o.daylight=[];
end

for i=1:cols2
  o.headers{cols1+i}=o2.headers{i};
  o.names{cols1+i}=o2.names{i};
  o.boards(cols1+i)=o2.boards(i);
  o.channels(cols1+i)=o2.channels(i);
end


