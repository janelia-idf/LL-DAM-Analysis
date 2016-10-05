function [h]= smeandur_3h(start,final,file1,Genotype1,file2,Genotype2,file3,Genotype3,file4,Genotype4)

if nargin==4
A1=file1.f(start:final,:);
Z1=fly_histo_cutted_180(A1);

H1=Z1;
[x,y]=size(H1);
for i=1:x
    for j=1:y
       if H1(i,j)<5
       H1(i,j)=NaN;
       end
    end
end

[x y]= size(H1);
for j=1:y                   
    for i=1:(x/180)          
        smeandur100(i,j)=nanmean(H1((1+(i-1)*180):i*180,j));
    end
end

smeandur1=smeandur100;
smeandur1(find(isnan(smeandur1)))=0;

[x,y]=size(smeandur1); 

if x==8
    smeandur1=[smeandur1];
end
if x==16
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:))/2];
end
if x==24
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:))/3];
end
if x==32
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:))/4];
end
if x==40
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:))/5];
end
if x==48
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:))/6];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:))/7];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:))/8];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:)+smeandur1(65:72,:))/9];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:)+smeandur1(65:72,:)+smeandur1(73:80,:))/10];
end



A=[mean(smeandur1(1,:))'];
AE=[sem(smeandur1(1,:))'];

B=[mean(smeandur1(2,:))'];
BE=[sem(smeandur1(2,:))'];

C=[mean(smeandur1(3,:))'];
CE=[sem(smeandur1(3,:))'];

D=[mean(smeandur1(4,:))'];
DE=[sem(smeandur1(4,:))'];

E=[mean(smeandur1(5,:))'];
EE=[sem(smeandur1(5,:))'];

F=[mean(smeandur1(6,:))'];
FE=[sem(smeandur1(6,:))'];

G=[mean(smeandur1(7,:))'];
GE=[sem(smeandur1(7,:))'];

H=[mean(smeandur1(8,:))'];
HE=[sem(smeandur1(8,:))'];

b=[A,B,C,D,E,F,G,H];
errdata=[AE,BE,CE,DE,EE,FE,GE,HE];

h = bar('v6',b,'grouped');
%h = bar(b,'grouped'); %If you are using MATLAB 6.5 (R13)
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
set (gca,'FontSize',8)
set(gca,'xticklabel', [{Genotype1}])
%xlabel(xname,'FontSize',12,'FontWeight','bold')
ylabel({'Mean Duration (min)'},'FontSize',12,'FontWeight','bold')
%line(1:length (h),[0])
f = legend('ZT0-3','ZT3-6','ZT6-9','ZT9-12','ZT12-15','ZT15-18','ZT18-21','ZT21-24',-1);
legend('boxoff')
title(ParName,'FontSize',12,'FontWeight','bold')
%line('XData',[0;3],'YData',[0;0],'LineWidth',0.5) %This is one of the determinants of the x-axis 


%ax1 = gca;
%set(ax1,'yticklabel',[-800;-400;0;100;200],...
           %'ylim',[-200 200],'xlim',[0 3])
%ax2 = axes('Position',get(ax1,'Position'),...
          % 'XAxisLocation','top',...
          % 'YAxisLocation','right',...
           %'Color','none',...
          % 'XColor','k','YColor','k','FontSize',5,...
          % 'ylim',[-200 200],'xlim',[0 1.5],...   %This is one of the determinants of the x-axis 
          % 'xticklabel',[],...
          % 'yticklabel',[{ '';'' ;'' ; '';'0';'25';'50';'75';'100';'125';'150'}]);
       %ylabel('Gain (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)


end


if nargin==6
    
A1=file1.f(start:final,:);
A2=file2.f(start:final,:);

Z1=fly_histo_cutted_180(A1);
Z2=fly_histo_cutted_180(A2);



H1=Z1;
[x,y]=size(H1);
for i=1:x
    for j=1:y
       if H1(i,j)<5
       H1(i,j)=NaN;
       end
    end
end

H2=Z2;
[x,y]=size(H2);
for i=1:x
    for j=1:y
       if H2(i,j)<5
       H2(i,j)=NaN;
       end
    end
end

[x y]= size(H1);
for j=1:y                   
    for i=1:(x/180)          
        smeandur100(i,j)=nanmean(H1((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H2);
for j=1:y                   
    for i=1:(x/180)          
        smeandur200(i,j)=nanmean(H2((1+(i-1)*180):i*180,j));
    end
end

smeandur1=smeandur100;
smeandur2=smeandur200;

smeandur1(find(isnan(smeandur1)))=0;
smeandur2(find(isnan(smeandur2)))=0;

[x,y]=size(smeandur1); 

if x==8
    smeandur1=[smeandur1];
    smeandur2=[smeandur2];
end
if x==16
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:))/2];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:))/2];
end
if x==24
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:))/3];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:))/3];
end
if x==32
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:))/4];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:))/4];
end
if x==40
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:))/5];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:))/5];
end
if x==48
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:))/6];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:))/6];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:))/7];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:))/7];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:))/8];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:)+smeandur2(57:64,:))/8];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:)+smeandur1(65:72,:))/9];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:)+smeandur2(57:64,:)+smeandur2(65:72,:))/9];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:)+smeandur1(65:72,:)+smeandur1(73:80,:))/10];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:)+smeandur2(57:64,:)+smeandur2(65:72,:)+smeandur2(73:80,:))/10];
end




A=[mean(smeandur1(1,:))';mean(smeandur2(1,:))'];
AE=[sem(smeandur1(1,:))';sem(smeandur2(1,:))'];

B=[mean(smeandur1(2,:))';mean(smeandur2(2,:))'];
BE=[sem(smeandur1(2,:))';sem(smeandur2(2,:))'];

C=[mean(smeandur1(3,:))';mean(smeandur2(3,:))'];
CE=[sem(smeandur1(3,:))';sem(smeandur2(3,:))'];

D=[mean(smeandur1(4,:))';mean(smeandur2(4,:))'];
DE=[sem(smeandur1(4,:))';sem(smeandur2(4,:))'];

E=[mean(smeandur1(5,:))';mean(smeandur2(5,:))'];
EE=[sem(smeandur1(5,:))';sem(smeandur2(5,:))'];

F=[mean(smeandur1(6,:))';mean(smeandur2(6,:))'];
FE=[sem(smeandur1(6,:))';sem(smeandur2(6,:))'];

G=[mean(smeandur1(7,:))';mean(smeandur2(7,:))'];
GE=[sem(smeandur1(7,:))';sem(smeandur2(7,:))'];

H=[mean(smeandur1(8,:))';mean(smeandur2(8,:))'];
HE=[sem(smeandur1(8,:))';sem(smeandur2(8,:))'];

b=[A,B,C,D,E,F,G,H];
errdata=[AE,BE,CE,DE,EE,FE,GE,HE];

h = bar('v6',b,'grouped');
%h = bar(b,'grouped'); %If you are using MATLAB 6.5 (R13)
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
f = legend('ZT0-3','ZT3-6','ZT6-9','ZT9-12','ZT12-15','ZT15-18','ZT18-21','ZT21-24',-1);
legend('boxoff')
set(f, 'Fontsize',8)
% To place the error bars - use the following:
hold on;
%eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
eh = errorbar('v6',centerX,b,errdata);
set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
set(eh(1),'color','k'); % This changes the color of the errorbars
set(eh(2),'linestyle','none'); % This removes the connecting line
set (gca,'FontSize',8)
set(gca,'xticklabel', [{Genotype1;Genotype2}])
%xlabel(xname,'FontSize',12,'FontWeight','bold')
ylabel({'Mean Duration (min)'},'FontSize',12,'FontWeight','Normal')
%line(1:length (h),[0])

%title('Jose','FontSize',12,'FontWeight','bold')
%line('XData',[0;3],'YData',[0;0],'LineWidth',0.5) %This is one of the determinants of the x-axis 


%ax1 = gca;
%set(ax1,'yticklabel',[-800;-400;0;100;200],...
           %'ylim',[-200 200],'xlim',[0 3])
%ax2 = axes('Position',get(ax1,'Position'),...
          % 'XAxisLocation','top',...
          % 'YAxisLocation','right',...
           %'Color','none',...
          % 'XColor','k','YColor','k','FontSize',5,...
          % 'ylim',[-200 200],'xlim',[0 1.5],...   %This is one of the determinants of the x-axis 
          % 'xticklabel',[],...
          % 'yticklabel',[{ '';'' ;'' ; '';'0';'25';'50';'75';'100';'125';'150'}]);
       %ylabel('Gain (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)


end

if nargin==8
    
A1=file1.f(start:final,:);
A2=file2.f(start:final,:);
A3=file3.f(start:final,:);

Z1=fly_histo_cutted_180(A1);
Z2=fly_histo_cutted_180(A2);
Z3=fly_histo_cutted_180(A3);



H1=Z1;
[x,y]=size(H1);
for i=1:x
    for j=1:y
       if H1(i,j)<5
       H1(i,j)=NaN;
       end
    end
end

H2=Z2;
[x,y]=size(H2);
for i=1:x
    for j=1:y
       if H2(i,j)<5
       H2(i,j)=NaN;
       end
    end
end

H3=Z3;
[x,y]=size(H3);
for i=1:x
    for j=1:y
       if H3(i,j)<5
       H3(i,j)=NaN;
       end
    end
end

[x y]= size(H1);
for j=1:y                   
    for i=1:(x/180)          
        smeandur100(i,j)=nanmean(H1((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H2);
for j=1:y                   
    for i=1:(x/180)          
        smeandur200(i,j)=nanmean(H2((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H3);
for j=1:y                   
    for i=1:(x/180)          
        smeandur300(i,j)=nanmean(H3((1+(i-1)*180):i*180,j));
    end
end


smeandur1=smeandur100;
smeandur2=smeandur200;
smeandur3=smeandur300;

smeandur1(find(isnan(smeandur1)))=0;
smeandur2(find(isnan(smeandur2)))=0;
smeandur3(find(isnan(smeandur3)))=0;


[x,y]=size(smeandur1); 

if x==8
    smeandur1=[smeandur1];
    smeandur2=[smeandur2];
    smeandur3=[smeandur3];
end
if x==16
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:))/2];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:))/2];
      smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:))/2];
end
if x==24
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:))/3];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:))/3];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:))/3];
end
if x==32
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:))/4];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:))/4];
      smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:))/4];
end
if x==40
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:))/5];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:))/5];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:))/5];
end
if x==48
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:))/6];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:))/6];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:)+smeandur3(41:48,:))/6];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:))/7];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:))/7];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:)+smeandur3(41:48,:)+smeandur3(49:56,:))/7];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:))/8];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:)+smeandur2(57:64,:))/8];
     smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:)+smeandur3(41:48,:)+smeandur3(49:56,:)+smeandur3(57:64,:))/8];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:)+smeandur1(65:72,:))/9];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:)+smeandur2(57:64,:)+smeandur2(65:72,:))/9];
     smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:)+smeandur3(41:48,:)+smeandur3(49:56,:)+smeandur3(57:64,:)+smeandur3(65:72,:))/9];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:)+smeandur1(65:72,:)+smeandur1(73:80,:))/10];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:)+smeandur2(57:64,:)+smeandur2(65:72,:)+smeandur2(73:80,:))/10];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:)+smeandur3(41:48,:)+smeandur3(49:56,:)+smeandur3(57:64,:)+smeandur3(65:72,:)+smeandur3(73:80,:))/10];
end





A=[mean(smeandur1(1,:))';mean(smeandur2(1,:))';mean(smeandur3(1,:))'];
AE=[sem(smeandur1(1,:))';sem(smeandur2(1,:))';sem(smeandur3(1,:))'];

B=[mean(smeandur1(2,:))';mean(smeandur2(2,:))';mean(smeandur3(2,:))'];
BE=[sem(smeandur1(2,:))';sem(smeandur2(2,:))';sem(smeandur3(2,:))'];

C=[mean(smeandur1(3,:))';mean(smeandur2(3,:))';mean(smeandur3(3,:))'];
CE=[sem(smeandur1(3,:))';sem(smeandur2(3,:))';sem(smeandur3(3,:))'];

D=[mean(smeandur1(4,:))';mean(smeandur2(4,:))';mean(smeandur3(4,:))'];
DE=[sem(smeandur1(4,:))';sem(smeandur2(4,:))';sem(smeandur3(4,:))'];

E=[mean(smeandur1(5,:))';mean(smeandur2(5,:))';mean(smeandur3(5,:))'];
EE=[sem(smeandur1(5,:))';sem(smeandur2(5,:))';sem(smeandur3(5,:))'];

F=[mean(smeandur1(6,:))';mean(smeandur2(6,:))';mean(smeandur3(6,:))'];
FE=[sem(smeandur1(6,:))';sem(smeandur2(6,:))';sem(smeandur3(6,:))'];

G=[mean(smeandur1(7,:))';mean(smeandur2(7,:))';mean(smeandur3(7,:))'];
GE=[sem(smeandur1(7,:))';sem(smeandur2(7,:))';sem(smeandur3(7,:))'];

H=[mean(smeandur1(8,:))';mean(smeandur2(8,:))';mean(smeandur3(8,:))'];
HE=[sem(smeandur1(8,:))';sem(smeandur2(8,:))';sem(smeandur3(8,:))'];

b=[A,B,C,D,E,F,G,H];
errdata=[AE,BE,CE,DE,EE,FE,GE,HE];

h = bar('v6',b,'grouped');
%h = bar(b,'grouped'); %If you are using MATLAB 6.5 (R13)
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
f = legend('ZT0-3','ZT3-6','ZT6-9','ZT9-12','ZT12-15','ZT15-18','ZT18-21','ZT21-24',-1);
legend('boxoff')
set(f, 'Fontsize',8)
end
% To place the error bars - use the following:
hold on;
%eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
eh = errorbar('v6',centerX,b,errdata);
set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
set(eh(1),'color','k'); % This changes the color of the errorbars
set(eh(2),'linestyle','none'); % This removes the connecting line
set (gca,'FontSize',8)
set(gca,'xticklabel', [{Genotype1;Genotype2;Genotype3}])%xlabel(xname,'FontSize',12,'FontWeight','bold')
ylabel({'Mean Duration (min)'},'FontSize',12,'FontWeight','bold')
%line(1:length (h),[0])
%title(ParName,'FontSize',12,'FontWeight','bold')
%line('XData',[0;3],'YData',[0;0],'LineWidth',0.5) %This is one of the determinants of the x-axis 


%ax1 = gca;
%set(ax1,'yticklabel',[-800;-400;0;100;200],...
           %'ylim',[-200 200],'xlim',[0 3])
%ax2 = axes('Position',get(ax1,'Position'),...
          % 'XAxisLocation','top',...
          % 'YAxisLocation','right',...
           %'Color','none',...
          % 'XColor','k','YColor','k','FontSize',5,...
          % 'ylim',[-200 200],'xlim',[0 1.5],...   %This is one of the determinants of the x-axis 
          % 'xticklabel',[],...
          % 'yticklabel',[{ '';'' ;'' ; '';'0';'25';'50';'75';'100';'125';'150'}]);
       %ylabel('Gain (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)


end

if nargin==10
    
A1=file1.f(start:final,:);
A2=file2.f(start:final,:);
A3=file3.f(start:final,:);
A4=file4.f(start:final,:);

Z1=fly_histo_cutted_180(A1);
Z2=fly_histo_cutted_180(A2);
Z3=fly_histo_cutted_180(A3);
Z4=fly_histo_cutted_180(A4);



H1=Z1;
[x,y]=size(H1);
for i=1:x
    for j=1:y
       if H1(i,j)<5
       H1(i,j)=NaN;
       end
    end
end

H2=Z2;
[x,y]=size(H2);
for i=1:x
    for j=1:y
       if H2(i,j)<5
       H2(i,j)=NaN;
       end
    end
end

H3=Z3;
[x,y]=size(H3);
for i=1:x
    for j=1:y
       if H3(i,j)<5
       H3(i,j)=NaN;
       end
    end
end

H4=Z4;
[x,y]=size(H4);
for i=1:x
    for j=1:y
       if H4(i,j)<5
       H4(i,j)=NaN;
       end
    end
end

[x y]= size(H1);
for j=1:y                   
    for i=1:(x/180)          
        smeandur100(i,j)=nanmean(H1((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H2);
for j=1:y                   
    for i=1:(x/180)          
        smeandur200(i,j)=nanmean(H2((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H3);
for j=1:y                   
    for i=1:(x/180)          
        smeandur300(i,j)=nanmean(H3((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H4);
for j=1:y                   
    for i=1:(x/180)          
        smeandur400(i,j)=nanmean(H4((1+(i-1)*180):i*180,j));
    end
end


smeandur1=smeandur100;
smeandur2=smeandur200;
smeandur3=smeandur300;
smeandur4=smeandur400;

smeandur1(find(isnan(smeandur1)))=0;
smeandur2(find(isnan(smeandur2)))=0;
smeandur3(find(isnan(smeandur3)))=0;
smeandur4(find(isnan(smeandur4)))=0;

[x,y]=size(smeandur1); 

if x==8
    smeandur1=[smeandur1];
    smeandur2=[smeandur2];
    smeandur3=[smeandur3];
    smeandur4=[smeandur4];
end
if x==16
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:))/2];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:))/2];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:))/2];
    smeandur4=[(smeandur4(1:8,:)+smeandur4(9:16,:))/2];
end
if x==24
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:))/3];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:))/3];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:))/3];
    smeandur4=[(smeandur4(1:8,:)+smeandur4(9:16,:)+smeandur4(17:24,:))/3];
end
if x==32
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:))/4];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:))/4];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:))/4];
    smeandur4=[(smeandur4(1:8,:)+smeandur4(9:16,:)+smeandur4(17:24,:)+smeandur4(25:32,:))/4];
end
if x==40
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:))/5];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:))/5];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:))/5];
    smeandur4=[(smeandur4(1:8,:)+smeandur4(9:16,:)+smeandur4(17:24,:)+smeandur4(25:32,:)+smeandur4(33:40,:))/5];
end
if x==48
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:))/6];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:))/6];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:)+smeandur3(41:48,:))/6];
    smeandur4=[(smeandur4(1:8,:)+smeandur4(9:16,:)+smeandur4(17:24,:)+smeandur4(25:32,:)+smeandur4(33:40,:)+smeandur4(41:48,:))/6];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:))/7];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:))/7];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:)+smeandur3(41:48,:)+smeandur3(49:56,:))/7];
    smeandur4=[(smeandur4(1:8,:)+smeandur4(9:16,:)+smeandur4(17:24,:)+smeandur4(25:32,:)+smeandur4(33:40,:)+smeandur4(41:48,:)+smeandur4(49:56,:))/7];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:))/8];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:)+smeandur2(57:64,:))/8];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:)+smeandur3(41:48,:)+smeandur3(49:56,:)+smeandur3(57:64,:))/8];
    smeandur4=[(smeandur4(1:8,:)+smeandur4(9:16,:)+smeandur4(17:24,:)+smeandur4(25:32,:)+smeandur4(33:40,:)+smeandur4(41:48,:)+smeandur4(49:56,:)+smeandur4(57:64,:))/8];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:)+smeandur1(65:72,:))/9];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:)+smeandur2(57:64,:)+smeandur2(65:72,:))/9];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:)+smeandur3(41:48,:)+smeandur3(49:56,:)+smeandur3(57:64,:)+smeandur3(65:72,:))/9];
    smeandur4=[(smeandur4(1:8,:)+smeandur4(9:16,:)+smeandur4(17:24,:)+smeandur4(25:32,:)+smeandur4(33:40,:)+smeandur4(41:48,:)+smeandur4(49:56,:)+smeandur4(57:64,:)+smeandur4(65:72,:))/9];
end
if x==56
    smeandur1=[(smeandur1(1:8,:)+smeandur1(9:16,:)+smeandur1(17:24,:)+smeandur1(25:32,:)+smeandur1(33:40,:)+smeandur1(41:48,:)+smeandur1(49:56,:)+smeandur1(57:64,:)+smeandur1(65:72,:)+smeandur1(73:80,:))/10];
    smeandur2=[(smeandur2(1:8,:)+smeandur2(9:16,:)+smeandur2(17:24,:)+smeandur2(25:32,:)+smeandur2(33:40,:)+smeandur2(41:48,:)+smeandur2(49:56,:)+smeandur2(57:64,:)+smeandur2(65:72,:)+smeandur2(73:80,:))/10];
    smeandur3=[(smeandur3(1:8,:)+smeandur3(9:16,:)+smeandur3(17:24,:)+smeandur3(25:32,:)+smeandur3(33:40,:)+smeandur3(41:48,:)+smeandur3(49:56,:)+smeandur3(57:64,:)+smeandur3(65:72,:)+smeandur3(73:80,:))/10];
    smeandur4=[(smeandur4(1:8,:)+smeandur4(9:16,:)+smeandur4(17:24,:)+smeandur4(25:32,:)+smeandur4(33:40,:)+smeandur4(41:48,:)+smeandur4(49:56,:)+smeandur4(57:64,:)+smeandur4(65:72,:)+smeandur4(73:80,:))/10];
end





A=[mean(smeandur1(1,:))';mean(smeandur2(1,:))';mean(smeandur3(1,:))';mean(smeandur4(1,:))'];
AE=[sem(smeandur1(1,:))';sem(smeandur2(1,:))';sem(smeandur3(1,:))';sem(smeandur4(1,:))'];

B=[mean(smeandur1(2,:))';mean(smeandur2(2,:))';mean(smeandur3(2,:))';mean(smeandur4(2,:))'];
BE=[sem(smeandur1(2,:))';sem(smeandur2(2,:))';sem(smeandur3(2,:))';sem(smeandur4(2,:))'];

C=[mean(smeandur1(3,:))';mean(smeandur2(3,:))';mean(smeandur3(3,:))';mean(smeandur4(3,:))'];
CE=[sem(smeandur1(3,:))';sem(smeandur2(3,:))';sem(smeandur3(3,:))';sem(smeandur4(3,:))'];

D=[mean(smeandur1(4,:))';mean(smeandur2(4,:))';mean(smeandur3(4,:))';mean(smeandur4(4,:))'];
DE=[sem(smeandur1(4,:))';sem(smeandur2(4,:))';sem(smeandur3(4,:))';sem(smeandur4(4,:))'];

E=[mean(smeandur1(5,:))';mean(smeandur2(5,:))';mean(smeandur3(5,:))';mean(smeandur4(5,:))'];
EE=[sem(smeandur1(5,:))';sem(smeandur2(5,:))';sem(smeandur3(5,:))';sem(smeandur4(5,:))'];

F=[mean(smeandur1(6,:))';mean(smeandur2(6,:))';mean(smeandur3(6,:))';mean(smeandur4(6,:))'];
FE=[sem(smeandur1(6,:))';sem(smeandur2(6,:))';sem(smeandur3(6,:))';sem(smeandur4(6,:))'];

G=[mean(smeandur1(7,:))';mean(smeandur2(7,:))';mean(smeandur3(7,:))';mean(smeandur4(7,:))'];
GE=[sem(smeandur1(7,:))';sem(smeandur2(7,:))';sem(smeandur3(7,:))';sem(smeandur4(7,:))'];

H=[mean(smeandur1(8,:))';mean(smeandur2(8,:))';mean(smeandur3(8,:))';mean(smeandur4(8,:))'];
HE=[sem(smeandur1(8,:))';sem(smeandur2(8,:))';sem(smeandur3(8,:))';sem(smeandur4(8,:))'];;

b=[A,B,C,D,E,F,G,H];
errdata=[AE,BE,CE,DE,EE,FE,GE,HE];

h = bar('v6',b,'grouped');
%h = bar(b,'grouped'); %If you are using MATLAB 6.5 (R13)
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
f = legend('ZT0-3','ZT3-6','ZT6-9','ZT9-12','ZT12-15','ZT15-18','ZT18-21','ZT21-24',-1);
legend('boxoff')
set(f, 'Fontsize',8)
end
% To place the error bars - use the following:
hold on;
%eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
eh = errorbar('v6',centerX,b,errdata);
set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
set(eh(1),'color','k'); % This changes the color of the errorbars
set(eh(2),'linestyle','none'); % This removes the connecting line
set (gca,'FontSize',8)
set(gca,'xticklabel', [{Genotype1;Genotype2;Genotype3;Genotype4}])%xlabel(xname,'FontSize',12,'FontWeight','bold')
ylabel({'Mean Duration (min)'},'FontSize',12,'FontWeight','bold')
%line(1:length (h),[0])
%title(ParName,'FontSize',12,'FontWeight','bold')
%line('XData',[0;3],'YData',[0;0],'LineWidth',0.5) %This is one of the determinants of the x-axis 


%ax1 = gca;
%set(ax1,'yticklabel',[-800;-400;0;100;200],...
           %'ylim',[-200 200],'xlim',[0 3])
%ax2 = axes('Position',get(ax1,'Position'),...
          % 'XAxisLocation','top',...
          % 'YAxisLocation','right',...
           %'Color','none',...
          % 'XColor','k','YColor','k','FontSize',5,...
          % 'ylim',[-200 200],'xlim',[0 1.5],...   %This is one of the determinants of the x-axis 
          % 'xticklabel',[],...
          % 'yticklabel',[{ '';'' ;'' ; '';'0';'25';'50';'75';'100';'125';'150'}]);
       %ylabel('Gain (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)


end
