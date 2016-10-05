function [new,a,b]=dam_names(list,prefix)
%DAM_NAMES  find filenames with trikinetics data
%
% This function is not usually called directly.
% use dam_load instead.
%
% [n,board,channel]=dam_names(list,prefix)
% list is a list of filenames
% prefix is an optional prefix
% returns, out of the list of names, only those that
% look like dam files... sorted in the proper way
% optional outputs: channel and board numbers. 
fprintf('DAM names    fix the prefix\n')
list
prefix
if nargin >= 2
  if ~isempty(prefix) & prefix(1)=='*'
    matches=[];
    pattern=prefix(2:end);
    for i=1:length(list)
      if ~isempty(findstr(list{i},pattern))
	matches=[matches,i];
      end
    end
    list=list(matches);
  else
    list=list(strmatch(prefix,list));
  end
end
newnames={};
indices=[];
count=0;
n=length(list);
if (n<=0)
  error(sprintf('Dam_names: No files were found (prefix="%s")\n',prefix));
end
for i=1:n;
  f=list{i};
  if (~isempty(findstr(f,'.')))         %<*>
     movefile(f,f(1:findstr(f,'.')-1));    
      f=f(1:findstr(f,'.')-1);           %<*>
  end                                   %<*>
  
  
  if (isempty(findstr(f,'.')))
    % no dot
    Cpos=findstr(f,'C');
    Cpos=[Cpos,findstr(f,'c')];
    if ( ~ isempty(Cpos) )
      lastC=Cpos(length(Cpos));
      Mpos=findstr(f,'M');
      Mpos=[Mpos,findstr(f,'m')];
      Mpos=Mpos(find(Mpos<lastC));
      if (~ isempty(Mpos))
	lastM=Mpos(length(Mpos));
	a1=str2num(f(lastM+1:lastC-1));
	a2=str2num(f(lastC+1:length(f)));
	if (a1 > 0 & a2 > 0)
	  count=count+1;
	  indices=[indices;count,a1,a2];
	  new{count}=f;
	end
      end
    end
  end
end
indices=sortrows(indices,[2 3]);
new=new(indices(:,1))';
a=indices(:,2);
b=indices(:,3);

	
