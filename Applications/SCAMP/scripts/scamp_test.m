


function scamp_test()

% scamp = Sleep and Circadian Analysis MATLAB Program

%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (C) Leslie Griffith Lab, Brandeis University.         %%
% Written primarily by Christopher G. Vecsey and Eugene Z. Kim.   %%
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

% Makes GUIs to select files - names of raw data files have to be formatted appropriately. Builds theList with names of boards.

    onePath = uigetdir('.','Select the one minute folder');
    thirtyPath = uigetdir('.','Select the thirty minute folder');
   
    if isa (onePath, 'double') || isa (thirtyPath, 'double')
      error('You did not select both folders!')
    end
    
    
    theList = {};
    last = '';
    filenames = dir(onePath); 
    theList = buildList(theList,last,filenames);
    
    last = '';
    filenames = dir(thirtyPath); 
    theList = buildList(theList,last,filenames);
         
    % Builds figure for choosing boards, flies, and assigning groups.

    fh = figure;
    set(fh,'Position',[200,200,1000,500],'Name','Choose boards','NumberTitle','off');

    panel = uipanel('Parent',fh,'Units','normalized','Position',[0.35,0,0.65,1]);

    for i=1:length(theList)  
    boardboxes(i) = uibuttongroup(panel,'visible','off','Title',...
                ['Board ' theList{i}],'Units','normalized','Position',[0,0,1,(490/500)]);
    
    % If you want the applyGroupToAll pushbutton function to actually apply to all instead of
    % to only the boards above the board on which you press the button, you
    % need to insert another for loop here so that all the boardboxes are
    % built before the applyGroupToAll button is formed.   
            
        for j=1:32
            if j<17
            channel(j) = uicontrol (boardboxes(i),'Style','checkbox',... 
            'String',['Channel ' num2str(j)],'Units','normalized',...
            'position',[(5/300),(260/290)-((j-1)*(15/290)),(50/300),(15/290)]);
            else
            channel(j) = uicontrol (boardboxes(i),'Style','checkbox',...
            'String',['Channel ' num2str(j)],'Units','normalized',...
            'position',[(150/300),(260/290)-((j-17)*(15/290)),(50/300),(15/290)]);
            end
        set(channel(j),'Value',1);
        end
    
        for j=1:32
            if j<17
            groupChoice(j) = uicontrol (boardboxes(i),'Style','edit',...
            'String','Group','Units','normalized',...
            'position',[(55/300),(260/290)-((j-1)*(15/290)),(90/300),(15/290)]);
            else
            groupChoice(j) = uicontrol (boardboxes(i),'Style','edit',...
            'String','Group','Units','normalized',...
            'position',[(205/300),(260/290)-((j-17)*(15/290)),(90/300),(15/290)]);
            end 
        end
    
        selectAll = uicontrol (boardboxes(i),'Style','checkbox',...
            'String','Select All Channels','Units','normalized',...
            'position',[(30/300), (8/290), (100/300), (15/290)],...
            'Callback',{@allSelect,channel});
        set(selectAll,'Value',1);
        
        applyGroupToAll = uicontrol (boardboxes(i),'Style','pushbutton',...
            'String','Apply Groups to Boards Above','Units','normalized',...
            'position',[(120/300),(7/290), (165/300),(20/290)],...
            'Callback',{@applyGroups,boardboxes,groupChoice});
    end    
    
    lbh = uicontrol(fh,'Style','listbox',...
                'String',theList,...
                'Max',length(theList),'Min',0,...
                'Units','Normalized','Position',[0,0,(100/500),1],...
                'Callback',{@makeBoardboxes,boardboxes},...
                'UserData',cell(2,length(theList)));      
    pbh = uicontrol(fh,'Style','pushbutton',...
                'Units','Normalized','Position',[(100/500),(150/300),(75/500),(150/300)],...
                'Callback',{@sleepRalph,lbh,theList,onePath,thirtyPath});
    set(pbh,'String','<html><p style="text-align: center;">LOAD<br>Individual<br>Sleep Plots</p>');

    pbh2 = uicontrol(fh,'Style','pushbutton',...
                'Units','Normalized','Position',[(100/500),0,(75/500),(150/300)],...
                'Callback',{@analyze,lbh,theList,boardboxes,onePath,thirtyPath},...
                'UserData',{cell(1,3)});
    set(pbh2,'String','<html><p style="text-align: center;">ANALYZE<br>Selected<br>Data</p>');
    end

function [theList] = buildList(theList,last,filenames)
    %This next for loop takes care of the fact that different computers have
    %different numbers of garbage files that precede the first real file -
    %these have names like ".", "..", and sometimes ".DS_Store". If these are 
    %included in the 2nd for loop below,they will cause problems because they 
    %lack a C in their file name. Thus,they must be removed/ignored.
    first = [];
    for i=1:length(filenames)
        current=filenames(i).name;
        index = strfind(current,'C');
        if isempty(first) && ~isempty(index)
            first = i;
        end
    end
    
    for i=first:length(filenames)
    current = filenames(i).name;
    index = strfind(current,'C');
    length(index);
        if length(index) == 1
        name = current(1:index-1);
        %This will screw up if you only have a single tube of data in a board on your
        %last board - shouldn't be a problem
        elseif length(index) == 2
            name = current(1:index(2)-1);
        else
            error('Your file names may have too few or too many "C"s in them!')
        end

        if ~strcmp(name,last) % || i==length(filenames) 
          theList = [theList {name}]; 
        end
        last = name;
    end
end
     
function [oneObject,thirtyObject]=myDamLoad(theList,onePath,thirtyPath) % Runs dam_load, which then calls a cascade of other functions to open and organize raw data. All from Rosbash/Hall labs.

%     oneObject = dam_load(board,'.',1,4);

    fprintf('onePath = %s\n',onePath)
    fprintf('thirtyPath = %s\n',thirtyPath)

    cd(onePath);
    oneObject = dam_load(theList(1),'.',1,4);
    
    cd(thirtyPath);
    thirtyObject = dam_load(theList(2),'.',1,4);
end

function sleepRalph(src,evt,lbh,theList,onePath,thirtyPath) % Runs sleepRalph, which prints a figure for each board, showing sleep bouts in blue. Used for de-selecting dead flies. 
% If you prefer to do this by looking at activity, uncomment two lines for running ralf instead.
    selected = get(lbh,'Value');
    data=get(lbh,'UserData');
    
    for i=1:length(selected)
       board = theList{selected(i)};
       [oneObject,thirtyObject]=myDamLoad(theList,onePath,thirtyPath);
       data{1,selected(i)}=oneObject;
       data{2,selected(i)}=thirtyObject;
       
       figure('Name',board,'NumberTitle','off');
       sleepralph2(oneObject,thirtyObject,5,1);
%        figure
%        ralf(thirtyObject);
    end
    
    set(lbh,'UserData',data);
    
    cd('..'); 
end

function makeBoardboxes(src,evt,boardboxes)
    selected = get(src,'Value');
    
    set(boardboxes,'visible','off');
    
    if length(selected) > 1
        set(boardboxes(selected(1)),'visible','on');
    elseif length(selected) == 1
        set(boardboxes(selected),'visible','on');
    end
end

function allSelect(src,evt,channel)
    response = get(src,'Value');
    for j=1:32
        if response == 1
        set(channel(j),'Value',1);
        elseif response == 0
        set(channel(j),'Value',0);
        end
    end
end

function applyGroups(src,evt,boardboxes,groupChoice)
    
    groupList = get(groupChoice,'String');

    for i=1:length(boardboxes)
        channels = get(boardboxes(i),'Children');
        styles = get(channels,'Style');
        channels = flipud(channels);    
        styles = flipud(styles);
        
        groupChildren = [];
        
        for j=1:length(channels)
            
            if strcmp(styles(j),'edit')
               groupChildren = [groupChildren channels(j)];    
            end
        end
        
        for j=1:length(groupChildren)
            set(groupChildren(j),'String',groupList{j});
%             This function if you write the group
%             names into the last board in the listbox and then apply to
%             all others. If you write the names into the first board and
%             then hit the button, nothing will happen.
        end
    end
end

function analyze(src,evt,lbh,theList,boardboxes,onePath,thirtyPath)

%     The section below makes a cell array called "list" and another array called
%     "index." "List" contains strings with the different names of groups
%     found within the groupChildren textboxes. "Index" has i rows (# boards) by 32
%     columns (# channels). Each point in the "index" array defines the group number of
%     that fly. 1 = the 1st item  from "list", 2 = the 2nd item from "list" etc.
    
    selectedBoards = get(lbh,'Value');
    list = {};
    index = zeros(length(boardboxes),32);
    for i=1:length(selectedBoards)
        board = selectedBoards(i);
        
        channels = get(boardboxes(board),'Children');
        styles = get(channels,'Style');
        channels = flipud(channels);    
        styles = flipud(styles);
        
        selected = get(channels,'Value');
        
        selectedChannels = [];
        for j=1:64
            if strcmp(styles(j),'checkbox') && selected{j} == 1
                selectedChannels = [selectedChannels j];
            end
        end 
        
        groupChildren = [];
        for j=1:length(channels)
            if strcmp(styles(j),'edit')
               groupChildren = [groupChildren channels(j)];    
            end
        end
        
        for j=1:length(selectedChannels)
            sel = selectedChannels(j);
            name = get(groupChildren(sel),'String');
            len=length(list);
            if len<1
                list{1}=name;
                index(board,sel)=1;
            else
                match = 0;
                for k=1:length(list)
                    if strcmp(name,list{k})
                        index(board,sel)=k;
                        match = 1;
                    end
                end
                if ~match
                    list{k+1}=name;
                    index(board,sel)=k+1;
                end  
            end
        end
    end
    
%     The section below should be set up to run dam_select the same number of times 
%     as the length of "list" for each appropriate number in "index". No
%     longer needs to control for checkboxes being selected, since this
%     information has already been processed in "index".

    data = get(lbh,'UserData');
    oneObject = {};
    thirtyObject = {};
    
    for i=1:length(selectedBoards)
       %This IF statement checks to see if sleep ralph (and therefore
       %Dam_Load) has been run already. If it hasn't, it runs Dam_Load
       %again...
       
       if  isempty(data{1,selectedBoards(i)}) 
           board = theList{selectedBoards(i)};    
           [oneObject,thirtyObject]=myDamLoad(theList,onePath,thirtyPath);
           
           data{1,selectedBoards(i)}=oneObject;
           data{2,selectedBoards(i)}=thirtyObject;
          
       end
    end
    % This section runs dam_select and dam_merge to create objects
    % containing all data for a given group.
    selectoneObject={};
    selectthirtyObject={};
    currentOne={};
    currentThirty={};
    oneGroupmerge={};
    thirtyGroupmerge={};
    
    for i=1:length(list)
            
        for j=1:length(selectedBoards)
            sel=selectedBoards(j);
            genotypeChannels=find(index(sel,:)==i);
         
            cd(onePath);
            selectoneObject{j} = dam_select(data{1,sel},genotypeChannels);
            cd(thirtyPath);
            selectthirtyObject{j} = dam_select(data{2,sel},genotypeChannels);     
        
            if j==1
                currentOne = selectoneObject{j};
                currentThirty = selectthirtyObject{j};
            else
                currentOne = dam_merge(currentOne,selectoneObject{j});
                currentThirty = dam_merge(currentThirty,selectthirtyObject{j});
            end
        end
        oneGroupmerge{i}=currentOne;
        thirtyGroupmerge{i}=currentThirty;
    end
    
    list;
    oneGroupmerge;
    thirtyGroupmerge;  

    cd('..')
    
%     allData = {};
   
    % Below is code to build a second window for choosing sleep analyses to run,
    % days to analyze, groups to analyze, if you want to average data
    % across days or not, if you want to export data, if you want to run
    % 3-hour analyses, choosing the appropriate LD, DD, or LL schedule (only changes labeling of figures) and if you want to run circadian analyses.
    
    fh2 = figure;
    set(fh2,'Position',[100,100,1400,800],'Name','Choose Analysis','NumberTitle','off');
    
%     panel1 = uipanel('Parent',fh2,'Units','pixels','Position',[0, 0, 200, 300]);
%     
%     panel2 = uipanel('Parent',fh2,'Units','pixels','Position',[200, 0, 300, 300]);
     
    buttongroup1 = uibuttongroup(fh2,'visible','on','Units','Normalized','Position',[0,0,350/800,1]);

    buttongroup2 = uibuttongroup(fh2,'visible','on','Units','Normalized','Position',[450/800,0,350/800,1]);
    
    
    analysisIDs={'amean';'s30';'stdur';'sfreq';'smax';'smeandur';'smedian';'oamean';...
    'atcounts';'namean';'ameandur';'afreq';'atdur';'latency';'MeanWakeDur';'wmax';'WSdiff'};

    analysisNames={'amean - Activity Counts/30 Mins';'s30 - Minutes of Sleep/30 Mins';'stdur - Total Sleep Duration';'sfreq - Number of Sleep Episodes';...
    'smax - Max Sleep Episode Duration';'smeandur - Mean Sleep Episode Duration';'smedian - Median Sleep Episode Duration';'oamean - Activity Counts/Time Awake';...
    'atcounts - Total Activity Counts';'namean - Mean Activity/Min while Moving';'ameandur - Mean Wake Episode Duration';'afreq - Number of Wake Episodes';'atdur - Total Time Awake';...
    'latency - Latency to Sleep during Bin';'MeanWakeDur - like ameandur minus 1st wake episode';'wmax - Max Wake Episode Duration';'WSdiff - Sleep Stability (wmax-smax)'};

    analysisLabels={'amean';'s30';'Total Sleep Duration (min)';'Number of Sleep Episodes';...
        'Maximum Sleep Episode Duration (min)';'Mean Sleep Episode Duration (min)';'Median Sleep Episode Duration (min)';'Activity while Awake (beam crosses/min)';...
        'Total Activity Counts';'Activity while Active (beam crosses/min)';'ameandur';'afreq';'atdur';'Sleep Latency (min)';'Mean Wake Episode Duration (min)';'Max Wake Episode Duration (min)';'Sleep State Stability'};

    for i=1:length(analysisNames)
            analysis(i) = uicontrol (buttongroup1,'Style','checkbox',... 
            'String',[analysisNames{i}],'Units','Normalized','position',[5/250,(260-((i-1)*12))/300,150/250,15/300]);
            set(analysis(i),'Value',0);
    end
    set(analysis(2:6),'Value',1);
    set(analysis(14),'Value',1);
    set(analysis(15),'Value',1);
    
    circadianAnalysisNames={'Actogram';'Histogram';'Autocorrelation';'MESA';'Flyplot';'Filtered Flyplot';'Periodogram'};
       
    circadianAnalysisLabels={};
    
    for i=1:length(circadianAnalysisNames)
            circAnalysis(i) = uicontrol (buttongroup1,'Style','checkbox',... 
            'String',[circadianAnalysisNames{i}],'Units','Normalized','position',[150/250,(260-((i-1)*12))/300,100/250,15/300]);
        if i<5
            set(circAnalysis(i),'Value',1);
        end
    end
    
    for i=1:length(list)
            groupname=list{i};
            group(i) = uicontrol (buttongroup2,'Style','checkbox',... 
            'String',['Group = ' groupname],'Units','Normalized','position',[10/300,(260-((i-1)*12))/300,150/300,15/300]);
            set(group(i),'Value',1);
    end            
     
        %   The line below determines the number of total days of experimental data by dividing the overall length of 
        %   the data in oneGroupmerge by 1440, the number of minutes in 1 day of data. 
    a = oneGroupmerge{1};
    [R C] = size(a.data);
    R = floor(R/1440);
    
    for i=1:R
        if i<=16
            day(i) = uicontrol (buttongroup2,'Style','checkbox',... 
        'String',['Day ' num2str(i)],'Units','Normalized','position',[175/300,(260-((i-1)*12))/300,50/300,15/300]);
        set(day(i),'Value',1);
        else
            day(i) = uicontrol (buttongroup2,'Style','checkbox',... 
        'String',['Day ' num2str(i)],'Units','Normalized','position',[235/300,(260-((i-17)*12))/300,50/300,15/300]);
        set(day(i),'Value',1);
        end
    end
    
    circIndividualChoice = uicontrol(buttongroup2,'Style','checkbox',...
            'String','Individual Circadian Data?','Units','Normalized','position',[150/300,5/300,120/300,15/300]);
       
    graphChoice = uicontrol(buttongroup2,'Style','checkbox',...
            'String','Graph Data?','Units','Normalized','position',[10/300,20/300,120/300,15/300]);
    
    exportChoice = uicontrol(buttongroup2,'Style','checkbox',...
            'String','Export Data?','Units','Normalized','position',[10/300,5/300,120/300,15/300]);
    
    lightSchedule = {'LD','DD','LL'};
        
    for i=1:3
         name=lightSchedule{i};
         chooseDDLDLL(i) = uicontrol (buttongroup2,'Style','radiobutton',... 
         'String',name,'Units','Normalized','position',[(150+(i-1)*40)/300,20/300,40/300,15/300]);
         set(chooseDDLDLL(1),'Value',1);
    end
    
    selectBinLength = uicontrol (buttongroup2,'Style','edit',...
            'String','Default (12/24hr)','Units','normalized',...
            'position',[(10/300),(60/300),(120/300),(15/300)]);
    
    analyzeforBin = uicontrol (buttongroup2,'Style','pushbutton',...
            'String','Analyze for Chosen Bin','Units','normalized',...
            'position',[(150/300),(60/300), (150/300),(15/300)],...
            'Callback',{@analyzeBin,oneGroupmerge,selectBinLength},...
            'Userdata', []);
    
    pbh = uicontrol(fh2,'Style','pushbutton',...
                'Units','Normalized','Position',[350/800,400/500,100/800,100/500],...
                'Callback',{@graphAllDays,analyzeforBin,day,list,group,analysisIDs,graphChoice,exportChoice});
        set(pbh,'String','<html><p style="text-align:center;">GRAPH<br>s30 and amean<br>for All Days<br>for Selected Groups<br>and EXPORT<br>All Data<br>for All Groups</p>');
    
    pbh2 = uicontrol(fh2,'Style','pushbutton',...
                'Units','Normalized','Position',[350/800,300/500,100/800,100/500],...
                'Callback',{@multDayExtract,analyzeforBin,day,group,analysis,analysisIDs,graphChoice,exportChoice,chooseDDLDLL,list},...
                'UserData',cell(1,length(list)));
        set(pbh2,'String','<html><p style="text-align:center;">AVERAGE Selected Days,<br>GRAPH Selected Data,<br>and EXPORT All Data</p>');
    
    pbh3 = uicontrol(fh2,'Style','pushbutton',...
                'Units','Normalized','Position',[350/800,250/500,100/800,50/500],...
                'Callback',{@graphCircadianData,thirtyGroupmerge,circAnalysis,group,day,chooseDDLDLL,list,circIndividualChoice,exportChoice},...
                'Userdata',circadianAnalysisLabels);
        set(pbh3,'String','<html><p style="text-align: center;">GRAPH/EXPORT<br>Selected Circadian Data<br>for Selected Groups</p>');
        
    pbh6 = uicontrol(fh2,'Style','pushbutton',...
                'Units','Normalized','Position',[350/800,200/500,100/800,50/500],...
                'Callback',{@phaseshiftanalysis,oneGroupmerge,group,list,exportChoice});
        set(pbh6,'String','<html><p style="text-align: center;">GRAPH/EXPORT<br>Phase Shift Data<br>for Selected Groups</p>');    
        
    pbh4 = uicontrol(fh2,'Style','pushbutton',...
                'Units','Normalized','Position',[350/800,100/500,100/800,100/500],...
                'Callback',{@rasterPlots,oneGroupmerge,group,day,list});
        set(pbh4,'String','<html><p style="text-align: center;">GRAPH<br>Individual<br>Raster<br>Plots</p>');
    
    pbh5 = uicontrol(fh2,'Style','pushbutton',...
                'Units','Normalized','Position',[350/800,0,100/800,100/500],...
                'Callback',{@SDanalysis,analyzeforBin,list});
        set(pbh5,'String','<html><p style="text-align: center;">Perform<br>Sleep<br>Deprivation<br>Analysis</p>');
            
    selectAllGroups = uicontrol (buttongroup2,'Style','checkbox',...
            'String','Select All Groups','Units','Normalized','position',[10/300,35/300,120/300,15/300],...
            'Callback',{@allGroupSelect,group});
        set(selectAllGroups,'Value',1);
    
    selectAllDays = uicontrol (buttongroup2,'Style','checkbox',...
            'String','Select All Days','Units','Normalized','position',[150/300,35/300,120/300,15/300],...
            'Callback',{@allDaySelect,day});
        set(selectAllDays,'Value',1);    
        
    analysisInstruct = uicontrol (buttongroup1,'Style','text','String',...
        'Select Sleep Data','Units','Normalized','Position',[5/250,280/300,120/250,10/300]);  
    
    circAnalysisInstruct = uicontrol (buttongroup1,'Style','text','String',...
        'Select Circadian Data','Units','Normalized','Position',[130/250,280/300,120/250,10/300]);
        
    groupInstruct = uicontrol (buttongroup2,'Style','text','String',...
            'Select Groups to Analyze','Units','Normalized','Position',[5/300,280/300,140/300,10/300]); 
    
    dayInstruct = uicontrol (buttongroup2,'Style','text','String',...
            'Select Days to Average','Units','Normalized','Position',[150/300,280/300,140/300,10/300]);

    function analyzeBin (src,evt,oneGroupmerge,selectBinLength)
        % Here begin all the calculations based on the group data established by dam_select
        % On 3-23-10, removed thirtyGroupmerge{i} as the 2nd input to sleepcalc2 -
        % it was never used by any of the calculations within. Doesn't seem like
        % the 30-min data is ever actually used...
        BinLength = get(selectBinLength,'string');
        BinLengthNum = str2num(BinLength);
        Calc12Object = {};
        Calc24Object = {};
        CalcXObject = {};
        
        for i=1:length(list)
            if strcmp(BinLength,'Default (12/24hr)') || strcmp (BinLength,'12/24');
                Calc12Object{i}=sleepcalc2EDIT(oneGroupmerge{i},5,720);
                Calc24Object{i}=sleepcalc2EDIT(oneGroupmerge{i},5,1440);
            elseif BinLengthNum-floor(BinLengthNum) == 0
                CalcXObject{i}=sleepcalc2EDIT(oneGroupmerge{i},5,(BinLengthNum*60));
            else error('Bin length must be an integer!');
                
            end
        end
        display('Bin Analysis Complete');
%     These are the current calculations. If you add more, make sure to add them at the end...
%     If you don't, it will not choose the correct data for subsequent analyses and printing...
%     Calc12 and Calc24 Objects: [amean,s30,stdur,sfreq,smax,smeandur,smedian,oamean,atcounts,...
%     namean,ameandur,afreq,atdur,latency,MeanWakeningsDur,wmax,WSDiff]  
    if  ~isempty(Calc12Object)    
        CalcXObject = {Calc12Object,Calc24Object};
        set(src,'Userdata',CalcXObject);
    else
        set(src,'Userdata',CalcXObject);
    end
    end

    function SDanalysis (src,evt,analyzeforBin,list)
                  
        CalcXObject = get(analyzeforBin,'Userdata');
        % If statement below catches the error of trying to perform sleep
        % deprivation analysis before performing bin analysis, a required
        % pre-requisite... The actual choice of bin length doesn't matter.
        if isempty(CalcXObject)
            error('You need to Analyze for Chosen Bin first!');
        end
        
        s30output = cell(1,length(list));
        
        for i = 1:length(list)
            % Following if/else statement controls for starting SD analysis
            % after having used 12/24 default bins (the IF part) or having
            % used a single bin length (the ELSE part).
            if length(CalcXObject)==2
                s30output{i} = CalcXObject{1}{i}{2};
            else
                s30output{i} = CalcXObject{i}{2};
            end
        end
        
        fh3 = figure;
        set(fh3,'Position',[400,200,450,600],'Name','Sleep Deprivation Analysis','NumberTitle','off');
        buttongroup3 = uibuttongroup(fh3,'visible','on','Units','Normalized','Position',[0,0,1,1]);
        
        groupInstruct = uicontrol (buttongroup3,'Style','text','String',...
            'Select Groups to Analyze','Units','Normalized','Position',[5/300,280/300,140/300,10/300]); 
    
        for i=1:length(list)
            groupname=list{i};
            if i<=12
                group(i) = uicontrol (buttongroup3,'Style','checkbox',...
                'String',['Group = ' groupname],'Units','Normalized','position',[10/300,(265-((i-1)*12))/300,150/300,15/300]);
            else
                
                group(i) = uicontrol (buttongroup3,'Style','checkbox',...
                'String',['Group = ' groupname],'Units','Normalized','position',[160/300,(265-((i-13)*12))/300,150/300,15/300]);
            end
            set(group(i),'Value',1);
        end
        
        %   The line below determines the number of total days of experimental data by dividing the overall length of
        %   the data in oneGroupmerge by 1440, the number of minutes in 1
        %   day of data.
        a = oneGroupmerge{1};
        [R C] = size(a.data);
        R = floor(R/1440);

% Because of the way this analysis has been set up, specifying individual
% days for analysis is not necessary.
%         for i=1:R
%             if i<=16
%                 day(i) = uicontrol (buttongroup3,'Style','checkbox',...
%                     'String',['Day ' num2str(i)],'Units','Normalized','position',[175/300,(260-((i-1)*12))/300,50/300,15/300]);
%                 set(day(i),'Value',1);
%             else
%                 day(i) = uicontrol (buttongroup3,'Style','checkbox',...
%                     'String',['Day ' num2str(i)],'Units','Normalized','position',[235/300,(260-((i-17)*12))/300,50/300,15/300]);
%                 set(day(i),'Value',1);
%             end
%         end
        SDgraphChoice = uicontrol(buttongroup3,'Style','checkbox',...
            'String','Graph Data?','Units','Normalized','position',[30/300,30/600,120/300,15/300]);
            set(SDgraphChoice,'value',1)
    
        SDexportChoice = uicontrol(buttongroup3,'Style','checkbox',...
            'String','Export Data?','Units','Normalized','position',[30/300,5/600,120/300,15/300]);

        SDinstructs = {'Baseline Start Day','Baseline Length (days)','SD Start Day','SD Start Time (hrs)','SD Duration (hrs)',...
            'Recovery Duration (hrs)'};
        SDdefaultchoices = {'1','3','4','12','12','24'};
        
        selectAllGroups = uicontrol (buttongroup3,'Style','checkbox',...
            'String','Select All Groups','Units','Normalized','position',[10/300,115/300,120/300,15/300],...
            'Callback',{@allGroupSelect,group});
        set(selectAllGroups,'Value',1);
        
        for i=1:length(SDinstructs)
            SDinstruct = SDinstructs{i};
            SDinstructions(i) = uicontrol (buttongroup3,'Style','text',...
                'String',SDinstruct,'Units','Normalized','position',[20/300,(92-((i-1)*12))/300,120/300,15/300]);
            
            SDdefaultchoice = SDdefaultchoices{i};
            SDchoices(i) = uicontrol (buttongroup3,'Style','edit',...
                'String',SDdefaultchoice,'Units','normalized',...
                'position',[150/300,(95-((i-1)*12))/300,120/300,15/300]);
        end
        
        setChoices = uicontrol (buttongroup3,'Style','pushbutton',...
            'String','Analyze for Choices Above','Units','normalized',...
            'position',[(135/300),(5/300),(150/300),(20/300)],...
            'Callback',{@SDchoiceanalysis,s30output,SDchoices,group,list,SDgraphChoice,SDexportChoice},...
            'Userdata', []);
    end

    function SDchoiceanalysis(src,evt,s30output,SDchoices,group,list,SDgraphChoice,SDexportChoice)
        % This does not have a contingency for non-contiguous stretches of
        % baseline or recovery. So if you had 3 days of baseline, but the
        % 2nd day had a problem and you wanted to exclude it from the
        % analysis, you wouldn't be able to do that using this script.
        SDgraph=get(SDgraphChoice,'value');
        SDexport=get(SDexportChoice,'value');
        SDplusRecCumallgroups=[];
        
        if SDgraph==0 && SDexport==0
            error('You did not choose to graph or export SD analysis output!');
        end
        
        a = get(SDchoices,'string');
        final = [];
        for i=1:length(a)
            temp = str2num(a{i});
            final = [final temp];
        end
        baselineStart = final(1);
        baselineEnd = final(1)+(final(2)-1);
        recoveryDur = final(6);
        SDday = final(3);
        
        SDduration = final(5);
        SDend = final(4)+final(5);
        
        SDstart = ((SDday-1)*48+1+final(4)*2);
        SDperiod = SDstart:SDstart+SDduration*2-1;
        RecStart = (1+(SDday-1)*48+((final(4)+SDduration)*2));
        RecPeriod = RecStart:RecStart+recoveryDur*2-1;
        
        if SDduration <= 0
            error('SD duration must be larger than 0!');
        end
        if baselineStart >= SDday
            error('Baseline and SD period are overlapping!');
        end
        
        if max(RecPeriod)>length(day)*48
            error('Recovery period extends beyond end of recorded data!');
        end
        % Created the following variable because its format worked with
        % existing data export code.
        exportData = cell(1,length(s30output));
        
        % Running through all groups
        for i=1:length(s30output)
            s30current = s30output{i};
            [r c] = size(s30current);
            
            %Running through individual flies in a group
            for j=1:c
                indivSDdata = s30current(SDperiod,j);
                
                % I have now added contingencies for SD spanning more than 
                % 1 day, and for analyzing more than 24 hours of recovery
                % data, including if recovery does not begin at the
                % beginning of a day.                 
                indivRecoverydata = s30current(RecPeriod,j);
                
                for k=1:48
                    temp=[];
                    for m=1:final(2)
                        temp(m) = s30current(k+(baselineStart+m-2)*48,j);
                    end
                    % Creates a matrix containing baseline
                    % values averaged across all baseline days.
                    indivBaselineAVG(k,1) = mean(temp);
                end
                groupBaselineAVG(:,j) = indivBaselineAVG;
                groupRecoverydata(:,j) = indivRecoverydata;
                groupSDdata(:,j) = indivSDdata;
            end
            %The following nested if statements are meant to take care of
            %situations where the lengths of SD and Recovery are <, =, or > the length of
            %baseline (always 24 hours, or 48 data points). 
            % First, for SD Data - Baseline. If equal, can subtract simply.
            if size(groupSDdata,1)==size(groupBaselineAVG,1)
                SDminusBaseline = groupSDdata-groupBaselineAVG;
            else
                % If SD period is shorter than a full day...
                if size(groupSDdata,1)<size(groupBaselineAVG,1)
                    % Need to create a duplicate of baseline data, in case
                    % SD needs to be compared against a period that spans
                    % the end of a day. For example, a 6-hour SD that
                    % starts at ZT20.
                    newgroupBaselineAVG = [groupBaselineAVG;groupBaselineAVG];
                    % bsAVG then becomes the portion of the baseline whose
                    % bins match up with the length of the SD period, so a
                    % simple subtraction can be done.
                    bsAVG = newgroupBaselineAVG(final(4)*2+1:final(4)*2+SDduration*2,:);
                    SDminusBaseline = groupSDdata-bsAVG;
                else
                    % If SD period is longer than a full day...
                   numSDdays = ceil(size(groupSDdata,1)/size(groupBaselineAVG,1));
                   temp = cell(numSDdays);
                   newgroupBaselineAVG = [];
                   % Duplicates baseline data enough to cover the length of
                   % the SD period.
                   for p=1:numSDdays
                       temp{p}=groupBaselineAVG;
                       newgroupBaselineAVG = [temp{p};newgroupBaselineAVG];
                   end
                   % As above, bsAVG becomes the portion of the baseline
                   % whose bins match up with the length of the SD period,
                   % so that a simple subtraction can be done.
                   bsAVG = newgroupBaselineAVG(SDperiod-((SDday-1)*48),:);
                   SDminusBaseline = groupSDdata-bsAVG;
                end
            end
            % Repeat of above but for Recovery Data - Baseline
            if size(groupRecoverydata,1)==size(groupBaselineAVG,1)
                RecminusBaseline = groupRecoverydata-groupBaselineAVG;            
            else
                if size(groupRecoverydata,1)<size(groupBaselineAVG,1)
                    newgroupBaselineAVG = [groupBaselineAVG;groupBaselineAVG];
                    brAVG = newgroupBaselineAVG(RecPeriod-(floor(RecStart/48)*48),:);
                    RecminusBaseline = groupRecoverydata-brAVG;
                else
                   numRecdays = ceil(size(groupRecoverydata,1)/size(groupBaselineAVG,1));
                   temp = cell(numRecdays);
                   newgroupBaselineAVG = [];
                   
                   for p=1:numRecdays
                       temp{p}=groupBaselineAVG;
                       newgroupBaselineAVG = [temp{p};newgroupBaselineAVG];
                   end     
                   recday = ceil(RecStart/48);
                   brAVG = newgroupBaselineAVG(RecPeriod-((recday-1)*48),:);
                   RecminusBaseline = groupRecoverydata-brAVG;
                end
            end
            
            %Next section turns SD-Baseline and Rec-Baseline data into
            %cumulative measures, Then the two are tacked together, where recovery builds off of where SD
            %left off. So if by the end of SD an animal is at -200 minutes
            %of sleep, and the first minute of recovery is +25, then that value
            %will become -175. And so on for the rest of recovery.
            SDminusBaselineCum = [];
            RecminusBaselineCum = [];
            for j=1:c
                for k=1:SDduration*2
                    if k==1
                        SDminusBaselineCum(k,j) = SDminusBaseline(k,j);
                    else
                        SDminusBaselineCum(k,j) = SDminusBaseline(k,j)+SDminusBaselineCum((k-1),j);
                    end
                end
                
                for k=1:length(RecPeriod)
                    if k==1
                        RecminusBaselineCum(k,j) = RecminusBaseline(k,j)+SDminusBaselineCum(SDduration*2,j);
                    else
                        RecminusBaselineCum(k,j) = RecminusBaseline(k,j)+RecminusBaselineCum((k-1),j);
                    end
                end   
            end

            SDplusRecCum = [SDminusBaselineCum;RecminusBaselineCum];
            exportData{i} = SDplusRecCum;
            SDplusRecCumallgroups = cat(2,SDplusRecCumallgroups,SDplusRecCum);
            %For each group, this next chunk averages across all animals, and if
            %there is more than 1 animal, also calculates an SEM.
            SDplusRecCumGroupAVG(:,i) = mean(SDplusRecCum,2);
            [r c]=size(SDplusRecCum);
            for k=1:r
                if c ~=1
                CumGroupError(k,i) = nansem(SDplusRecCum(k,:));
                end
            end
        end
        
        % Next section gets the names and data from the selected groups for
        % graphing.
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
        
        if isempty(selectedGroups)
            error('You did not select any groups!')
        end
        
        groupnames={};
        for i=1:length(selectedGroups)
            current=SDplusRecCumGroupAVG(:,selectedGroups(i));
            if ~isempty(CumGroupError)
                currentSEM=CumGroupError(:,selectedGroups(i));
                SEMsel(:,i)=currentSEM;
            end
            datasel(:,i)=current;
            groupnames=[groupnames list(selectedGroups(i))];
        end
        
        if SDgraph == 1
            % Next section creates a figure and graphs using plot if there is
            % only 1 animal, or errorbar if there are more. Legend is populated
            % with group names.
            set(0,'DefaultAxesColorOrder',[0,0,1;1,0.6,0;0,0.6,0;1,0,0;0,0.6,1;1,0,1;0,0,0;0.6,0,0;0.6,1,0.2;0.6,0,1;1,0.8,0.2;0.5,0.5,0.5])
            figure
            
            if  isempty(CumGroupError)
                plot(datasel,'linewidth',1.5)
                hold on;
            else
                errorbar(datasel,SEMsel)
            end
            
            %  set(gca,'Fontsize',10,'Xtick',[0 12 24 36 48],'XTickLabel',{'0';'6';'12';'18';'24'});
            set(gcf,'PaperOrientation','landscape');
            set(gcf, 'PaperPositionMode', 'manual');
            set(gcf, 'PaperPosition', [0.25 0.25 10.75 8.25]);
            legend(groupnames);
        end
        
        if SDexport == 1
            % Running through # of analyses (currently 17)
            fprintf('%s\n','Exporting data from SD analysis');
            tophead='Group,Fly Number,Bin Length,';
            [r c]=size(exportData{1});

            for n=1:r
                if recoveryDur>0
                    if n==r
                        tophead=[tophead 'Recovery Bin ' num2str(n-(SDduration*2))];
                    elseif n<=SDduration*2
                        tophead=[tophead 'SD Bin ' num2str(n) ','];
                    else
                        tophead=[tophead 'Recovery Bin ' num2str(n-(SDduration*2)) ','];
                    end
                elseif recoveryDur==0
                    if n==r
                        tophead=[tophead 'SD Bin ' num2str(n)];
                    else
                        tophead=[tophead 'SD Bin ' num2str(n) ','];
                    end
                end
            end
            
            dlmwrite('CumulativeSleepLossexport.csv', tophead,'');
            % Running through # of groups
            for j=1:length(exportData)
                fileX = exportData{j};
                [rX numFlies] = size(fileX);
                nanmeanX = (nanmean(fileX,2))';
                nansemX = (nansem(fileX,2))';
                sideheadAVGX = [list{j} ',Average,30 min,'];
                sideheadSEMX = [list{j} ',SEM,30 min,'];
                
                for k=1:numFlies
                    sideheadX = [list{j} ',Fly ' num2str(k) ',30 min,'];
                    dataX = [];
                    meanX = [];
                    semX = [];
                    for n=1:rX
                        if n==rX
                            dataX = [dataX num2str(fileX(n,k))];
                            meanX = [meanX num2str(nanmeanX(n))];
                            semX = [semX num2str(nansemX(n))];
                        else
                            dataX = [dataX num2str(fileX(n,k)) ','];
                            meanX = [meanX num2str(nanmeanX(n)) ','];
                            semX = [semX num2str(nansemX(n)) ','];
                        end
                    end
                    
                    tempX = cat(2,sideheadX,dataX);
                    fullmeanX = cat(2,sideheadAVGX,meanX);
                    fullsemX = cat(2,sideheadSEMX,semX);
                    dlmwrite('CumulativeSleepLossexport.csv', sprintf('%s',tempX), '-append','delimiter','');
                end
                
                dlmwrite('CumulativeSleepLossexport.csv', sprintf('%s',fullmeanX), '-append','delimiter','');
                dlmwrite('CumulativeSleepLossexport.csv', sprintf('%s',fullsemX), '-append','delimiter','');
            end
        end
    end

    function allGroupSelect(src,evt,group)
        response = get(src,'Value');
        for i=1:length(group)
            if response == 1
            set(group(i),'Value',1);
            elseif response == 0
            set(group(i),'Value',0);
            end
        end
    end

    function allDaySelect(src,evt,day)
        response = get(src,'Value');
        for i=1:length(day)
            if response == 1
            set(day(i),'Value',1);
            elseif response == 0
            set(day(i),'Value',0);
            end
        end
    end

    function graphAllDays(src,evt,analyzeforBin,day,list,group,analysisNames,graphChoice,exportChoice)
        
        data=get(analyzeforBin,'Userdata');
        graphChoice=get(graphChoice,'Value');
        export=get(exportChoice,'Value'); 
        Calc12Object ={};
        Calc24Object = {};
        CalcXObject = {};
        % Following line to distinguish between default or custom bin
        % analysis will not function if there are exactly 17 experimental
        % groups. This is unlikely, but possible...
        if length(data{1}{1})==17
            Calc12Object = data{1};
            Calc24Object = data{2};
        else
            CalcXObject = data;
        end
        
        if export==1 && isempty(CalcXObject)
            % Running through # of analyses (currently 17)
            for i=1:length(Calc12Object{1})
                fprintf('%s\n',['Exporting data from analysis ' analysisNames{i}]);
                tophead='Group,Fly Number,Bin Length,';
                [r numFlies] = size(Calc12Object{1}{i});
                for n=1:r
                    if n==r
                        tophead=[tophead 'Bin ' num2str(n)];
                    else
                        tophead=[tophead 'Bin ' num2str(n) ','];
                    end
                end
                
                dlmwrite([analysisNames{i} '.csv'], tophead,'');
                % Running through # of groups
                for j=1:length(Calc12Object)
                    file12 = Calc12Object{j}{i};
                    file24 = Calc24Object{j}{i};
                    [r12 numFlies] = size(file12);
                    [r24 numFlies] = size(file24);
                    nanmean12 = (nanmean(file12,2))';
                    nansem12 = (nansem(file12,2))';
                    nanmean24 = (nanmean(file24,2))';
                    nansem24 = (nansem(file24,2))';
                    
                    if i<3
                       sideheadAVG12 = [list{j} ',Average,30 min,'];
                       sideheadSEM12 = [list{j} ',SEM,30 min,']; 
                    else
                        sideheadAVG12 = [list{j} ',Average,' num2str(12) ','];
                        sideheadSEM12 = [list{j} ',SEM,' num2str(12) ','];
                    end
                    
                    sideheadAVG24 = [list{j} ',Average,' num2str(24) ','];
                    sideheadSEM24 = [list{j} ',SEM,' num2str(24) ','];
                    
                    for k=1:numFlies
                        if i<3
                            sidehead12 = [list{j} ',Fly ' num2str(k) ',30 min,'];
                        else    
                            sidehead12 = [list{j} ',Fly ' num2str(k) ',' num2str(12) ','];
                        end
                        data12 = [];
                        mean12 = [];
                        sem12 = [];
                        for n=1:r12
                            if n==r12
                                data12 = [data12 num2str(file12(n,k))];
                                mean12 = [mean12 num2str(nanmean12(n))];
                                sem12 = [sem12 num2str(nansem12(n))];
                            else
                                data12 = [data12 num2str(file12(n,k)) ','];
                                mean12 = [mean12 num2str(nanmean12(n)) ','];
                                sem12 = [sem12 num2str(nansem12(n)) ','];
                            end
                        end
                        
                        temp12 = cat(2,sidehead12,data12);
                        fullmean12 = cat(2,sideheadAVG12,mean12);
                        fullsem12 = cat(2,sideheadSEM12,sem12);
                        dlmwrite([analysisNames{i} '.csv'], sprintf('%s',temp12), '-append','delimiter','');
                    end
                    
                    dlmwrite([analysisNames{i} '.csv'], sprintf('%s',fullmean12), '-append','delimiter','');
                    dlmwrite([analysisNames{i} '.csv'], sprintf('%s',fullsem12), '-append','delimiter','');
                    if i>2
                        for k=1:numFlies
                            sidehead24 = [list{j} ',Fly ' num2str(k) ',' num2str(24) ','];
                            data24 = [];
                            mean24 = [];
                            sem24 = [];
                            
                            for n=1:r24
                                if n==r24
                                    data24 = [data24 num2str(file24(n,k))];
                                    mean24 = [mean24 num2str(nanmean24(n))];
                                    sem24 = [sem24 num2str(nansem24(n))];
                                else
                                    data24 = [data24 num2str(file24(n,k)) ','];
                                    mean24 = [mean24 num2str(nanmean24(n)) ','];
                                    sem24 = [sem24 num2str(nansem24(n)) ','];
                                end
                            end
                            temp24 = cat(2,sidehead24,data24);
                            fullmean24 = cat(2,sideheadAVG24,mean24);
                            fullsem24 = cat(2,sideheadSEM24,sem24);
                            dlmwrite([analysisNames{i} '.csv'], sprintf('%s',temp24), '-append','delimiter','');
                        end
                        
                        dlmwrite([analysisNames{i} '.csv'], sprintf('%s',fullmean24), '-append','delimiter','');
                        dlmwrite([analysisNames{i} '.csv'], sprintf('%s',fullsem24), '-append','delimiter','');
                    end
                end
            end
        end
        
        if export == 1 && ~isempty(CalcXObject)
            % Running through # of analyses (currently 17)
            for i=1:length(CalcXObject{1})
                fprintf('%s\n',['Exporting data from analysis ' analysisNames{i}]);
                tophead='Group,Fly Number,Bin Length,';
                [r numFlies] = size(CalcXObject{1}{i});
                binlength=24/(r/length(day));
                for n=1:r
                    if n==r
                        tophead=[tophead 'Bin ' num2str(n)];
                    else
                        tophead=[tophead 'Bin ' num2str(n) ','];
                    end
                end
                
                dlmwrite([analysisNames{i} '.csv'], tophead,'');
                % Running through # of groups
                for j=1:length(CalcXObject)
                    fileX = CalcXObject{j}{i};
                    [rX numFlies] = size(fileX);
                  
                    nanmeanX = (nanmean(fileX,2))';
                    nansemX = (nansem(fileX,2))';
                    
                    if i<3
                       sideheadAVGX = [list{j} ',Average,30 min,'];
                       sideheadSEMX = [list{j} ',SEM,30 min,']; 
                    else
                        sideheadAVGX = [list{j} ',Average,' num2str(binlength) ','];
                        sideheadSEMX = [list{j} ',SEM,' num2str(binlength) ','];
                    end
                    
                    for k=1:numFlies
                        if i<3
                            sideheadX = [list{j} ',Fly ' num2str(k) ',30 min,'];
                        else
                            sideheadX = [list{j} ',Fly ' num2str(k) ',' num2str(binlength) ','];
                        end
                        
                        dataX = [];
                        meanX = [];
                        semX = [];
                        for n=1:rX
                            if n==rX
                                dataX = [dataX num2str(fileX(n,k))];
                                meanX = [meanX num2str(nanmeanX(n))];
                                semX = [semX num2str(nansemX(n))];
                            else
                                dataX = [dataX num2str(fileX(n,k)) ','];
                                meanX = [meanX num2str(nanmeanX(n)) ','];
                                semX = [semX num2str(nansemX(n)) ','];
                            end
                        end
                        
                        tempX = cat(2,sideheadX,dataX);
                        fullmeanX = cat(2,sideheadAVGX,meanX);
                        fullsemX = cat(2,sideheadSEMX,semX);
                        dlmwrite([analysisNames{i} '.csv'], sprintf('%s',tempX), '-append','delimiter','');
                    end
                    
                    dlmwrite([analysisNames{i} '.csv'], sprintf('%s',fullmeanX), '-append','delimiter','');
                    dlmwrite([analysisNames{i} '.csv'], sprintf('%s',fullsemX), '-append','delimiter','');
                end
            end
        end
        
        if graphChoice==1
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

            if isempty(selectedGroups)
                 error('You did not select any groups!')
            end

            groupnames={};
            for i=1:length(selectedGroups)
                if isempty (CalcXObject)
                    s30current=Calc12Object{selectedGroups(i)}{2};
                    ameancurrent=Calc12Object{selectedGroups(i)}{1};
                else
                    s30current=CalcXObject{selectedGroups(i)}{2};
                    ameancurrent=CalcXObject{selectedGroups(i)}{1};
                end
                s30{i}=s30current;
                amean{i}=ameancurrent;
                groupnames=[groupnames list(selectedGroups(i))];
            end

            %This function graphs s30 data for all days separately for the groups selected, with
            %error bars. The first input is a print option. If you want this
            %function to print automatically, change the 0 to a 1.
            set(0,'DefaultAxesColorOrder',[0,0,1;1,0.6,0;0,0.6,0;1,0,0;0,0.6,1;1,0,1;0,0,0;0.6,0,0;0.6,1,0.2;0.6,0,1;1,0.8,0.2;0.5,0.5,0.5])
            figure
            grouperrorbarAllD2(0,s30,groupnames)
            
            figure
            grouperrorbarAllD2amean(0,amean,groupnames)
        end
    end
        
    function multDayExtract(src,evt,analyzeforBin,day,group,analysis,analysisIDs,graphChoice,exportChoice,chooseDDLDLL,list)
        
        calcs=get(analyzeforBin,'Userdata');
        graphChoice=get(graphChoice,'Value');
        export=get(exportChoice,'Value');
        
        dayChoice = get(day,'Value');
        selectedDays=[];
        for i=1:length(day)
            % this will screw up if you only have 1 day of data - need to
            % add extra if statement written day(i)==1
            if dayChoice{i} == 1
                selectedDays = [selectedDays i];
            end
        end
        
        if isempty(selectedDays)
            error('You did not select any days to analyze!')
        end        
        
        % Controls for both situations - default 12/24 hr analysis or custom
        % binning - to make sure that len = the # of groups. Note: This
        % will fail if the number of total groups in the experiment is
        % exactly 17. Unlikely, but could happen.
        if length(calcs{1}{1})==17
            len=length(calcs{1});
        else
            len=length(calcs);
        end
        
        allData = {};
        avgData = {};
        dataset = [];
        dataset24 = [];
        % First condition: 12/24 hr default analysis
        % runs through # of groups. Again, this will fail if the number of
        % total groups in the experiment is exactly 17.
        for i=1:len
            if length(calcs{1}{1})==17
                dataset = calcs{1}{i};
                dataset24 = calcs{2}{i};
            else
                dataset = calcs{i};
            end
            data = [];
            data24 = [];
            
            %Condition for amean, s30 - this analysis is identical regardless of
            %the bin length that the user set.
            for j=1:2
                final = [];
                data = dataset{j};
                flipgroupavg=[];
                
                for k=1:length(day)
                    if dayChoice{k}==1
                        current=data(1+((k-1)*48):48*k,:);
                        final=[final; current];
                    end
                end
                
                allData{i}{j}=final;
                
                [r c]=size(final);
                groupavg=[];
                avg=[];
                
                for m=1:c % running through # of animals in each group
                    final2=[];
                    
                    for k=1:length(selectedDays) % running through # of selected days
                        current=final(1+((k-1)*48):48*k,m);
                        final2=[final2 current];
                    end
                    
                    flipfinal2=final2';
                    
                    % If there is only 1 day being analyzed, this will skip averaging step
                    if length(selectedDays)==1
                        avg=flipfinal2;
                    else
                        avg=nanmean(flipfinal2);
                    end
                    flipgroupavg=[flipgroupavg; avg];
                    groupavg=flipgroupavg';
                end
                avgData{i}{j}=groupavg;
            end
            
            %Condition for:
            %stdur,sfreq,smax,smeandur,smedian,oamean,atcounts,namean,
            %ameandur,afreq,atdur,latency,MeanWakeDur,wmax,WSdiff -
            %these have to be different depending on whether user chose
            %default 12/24 hr or custom bin length.
            if ~isempty(dataset24)
                for j=3:17
                    
                    finalL = [];
                    finalD = [];
                    final24 = [];
                    data = dataset{j};
                    data24 = dataset24{j};
                    flipgroupavgL=[];
                    flipgroupavgD=[];
                    flipgroupavg24=[];
                    
                    for k=1:length(day)
                        if dayChoice{k}==1
                            currentL=data(1+((k-1)*2),:);
                            currentD=data(2+((k-1)*2),:);
                            current24=data24(k,:);
                            finalL=[finalL;currentL];
                            finalD=[finalD;currentD];
                            final24=[final24;current24];
                        end
                    end
                    allData{i}{j}{1}=final24;
                    allData{i}{j}{2}=finalL;
                    allData{i}{j}{3}=finalD;
                    
                    if length(selectedDays)==1
                        avgData{i}{j}{1}=final24;
                        avgData{i}{j}{2}=finalL;
                        avgData{i}{j}{3}=finalD;
                    else
                        avgData{i}{j}{1}=nanmean(final24,1);
                        avgData{i}{j}{2}=nanmean(finalL,1);
                        avgData{i}{j}{3}=nanmean(finalD,1);
                    end
                end
                % Condition 2 - user has made a custom bin length choice.
            else
                [r c] = size(dataset{3});
                binsperday = r/length(day);
                XTickLabels=cell(1,binsperday);
                %                     The following for loop creates x-axis label names based on
                %                     the # of bins in the custom analysis. Right now it
                %                     just numbers the bins. Could edit this to make it
                %                     specify the hours of the day covered by each bin.
                for p=1:length(XTickLabels)
                    XTickLabels{p}=num2str(p);
                end
                
                for j=3:17
                    data = dataset{j};
                    finalbindata=cell(binsperday,1);
                    %Runs through # of days
                    for k=1:length(day)
                        if dayChoice{k}==1
                            %Runs through # of bins per day
                            for m=1:binsperday
                                currentbindata = cell(binsperday,1);
                                currentbindata{m} = data(m+((k-1)*binsperday),:);
                                finalbindata{m} = [finalbindata{m};currentbindata{m}];  
                            end
                        end
                    end
                    
                    allData{i}{j}=finalbindata;
                    
                    for m=1:binsperday
                        if length(selectedDays)==1
                            avgData{i}{j}{m}=allData{i}{j}{m};
                        else
                            avgData{i}{j}{m}=nanmean(allData{i}{j}{m});
                        end   
                    end
                end
            end
        end
    
        % This is what the results look like (for default 12/24 hr bin length analysis)...
        % allData{group}{analysistype}{24, L, or D}
        % When a custom bin length is used, it will change to:
        % allData{group}{analysistype}{# of cells corresponding to # of
        % bins/day}, except in the case of amean and s30 (analyses 1 and
        % 2), in which allData{i}{j} is the data itself.
        
        set(src,'UserData',allData);
        
        % If exporting is chosen, the following code exports data
        % averaged across the selected days
        export=get(exportChoice,'Value');
        
        % Next to do: replace following section with new export code,
        % replacing tempX with tempL, tempD, temp24, etc.
        if export==1 && ~isempty(dataset24)
              % Running through # of analyses (currently 17)
            for i=1:length(avgData{1})
            tophead='Group,Fly Number,Bin Length,'; 
                fprintf('%s\n',['Exporting data from analysis ' analysisIDs{i}]);
                if i<3
                    [r numFlies] = size(avgData{1}{i});
                    for n=1:r
                        if n==r
                            tophead=[tophead 'Bin ' num2str(n)];
                        else
                            tophead=[tophead 'Bin ' num2str(n) ','];
                        end
                    end
                    dlmwrite(['BinAVG' analysisIDs{i} '.csv'], tophead,'');
                   
                    % Running through # of groups
                    for j=1:length(avgData)
                        fileX = avgData{j}{i};
                        [rX numFlies] = size(fileX);
                        
                        nanmeanX = (nanmean(fileX,2))';
                        nansemX = (nansem(fileX,2))';
                        
                        sideheadAVGX = [list{j} ',Average,30 min,'];
                        sideheadSEMX = [list{j} ',SEM,30 min,'];
                        
                        for k=1:numFlies
                            sideheadX = [list{j} ',Fly ' num2str(k) ',30 min,'];
                            dataX = [];
                            meanX = [];
                            semX = [];
                            for n=1:rX
                                if n==rX
                                    dataX = [dataX num2str(fileX(n,k))];
                                    meanX = [meanX num2str(nanmeanX(n))];
                                    semX = [semX num2str(nansemX(n))];
                                else
                                    dataX = [dataX num2str(fileX(n,k)) ','];
                                    meanX = [meanX num2str(nanmeanX(n)) ','];
                                    semX = [semX num2str(nansemX(n)) ','];
                                end
                            end
                            
                            tempX = cat(2,sideheadX,dataX);
                            fullmeanX = cat(2,sideheadAVGX,meanX);
                            fullsemX = cat(2,sideheadSEMX,semX);
                            dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',tempX), '-append','delimiter','');
                        end
                        
                        dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',fullmeanX), '-append','delimiter','');
                        dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',fullsemX), '-append','delimiter','');
                    end
                else    %Any analysis type other than 'amean' or 's30'
                    binsperday = 3;
                    binlength = '12/24 Default';
                    tophead=[tophead '24-hour bin, 1st 12-hour bin, 2nd 12-hour bin'];
                    dlmwrite(['BinAVG' analysisIDs{i} '.csv'], tophead,'');
                    
                    % Running through # of groups
                    for j=1:length(avgData)
                        fileX=[];     
                            % Runs through # of bins, stacking bin data
                            % on top of each other.
                            for n=1:binsperday
                                fileX=cat(1,fileX,avgData{j}{i}{n});
                            end
                        
                        [rX numFlies] = size(fileX);
                        nanmeanX = (nanmean(fileX,2))';
                        nansemX = (nansem(fileX,2))';
                        sideheadAVGX = [list{j} ',Average,' binlength ','];
                        sideheadSEMX = [list{j} ',SEM,' binlength ','];
                        
                        for k=1:numFlies
                            sideheadX = [list{j} ',Fly ' num2str(k) ',' binlength ','];
                            dataX = [];
                            meanX = [];
                            semX = [];
                            for n=1:rX
                                if n==rX
                                    dataX = [dataX num2str(fileX(n,k))];
                                    meanX = [meanX num2str(nanmeanX(n))];
                                    semX = [semX num2str(nansemX(n))];
                                else
                                    dataX = [dataX num2str(fileX(n,k)) ','];
                                    meanX = [meanX num2str(nanmeanX(n)) ','];
                                    semX = [semX num2str(nansemX(n)) ','];
                                end
                            end
                            
                            tempX = cat(2,sideheadX,dataX);
                            fullmeanX = cat(2,sideheadAVGX,meanX);
                            fullsemX = cat(2,sideheadSEMX,semX);
                            dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',tempX), '-append','delimiter','');
                        end
                        
                        dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',fullmeanX), '-append','delimiter','');
                        dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',fullsemX), '-append','delimiter','');
                    end  
                end
            end
            
            % Condition 2 - user has set custom bin length
        elseif export==1 && isempty(dataset24)
            % Running through # of analyses (currently 17)
            for i=1:length(avgData{1})
                fprintf('%s\n',['Exporting data from analysis ' analysisIDs{i}]);
                tophead='Group,Fly Number,Bin Length,'; 
                if i<3
                    [r numFlies] = size(avgData{1}{i});
                    for n=1:r
                        if n==r
                            tophead=[tophead 'Bin ' num2str(n)];
                        else
                            tophead=[tophead 'Bin ' num2str(n) ','];
                        end
                    end
                    dlmwrite(['BinAVG' analysisIDs{i} '.csv'], tophead,'');
                   
                    % Running through # of groups
                    for j=1:length(avgData)
                        fileX = avgData{j}{i};
                        [rX numFlies] = size(fileX);
                        
                        nanmeanX = (nanmean(fileX,2))';
                        nansemX = (nansem(fileX,2))';
                        
                        sideheadAVGX = [list{j} ',Average,30 min,'];
                        sideheadSEMX = [list{j} ',SEM,30 min,'];
                        
                        for k=1:numFlies
                            sideheadX = [list{j} ',Fly ' num2str(k) ',30 min,'];
                            dataX = [];
                            meanX = [];
                            semX = [];
                            for n=1:rX
                                if n==rX
                                    dataX = [dataX num2str(fileX(n,k))];
                                    meanX = [meanX num2str(nanmeanX(n))];
                                    semX = [semX num2str(nansemX(n))];
                                else
                                    dataX = [dataX num2str(fileX(n,k)) ','];
                                    meanX = [meanX num2str(nanmeanX(n)) ','];
                                    semX = [semX num2str(nansemX(n)) ','];
                                end
                            end
                            
                            tempX = cat(2,sideheadX,dataX);
                            fullmeanX = cat(2,sideheadAVGX,meanX);
                            fullsemX = cat(2,sideheadSEMX,semX);
                            dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',tempX), '-append','delimiter','');
                        end
                        
                        dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',fullmeanX), '-append','delimiter','');
                        dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',fullsemX), '-append','delimiter','');
                    end
                    
                else    %Any analysis type other than 'amean' or 's30'
                    binlength=24/binsperday;
                    for n=1:binsperday
                        if n==binsperday
                            tophead=[tophead 'Bin ' num2str(n)];
                        else
                            tophead=[tophead 'Bin ' num2str(n) ','];
                        end
                    end
                    dlmwrite(['BinAVG' analysisIDs{i} '.csv'], tophead,'');
                    
                    % Running through # of groups
                    for j=1:length(avgData)
                        fileX=[];     
                            % Runs through # of bins, stacking bin data
                            % on top of each other.
                            for n=1:binsperday
                                fileX=cat(1,fileX,avgData{j}{i}{n});
                            end
                        
                        [rX numFlies] = size(fileX);
                        nanmeanX = (nanmean(fileX,2))';
                        nansemX = (nansem(fileX,2))';
                        sideheadAVGX = [list{j} ',Average,' num2str(binlength) ','];
                        sideheadSEMX = [list{j} ',SEM,' num2str(binlength) ','];
                        
                        for k=1:numFlies
                            sideheadX = [list{j} ',Fly ' num2str(k) ',' num2str(binlength) ','];
                            dataX = [];
                            meanX = [];
                            semX = [];
                            for n=1:rX
                                if n==rX
                                    dataX = [dataX num2str(fileX(n,k))];
                                    meanX = [meanX num2str(nanmeanX(n))];
                                    semX = [semX num2str(nansemX(n))];
                                else
                                    dataX = [dataX num2str(fileX(n,k)) ','];
                                    meanX = [meanX num2str(nanmeanX(n)) ','];
                                    semX = [semX num2str(nansemX(n)) ','];
                                end
                            end
                            
                            tempX = cat(2,sideheadX,dataX);
                            fullmeanX = cat(2,sideheadAVGX,meanX);
                            fullsemX = cat(2,sideheadSEMX,semX);
                            dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',tempX), '-append','delimiter','');
                        end
                        
                        dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',fullmeanX), '-append','delimiter','');
                        dlmwrite(['BinAVG' analysisIDs{i} '.csv'], sprintf('%s',fullsemX), '-append','delimiter','');
                    end  
                end
            end
        end
        
        % If you choose to graph, the following code will be executed,
        % based on selected days, groups, and analysis
        if graphChoice==1
            
            analysis=get(analysis,'Value');
            lightSchedule=get(chooseDDLDLL,'Value');
            
            selectedAnalysis=[];
            
            for i=1:length(analysis)
                if analysis{i} == 1
                    selectedAnalysis = [selectedAnalysis i];
                end
            end
            
            if isempty(selectedAnalysis)
                error('You did not select any analyses to graph!')
            end
            
            selected = get(group,'Value');
            
            selectedGroups = [];
            for i=1:length(selected)
                if length(selected)==1
                    if selected(i) == 1
                        selectedGroups = [selectedGroups i];
                    end
                elseif length(selected) > 1
                    if selected{i} == 1
                        selectedGroups = [selectedGroups i];
                    end
                end
            end
            
            if isempty(selectedGroups)
                error('You did not select any groups!')
            end
            
            groupnames={};
            for i=1:length(selectedGroups)
                groupnames=[groupnames list(selectedGroups(i))];
            end
            
            figure('Name','Data for Selected Days','NumberTitle','off');
            
            % Setting default axes color order below will apply to
            % graphs made using 'plot' or 'errorbar' but not 'bar'.
            % This currently specifies 12 different colors. If there are
            % more groups than that, the color scheme will cycle back
            % through the list again.
            
            set(0,'DefaultAxesColorOrder',[0,0,1;1,0.6,0;0,0.6,0;1,0,0;0,0.6,1;1,0,1;0,0,0;0.6,0,0;0.6,1,0.2;0.6,0,1;1,0.8,0.2;0.5,0.5,0.5])
            
            for i=1:length(selectedAnalysis)
                
                a=selectedAnalysis(i);
                subplot(3,3,i);
                
                % amean or s30 for mdays data
                if a<=2
                    grouperrorbarDOIcolor2(length(selectedDays),allData,selectedGroups,a);
                    if a==2
                        ylabel('Sleep (min/30min)'),xlim([0 48]),ylim([0 35]),...
                            set(gca,'Xtick',[0 12 24 36 48],'XTickLabel',{'0';'6';'12';'18';'24'});
                    else ylabel('Activity Counts/30min'),xlim([0 48]),ylim([0 100]),...
                            set(gca,'Xtick',[0 12 24 36 48],'XTickLabel',{'0';'6';'12';'18';'24'});
                    end
                    
                    if lightSchedule{1}==1
                        xlabel('ZT')
                    else xlabel('CT')
                        
                    end
                end
                %The following colormap code provides a set of 12 colors
                %that the "bar" function will cycle through. This is the
                %same set of 12 colors that I have provided using
                %set(0,'DefaultAxesColorOrder'... above. Currently it
                %can handle up to 24 groups.
                colour = [0,0,1;1,0.6,0;0,0.6,0;1,0,0;0,0.6,1;1,0,1;0,0,0;0.6,0,0;0.6,1,0.2;0.6,0,1;1,0.8,0.2;0.5,0.5,0.5];
                [r c]=size(colour);
                if length(selectedGroups)<=r
                    colour=colour(1:length(selectedGroups),:);
                else
                    colour=[colour;colour];
                    colour=colour(1:length(selectedGroups),:);
                end
                colormap(colour);
                % Edited following graphing function to give 24, LP, DP
                % labels for all graphs.
                if a>2
                    DayNightbargraphnew(allData,selectedGroups,a);
                    ylabel(analysisLabels{a})
                    % Following line of code will fail if there are exactly
                    % 17 total experimental groups.
                    if length(calcs{1}{1})==17
                        if lightSchedule{1}==1
                            %                             if a<=13
                            set(gca,'XTickLabel',{'24';'LP';'DP'})
                            % Commented code used to create alternate code
                            % for Latency and MeanWakeDur that omitted the
                            % '24 hr' data and labels
                            %                             elseif a>13
                            %                             set(gca,'XTickLabel',{'LP';'DP'})
                            %                             end
                        else
                            %                             if a<=13
                            set(gca,'XTickLabel',{'24';'sLP';'sDP'})
                            %                             elseif a>13
                            %                             set(gca,'XTickLabel',{'sLP';'sDP'})
                            %                             end
                        end
                    else
                        % Sets XTick # to be the # of bins per day, and
                        % gives them labels 'Bin 1' : 'Bin binsperday'
                        
                            set(gca,'XTick',[1:binsperday],'XTickLabel',XTickLabels)
                            xlabel('Bin')
                    end
                    % Following code was added to allow for larger numbers
                    % of xticklabels to fit under the figure. See the
                    % script itself for formatting - can specify degree of
                    % rotation, fontsize, etc.
                    % Problem with this solution is that, once rotated,
                    % labels will not line up with the data above them, once 
                    % figure is resized. Can type the following code in manually 
                    % after resizing, but that has to be done separately for each panel in the figure. 
                   
%                     xticklabel_rotate;
                end
                
                if i==1
                    legend(groupnames)
                end
            end
        end
    end
end

function graphCircadianData(src,evt,thirtyGroupmerge,circAnalysis,group,day,chooseDDLDLL,list,circIndividualChoice,exportChoice)

    selected = get(group,'Value');
    dayChoice = get(day,'Value');
    circAnalysis=get(circAnalysis,'Value');
    lightSchedule=get(chooseDDLDLL,'Value');
    IndivChoice=get(circIndividualChoice,'Value');
    
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

    if isempty(selectedGroups)
         error('You did not select any groups!')
    end

    selectedDays=[];
    for i=1:length(day)
        % this will screw up if you only have 1 day of data - if you do you need to
        % add extra if statement written day(i)==1
        if dayChoice{i} == 1
            selectedDays = [selectedDays i];
        end
    end

    if isempty(selectedDays)
        error('You did not select any days to analyze!')
    end
    
    selectedAnalysis=[];
    for i=1:length(circAnalysis)
        if circAnalysis{i} == 1
            selectedAnalysis = [selectedAnalysis i];
        end
    end

    if isempty(selectedAnalysis)
            error('You did not select any analyses to graph!')
    end
    
    figure('Name','Circadian Group Data','NumberTitle','off');
    for i=1:length(selectedGroups)
        data=thirtyGroupmerge{selectedGroups(i)}.data;
        f=thirtyGroupmerge{selectedGroups(i)}.f;
        x=thirtyGroupmerge{selectedGroups(i)}.x;
        finaldata=[];
        finalf=[];
        finalx=[];
        for k=1:length(day)
            if dayChoice{k}==1
                currentdata=data(1+((k-1)*48):48*k,:);
                currentf=f(1+((k-1)*48):48*k,:);
                currentx=x(1+((k-1)*48):48*k,:);
                finaldata=[finaldata; currentdata];
                finalf=[finalf;currentf];
                finalx=[finalx;currentx];
            end
        end
        thirtyGroupmerge{selectedGroups(i)}.data=finaldata;
        thirtyGroupmerge{selectedGroups(i)}.f=finalf;
        thirtyGroupmerge{selectedGroups(i)}.x=finalx;
%         Need to add dam_truncate function based on day selection - just
%         truncating thirtyGroupmerge{selectedGroups(i)}.data is not enough
%         b/c .f and .x are still utilized by dam_panels, so final output
%         will always show data for all days, not just selected days... I
%         have now added manual truncation of .f and .x, without actually
%         running dam_truncate, which only accepts consecutive blocks of
%         days (which might be all that circadian folks will ever want to
%         use, but I'd rather leave in the flexibility). Other
%         things to do (minor): Bring in "list" to allow for labeling with
%         group names, and bring in lights data to allow for shading of graphs.
        [r c]=size(thirtyGroupmerge{selectedGroups(i)}.data);
        groupname=list{selectedGroups(i)};
        dam_panels(thirtyGroupmerge{selectedGroups(i)},1:c,length(selectedGroups),i,selectedAnalysis,groupname);
    end
    
    circGroupData={};
    if IndivChoice==1
        for i=1:length(selectedGroups)
            circIndivData=dam_analyze(thirtyGroupmerge{selectedGroups(i)},0,selectedAnalysis,selectedGroups(i),list);
            circGroupData{i}=circIndivData;
        end
    end
    
    % Unlike sleep analysis export functions, this circadian one will only export
    % individual data from the groups you have selected. The data currently exported
    % are px, ri, and rs, from the autocorrelogram.
    export=get(exportChoice,'Value'); 
    if export==1
        if circAnalysis{3} == 0
            error('You did not run autocorrelation, and hence have no data to export!')
        end
        
        if isempty(circGroupData)
            error('You need to choose "Individual Circadian Data" in order to export!')
        end
        
        dataNames={'px','ri','rs'};
        
        tophead='Group,Fly Number,px,ri,rs,';
        fprintf('%s\n','Exporting data from circadian analysis');
        
        dlmwrite('Circadian Data Export.csv', tophead,'');
        
        % Running through # of groups
        for j=1:length(circGroupData)
            fileX=[];
            % Runs through # of bins, stacking bin data
            % on top of each other.
            for n=1:3
                fileX=cat(1,fileX,circGroupData{j}{n});
            end
            
            [rX numFlies] = size(fileX);
            nanmeanX = (nanmean(fileX,2))';
            nansemX = (nansem(fileX,2))';
            sideheadAVGX = [list{selectedGroups(j)} ',Average,'];
            sideheadSEMX = [list{selectedGroups(j)} ',SEM,'];
            
            for k=1:numFlies
                sideheadX = [list{selectedGroups(j)} ',Fly ' num2str(k) ','];
                dataX = [];
                meanX = [];
                semX = [];
                for n=1:rX
                    if n==rX
                        dataX = [dataX num2str(fileX(n,k))];
                        meanX = [meanX num2str(nanmeanX(n))];
                        semX = [semX num2str(nansemX(n))];
                    else
                        dataX = [dataX num2str(fileX(n,k)) ','];
                        meanX = [meanX num2str(nanmeanX(n)) ','];
                        semX = [semX num2str(nansemX(n)) ','];
                    end
                end
                
                tempX = cat(2,sideheadX,dataX);
                fullmeanX = cat(2,sideheadAVGX,meanX);
                fullsemX = cat(2,sideheadSEMX,semX);
                dlmwrite('Circadian Data Export.csv', sprintf('%s',tempX), '-append','delimiter','');
            end
            
            dlmwrite('Circadian Data Export.csv', sprintf('%s',fullmeanX), '-append','delimiter','');
            dlmwrite('Circadian Data Export.csv', sprintf('%s',fullsemX), '-append','delimiter','');
        end
    end
end

% New Version of phaseshiftanalysis below...
function phaseshiftanalysis (src,evt,oneGroupmerge,group,list,exportChoice)

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

if isempty(selectedGroups)
            error('You did not select any groups!')
elseif length(selectedGroups)~=2
            error('You need to select exactly 2 groups!')
end

list=list(selectedGroups);
oneGroupmerge=oneGroupmerge(selectedGroups);

[peaktimes1,peaktimes2,phaseshift]=peakphaseplot(oneGroupmerge{1},oneGroupmerge{2},0,12,'m','',list);

export=get(exportChoice,'Value'); 
     if export==1
        dataNames='Peak Times 1,Peak Times 2,Phase Difference';
        tophead = [list{1} ',' list{2} ',' list{2} '-' list{1}];
        fprintf('%s\n','Exporting data from phase shift analysis');
        dlmwrite('Phase Shift Data Export.csv', tophead,'');
        dlmwrite('Phase Shift Data Export.csv', sprintf('%s',dataNames), '-append','delimiter','');
        for i=1:length(peaktimes1)
            datai=[];
            if i==length(peaktimes1)
                datai=[datai num2str(peaktimes1(i)) ',' num2str(peaktimes2(i)) ',' num2str(phaseshift(i))];
            else
                datai=[datai num2str(peaktimes1(i)) ',' num2str(peaktimes2(i)) ',' num2str(phaseshift(i)) ','];
            end
                dlmwrite('Phase Shift Data Export.csv', sprintf('%s',datai), '-append','delimiter','');
        end
     end
         
end

% Following code generates raster plot graphs for individual flies from all 
% selected groups and days. This can take a long time to generate if there 
% are a lot of flies in each group
function rasterPlots(src,evt,oneGroupmerge,group,day,list)
    selected = [];
    dayChoice = [];
    selected = get(group,'Value');
    dayChoice = get(day,'Value');
    
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

        if isempty(selectedGroups)
             error('You did not select any groups!')
        end
        
        selectedDays=[];
        for i=1:length(dayChoice)
            % this will screw up if you only have 1 day of data - need to
            % add extra if statement written day(i)==1
            if dayChoice{i} == 1
                selectedDays = [selectedDays i];
            end
        end
        
        if isempty(selectedDays)
            error('You did not select any days to analyze!')
        end
        
    for i=1:length(selectedGroups)
        groupname=list(selectedGroups(i));
        groupname=groupname{1};
        ii=selectedGroups(i);
        rasterplots(5,0,selectedDays,oneGroupmerge{ii},groupname);
    end
end     