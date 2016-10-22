function [a,start,int,len,headers,names] = dam_read_names(remain, cwd)
%DAM_READ_NAMES  Read named trykinetics activity files
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
a=[];
nchannels=length(remain);
for i=1:nchannels
  f=remain{i};
  fprintf('Reading %s (%d)\n',f,i);
  [x,start1,int1,len1,header]=dam_file(f);
  if (length(a)==0)
    start=start1;
    int=int1;
    len=len1;
    headers=cell(1,nchannels);
    names=cell(1,nchannels);
    a=zeros(length(x),nchannels);
    headers{i}=header;
    names{i}=f;
    a(:,i)=x;
  else
    if (~(len1 == len & int1 == int & start1 == start)) 
      fprintf('ERROR (start,int,len) %s = (%d,%d,%d) %s=(%d,%d,%d)\n', ...
	      remain{i-1},start,int,len, ...
	      f,start1,int1,len1);
      cd(cwd);
      return;
    else
      a(:,i)=x;
      headers{i}=header;
      names{i}=f;
    end
  end
end
cd(cwd);

