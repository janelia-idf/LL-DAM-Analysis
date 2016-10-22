% EnvMonData = Environmental Monitor Data Analysis

%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (C) Leslie Griffith Lab, Brandeis University.         %%
% Written by Christopher G. Vecsey                                %%
% Use and distribution of this software is free for academic      %%
% purposes only, provided this copyright notice is not removed.   %%
% Not for commercial use, unless by explicit permission from the  %%
% copyright holder.                                               %%
% If used for analysis that results in publication, cite the      %%
% source of this code as the following:                           %%
% Donelson, N., Kim, E. Z., Slawson, J. B., Vecsey, C. G.,        %%
% Huber, R. and Griffith, L. C. (2012) 'High-resolution           %%
% positional tracking for long-term analysis of Drosophila sleep  %%
% and locomotion using the "tracker" program', PLoS One, 7(5):    %%
% e37250. doi:10.1371/journal.pone.0037250                        %%
% Mailing address:                                                %%
% Leslie Griffith Lab, MS008,                                     %%
% Brandeis University, Waltham MA 02454 USA                       %%
% Email: griffith@brandeis.edu, cvecsey@skidmore.edu              %%
%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Creates a GUI that allows you to select Light, Temperature, and Humidity
% readings from an environmental monitor.
[filenames, pathname] = uigetfile('*', 'Choose all Environmental Monitor files from a group for graphing','MultiSelect','on');
cd(pathname);

alldata = [];
numFiles = length(filenames);
figure
set(0,'DefaultAxesColorOrder',[0,0,1;1,0.6,0;0,0.6,0;1,0,0;0,0.6,1;1,0,1;0,0,0;0.6,0,0;0.6,1,0.2;0.6,0,1;1,0.8,0.2;0.5,0.5,0.5])
% Gets the appropriate data from the selected files.
for i=1:(numFiles)
    current = importdata(filenames{i}, '\t',4);
    data=current.data;
    alldata=[alldata data];    
end
columnmin = min(alldata);
overallmin = min(columnmin');
columnmax = max(alldata);
overallmax = max(columnmax');
% Graphs the three data types all in the same plot. Legend will include
% filenames. Blue = light, orange = temperature, green = humidity.
plot(alldata)
ylim([overallmin-100,overallmax+100])
legend(filenames)