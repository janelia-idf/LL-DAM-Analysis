function o = dam_load(prefix, directory, use_daylight, incubator)
%DAM_LOAD  Input function for DAM data
%
% o=dam_load(prefix,directory,use_daylight,incubator)
% Reads and cleans-up DAM data files, and
% places all information into a single "dam object" o. 
%
% main fields of o:
%
% o.f: Cleaned up data matrix, one column per fly.
% o.x: Time vector (ie, plot(o.x,o.f(:,1))) in hours.
% o.lights: daylight vector if available
% o.int: interval between measurements.
% o.names: cell array of filenames, one per fly. 
% 
% other fields:
%
% o.boards,o.channels: vector with board and channel numbers
% (deduced from the filename).
% 
% raw data fields:
% o.data: raw activity data (uncleaned)
% o.start: raw start time (*)
% o.headers: cell array of file's first lines
% o.first: bin no. (within o.data) of first nonnegative entry.
% 
% (*) Warning: o.start is the starting timestamp of the data file. Often
% data recording begins later. Use o.x(1) to know the staring time
% of the data collection, not o.start. 
%
% Parameters
%
%   prefix: Read only files whose names begin with prefix
%
%   directory: chdir to directory for reading
%
%   use_daylight: use (1=default) or don't (0) use daylight files
%                 or specify daylight file to use name (ie. 'f100DAYLIGHT'). 
%
%   incubator: letter (F=1 E=2 Z=3 D=4 N=5) or number 
%             ... otherwise deduced from the file name firstletter
%
% examples:
% 
% o=dam_load; Most frequent form: read all files
% o=dam_load('F'); Read only files named F*.*
% o=dam_load('','.',1,3); the incubator number is three. 
%
% new! now you can specify an asterisk (*) to match 
% without a prefix, as in:
%
% o69=dam_load('*M069');

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
fprintf('DAM Load',prefix, directory, use_daylight, incubator)
switch (nargin)
 case 0
  if isunix
    pattern='*';
  else
    pattern='*.*';
  end
  onename=uigetfile('pattern','Select a file');
  ms=[findstr(onename,'C'),findstr(onename,'c')];
  ms=max(ms);
  prefix=onename(1:ms-1);
  [a,boards,channels,start,int,len,headers,names]=dam_read(prefix);
 case 1
  [a,boards,channels,start,int,len,headers,names]=dam_read(prefix);
 otherwise
  [a,boards,channels,start,int,len,headers,names]=dam_read(prefix, directory);
end

if nargin<2
  directory='.';
end

if nargin<3
  use_daylight=1;
end

if nargin<4
  incubator=0;
else
  if isa(incubator,'char')
    incubator=incubator_char(incubator)
  end
end

o = dam_assemble(a,boards,channels,start,...
          int,len,headers,names,directory, incubator,use_daylight);

     
