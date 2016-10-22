function [x,start,int,len,header]=dam_file(name)
% [x,start,int,len,header]=read_luc(name)
% x=data; start=(military) start time; int=interval (min)
% len=how many; header=original mac filename and date
% reads luc file
% Lines 1-header, 2-len, 3-interval, 4-start, 5-len+4 data
% sample:
% Desktop Folder:N65:N65M92C8   19 Oct 1999
% 766
% 30
% 2330
%  -501
%  -501

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
[fid,err]=fopen(name,'r');
if (fid < 0) 
  fprintf(1,'%s: File not open (%s)\n',name,err)
  return;
end
header=fgets(fid);
rest=fscanf(fid,'%d');
fclose(fid);
if length(rest) < 4
  fprintf(1,'%s: Only %d data lines, aborting\n',name, ...
	  length(rest));
  return;
end
len=rest(1);
int=rest(2);
start=rest(3);
x=rest(4:length(rest));
if len ~= length(x)
  fprintf(1,'%s: WARNING!, %d lines, expected %d\n',name,length(x), ...
	  len);
end

  
