clear;
txt_date = '23 Aug 2016';
txt_time = '13:52:17';

inputdir = 'V:\DAMAnalysis-Lori\20160823_NC';
filename = 'Monitor01.txt';
outputname = 'V:\DAMAnalysis-Lori\20160823_NC\Monitor3.txt';

cd(inputdir);

% calculate numeric value for start date and time provided by PySolo
%       Acquire
zerodatetime = datenum('31 Dec 69 19 01 00','dd mmm yy HH MM SS');

% calculate numeric value for actual start date and time for the video
txt_start = [txt_date,' ',txt_time];     
startdatetime = datenum(txt_start,'dd mmm yy HH:MM:SS');

% read file contents into a table.
intable = importdata(filename);        

% create a new file, one row at a time with adjusted date and time columns
% replace '?' in column 10 with a '0'

fileID = fopen(outputname,'w');
for row = 1:size(intable.data,1)         % read each row in the input table
    
    % calculate the new time and date to be used
    txt_olddate = intable.textdata{row,2};     % read PySolo date
    txt_oldtime = intable.textdata{row,3};      % read PySolo time
    txt_olddatetime = [txt_olddate,' ',txt_oldtime];   % concatenate into datetime
    olddatetime = datenum(txt_olddatetime,'dd mmm yy HH:MM:SS');   % convert to number
    
    newdatetime = startdatetime + olddatetime - zerodatetime;   % calculate new datetime number
    txt_newdatetime = datestr(newdatetime,'dd mmm yy\tHH:MM:SS');  % convert to string
    
    fprintf('%d  %s\n', row, txt_newdatetime)           % show the user its working
    newstr = sprintf('%s\t%s', intable.textdata{row,1}, ... 
                     txt_newdatetime);                 %    print col_1, date, time to output string
                 
     for col = 4:9                             % keep columns 4 to 10 the same & add to output string
         newstr = sprintf('%s\t%s',newstr, intable.textdata{row,col});
     end %for col
     
     newstr = sprintf('%s\t0', newstr);           % replace ? with 0 & add to output string

     for col = 1:size(intable.data,2)           % keep remaining columns the same & add to output string
         newstr = sprintf('%s\t%s',newstr, num2str(intable.data(row,col)));
     end %for col


     fprintf(fileID,'%s\r\n',newstr);          % output new string to file
end %for row


fclose(fileID);



