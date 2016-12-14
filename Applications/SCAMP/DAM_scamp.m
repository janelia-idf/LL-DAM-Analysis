% tier2 projtechres should be mapped to drive V:.  If not, change the 
% drive letter in the parentfolder name.

parentfolder = 'c:\Users\laughreyl\Documents\GitHub\LL-DAM-Analysis\Applications\SCAMP\scripts\';
cd(parentfolder);
folders = dir('*.*');

for n=1 : size(folders,1)
    if isdir(folders(n).name)
        path(path,strcat(parentfolder,folders(n).name));
    end %if
    
end % for n

DAM_scamp()
