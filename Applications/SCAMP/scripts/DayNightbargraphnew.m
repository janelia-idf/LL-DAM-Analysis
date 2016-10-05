function DayNightbargraphnew(allData,selectedGroups,analysistype)

b=[];
errdata=[];
groupavg=[];
grouperror=[];

    for i=1:length(selectedGroups)
        A=[];
        AE=[];
        for j=1:length(allData{selectedGroups(i)}{analysistype})
            current = (allData{selectedGroups(i)}{analysistype}{j});
            
            % animalavg takes the average value across days for each
            % animal - if there is only one day, this is simply the raw
            % data with no averaging.
            [r c]=size(current);
            if r==1
                animalavg=current;
            else
                animalavg=nanmean(current);
            end
            % groupavg averages across animals, unless there is only 1
            % animal in the group. In that case, groupavg is again just the
            % raw data, and group error is simply 0
            [r c]=size(animalavg);
            if c==1
                groupavg=[animalavg];
                grouperror=0;
            else
                groupavg=nanmean(animalavg);
                grouperror=nansem(animalavg);
            end
            % A becomes a column of groupavg for 24 hour data, LP, and D
            A=[A;groupavg];
            AE=[AE;grouperror];
        end
        
        b(:,i)=A;
        errdata(:,i)=AE;
    end
        h=bar(b,'grouped');
        %h = bar(b,'grouped');% If you are using MATLAB 6.5 (R13)
        hold on;
        
%         This commented material was removed when the 'v6' argument in the
%         bar function became defunct, making the xdata command not
%         retrieve the correct info for finding the centerpoint of each bar
%         for the errobars to be placed appropriately. Replaced with lines
%         80-94.

%         xdata = get(h,'XData');
%         xdata2={};
%         if ~isa(xdata,'cell')
%             xdata2{1}=xdata;
%             xdata=xdata2;
%         end
%         
%         sizz = size(b);
%         % determine the number of sets of bars and groups
%         NumGroups = sizz(1);
%         SizeGroups = sizz(2);
%         NumBars = SizeGroups * NumGroups;
%         % Use the Indices of Non Zero Y values to get both X values 
%         % for each bar. xb becomes a 2 by NumBars matrix of the X values.
%         INZY = [1 3];
%         xb = [];
%         
%         for i = 1:SizeGroups
%             for j = 1:NumGroups
%                 xb = [xb xdata{i}(INZY, j)];
%             end
%         end
% 
%         % find the center X value of each bar.
%         for i = 1:NumBars
%             centerX(i) = (xb(1,i) + xb(2,i))/2;
%         end

numgroups = size(b, 1); 

numbars = size(b, 2); 

groupwidth = min(0.8, numbars/(numbars+1.5));

for i = 1:numbars

      % Based on barweb.m by Bolu Ajiboye from MATLAB File Exchange

      x = (1:numgroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*numbars);  % Aligning error bar with individual bar

      eh = errorbar(x, b(:,i), errdata(:,i),'k', 'linestyle', 'none');

end
%         Commented material below also become unnecessary after adding the
%         new material above in lines 80-94.
% 
%         % To place the error bars - use the following:
%         
%         % eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
%         eh = errorbar('v6',centerX,b,errdata);
       
        set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
%         set(eh(1),'color','k'); % This changes the color of the errorbars
%         set(eh(2),'linestyle','none'); % This removes the connecting line
        set (gca,'FontSize',8,'FontWeight','bold')
        
        % set(gca,'xticklabel', [{'5-15';'16-60';'61-180';'181-300';'301-420';'421-540';'>540'}])
        % xlabel('Sleep Epidode Duration (min)','FontSize',10,'FontWeight','bold')
        % ylabel('Number of Sleep Episodes','FontSize',10,'FontWeight','bold')
        % set(gcf,'Color',[1,1,1]) 
        % legend(name1,name2)
        % legend('boxoff')
        % ax1 = gca;
        % set(ax1,'yticklabel',[0;5;10;15;20;25;30;35],...
            % 'ylim',[0 35],'xlim',[0 5])
        % ax2 = axes('Position',get(ax1,'Position'),...
            % 'XAxisLocation','top',...
            %'YAxisLocation','right',...
            %'Color','none',...
            %'XColor','k','YColor','k','FontSize',5,...
            %'yticklabel',[0;0.5;1.0;1.5;2.0;2.5;3.0;3.5],...
            %'xticklabel',[],...
            % 'ylim',[0 35],'xlim',[0 2])
        % ylabel('Gain
        % (%)','FontSize',7,'Position',[1.6150,100,1],'Rotation',270)
        
        