function mybox(s,pos)

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
if nargin<1 | isempty(s)
  cleanboxes(gca)
elseif ishandle(s)
  % called from resize handler
  stringlist=cleanboxes(s);
  for i=1:length(stringlist)
    axes(stringlist{i}.axes);
    mybox(stringlist{i}.text,stringlist{i}.pos);
  end
else
  hold on
  if nargin<2 | isempty(pos)
    pos=2;
  end
  fontsize=get(gca,'FontSize');
  %s=[' ',s,' '];
  %h=text(0,0,'M','visible','off','FontSize',fontsize);
  %e=get(h,'extent');
  %xm=e(3)*.05;
  %ym=e(4)*.05;
  %delete(h);
  xm=0;
  ym=0;
  h=text(0,0,s,'visible','off','FontSize',fontsize);
  e=get(h,'extent');
  delete(h);
  height=e(4);
  width=e(3);
  xl=get(gca,'xlim');
  yl=get(gca,'ylim');
  %xspan=xl(2)-xl(1);
  %yspan=yl(2)-yl(1);
  %xm=xspan/50;
  %ym=yspan/50;
  %height=height+2*ym;
  %width=width+2*xm;
  switch(pos)
   case 1
    boxx=xl(2)-width;
    boxy=yl(2)-height;
   case 2
    boxx=xl(1);
    boxy=yl(2)-height;
   case 3
    boxx=xl(1);
    boxy=yl(1);
   case 4
    boxx=xl(2)-width;
    boxy=yl(1);
   case 5
    boxx=xl(1)+(xl(2)-xl(1))/2-width/2;
    boxy=yl(2)-height;
  end
  h=fill(boxx+[0 0 width width],boxy+[0 height height 0],'w','linestyle','none');
  set(h,'tag','mybox');
  h=text(boxx+2*xm,boxy+height/2,s,'FontSize',fontsize);
  set(h,'tag','mybox','UserData',pos);
  set(gcf,'ResizeFcn','mybox(gcbf)');
end

function stringlist=cleanboxes(s)
stringlist={};
childs=findall(s,'tag','mybox');
for i=1:length(childs)
  if strcmp(get(childs(i),'type'),'text')==1
    stringlist{end+1}.text=get(childs(i),'String');
    stringlist{end}.axes=get(childs(i),'Parent');
    stringlist{end}.pos=get(childs(i),'UserData');
  end
  delete(childs(i))
end
