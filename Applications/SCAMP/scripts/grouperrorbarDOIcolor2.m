function grouperrorbarDOIcolor(n,allData,selectedGroups,analysistype)
%n=day of interest
      
        if n==0
                error('You did not select any days!')
        end

A=[];
AE=[];
raw=[];

    for i=1:length(selectedGroups)
        data=(allData{selectedGroups(i)}{analysistype});
        [r c]=size(data);
        groupavg=[];
        avg=[];
        
        for j=1:c % running through # of animals in each group
            final=[];        
            
            for k=1:n % running through # of selected days
                current=data(1+((k-1)*48):48*k,j);
                final=[final current];
            end
        flipfinal=final';
        
        % If there is only 1 day being analyzed, this will skip averaging step             
            if n==1
                avg=flipfinal;
            else
                avg=nanmean(flipfinal);
            end
                groupavg=[groupavg; avg];
        end

        % If there is only 1 animal in some groups, this will skip
        % averaging step and SEM calculation
        if c==1
                raw=[raw;groupavg];
        else
                A=[A;nanmean(groupavg)];
                AE=[AE;nansem(groupavg)];
        end       
    end
    
    if ~isempty(raw)
        plot (raw(:,1:48)','LineWidth',1.5)
    end

    if ~isempty(A)
        errorbar (A(:,1:48)',AE(:,1:48)','LineWidth',1.5)   
    end