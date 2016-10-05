function delpeaks1=manualpeaks_new(x1all,sp1all,pp1all,xx1all,list)

delpeaks1=[];
% [delpeaks1,delpeaks2]=manualpeaks(x1,sp1,pp1,xx1,... ...
% x2,sp2,pp2,xx2);

fhphase = figure;
set(fhphase,'Position',[400,200,500,400],'Name','Phase Shift Analysis','NumberTitle','off');
buttongroupphase = uibuttongroup(fhphase,'visible','on','Units','Normalized','Position',[0,0,1,1]);

groupInstruct = uicontrol (buttongroupphase,'Style','text','String',...
    'Select a Pair of Groups to Analyze','Units','Normalized','Position',[5/300,280/300,140/300,10/300]);

for i=1:length(list)
    groupname=list{i};
    if i<=12
        group(i) = uicontrol (buttongroupphase,'Style','checkbox',...
            'String',['Group = ' groupname],'Units','Normalized','position',[10/300,(260-((i-1)*15))/300,150/300,15/300]);
    else
        
        group(i) = uicontrol (buttongroupphase,'Style','checkbox',...
            'String',['Group = ' groupname],'Units','Normalized','position',[160/300,(260-((i-13)*15))/300,150/300,15/300]);
    end
    set(group(i),'Value',1);
end

pbhphase = uicontrol(buttongroupphase,'Style','pushbutton',...
    'Units','Normalized','Position',[10/300,10/300,200/500,50/400],...
    'Callback',{@manualpeaks});
set(pbhphase,'String','<html><p style="text-align: center;">GRAPH<br>Peaks for<br>Selected Groups</p>');

pbhend = uicontrol(buttongroupphase,'Style','pushbutton',...
    'Units','Normalized','Position',[160/300,10/300,200/500,50/400],...
    'Callback',{@pbhphaseend});
set(pbhend,'String','<html><p style="text-align: center;">Done<br>Picking Peaks<br>for All Groups?</p>');



    function manualpeaks(src,evt)
     
        selected = get(group,'Value');
        
        selectedGroups = [];
        for i=1:length(selected)
            if length(group)==1
                if selected(i) == 1
                    selectedGroups = [selectedGroups i];
                end
            elseif length(selected) > 1
                if selected{i} == 1
                    selectedGroups = [selectedGroups i];
                end
            end
        end
        %The catches below should be unnecessary because scamp currently
        %filters for exactly 2 groups in the analysis
        if isempty(selectedGroups)
            error('You did not select any groups!')
        elseif length(selectedGroups)~=2
            error('You need to select exactly 2 groups!')
        end
        
        listpair=list(selectedGroups);
        x1pair=x1all(selectedGroups);
        sp1pair=sp1all(selectedGroups);
        pp1pair=pp1all(selectedGroups);
        xx1pair=xx1all(selectedGroups);
        
        x1=x1pair{1};
        sp1=sp1pair{1};
        pp1=pp1pair{1};
        xx1=xx1pair{1};
        x2=x1pair{2};
        sp2=sp1pair{2};
        pp2=pp1pair{2};
        xx2=xx1pair{2};
        
        handle_id=155;
        handle_id=figure ;
        hold on
        delpeaks1=[];
        delpeaks2=[];
        plot(x1,sp1);
        plot(x2,sp2);
        plot(x1(xx1),pp1,'*','markersize',9)
        plot(x2(xx2),pp2,'o','markersize',9)
        finish=0;
        xlim=get(gca,'xlim');
        ylim=get(gca,'ylim');
        
        while(finish==0 )
            if (length(xx1)-length(delpeaks1)) ~= (length(xx2)-length(delpeaks2))
                title('WRONG');
            else
                title('MAYBE RIGHT');
            end
            uu=[];
            if ~isempty(delpeaks1)
                uu=[uu,'DEL1=',sprintf('%d ',delpeaks1)];
            end
            if ~isempty(delpeaks2)
                uu=[uu,'DEL1=',sprintf('%d ',delpeaks2)];
            end
            [x,y]=ginput(1);
            if (x<xlim(1) || x > xlim(2) || y<ylim(1) || y>ylim(2))
                finish=1;
            else
                di1=(x1(xx1)-x).^2+(pp1-y).^2;
                n1=find(di1==min(di1));
                di1=di1(n1(1));
                di2=(x2(xx2)-x).^2+(pp2-y).^2;
                n2=find(di2==min(di2));
                di2=di2(n2(1));
                if di1<di2
                    delpeaks1=[delpeaks1,n1];
                    for i=1:4:13
                        plot(x1(xx1(n1)),pp1(n1),'o','markersize',i);
                    end
                else
                    delpeaks2=[delpeaks2,n2];
                    for i=1:4:13
                        plot(x2(xx2(n2)),pp2(n2),'o','markersize',i);
                    end
                end
            end
        end
%         delpeaks1;
%         delpeaks2;
        close(handle_id)
    end

% finishall=0;
% 'abdc'
% while finishall==0
%     
% end
% 'abcd'

    function pbhphaseend(src,evt)
        finishall=1;
    end
end
