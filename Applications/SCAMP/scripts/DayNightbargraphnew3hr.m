function DayNightbargraphnew3hr(avg3HrData,selectedGroups,analysistype)

b=[];
errdata=[];
groupavg=[];
grouperror=[];
avg3HrData{1}{1};

    for i=1:length(selectedGroups)
        A=[];
        AE=[];
            current = (avg3HrData{selectedGroups(i)}{analysistype});
            
            % animalavg takes the average value across days for each
            % animal - if there is only one day, this is simply the raw
            % data with no averaging.
            
%             [r c]=size(current);
%             if r==1
%                 animalavg=current;
%             else
%                 animalavg=nanmean(current);
%             end
            
            % groupavg averages across animals, unless there is only 1
            % animal in the group. In that case, groupavg is again just the
            % raw data, and group error is simply 0
            [r c]=size(current);
            for k=1:r
                if c==1
                    groupavg=current(k,:);
                    grouperror=0;
                else
                    groupavg=nanmean(current(k,:));
                    grouperror=nansem(current(k,:));
                end
                % A becomes a row of groupavg the length of r (should be 8 for
                % 3 hr data)
                A=[A;groupavg];
                AE=[AE;grouperror];
            end

        b(:,i)=A;
        errdata(:,i)=AE;
        
    end
        
        h=bar('v6',b,'grouped');
        %h = bar(b,'grouped');% If you are using MATLAB 6.5 (R13)
        xdata = get(h,'XData');
        sizz = size(b);
        % determine the number of bars and groups
        NumGroups = sizz(1);
        SizeGroups = sizz(2);
        NumBars = SizeGroups * NumGroups;
        % Use the Indices of Non Zero Y values to get both X values 
        % for each bar. xb becomes a 2 by NumBars matrix of the X values.
        INZY = [1 3];
        xb = [];
        
        for i = 1:SizeGroups

            for j = 1:NumGroups
                xb = [xb xdata{i}(INZY, j)];
            end
        end

        % find the center X value of each bar.
        for i = 1:NumBars
            centerX(i) = (xb(1,i) + xb(2,i))/2;
        end

        % To place the error bars - use the following:
        hold on;
        % eh = errorbar(centerX,b,errdata); %If you are using MATLAB 6.5 (R13)
        eh = errorbar('v6',centerX,b,errdata);
        set(eh(1),'linewidth',1); % This changes the thickness of the errorbars
        set(eh(1),'color','k'); % This changes the color of the errorbars
        set(eh(2),'linestyle','none'); % This removes the connecting line
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
        
        