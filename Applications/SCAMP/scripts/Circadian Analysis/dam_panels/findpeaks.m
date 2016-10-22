function [peaks,peakx]=findpeaks(g)
% [p,x]=findpeaks(g)
% finds peaks on vector g
% where peak is: numbers go up, then down
% and returns values (p) and positions (x)

%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (C)Jeffrey Hall Lab, Brandeis University.             %%
% Use and distribution of this software is free for academic      %%
% purposes only, provided this copyright notice is not removed.   %%
% Not for commercial use.                                         %%
% Unless by explicit permission from the copyright holder.        %%
% Mailing address:                                                %%
% Jeff Hall Lab, Kalman Bldg, Brandeis Univ, Waltham MA 02454 USA %%
% Email: hall@brandeis.edu                                        %%
%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
n=length(g);
gp=g(1:n-1)-g(2:n); % Finds any locations where curve is increasing from one point to the next.
ud=gp>0; % Marks with a 1 wherever those points are located, and a 0 wherever values were unchanging or going down from one point to the next.
udp=ud(1:n-2)-ud(2:n-1); % Again subtracts from each point the subsequent point. This effectively indicates whenever the curve changed from increasing to either unchanging or decreasing.
peakx=1+find(udp==-1); % Finds the locations of these peaks.
peaks=g(peakx); % Actually reads out the values of each peak
