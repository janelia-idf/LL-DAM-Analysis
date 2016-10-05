function grouperrorbarAllD(doprint,file1,file2,file3,file4,file5)

if nargin==6
A=[nanmean(file1');nanmean(file2');nanmean(file3');nanmean(file4');nanmean(file5')];
AE=[nansem(file1');nansem(file2');nansem(file3');nansem(file4');nansem(file5')];
[x y]=size(file1);
j=x/48;
if j<=12
    for n=1:j;
    subplot(4,3,n);errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)')
    
    end
else
     for n=1:j;
    subplot(4,4,n);errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)')
     end
end
end
if nargin==5
A=[nanmean(file1');nanmean(file2');nanmean(file3');nanmean(file4')];
AE=[nansem(file1');nansem(file2');nansem(file3');nansem(file4')];
[x y]=size(file1);
j=x/48;
if j<=12
    for n=1:j;
    subplot(4,3,n);errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)')
    
    end
else
     for n=1:j;
    subplot(4,4,n);errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)')
     end
end
end

if nargin==4
A=[nanmean(file1');nanmean(file2');nanmean(file3')];
AE=[nansem(file1');nansem(file2');nansem(file3')];
[x y]=size(file1);
j=x/48;
if j<=12
    for n=1:j;
    subplot(4,3,n);errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)')
    
    end
else
     for n=1:j;
    subplot(4,4,n);errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)')
     end
end
end
if nargin==3
A=[nanmean(file1');nanmean(file2')];
AE=[nansem(file1');nansem(file2')];
[x y]=size(file1);
j=x/48;
if j<=12
    for n=1:j;
    subplot(4,3,n);errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)')
    
    end
else
     for n=1:j;
    subplot(4,4,n);errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)')
     end
end
end

if nargin==2
A=[nanmean(file1')];
AE=[nansem(file1')];
[x y]=size(file1);
j=x/48;
if j<=12
    for n=1:j;
    subplot(4,3,n);errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)')
    
    end
else
     for n=1:j;
    subplot(4,4,n);errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)')
     end
end
end

set(gcf,'PaperOrientation','landscape');
set(gcf, 'PaperPositionMode', 'manual');
set(gcf, 'PaperPosition', [0.25 0.25 10.75 8.25]);
set (gca,'FontSize',6)
if doprint>0
   print
end