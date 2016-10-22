function delpeaks=peakphaseplot_new(objects,trunc,filter_hours,delpeaks,list)
%PEAKPHASEPLOT Compare two groups' peaks and plot peaks and delays
%
% peakphaseplot(o1,o2,trunc,filter_hours,delpeaks1,delpeaks2)
% Uses a butterworth filter to smooth out two averaged activity datas
% loaded with dam_load and generates three plots: fly1, fly2
% and peaks differences. See Levine, et. al., Signal Analysis
% of behavioral and molecular cycles, BMC % Neuroscience 2002;3(1):1
% Fig. 9 http://www.biomedcentral.com/1471-2202/3/1
%
% o1: first (control) group of flies (see dam_load)
% o2: second(experiment) group of flies
% trunc: number of last valid bin (or 0 to use all)
% filter_hours: number of hours on the butterworth filter
%
% SEE ALSO: PEAKCIRCPLOT (Same test using circular statistics)
%
% NOTES:
% (1)The problem with this figure is that often there are
%    false peaks that make the comparison invalid. So you have three
%    methods to clean them up:
%    1. Use more hours on the butterworth filter
%    2. count peaks manually, starting from peak 1 on the left, and
%       decide which ones should be eliminated; insert the list of
%       peaks to be deleted as delpeaks1 (for o1) and delpeaks2 (for o2).
%    3. Manually pinpoint the wrong peaks. For this, insert 'm' instead
%       of parameter delpeaks1 (ie peakhpaseplot(o1,o2,0,8,'m')).
%       (to save the list for plot scripts, use the syntax
%       [delpeaks1,delpeaks2]=peakphaseplot(o1,o2,...,'m')).
%
% (2)For non-dam objects, use the following format:
%     peakphaseplot(a1,a2,int,filter_hours,delpeaks1,delpeaks2)
%     or
%     peakphaseplot(a1,a2,[int,start1,start2],filter_hours,delpeaks1,delpeaks2)
%     (int=sampling interval, in minutes; start1,2=hours of first observation for a1,a2)

%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (C)Jeffrey Hall Lab, Brandeis University.             %%
% Use and distribution of this software is free for academic      %%
% purposes only, provided this copyright notice is not removed.   %%
% Not for commercial use.                                         %%
% Unless by explicit permission from the copyright holder.        %%
% Mailing address:                                                %%
% Jeff Hall Lab, Kalman Bldg, Brandeis Univ, Waltham MA 02454 USA %%
% Email: hall@brandeis.edu                                        %%
% Edited 9/13/2012 by Chris Vecsey, Griffith Lab, Brandeis        %%
%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% % Requires the following other scripts:
% % build_fake_dam
% % dam_truncate - already in our toolbox
% % dam_flyplot
%     % which uses flyplot and dam_cleanup - both are already in our toolbox
% % butt_filter - already in our toolbox
% % findpeaks - already in our toolbox
% % manualpeaks (this is defined within this script)

% clf;

% if nargin<3
%   trunc=0;
% end
% if nargin<4
%   filter_hours=12; % filter hours
% end
%
% if nargin<5
%   delpeaks1=[];
% end
% if nargin<6
%   delpeaks2=[];
% end
% if ~isstruct(o1)
%   damformat=0;
%   int=trunc(1);
%   if length(trunc)>2
%     start1=trunc(2);
%     start2=trunc(3);
%   else
%     start1=0;
%     start2=0;
%   end
%   o1=build_fake_dam(o1,int,start1,'A');
%   o2=build_fake_dam(o2,int,start2,'B');
%   trunc=0;
% else
%   damformat=1;
% end
%
% if trunc>0
%   o1=dam_truncate(o1,1,trunc,'bins');
%   o2=dam_truncate(o2,1,trunc,'bins');
% end
%
% dir1=sprintf('%s:%s',o1.names{1},o1.names{length(o1.names)});
% dir2=sprintf('%s:%s',o2.names{1},o2.names{length(o2.names)});

% subplot(4,1,1);
% set(gca,'ylim',[0 150]);
% hold on
% rd1=o1.f;
% x1=o1.x;
%
% d1=mean(rd1,2);
% dam_flyplot(o1);
%
% %plot(x1,d1);
% title(sprintf('%s (n=%d)',dir1,size(o1.f,2)));
% %xlabel('time (hrs.)')
% ylabel('mean activity');
% % if (damformat)
% %     set(gca,'ylim',[0 150]);
% % end
% maxact1=max(d1);
% a1=ceil(maxact1/5);
% set(gca,'ylim',[0 a1*5])
% xlim1=get(gca,'xlim');
%
%
% subplot(4,1,2)
% if (damformat)
%     set(gca,'ylim',[0 150]);
% end
% hold on
% rd2=o2.f;
% x2=o2.x;
% d2=mean(rd2,2);
% %plot(x2,d2);
% dam_flyplot(o2);
% %xlabel('time (hrs.)');
% title(sprintf('%s (n=%d)',dir2,size(o2.f,2)));
% ylabel('mean activity');
% % if (damformat)
% %     set(gca,'ylim',[0 150]);
% % end
% maxact2=max(d2);
% a2=ceil(maxact2/5);
% set(gca,'ylim',[0 a2*5])
% xlim=get(gca,'xlim');
%
% if (xlim1(2)>xlim(2))
%   subplot(4,1,1);
%   set(gca,'xlim',xlim)
% end
% if (xlim1(2)<xlim(2))
%   xlim(2)=xlim1(2);
%   set(gca,'xlim',xlim)
% end
% %

% if filter_hours==0
%     sp1=d1;
%     sp2=d2;
% else
%     sp1=butt_filter(d1,60/o1.int*filter_hours);
%     sp2=butt_filter(d2,60/o2.int*filter_hours);
% end
% [pp1,xx1]=findpeaks(sp1);
% [pp2,xx2]=findpeaks(sp2);

% if ischar(delpeaks1) || ischar(delpeaks2)
%   % don't put a semicolon on the next line ;-)
%   [delpeaks1,delpeaks2]=manualpeaks(x1,sp1,pp1,xx1,x2,sp2,pp2,xx2);
% end
% if length(delpeaks1)>0
%   l=ones(length(pp1),1);
%   l(delpeaks1)=0;
%   l=find(l>0);
%   pp1=pp1(l);
%   xx1=xx1(l);
% end
% if length(delpeaks2)>0
%   l=ones(size(pp2));
%   l(delpeaks2)=0;
%   l=find(l>0);
%   pp2=pp2(l);
%   xx2=xx2(l);
% end

fullfig=figure;

if~isstruct(objects{1})
    error('Data file is not in DAM format!')
else
    damformat=1;
end

x1all=cell(length(objects),1);
sp1all=cell(length(objects),1);
pp1all=cell(length(objects),1);
xx1all=cell(length(objects),1);

for i=1:length(objects)
    d1=[];
    o1=[];
    rd1=[];
    x1=[];
    a1=[];
    o1=objects{i};
    if trunc>0
        o1=dam_truncate(o1,1,trunc,'bins');
    end
    
    dir1{i}=sprintf('%s:%s',o1.names{1},o1.names{length(o1.names)});
    
    subplot((length(objects)+1),1,i);
    hold on
    rd1=o1.f;
    x1=o1.x;
    
    d1=mean(rd1,2);
    dam_flyplot(o1);
    
    %plot(x1,d1);
    title(sprintf('%s (n=%d)',dir1{i},size(o1.f,2)));
    %xlabel('time (hrs.)')
    ylabel('mean activity');
    % if (damformat)
    %     set(gca,'ylim',[0 150]);
    % end
    maxact1=max(d1);
    a1=ceil(maxact1/5);
    set(gca,'ylim',[0 a1*5]);
    xlim1=get(gca,'xlim');
    
    if filter_hours==0
        sp1=d1;
    else
        sp1=butt_filter(d1,60/o1.int*filter_hours);
    end
    
    [pp1,xx1]=findpeaks(sp1);
    
    x1all{i}=x1;
    sp1all{i}=sp1;
    pp1all{i}=pp1;
    xx1all{i}=xx1;
end

subplot((length(objects)+1),1,length(objects)+1);

if ischar(delpeaks) %Checks that 'm' input was used for delpeaks input, which initiates manualpeaks peak selection method.
    delpeaks1=manualpeaks_new(x1all,sp1all,pp1all,xx1all,list);
else
    error('Unknown peak selection method! Check delpeaks input')
end

% if isempty(delpeaks1)
%     error('No peaks found!')
% else
%     for i=1:length(delpeaks1)
%         l=ones(length(pp1all{i}),1);
%         l(delpeaks1{i})=0;
%         l=find(l>0);
%         pp1all{i}=pp1all{i}(l);
%         xx1all{i}=xx1all{i}(l);
%     end
% end
% 'abcd'
% 
% hold on;
% plot(x1(xx1),pp1,'*','MarkerSize',6);
% plot(x1,sp1);
% plot(x2,sp2,'--');
% plot(x2(xx2),pp2,'o','MarkerSize',6);
% 
% %xlabel('time (hrs.)');
% ylabel(sprintf('mean activity (lowpass/%dhrs.)',filter_hours));
% legend(dir1,'',dir2,'',4)
% 
% title('peaks')
% set(gca,'xlim',xlim);
% firsthour=24*floor(min(x1(1),x2(1))/24);
% lasthour=24*ceil(max(x1(end),x2(end))/24);
% set(gca,'xtick',firsthour:24:lasthour);
% set(gca,'xgrid','on','ygrid','on');
% 
% 
% subplot(4,1,4)
% %plot(x2(xx2),(xx2-xx1)/2,'*-','MarkerSize',6);
% plot(x2(xx2),x2(xx2)-x1(xx1),'*-','MarkerSize',6);
% set(gca,'xlim',xlim);
% xlabel('time (hrs.)');
% ylabel('delay (hrs.)');
% set(gca,'xtick',firsthour:24:lasthour);
% title(sprintf('%s-%s peaks',dir2,dir1));
% figfonts('FontSize',6);
% 
% x=get(gcf,'Position');
% %et(gcf,'Position',[x(1)/1.5 x(2) x(3)-x(1)/1.5 x(4)]);
% set(gcf,'PaperPosition',[1 1 6.5 9]);
% %set(gcf,'PaperPositionMode','Manual');
% set(gca,'xgrid','on','ygrid','on');
% set(gca,'xlim',xlim);
% % print tmp
% 
% 
% %     function delpeaks1=manualpeaks(x1all,sp1all,pp1all,xx1all,list)
% %         
% %         delpeaks1=[];
% %         % [delpeaks1,delpeaks2]=manualpeaks(x1,sp1,pp1,xx1,... ...
% %         % x2,sp2,pp2,xx2);
% %         
% %         fhphase = figure;
% %         set(fhphase,'Position',[400,200,500,400],'Name','Phase Shift Analysis','NumberTitle','off');
% %         buttongroupphase = uibuttongroup(fhphase,'visible','on','Units','Normalized','Position',[0,0,1,1]);
% %         
% %         groupInstruct = uicontrol (buttongroupphase,'Style','text','String',...
% %             'Select a Pair of Groups to Analyze','Units','Normalized','Position',[5/300,280/300,140/300,10/300]);
% %         
% %         for i=1:length(list)
% %             groupname=list{i};
% %             if i<=12
% %                 group(i) = uicontrol (buttongroupphase,'Style','checkbox',...
% %                     'String',['Group = ' groupname],'Units','Normalized','position',[10/300,(260-((i-1)*15))/300,150/300,15/300]);
% %             else
% %                 
% %                 group(i) = uicontrol (buttongroupphase,'Style','checkbox',...
% %                     'String',['Group = ' groupname],'Units','Normalized','position',[160/300,(260-((i-13)*15))/300,150/300,15/300]);
% %             end
% %             set(group(i),'Value',1);
% %         end
% %         
% %         finishall=0;
% %         
% %         pbhphase = uicontrol(buttongroupphase,'Style','pushbutton',...
% %             'Units','Normalized','Position',[10/300,10/300,200/500,50/400],...
% %             'Callback',{@manualpeakspair,finishall});
% %         set(pbhphase,'String','<html><p style="text-align: center;">GRAPH<br>Peaks for<br>Selected Groups</p>');
% %         
% %         pbhend = uicontrol(buttongroupphase,'Style','pushbutton',...
% %             'Units','Normalized','Position',[160/300,10/300,200/500,50/400],...
% %             'Callback',{@pbhphaseend});
% %         set(pbhend,'String','<html><p style="text-align: center;">Done<br>Picking Peaks<br>for All Groups?</p>');
% %         
% %         function manualpeakspair(src,evt,finishall)
% %             handle_id=155;
% %             handle_id=figure ;
% %             hold on
% %             delpeaks1=[];
% %             delpeaks2=[];
% %             plot(x1,sp1);
% %             plot(x2,sp2);
% %             plot(x1(xx1),pp1,'*','markersize',9)
% %             plot(x2(xx2),pp2,'o','markersize',9)
% %             finish=0;
% %             xlim=get(gca,'xlim');
% %             ylim=get(gca,'ylim');
% %             
% %             while(finish==0 )
% %                 if (length(xx1)-length(delpeaks1)) ~= (length(xx2)-length(delpeaks2))
% %                     title('WRONG');
% %                 else
% %                     title('MAYBE RIGHT');
% %                 end
% %                 uu=[];
% %                 if ~isempty(delpeaks1)
% %                     uu=[uu,'DEL1=',sprintf('%d ',delpeaks1)];
% %                 end
% %                 if ~isempty(delpeaks2)
% %                     uu=[uu,'DEL1=',sprintf('%d ',delpeaks2)];
% %                 end
% %                 [x,y]=ginput(1);
% %                 if (x<xlim(1) | x > xlim(2) | y<ylim(1) | y>ylim(2))
% %                     finish=1;
% %                 else
% %                     di1=(x1(xx1)-x).^2+(pp1-y).^2;
% %                     n1=find(di1==min(di1));
% %                     di1=di1(n1(1));
% %                     di2=(x2(xx2)-x).^2+(pp2-y).^2;
% %                     n2=find(di2==min(di2));
% %                     di2=di2(n2(1));
% %                     if di1<di2
% %                         delpeaks1=[delpeaks1,n1];
% %                         for i=1:4:13
% %                             plot(x1(xx1(n1)),pp1(n1),'o','markersize',i);
% %                         end
% %                     else
% %                         delpeaks2=[delpeaks2,n2];
% %                         for i=1:4:13
% %                             plot(x2(xx2(n2)),pp2(n2),'o','markersize',i);
% %                         end
% %                     end
% %                 end
% %             end
% %             %delpeaks1
% %             %delpeaks2
% %             close(handle_id)
% %         end
% %         
% %         function pbhphaseend(src,evt)
% %             finishall=1;
% %         end
% %     end
