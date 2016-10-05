function [a,boards,channels,start,int,len,headers,names]= ...
    dam_read(prefix,directory)
%DAM_READ  Read trykinetics activity file
%
% This function is not usually called directly, 
% use dam_load.
%
% [a,board,channel,start,int,len,headers,names]=dam_read(prefix)
% reads all dam files whose name begins with prefix
% optionally changes to directory requested for reading
% 
% the main output is a, a matrix of fly activity
% a contains all the activity data from the dam files
% including negative errors,
% one channel per column.
%
% optional outputs:
% board, channel: board and channel numbers (from filename) (one
%     per fly)
% start,int,len: start, interval and length (one for all)
% headers,names: headers (first line in data file) and filenames
% (one per channel)
%
% see also dam_load, dam_cleanup
fprintf('DAM Read',prefix,directory)
cwd=cd;
if nargin>1
  cd(directory);
end
if nargin <1
  prefix='';
end
direc = dir; filenames = {};
[filenames{1:length(direc),1}] = deal(direc.name);
[remain,boards,channels] = dam_names(filenames,prefix);

if length(remain) ==0
  fprintf('Error: No files found\n')
  return;
end

[a,start,int,len,headers,names] = dam_read_names(remain, cwd);