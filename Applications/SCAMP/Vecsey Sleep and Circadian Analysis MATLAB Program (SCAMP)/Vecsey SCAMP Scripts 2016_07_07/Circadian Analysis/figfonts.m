function figfonts(property,newval,oid) 
% figfonts(property,newval)
% sets property=newval in
% figure axis,title,xlabel,ylabel,zlabel
%if nargin<3
%    oid=gcf;
%end
%v=get(oid);
%if isfield(v,property)
%    set(oid,property,newval)
%end
%if isfield(v,'Children')
%    for i=1:length(v.Children)
%        figfonts(property,newval,v.Children(i))
%    end
%end

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
axes=findall(gcf,'Type','Axes');
for i=1:length(axes)
  gcx=axes(i);
  set(gcx,property,newval)
  set(get(gcx,'xlabel'),property,newval)
  set(get(gcx,'ylabel'),property,newval)
  set(get(gcx,'zlabel'),property,newval)
  set(get(gcx,'title'),property,newval)
end
