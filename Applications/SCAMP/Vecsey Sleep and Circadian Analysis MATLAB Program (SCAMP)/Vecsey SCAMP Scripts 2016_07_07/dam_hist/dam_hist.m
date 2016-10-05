%DAM_HIST Histogram of dam fly activity
% [avg,sem]=dam_hist(o,wells,p)
%
% SDL 23-JUN-02 : abstracted core functionality to HIST.M 
%
function [avg,sem]=dam_hist(o,wells,p)

if nargin < 2 | isempty(wells)
  wells=1:size(o.data,2);
end
if nargin<3
  p=dam_hist_par;
end

if isempty(p.title)
  if length(wells)>1
    titl=sprintf('%s-%s',o.names{wells(1)}, o.names{wells(length(wells))});
  else
%    titl=o.names{wells(1)};
  end
else
  titl=p.title;
end

x = o.x;
f = o.f(:,wells);

first_hour = 1;
if ~isempty(o.daylight) & ~isempty(o.daylight{wells(1)})
  lights=o.lights;
  if ~isempty(lights)
    lights=lights(first_hour:length(x)-(1-first_hour));
  end
else
  lights=[];
end

[avg,sem] = my_hist(x, f, lights, p.method, ...
	         p.hours, p.skipDays, p.spanDays, p.lightsOn, ...
		 p.lightsOff, p.firstHour, p.barSize, p.plotSEM);

title(sprintf('%s (n=%d days=%.1f)',titl,length(wells),length(f)/48));

function [avg,sem]=my_hist(x, f, lights, method, ...
			hours, skipDays, spanDays, lightsOn, ...
			lightsOff, firstHour, minPerBar, plotSEM)

% HIST Histogram of fly activity.  
%
% Input Arguments:
%
%   x         hour values
%   f         activity by hour
%   lights    daylight on/off flags
%   method    plotting method: 0 = first hour to last (default)
%                              1 = center dark
%                              2 = center light
%                              3 = lights off to lights on
%                              4 = lights on to lights off
%   hours     baseline hours
%   skipDays 
%   spanDays
%   lightsOn
%   lightsOff
%   firstHour
%   minPerBar
%   plotSEM
%
%
% Output Arguments:
% 
%   AVG mean activities by hour
%   SEM std dev of activities by hour
%
% abstracted from Pablo's DAM_HIST.M by Simon Levy, 24-JUN-02

hours_per_bin = minPerBar / 60;
bins_per_hour = 60 / minPerBar;


lightsoff_color = .5;
lightson_color = 1;

nbins = round(hours * bins_per_hour);

% post-hoc warning about display
warning = '';

%m002 this is a hack, fixes a bug brutely
if x(1) <= 0
  x = x+hours;
end

f = mean(f,2);
xfirst = min(find(x>(skipDays*hours)));
xlast = xfirst-1+nbins*floor((length(x)-xfirst+1)/nbins);

if (spanDays>0) & (spanDays<Inf)
  xlast = min(xlast,xfirst+48*spanDays-1);
end

f = f(xfirst:xlast);
x = x(xfirst:xlast);

if ~isempty(lights)
  lights = lights(xfirst:xlast);
end

n = length(f);
if isempty(firstHour)
  firstHour=x(1);
end
binno = floor(bins_per_hour*mod(x-firstHour,hours))+1;
binhour = (0:hours_per_bin:hours-hours_per_bin)+firstHour;
binhour = mod(binhour,1)*60+100*floor(mod(binhour,hours));

if lightsOff>lightsOn
  binlight = (binhour > lightsOn) & (binhour <= lightsOff);
else
  binlight=~((binhour > lightsOff) & (binhour <= lightsOn));
end

binhour = floor(binhour./100)+mod(binhour,100)./60;
s = full(sparse(binno,1,f));
c = full(sparse(binno,1,ones(size(f,1),1)));
avg = s ./ c;
sumsq = full(sparse(binno,1,f.^2));
se = sqrt(((sumsq ./ c) - (avg.^2)));
sem = se ./ sqrt(c);

% default to normal order
bins = 1:length(s);

% process daylight vector
if ~isempty(lights)
  ls = full(sparse(binno,1,lights));
  lc = full(sparse(binno,1,ones(size(lights,1),1)));
  lmean = ls ./ lc;
  binlight = lmean;
  on  =  find(lights);
  off = find(lights == 0);
  txt = sprintf('Mean on=%.1f off=%.1f all=%.1f', ...
		mean(f(on)), mean(f(off)), mean(f));
  
  % get contiguous dark or light bins
  if method
    if method == 1 | method == 4
      bit = 1;
    else
      bit = 0;
    end
    maxbins = length(binlight);
    where = find(binlight == bit);
    diff = where(2:end) - where(1:end-1);
    split = find(diff > 1);
    if ~isempty(split)
      if length(split) > 1
        warning = 'More than one dark/light cycle; using normal format';
	method = 0;
      end
      where = [where(split+1:end);where(1:split)];
    end
  end

  if ~isempty(find(binlight ~= fix(binlight)))
    %warning = 'Grayscale light bins; using normal format';
    method = 0;
  end
  
  switch method
  
   case 1	% center light

    bins = center(where, binlight);
    
   case 2	% center dark

    bins = center(where, binlight);
    
   case 3	% lights off to lights on
    
    bins = left(where, binlight);
  
   case 4	% lights on to lights off
  
    bins = left(where, binlight);
  
  end

else
  txt = sprintf('Mean=%f', mean(f));
%  txt = sprintf('Sum=%f', sum(f));

end

cla;hold on;

% plot histogram boxes
for i=1:length(bins)
  j = bins(i);
  a = [i-1 i i i-1];
  b = [ 0 0 avg(j) avg(j)];
  grayscale = .65+0.3*(0.5*((binlight(j)>0) + (binlight(j)>0.99)));
  grayscale = (1-binlight(j)) * lightsoff_color + (binlight(j))*lightson_color;
  fill(a,b,[1 1 1]*grayscale);
end

% plot standard error mean
if (plotSEM)
  hold on
  plot((1:length(s))-0.5, avg(bins)+sem(bins),'.');
end

% axis labels etc.
%set(gca, 'xticklabel', fix(bin2hrs(bins(1:2:end))+.5));
xtick=[0:1:length(bins)];
%binhour
ticklabel=cell(1,length(xtick)); % empty tick labels
% find bins for 0,6,12,18 hrs and label those ticks
for i=0:6:18
  %bin=1+max(find(binhour<=i));
  offset=mod(binhour-i,hours);
  ofzero=find(offset==min(offset));
  bin=ofzero+1;
  if (bin>length(xtick)) 
    bin=1;
  end
  if ~isempty(bin)
    ticklabel{bin}=num2str(i);
    %fprintf('bin %d=%d\n',i,bin);
  end
end



set(gca, 'xtick', xtick)
%xtick
set(gca,'xticklabel',ticklabel);
%ticklabel
set(gca,'xlim',[xtick(1) xtick(end)]);
set(gca,'tickdir','in');
xlabel('hours');
ylabel('mean activity');
text(1, max(avg), txt)

% put up any warning afterwards
if ~isempty(warning)
  warndlg(warning)
end



% return bin numbers for center-aligning light or dark
function bins = center(where, light)
  maxbins = length(light);
  pad = maxbins - length(where);
  if (pad/2) == fix(pad/2)
    lpad = pad / 2;
    rpad = pad / 2;
  else
    lpad = fix(pad/2) + 1;
    rpad = fix(pad/2);
  end
  bbeg = where(1) - lpad;
  if bbeg < 0
    bbeg = maxbins + bbeg;
  end
  bin = bbeg;
  for i = 1:lpad
    bins(i) = bin;
    bin = bin + 1;
    if bin > maxbins
      bin = 1;
    end
  end
  bins = [bins';where];
  lastbin = bins(end);
  for i = 1:rpad
    bin = lastbin + i;
    if bin > maxbins
      bin = 1;
    end
    bins(end+1) = bin;
  end
  
  
% return bin numbers for left-aligning light or dark
function bins = left(bins, light)
  bin = bins(end);
  for i = 1:length(light)-length(bins)
    bin = bin + 1;
    if bin > length(light)
      bin = 1;
    end
    bins(end+1) = bin;
  end
