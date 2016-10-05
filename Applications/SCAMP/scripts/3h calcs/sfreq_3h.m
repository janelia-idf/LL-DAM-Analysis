function [h]= sfreq_3h(start,final,file1,Genotype1,file2,Genotype2,file3,Genotype3,file4,Genotype4)

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
H1=(Z1>=5);

[x y]= size(H1);
for j=1:y                   
    for i=1:(x/180)          
        smax100(i,j)=nansum(H1((1+(i-1)*180):i*180,j));
    end
end

smax1=smax100;
smax1(find(isnan(smax1)))=0;

[x,y]=size(smax1); 

if x==8
    smax1=[smax1];
end
if x==16
    smax1=[(smax1(1:8,:)+smax1(9:16,:))/2];
end
if x==24
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:))/3];
end
if x==32
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:))/4];
end
if x==40
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:))/5];
end
if x==48
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:))/6];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:))/7];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:))/8];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:)+smax1(65:72,:))/9];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:)+smax1(65:72,:)+smax1(73:80,:))/10];
end



A=[mean(smax1(1,:))'];
AE=[sem(smax1(1,:))'];

B=[mean(smax1(2,:))'];
BE=[sem(smax1(2,:))'];

C=[mean(smax1(3,:))'];
CE=[sem(smax1(3,:))'];

D=[mean(smax1(4,:))'];
DE=[sem(smax1(4,:))'];

E=[mean(smax1(5,:))'];
EE=[sem(smax1(5,:))'];

F=[mean(smax1(6,:))'];
FE=[sem(smax1(6,:))'];

G=[mean(smax1(7,:))'];
GE=[sem(smax1(7,:))'];

H=[mean(smax1(8,:))'];
HE=[sem(smax1(8,:))'];

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
ylabel({'Frequency'; '(Episodes/3h)'},'FontSize',12,'FontWeight','bold')
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

H1=(Z1>=5);
H2=(Z2>=5);

[x y]= size(H1);
for j=1:y                   
    for i=1:(x/180)          
        smax100(i,j)=nansum(H1((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H2);
for j=1:y                   
    for i=1:(x/180)          
        smax200(i,j)=nansum(H2((1+(i-1)*180):i*180,j));
    end
end

smax1=smax100;
smax2=smax200;

smax1(find(isnan(smax1)))=0;
smax2(find(isnan(smax2)))=0;

[x,y]=size(smax1); 

if x==8
    smax1=[smax1];
    smax2=[smax2];
end
if x==16
    smax1=[(smax1(1:8,:)+smax1(9:16,:))/2];
    smax2=[(smax2(1:8,:)+smax2(9:16,:))/2];
end
if x==24
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:))/3];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:))/3];
end
if x==32
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:))/4];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:))/4];
end
if x==40
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:))/5];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:))/5];
end
if x==48
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:))/6];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:))/6];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:))/7];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:))/7];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:))/8];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:)+smax2(57:64,:))/8];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:)+smax1(65:72,:))/9];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:)+smax2(57:64,:)+smax2(65:72,:))/9];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:)+smax1(65:72,:)+smax1(73:80,:))/10];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:)+smax2(57:64,:)+smax2(65:72,:)+smax2(73:80,:))/10];
end




A=[mean(smax1(1,:))';mean(smax2(1,:))'];
AE=[sem(smax1(1,:))';sem(smax2(1,:))'];

B=[mean(smax1(2,:))';mean(smax2(2,:))'];
BE=[sem(smax1(2,:))';sem(smax2(2,:))'];

C=[mean(smax1(3,:))';mean(smax2(3,:))'];
CE=[sem(smax1(3,:))';sem(smax2(3,:))'];

D=[mean(smax1(4,:))';mean(smax2(4,:))'];
DE=[sem(smax1(4,:))';sem(smax2(4,:))'];

E=[mean(smax1(5,:))';mean(smax2(5,:))'];
EE=[sem(smax1(5,:))';sem(smax2(5,:))'];

F=[mean(smax1(6,:))';mean(smax2(6,:))'];
FE=[sem(smax1(6,:))';sem(smax2(6,:))'];

G=[mean(smax1(7,:))';mean(smax2(7,:))'];
GE=[sem(smax1(7,:))';sem(smax2(7,:))'];

H=[mean(smax1(8,:))';mean(smax2(8,:))'];
HE=[sem(smax1(8,:))';sem(smax2(8,:))'];

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
ylabel({'Frequency'; '(Episodes/3h)'},'FontSize',12,'FontWeight','Normal')
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

H1=(Z1>=5);
H2=(Z2>=5);
H3=(Z3>=5);

[x y]= size(H1);
for j=1:y                   
    for i=1:(x/180)          
        smax100(i,j)=nansum(H1((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H2);
for j=1:y                   
    for i=1:(x/180)          
        smax200(i,j)=nansum(H2((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H3);
for j=1:y                   
    for i=1:(x/180)          
        smax300(i,j)=nansum(H3((1+(i-1)*180):i*180,j));
    end
end


smax1=smax100;
smax2=smax200;
smax3=smax300;

smax1(find(isnan(smax1)))=0;
smax2(find(isnan(smax2)))=0;
smax3(find(isnan(smax3)))=0;


[x,y]=size(smax1); 

if x==8
    smax1=[smax1];
    smax2=[smax2];
    smax3=[smax3];
end
if x==16
    smax1=[(smax1(1:8,:)+smax1(9:16,:))/2];
    smax2=[(smax2(1:8,:)+smax2(9:16,:))/2];
      smax3=[(smax3(1:8,:)+smax3(9:16,:))/2];
end
if x==24
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:))/3];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:))/3];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:))/3];
end
if x==32
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:))/4];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:))/4];
      smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:))/4];
end
if x==40
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:))/5];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:))/5];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:))/5];
end
if x==48
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:))/6];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:))/6];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:)+smax3(41:48,:))/6];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:))/7];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:))/7];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:)+smax3(41:48,:)+smax3(49:56,:))/7];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:))/8];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:)+smax2(57:64,:))/8];
     smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:)+smax3(41:48,:)+smax3(49:56,:)+smax3(57:64,:))/8];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:)+smax1(65:72,:))/9];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:)+smax2(57:64,:)+smax2(65:72,:))/9];
     smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:)+smax3(41:48,:)+smax3(49:56,:)+smax3(57:64,:)+smax3(65:72,:))/9];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:)+smax1(65:72,:)+smax1(73:80,:))/10];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:)+smax2(57:64,:)+smax2(65:72,:)+smax2(73:80,:))/10];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:)+smax3(41:48,:)+smax3(49:56,:)+smax3(57:64,:)+smax3(65:72,:)+smax3(73:80,:))/10];
end





A=[mean(smax1(1,:))';mean(smax2(1,:))';mean(smax3(1,:))'];
AE=[sem(smax1(1,:))';sem(smax2(1,:))';sem(smax3(1,:))'];

B=[mean(smax1(2,:))';mean(smax2(2,:))';mean(smax3(2,:))'];
BE=[sem(smax1(2,:))';sem(smax2(2,:))';sem(smax3(2,:))'];

C=[mean(smax1(3,:))';mean(smax2(3,:))';mean(smax3(3,:))'];
CE=[sem(smax1(3,:))';sem(smax2(3,:))';sem(smax3(3,:))'];

D=[mean(smax1(4,:))';mean(smax2(4,:))';mean(smax3(4,:))'];
DE=[sem(smax1(4,:))';sem(smax2(4,:))';sem(smax3(4,:))'];

E=[mean(smax1(5,:))';mean(smax2(5,:))';mean(smax3(5,:))'];
EE=[sem(smax1(5,:))';sem(smax2(5,:))';sem(smax3(5,:))'];

F=[mean(smax1(6,:))';mean(smax2(6,:))';mean(smax3(6,:))'];
FE=[sem(smax1(6,:))';sem(smax2(6,:))';sem(smax3(6,:))'];

G=[mean(smax1(7,:))';mean(smax2(7,:))';mean(smax3(7,:))'];
GE=[sem(smax1(7,:))';sem(smax2(7,:))';sem(smax3(7,:))'];

H=[mean(smax1(8,:))';mean(smax2(8,:))';mean(smax3(8,:))'];
HE=[sem(smax1(8,:))';sem(smax2(8,:))';sem(smax3(8,:))'];

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
ylabel({'Frequency'; '(Episodes/3h)'},'FontSize',12,'FontWeight','bold')
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

H1=(Z1>=5);
H2=(Z2>=5);
H3=(Z3>=5);
H4=(Z4>=5);

[x y]= size(H1);
for j=1:y                   
    for i=1:(x/180)          
        smax100(i,j)=nansum(H1((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H2);
for j=1:y                   
    for i=1:(x/180)          
        smax200(i,j)=nansum(H2((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H3);
for j=1:y                   
    for i=1:(x/180)          
        smax300(i,j)=nansum(H3((1+(i-1)*180):i*180,j));
    end
end

[x y]= size(H4);
for j=1:y                   
    for i=1:(x/180)          
        smax400(i,j)=nansum(H4((1+(i-1)*180):i*180,j));
    end
end


smax1=smax100;
smax2=smax200;
smax3=smax300;
smax4=smax400;

smax1(find(isnan(smax1)))=0;
smax2(find(isnan(smax2)))=0;
smax3(find(isnan(smax3)))=0;
smax4(find(isnan(smax4)))=0;

[x,y]=size(smax1); 

if x==8
    smax1=[smax1];
    smax2=[smax2];
    smax3=[smax3];
    smax4=[smax4];
end
if x==16
    smax1=[(smax1(1:8,:)+smax1(9:16,:))/2];
    smax2=[(smax2(1:8,:)+smax2(9:16,:))/2];
    smax3=[(smax3(1:8,:)+smax3(9:16,:))/2];
    smax4=[(smax4(1:8,:)+smax4(9:16,:))/2];
end
if x==24
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:))/3];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:))/3];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:))/3];
    smax4=[(smax4(1:8,:)+smax4(9:16,:)+smax4(17:24,:))/3];
end
if x==32
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:))/4];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:))/4];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:))/4];
    smax4=[(smax4(1:8,:)+smax4(9:16,:)+smax4(17:24,:)+smax4(25:32,:))/4];
end
if x==40
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:))/5];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:))/5];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:))/5];
    smax4=[(smax4(1:8,:)+smax4(9:16,:)+smax4(17:24,:)+smax4(25:32,:)+smax4(33:40,:))/5];
end
if x==48
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:))/6];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:))/6];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:)+smax3(41:48,:))/6];
    smax4=[(smax4(1:8,:)+smax4(9:16,:)+smax4(17:24,:)+smax4(25:32,:)+smax4(33:40,:)+smax4(41:48,:))/6];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:))/7];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:))/7];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:)+smax3(41:48,:)+smax3(49:56,:))/7];
    smax4=[(smax4(1:8,:)+smax4(9:16,:)+smax4(17:24,:)+smax4(25:32,:)+smax4(33:40,:)+smax4(41:48,:)+smax4(49:56,:))/7];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:))/8];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:)+smax2(57:64,:))/8];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:)+smax3(41:48,:)+smax3(49:56,:)+smax3(57:64,:))/8];
    smax4=[(smax4(1:8,:)+smax4(9:16,:)+smax4(17:24,:)+smax4(25:32,:)+smax4(33:40,:)+smax4(41:48,:)+smax4(49:56,:)+smax4(57:64,:))/8];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:)+smax1(65:72,:))/9];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:)+smax2(57:64,:)+smax2(65:72,:))/9];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:)+smax3(41:48,:)+smax3(49:56,:)+smax3(57:64,:)+smax3(65:72,:))/9];
    smax4=[(smax4(1:8,:)+smax4(9:16,:)+smax4(17:24,:)+smax4(25:32,:)+smax4(33:40,:)+smax4(41:48,:)+smax4(49:56,:)+smax4(57:64,:)+smax4(65:72,:))/9];
end
if x==56
    smax1=[(smax1(1:8,:)+smax1(9:16,:)+smax1(17:24,:)+smax1(25:32,:)+smax1(33:40,:)+smax1(41:48,:)+smax1(49:56,:)+smax1(57:64,:)+smax1(65:72,:)+smax1(73:80,:))/10];
    smax2=[(smax2(1:8,:)+smax2(9:16,:)+smax2(17:24,:)+smax2(25:32,:)+smax2(33:40,:)+smax2(41:48,:)+smax2(49:56,:)+smax2(57:64,:)+smax2(65:72,:)+smax2(73:80,:))/10];
    smax3=[(smax3(1:8,:)+smax3(9:16,:)+smax3(17:24,:)+smax3(25:32,:)+smax3(33:40,:)+smax3(41:48,:)+smax3(49:56,:)+smax3(57:64,:)+smax3(65:72,:)+smax3(73:80,:))/10];
    smax4=[(smax4(1:8,:)+smax4(9:16,:)+smax4(17:24,:)+smax4(25:32,:)+smax4(33:40,:)+smax4(41:48,:)+smax4(49:56,:)+smax4(57:64,:)+smax4(65:72,:)+smax4(73:80,:))/10];
end





A=[mean(smax1(1,:))';mean(smax2(1,:))';mean(smax3(1,:))';mean(smax4(1,:))'];
AE=[sem(smax1(1,:))';sem(smax2(1,:))';sem(smax3(1,:))';sem(smax4(1,:))'];

B=[mean(smax1(2,:))';mean(smax2(2,:))';mean(smax3(2,:))';mean(smax4(2,:))'];
BE=[sem(smax1(2,:))';sem(smax2(2,:))';sem(smax3(2,:))';sem(smax4(2,:))'];

C=[mean(smax1(3,:))';mean(smax2(3,:))';mean(smax3(3,:))';mean(smax4(3,:))'];
CE=[sem(smax1(3,:))';sem(smax2(3,:))';sem(smax3(3,:))';sem(smax4(3,:))'];

D=[mean(smax1(4,:))';mean(smax2(4,:))';mean(smax3(4,:))';mean(smax4(4,:))'];
DE=[sem(smax1(4,:))';sem(smax2(4,:))';sem(smax3(4,:))';sem(smax4(4,:))'];

E=[mean(smax1(5,:))';mean(smax2(5,:))';mean(smax3(5,:))';mean(smax4(5,:))'];
EE=[sem(smax1(5,:))';sem(smax2(5,:))';sem(smax3(5,:))';sem(smax4(5,:))'];

F=[mean(smax1(6,:))';mean(smax2(6,:))';mean(smax3(6,:))';mean(smax4(6,:))'];
FE=[sem(smax1(6,:))';sem(smax2(6,:))';sem(smax3(6,:))';sem(smax4(6,:))'];

G=[mean(smax1(7,:))';mean(smax2(7,:))';mean(smax3(7,:))';mean(smax4(7,:))'];
GE=[sem(smax1(7,:))';sem(smax2(7,:))';sem(smax3(7,:))';sem(smax4(7,:))'];

H=[mean(smax1(8,:))';mean(smax2(8,:))';mean(smax3(8,:))';mean(smax4(8,:))'];
HE=[sem(smax1(8,:))';sem(smax2(8,:))';sem(smax3(8,:))';sem(smax4(8,:))'];;

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
ylabel({'Frequency'; '(Episodes/3h)'},'FontSize',12,'FontWeight','bold')
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
