function p=dam_hist_par();
% dam_hist_par
% parameters (default values) for dam_hist & fly_hist:
% hour (24): number of hours per day
% skipDays (0): number of days to remove at the beginning
% lightsOn (600): time (military) when lights go on
% lightsOff (2400): time (military) when lights go off
% firstHour (800): hour of the first column on the histogram
% barSize (30): size (minutes) of each column
% plotSEM (1): do(1) or don't (0) plot Standard Error of the Mean
% values
global DAILY_HOURS
if isempty(DAILY_HOURS)
  DAILY_HOURS=24;
end
p.hours=DAILY_HOURS;
p.skipDays=0;
p.spanDays=Inf;
p.lightsOn=-1;
p.lightsOff=2500;
p.firstHour=[];
p.barSize=60;
p.plotSEM=1;
p.title=[];
p.method = 0; % sdl 03-JUL-02: default to vanilla X axis
p.int=60;
