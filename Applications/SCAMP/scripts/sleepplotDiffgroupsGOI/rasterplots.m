function rasterplots(t,doprint,selectedDays,file,groupname)

[a,s30]=fly_sleepthresh(file,t);
[x y]= size(a);
% This will create a separate figure for each group that you choose in the
% analysis dialog box. The dimensions of subplot are determined by the
% number of flies in the group (rows) and the number of days selected
% (columns), and the panel calculation makes sure that all the flies from
% the same day are stacked on top of each other.
figure('Name',[groupname ' - Individual Raster Plots'],'NumberTitle','off');
    
    for j=1:length(selectedDays)
        for n=1:y;
            subplot(y,length(selectedDays),(n+(j-1))+(length(selectedDays)-1)*(n-1)); 
            bar (a(selectedDays(j)+((selectedDays(j)-1)*1440):selectedDays(j)*1440,n));
            axis tight
            set(gca,'ytick',[])
            set(gca,'xtick',[])
        end
    end
set(gcf,'PaperOrientation','landscape');
set(gcf, 'PaperPositionMode', 'manual');
set(gcf, 'PaperPosition', [0.05 0.25 10.75 8.25]);
set (gca,'FontSize',6)

if doprint>0
   print
end
