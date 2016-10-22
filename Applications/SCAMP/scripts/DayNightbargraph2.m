function DayNightbargraph2(bin,file24G1,fileDPG1,fileLPG1,file24G2,fileDPG2,fileLPG2,file24G3,fileDPG3,fileLPG3,file24G4,fileDPG4,fileLPG4,file24G5,fileDPG5,fileLPG5)
if nargin==7
A=[nanmean(file24G1');nanmean(fileDPG1');nanmean(fileLPG1')];
AE=[nansem(file24G1');nansem(fileDPG1');nansem(fileLPG1')];

B=[nanmean(file24G2');nanmean(fileDPG2');nanmean(fileLPG2')];
BE=[nansem(file24G2');nansem(fileDPG2');nansem(fileLPG2')];

 
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

if nargin==10
A=[nanmean(file24G1');nanmean(fileDPG1');nanmean(fileLPG1')];
AE=[nansem(file24G1');nansem(fileDPG1');nansem(fileLPG1')];

B=[nanmean(file24G2');nanmean(fileDPG2');nanmean(fileLPG2')];
BE=[nansem(file24G2');nansem(fileDPG2');nansem(fileLPG2')];

C=[nanmean(file24G3');nanmean(fileDPG3');nanmean(fileLPG3')];
CE=[nansem(file24G3');nansem(fileDPG3');nansem(fileLPG3')];

 
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
if nargin==13
A=[nanmean(file24G1');nanmean(fileDPG1');nanmean(fileLPG1')];
AE=[nansem(file24G1');nansem(fileDPG1');nansem(fileLPG1')];

B=[nanmean(file24G2');nanmean(fileDPG2');nanmean(fileLPG2')];
BE=[nansem(file24G2');nansem(fileDPG2');nansem(fileLPG2')];

C=[nanmean(file24G3');nanmean(fileDPG3');nanmean(fileLPG3')];
CE=[nansem(file24G3');nansem(fileDPG3');nansem(fileLPG3')];

D=[nanmean(file24G4');nanmean(fileDPG4');nanmean(fileLPG4')];
DE=[nansem(file24G4');nansem(fileDPG4');nansem(fileLPG4')];


 
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

if nargin==16
A=[nanmean(file24G1');nanmean(fileDPG1');nanmean(fileLPG1')];
AE=[nansem(file24G1');nansem(fileDPG1');nansem(fileLPG1')];

B=[nanmean(file24G2');nanmean(fileDPG2');nanmean(fileLPG2')];
BE=[nansem(file24G2');nansem(fileDPG2');nansem(fileLPG2')];

C=[nanmean(file24G3');nanmean(fileDPG3');nanmean(fileLPG3')];
CE=[nansem(file24G3');nansem(fileDPG3');nansem(fileLPG3')];

D=[nanmean(file24G4');nanmean(fileDPG4');nanmean(fileLPG4')];
DE=[nansem(file24G4');nansem(fileDPG4');nansem(fileLPG4')];

E=[nanmean(file24G5');nanmean(fileDPG5');nanmean(fileLPG5')];
EE=[nansem(file24G5');nansem(fileDPG5');nansem(fileLPG5')];


 
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