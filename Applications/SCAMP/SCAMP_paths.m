% tier2 projtechres should be mapped to drive V:.  If not, change the 
% drive letter in the parentfolder name.

parentfolder = 'V:\DAMAnalysis-Lori\SCAMP\scripts\';
cd(parentfolder);
folders = dir('*.*');

for n=1 : size(folders,1)
    if isdir(folders(n).name)
        path(path,strcat(parentfolder,folders(n).name));
    end %if
    
end % for n

scamp()
