function grouperrorbarDOIcolor(n,file1,file2,file3,file4,file5)
%n=day of interest
if nargin==6
A=[mean(file1');mean(file2');mean(file3');mean(file4');mean(file5')];
AE=[SEM(file1');SEM(file2');SEM(file3');SEM(file4');SEM(file5')];

errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)','LineWidth',1.5);
                
end
if nargin==5
A=[mean(file1');mean(file2');mean(file3');mean(file4')];
AE=[SEM(file1');SEM(file2');SEM(file3');SEM(file4')];
errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)','LineWidth',1.5);
end
if nargin==4
A=[mean(file1');mean(file2');mean(file3')];
AE=[SEM(file1');SEM(file2');SEM(file3')];
errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)','LineWidth',1.5);
end
if nargin==3
A=[mean(file1');mean(file2')];
AE=[SEM(file1');SEM(file2')];
errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)','LineWidth',1.5);

end