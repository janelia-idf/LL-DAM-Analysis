function DayNightbargraph3(bin,fileLPG1,fileDPG1,fileLPG2,fileDPG2,fileLPG3,fileDPG3,fileLPG4,fileDPG4,fileLPG5,fileDPG5)


if nargin==11

A=[nanmean(fileLPG1');nanmean(fileDPG1')];
AE=[nansem(fileLPG1');nansem(fileDPG1')];

B=[nanmean(fileLPG2');nanmean(fileDPG2')];
BE=[nansem(fileDPG2');nansem(fileDPG2')];

C=[nanmean(fileLPG3');nanmean(fileDPG3')];
CE=[nansem(fileLPG3');nansem(fileDPG3')];

D=[nanmean(fileLPG4');nanmean(fileDPG4')];
DE=[nansem(fileLPG4');nansem(fileDPG4')];

E=[nanmean(fileLPG5');nanmean(fileDPG5')];
EE=[nansem(fileLPG5');nansem(fileDPG5')];

 
b=[A(:,bin),B(:,bin),C(:,bin),D(:,bin),E(:,bin)];
errdata=[AE(:,bin),BE(:,bin),CE(:,bin),DE(:,bin),EE(:,bin)];

h = bar('v6',b,'grouped');
%h = bar(b,'grouped');% If you are using MATLAB 6.5 (R13)
xdata = get(h,'XData');
sizz = size(b);
%determine the number of bars and groups
NumGroups = sizz(1);
SizeGroups = sizz(2);
NumBars = SizeGroups * NumGroups;
% Use the Indices of Non Zero Y values to get both X values 
% for each bar. xb becomes a 2 by NumBars matrix of the X values.
INZY = [1 3];
xb = [];
for i = 1:SizeGroups
for j = 1:NumGroups
xb = [xb xdata{i}(INZY, j)];
end
end
%find the center X value of each bar.
for i = 1:NumBars
centerX(i) = (xb(1,i) + xb(2,i))/2;
end
% To place the error bars - use the following:
hold on;
%eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
eh = errorbar('v6',centerX,b,errdata);
set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
set(eh(1),'color','k'); % This changes the color of the errorbars
set(eh(2),'linestyle','none'); % This removes the connecting line
set (gca,'FontSize',8,'FontWeight','bold')
%set(gca,'xticklabel', [{'5-15';'16-60';'61-180';'181-300';'301-420';'421-540';'>540'}])
%xlabel('Sleep Epidode Duration (min)','FontSize',10,'FontWeight','bold')
%ylabel('Number of Sleep Episodes','FontSize',10,'FontWeight','bold')
%set(gcf,'Color',[1,1,1]) 
%legend(name1,name2)
%legend('boxoff')
%ax1 = gca;
%set(ax1,'yticklabel',[0;5;10;15;20;25;30;35],...
          % 'ylim',[0 35],'xlim',[0 5])
%ax2 = axes('Position',get(ax1,'Position'),...
          % 'XAxisLocation','top',...
           %'YAxisLocation','right',...
           %'Color','none',...
           %'XColor','k','YColor','k','FontSize',5,...
           %'yticklabel',[0;0.5;1.0;1.5;2.0;2.5;3.0;3.5],...
           %'xticklabel',[],...
          % 'ylim',[0 35],'xlim',[0 2])
       %ylabel('Gain (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)
       
end
if nargin==9

A=[nanmean(fileLPG1');nanmean(fileDPG1')];
AE=[nansem(fileLPG1');nansem(fileDPG1')];

B=[nanmean(fileLPG2');nanmean(fileDPG2')];
BE=[nansem(fileDPG2');nansem(fileDPG2')];

C=[nanmean(fileLPG3');nanmean(fileDPG3')];
CE=[nansem(fileLPG3');nansem(fileDPG3')];

D=[nanmean(fileLPG4');nanmean(fileDPG4')];
DE=[nansem(fileLPG4');nansem(fileDPG4')];

 
b=[A(:,bin),B(:,bin),C(:,bin),D(:,bin)];
errdata=[AE(:,bin),BE(:,bin),CE(:,bin),DE(:,bin)];

h = bar('v6',b,'grouped');
%h = bar(b,'grouped');% If you are using MATLAB 6.5 (R13)
xdata = get(h,'XData');
sizz = size(b);
%determine the number of bars and groups
NumGroups = sizz(1);
SizeGroups = sizz(2);
NumBars = SizeGroups * NumGroups;
% Use the Indices of Non Zero Y values to get both X values 
% for each bar. xb becomes a 2 by NumBars matrix of the X values.
INZY = [1 3];
xb = [];
for i = 1:SizeGroups
for j = 1:NumGroups
xb = [xb xdata{i}(INZY, j)];
end
end
%find the center X value of each bar.
for i = 1:NumBars
centerX(i) = (xb(1,i) + xb(2,i))/2;
end
% To place the error bars - use the following:
hold on;
%eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
eh = errorbar('v6',centerX,b,errdata);
set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
set(eh(1),'color','k'); % This changes the color of the errorbars
set(eh(2),'linestyle','none'); % This removes the connecting line
set (gca,'FontSize',8,'FontWeight','bold')
%set(gca,'xticklabel', [{'5-15';'16-60';'61-180';'181-300';'301-420';'421-540';'>540'}])
%xlabel('Sleep Epidode Duration (min)','FontSize',10,'FontWeight','bold')
%ylabel('Number of Sleep Episodes','FontSize',10,'FontWeight','bold')
%set(gcf,'Color',[1,1,1]) 
%legend(name1,name2)
%legend('boxoff')
%ax1 = gca;
%set(ax1,'yticklabel',[0;5;10;15;20;25;30;35],...
          % 'ylim',[0 35],'xlim',[0 5])
%ax2 = axes('Position',get(ax1,'Position'),...
          % 'XAxisLocation','top',...
           %'YAxisLocation','right',...
           %'Color','none',...
           %'XColor','k','YColor','k','FontSize',5,...
           %'yticklabel',[0;0.5;1.0;1.5;2.0;2.5;3.0;3.5],...
           %'xticklabel',[],...
          % 'ylim',[0 35],'xlim',[0 2])
       %ylabel('Gain (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)
       
end

if nargin==7

A=[nanmean(fileLPG1');nanmean(fileDPG1')];
AE=[nansem(fileLPG1');nansem(fileDPG1')];

B=[nanmean(fileLPG2');nanmean(fileDPG2')];
BE=[nansem(fileDPG2');nansem(fileDPG2')];

C=[nanmean(fileLPG3');nanmean(fileDPG3')];
CE=[nansem(fileLPG3');nansem(fileDPG3')];

 
b=[A(:,bin),B(:,bin),C(:,bin)];
errdata=[AE(:,bin),BE(:,bin),CE(:,bin)];

h = bar('v6',b,'grouped');
%h = bar(b,'grouped');% If you are using MATLAB 6.5 (R13)
xdata = get(h,'XData');
sizz = size(b);
%determine the number of bars and groups
NumGroups = sizz(1);
SizeGroups = sizz(2);
NumBars = SizeGroups * NumGroups;
% Use the Indices of Non Zero Y values to get both X values 
% for each bar. xb becomes a 2 by NumBars matrix of the X values.
INZY = [1 3];
xb = [];
for i = 1:SizeGroups
for j = 1:NumGroups
xb = [xb xdata{i}(INZY, j)];
end
end
%find the center X value of each bar.
for i = 1:NumBars
centerX(i) = (xb(1,i) + xb(2,i))/2;
end
% To place the error bars - use the following:
hold on;
%eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
eh = errorbar('v6',centerX,b,errdata);
set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
set(eh(1),'color','k'); % This changes the color of the errorbars
set(eh(2),'linestyle','none'); % This removes the connecting line
set (gca,'FontSize',8,'FontWeight','bold')
%set(gca,'xticklabel', [{'5-15';'16-60';'61-180';'181-300';'301-420';'421-540';'>540'}])
%xlabel('Sleep Epidode Duration (min)','FontSize',10,'FontWeight','bold')
%ylabel('Number of Sleep Episodes','FontSize',10,'FontWeight','bold')
%set(gcf,'Color',[1,1,1]) 
%legend(name1,name2)
%legend('boxoff')
%ax1 = gca;
%set(ax1,'yticklabel',[0;5;10;15;20;25;30;35],...
          % 'ylim',[0 35],'xlim',[0 5])
%ax2 = axes('Position',get(ax1,'Position'),...
          % 'XAxisLocation','top',...
           %'YAxisLocation','right',...
           %'Color','none',...
           %'XColor','k','YColor','k','FontSize',5,...
           %'yticklabel',[0;0.5;1.0;1.5;2.0;2.5;3.0;3.5],...
           %'xticklabel',[],...
          % 'ylim',[0 35],'xlim',[0 2])
       %ylabel('Gain (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)
       
end


if nargin==5



A=[nanmean(fileLPG1');nanmean(fileDPG1')];
AE=[nansem(fileLPG1');nansem(fileDPG1')];

B=[nanmean(fileLPG2');nanmean(fileDPG2')];
BE=[nansem(fileLPG2');nansem(fileDPG2')];

 
b=[A(:,bin),B(:,bin)];
errdata=[AE(:,bin),BE(:,bin)];
 

h = bar('v6',b,'grouped');
%h = bar(b,'grouped');% If you are using MATLAB 6.5 (R13)
xdata = get(h,'XData');
sizz = size(b);
%determine the number of bars and groups
NumGroups = sizz(1);
SizeGroups = sizz(2);
NumBars = SizeGroups * NumGroups;
% Use the Indices of Non Zero Y values to get both X values 
% for each bar. xb becomes a 2 by NumBars matrix of the X values.
INZY = [1 3];
xb = [];
for i = 1:SizeGroups
for j = 1:NumGroups
xb = [xb xdata{i}(INZY, j)];
end
end
%find the center X value of each bar.
for i = 1:NumBars
centerX(i) = (xb(1,i) + xb(2,i))/2;
end
% To place the error bars - use the following:
hold on;
%eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
eh = errorbar('v6',centerX,b,errdata);
set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
set(eh(1),'color','k'); % This changes the color of the errorbars
set(eh(2),'linestyle','none'); % This removes the connecting line
set (gca,'FontSize',8,'FontWeight','bold')
%set(gca,'xticklabel', [{'5-15';'16-60';'61-180';'181-300';'301-420';'421-540';'>540'}])
%xlabel('Sleep Epidode Duration (min)','FontSize',10,'FontWeight','bold')
%ylabel('Number of Sleep Episodes','FontSize',10,'FontWeight','bold')
%set(gcf,'Color',[1,1,1]) 
%legend(name1,name2)
%legend('boxoff')
%ax1 = gca;
%set(ax1,'yticklabel',[0;5;10;15;20;25;30;35],...
          % 'ylim',[0 35],'xlim',[0 5])
%ax2 = axes('Position',get(ax1,'Position'),...
          % 'XAxisLocation','top',...
           %'YAxisLocation','right',...
           %'Color','none',...
           %'XColor','k','YColor','k','FontSize',5,...
           %'yticklabel',[0;0.5;1.0;1.5;2.0;2.5;3.0;3.5],...
           %'xticklabel',[],...
          % 'ylim',[0 35],'xlim',[0 2])
       %ylabel('Gain (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)
       
end

if nargin==4
A=[nanmean(fileDPG1');0];
AE=[nansem(fileDPG1');0];

B=[nanmean(fileDPG2');0];
BE=[nansem(fileDPG2');0];

C=[nanmean(fileLPG1');0];
CE=[nansem(fileLPG1');0];
 
b=[A(:,bin),B(:,bin),C(:,bin)];
errdata=[AE(:,bin),BE(:,bin),CE(:,bin)];
h = bar('v6',b,'grouped');
%h = bar(b,'grouped');% If you are using MATLAB 6.5 (R13)
xdata = get(h,'XData');
sizz = size(b);
%determine the number of bars and groups
NumGroups = sizz(1);
SizeGroups = sizz(2);
NumBars = SizeGroups * NumGroups;
% Use the Indices of Non Zero Y values to get both X values 
% for each bar. xb becomes a 2 by NumBars matrix of the X values.
INZY = [1 3];
xb = [];
for i = 1:SizeGroups
for j = 1:NumGroups
xb = [xb xdata{i}(INZY, j)];
end
end
%find the center X value of each bar.
for i = 1:NumBars
centerX(i) = (xb(1,i) + xb(2,i))/2;
end
% To place the error bars - use the following:
hold on;
%eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
eh = errorbar('v6',centerX,b,errdata);
set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
set(eh(1),'color','k'); % This changes the color of the errorbars
set(eh(2),'linestyle','none'); % This removes the connecting line
set (gca,'FontSize',8,'FontWeight','bold')
%set(gca,'xticklabel', [{'5-15';'16-60';'61-180';'181-300';'301-420';'421-540';'>540'}])
%xlabel('Sleep Epidode Duration (min)','FontSize',10,'FontWeight','bold')
%ylabel('Number of Sleep Episodes','FontSize',10,'FontWeight','bold')
%set(gcf,'Color',[1,1,1]) 
%legend('a','b')
%legend('boxoff')
%ax1 = gca;

set(gca,'xlim',[0.5 1.5],'xtick',[0.78,1,1.23],'xticklabel',['a';'b'])


%set(ax1,'yticklabel',[0;5;10;15;20;25;30;35],...
          % 'ylim',[0 35],'xlim',[0 5])
%ax2 = axes('Position',get(ax1,'Position'),...
          % 'XAxisLocation','top',...
           %'YAxisLocation','right',...
           %'Color','none',...
           %'XColor','k','YColor','k','FontSize',5,...
           %'yticklabel',[0;0.5;1.0;1.5;2.0;2.5;3.0;3.5],...
           %'xticklabel',[],...
          % 'ylim',[0 35],'xlim',[0 2])
       %ylabel('Gain (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)
       
end


if nargin==3
A=[nanmean(fileDPG1');0];
AE=[nansem(fileDPG1');0];

B=[nanmean(fileDPG2');0];
BE=[nansem(fileDPG2');0];

 
b=[A(:,bin),B(:,bin)];
errdata=[AE(:,bin),BE(:,bin)];
h = bar('v6',b,'grouped');
%h = bar(b,'grouped');% If you are using MATLAB 6.5 (R13)
xdata = get(h,'XData');
sizz = size(b);
%determine the number of bars and groups
NumGroups = sizz(1);
SizeGroups = sizz(2);
NumBars = SizeGroups * NumGroups;
% Use the Indices of Non Zero Y values to get both X values 
% for each bar. xb becomes a 2 by NumBars matrix of the X values.
INZY = [1 3];
xb = [];
for i = 1:SizeGroups
for j = 1:NumGroups
xb = [xb xdata{i}(INZY, j)];
end
end
%find the center X value of each bar.
for i = 1:NumBars
centerX(i) = (xb(1,i) + xb(2,i))/2;
end
% To place the error bars - use the following:
hold on;
%eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
eh = errorbar('v6',centerX,b,errdata);
set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
set(eh(1),'color','k'); % This changes the color of the errorbars
set(eh(2),'linestyle','none'); % This removes the connecting line
set (gca,'FontSize',8,'FontWeight','bold')
%set(gca,'xticklabel', [{'5-15';'16-60';'61-180';'181-300';'301-420';'421-540';'>540'}])
%xlabel('Sleep Epidode Duration (min)','FontSize',10,'FontWeight','bold')
%ylabel('Number of Sleep Episodes','FontSize',10,'FontWeight','bold')
%set(gcf,'Color',[1,1,1]) 
%legend('a','b')
%legend('boxoff')
%ax1 = gca;

set(gca,'xlim',[0.5 1.5],'xtick',[0.85,1.15],'xticklabel',['a';'b'])


%set(ax1,'yticklabel',[0;5;10;15;20;25;30;35],...
          % 'ylim',[0 35],'xlim',[0 5])
%ax2 = axes('Position',get(ax1,'Position'),...
          % 'XAxisLocation','top',...
           %'YAxisLocation','right',...
           %'Color','none',...
           %'XColor','k','YColor','k','FontSize',5,...
           %'yticklabel',[0;0.5;1.0;1.5;2.0;2.5;3.0;3.5],...
           %'xticklabel',[],...
          % 'ylim',[0 35],'xlim',[0 2])
       %ylabel('Gain (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)
       
end